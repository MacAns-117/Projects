"""Tests for FastAPI auth dependency (no orchestrator / live keys required)."""
import os
from unittest.mock import patch

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from api import require_api_token


def _make_app() -> FastAPI:
    app = FastAPI()

    @app.get("/protected", dependencies=[Depends(require_api_token)])
    def protected():
        return {"ok": True}

    return app


@pytest.fixture
def clear_auth_env(monkeypatch):
    monkeypatch.delenv("RESEARCH_API_TOKEN", raising=False)
    monkeypatch.delenv("RESEARCH_DEV", raising=False)


class TestApiAuth:
    def test_no_token_no_dev_returns_503(self, clear_auth_env, monkeypatch):
        client = TestClient(_make_app())
        resp = client.get("/protected")
        assert resp.status_code == 503

    def test_dev_mode_allows_without_token(self, clear_auth_env, monkeypatch):
        monkeypatch.setenv("RESEARCH_DEV", "1")
        client = TestClient(_make_app())
        resp = client.get("/protected")
        assert resp.status_code == 200
        assert resp.json()["ok"] is True

    def test_wrong_token_returns_401(self, clear_auth_env, monkeypatch):
        monkeypatch.setenv("RESEARCH_API_TOKEN", "secret")
        client = TestClient(_make_app())
        resp = client.get("/protected", headers={"X-API-Token": "wrong"})
        assert resp.status_code == 401

    def test_missing_token_returns_401(self, clear_auth_env, monkeypatch):
        monkeypatch.setenv("RESEARCH_API_TOKEN", "secret")
        client = TestClient(_make_app())
        resp = client.get("/protected")
        assert resp.status_code == 401

    def test_correct_token_ok(self, clear_auth_env, monkeypatch):
        monkeypatch.setenv("RESEARCH_API_TOKEN", "secret")
        client = TestClient(_make_app())
        resp = client.get("/protected", headers={"X-API-Token": "secret"})
        assert resp.status_code == 200
