"""
Extract tools — web page content extraction for the research agent.

Fetches a URL and extracts the main text content using trafilatura.
This gives the agent access to the full article, not just the search snippet.

Security: only http/https; blocks private/link-local/metadata addresses;
caps response body size to limit SSRF/DoS impact.
"""

from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from urllib.parse import urlparse

import requests
import trafilatura

# Max response body to download (2 MiB)
MAX_RESPONSE_BYTES = 2 * 1024 * 1024


@dataclass(frozen=True)
class ExtractResult:
    """Structured extract outcome — prefer this over string-matching errors."""
    ok: bool
    content: str = ""
    error: str | None = None


def _is_blocked_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Reject loopback, private, link-local, and other non-global addresses."""
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
        or (ip.version == 6 and ip.ipv4_mapped is not None and _is_blocked_ip(ip.ipv4_mapped))
    )


def _validate_url(url: str) -> str:
    """Validate scheme and resolve host; raise ValueError if unsafe."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme or '(none)'}")
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL missing hostname")

    # Block obvious metadata hostnames even before DNS
    lowered = hostname.lower().rstrip(".")
    if lowered in {"metadata.google.internal", "metadata", "localhost"}:
        raise ValueError(f"Blocked hostname: {hostname}")

    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as e:
        raise ValueError(f"Could not resolve host: {hostname}") from e

    if not infos:
        raise ValueError(f"Could not resolve host: {hostname}")

    for info in infos:
        ip_str = info[4][0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            continue
        if _is_blocked_ip(ip):
            raise ValueError(f"Blocked address for host {hostname}: {ip}")

    return url


def extract_page_content(url: str, timeout: int = 10) -> ExtractResult:
    """Extract the main text content from a web page.

    Use this tool when you need the full text of an article (not just the
    search snippet). Downloads the page and uses trafilatura to extract
    the main content, stripping navigation, ads, and footers.

    Args:
        url: The full URL of the page to extract.
        timeout: Request timeout in seconds (default 10).

    Returns:
        ExtractResult with ok=True and content, or ok=False and error message.
    """
    try:
        _validate_url(url)
    except ValueError as e:
        return ExtractResult(ok=False, error=str(e))

    try:
        with requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 (compatible; AIResearchAgent/1.0)"},
            stream=True,
            allow_redirects=True,
        ) as response:
            # Re-check final URL after redirects
            try:
                _validate_url(response.url)
            except ValueError as e:
                return ExtractResult(ok=False, error=str(e))

            response.raise_for_status()

            chunks: list[bytes] = []
            total = 0
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                total += len(chunk)
                if total > MAX_RESPONSE_BYTES:
                    return ExtractResult(
                        ok=False,
                        error=f"Response from {url} exceeded {MAX_RESPONSE_BYTES} byte limit.",
                    )
                chunks.append(chunk)

            raw = b"".join(chunks)
            encoding = response.encoding or "utf-8"
            try:
                html = raw.decode(encoding, errors="replace")
            except LookupError:
                html = raw.decode("utf-8", errors="replace")

        text = trafilatura.extract(html, include_links=True, include_tables=True)

        if not text:
            return ExtractResult(
                ok=False,
                error=f"Could not extract text from {url} (page may be JS-rendered or empty).",
            )

        return ExtractResult(ok=True, content=text)

    except requests.exceptions.Timeout:
        return ExtractResult(
            ok=False,
            error=f"Request to {url} timed out after {timeout} seconds.",
        )
    except requests.exceptions.RequestException as e:
        return ExtractResult(ok=False, error=f"Error fetching {url}: {e}")
    except Exception as e:
        return ExtractResult(ok=False, error=f"Error extracting content from {url}: {e}")


def extract_multiple_pages(urls: list[str], timeout: int = 10) -> dict[str, ExtractResult]:
    """Extract content from multiple URLs.

    Args:
        urls: List of URLs to extract.
        timeout: Request timeout per URL.

    Returns:
        Dictionary mapping URL to ExtractResult.
    """
    results = {}
    for url in urls:
        print(f"  Extracting: {url[:60]}...")
        results[url] = extract_page_content(url, timeout)
    return results


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    print("Testing extract_tools...\n")

    test_url = "https://en.wikipedia.org/wiki/Large_language_model"
    print(f"Extracting: {test_url}\n")

    result = extract_page_content(test_url)
    if result.ok:
        print(f"Extracted {len(result.content)} characters.")
        print(f"First 300 chars:\n{result.content[:300]}...")
    else:
        print(f"Failed: {result.error}")
