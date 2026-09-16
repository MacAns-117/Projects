from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

from .forms import RequestForm, SignUpForm
from .models import ServiceRequest


def staff_user(user):
    return user.is_authenticated and user.is_staff


def _send(subject, template, context, to_email):
    """Send HTML mail. Console backend is the default so this still works offline."""
    if not to_email:
        return
    html = render_to_string(template, context)
    send_mail(
        subject,
        strip_tags(html),
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        html_message=html,
        fail_silently=True,
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("adminpanel" if request.user.is_staff else "request_form")
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )
        if user is not None:
            login(request, user)
            if user.is_staff:
                messages.success(request, "Admin login successful.")
                return redirect("adminpanel")
            messages.success(request, "Login successful.")
            return redirect("request_form")
        messages.error(request, "Invalid credentials.")
    return render(request, "login.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("request_form")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Log in.")
            return redirect("login")
        for error in form.errors.values():
            messages.error(request, error.as_text().lstrip("* ").strip())
    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def request_form(request):
    if request.user.is_staff:
        return redirect("adminpanel")
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.submitted_by = request.user
            req.save()
            notify = settings.ADMIN_NOTIFY_EMAIL
            if notify:
                _send(
                    "New request submitted",
                    "newrequest.html",
                    {"req": req},
                    notify,
                )
            messages.success(request, "Request submitted.")
            return redirect("request_form")
    else:
        form = RequestForm(initial={"email": request.user.email})
    mine = ServiceRequest.objects.filter(submitted_by=request.user)
    return render(request, "request_form.html", {"form": form, "mine": mine})


@login_required
@user_passes_test(staff_user, login_url="login")
def adminpanel(request):
    status = request.GET.get("status", ServiceRequest.PENDING)
    qs = ServiceRequest.objects.all()
    if status in {ServiceRequest.PENDING, ServiceRequest.APPROVED, ServiceRequest.REJECTED}:
        qs = qs.filter(status=status)
    counts = {
        "pending": ServiceRequest.objects.filter(status=ServiceRequest.PENDING).count(),
        "approved": ServiceRequest.objects.filter(status=ServiceRequest.APPROVED).count(),
        "rejected": ServiceRequest.objects.filter(status=ServiceRequest.REJECTED).count(),
    }
    return render(
        request,
        "adminpanel.html",
        {"requests": qs, "status": status, "counts": counts},
    )


@login_required
@user_passes_test(staff_user, login_url="login")
@require_POST
def approved(request, req_id):
    req = get_object_or_404(ServiceRequest, pk=req_id)
    req.status = ServiceRequest.APPROVED
    req.reviewed_at = timezone.now()
    req.save(update_fields=["status", "reviewed_at"])
    _send("Request approved", "approved.html", {"req": req}, req.email)
    messages.success(request, f"Approved {req.name}.")
    return redirect("adminpanel")


@login_required
@user_passes_test(staff_user, login_url="login")
@require_POST
def rejected(request, req_id):
    req = get_object_or_404(ServiceRequest, pk=req_id)
    req.status = ServiceRequest.REJECTED
    req.reviewed_at = timezone.now()
    req.save(update_fields=["status", "reviewed_at"])
    _send("Request rejected", "rejected.html", {"req": req}, req.email)
    messages.success(request, f"Rejected {req.name}.")
    return redirect("adminpanel")
