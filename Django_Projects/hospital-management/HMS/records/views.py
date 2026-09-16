from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import NurseForm, PatientForm, SignUpForm
from .models import Nurse, Patient


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
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
def dashboard(request):
    return render(
        request,
        "dashboard.html",
        {
            "patient_count": Patient.objects.count(),
            "nurse_count": Nurse.objects.count(),
        },
    )


@login_required
def patient_list(request):
    query = request.GET.get("q", "").strip()
    patients = Patient.objects.all()
    if query:
        if query.isdigit():
            patients = patients.filter(pk=query)
        else:
            patients = patients.filter(name__icontains=query)
    return render(request, "patient_list.html", {"patients": patients, "q": query})


@login_required
def patient_create(request):
    form = PatientForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Patient saved.")
        return redirect("patient_list")
    return render(request, "patient_form.html", {"form": form, "title": "Add patient"})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Patient updated.")
        return redirect("patient_list")
    return render(request, "patient_form.html", {"form": form, "title": "Edit patient"})


@login_required
@require_http_methods(["GET", "POST"])
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        patient.delete()
        messages.success(request, "Patient deleted.")
        return redirect("patient_list")
    return render(request, "confirm_delete.html", {"object": patient, "kind": "patient"})


@login_required
def nurse_list(request):
    nurses = Nurse.objects.all()
    department = request.GET.get("department", "")
    shift = request.GET.get("shift", "")
    if department:
        nurses = nurses.filter(department=department)
    if shift:
        nurses = nurses.filter(shift=shift)
    return render(
        request,
        "nurse_list.html",
        {
            "nurses": nurses,
            "department": department,
            "shift": shift,
            "departments": Nurse.DEPARTMENT_CHOICES,
            "shifts": Nurse.SHIFT_CHOICES,
        },
    )


@login_required
def nurse_create(request):
    form = NurseForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Nurse saved.")
        return redirect("nurse_list")
    return render(request, "nurse_form.html", {"form": form, "title": "Add nurse"})


@login_required
def nurse_update(request, pk):
    nurse = get_object_or_404(Nurse, pk=pk)
    form = NurseForm(request.POST or None, request.FILES or None, instance=nurse)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Nurse updated.")
        return redirect("nurse_list")
    return render(request, "nurse_form.html", {"form": form, "title": "Edit nurse"})


@login_required
@require_http_methods(["GET", "POST"])
def nurse_delete(request, pk):
    nurse = get_object_or_404(Nurse, pk=pk)
    if request.method == "POST":
        nurse.delete()
        messages.success(request, "Nurse deleted.")
        return redirect("nurse_list")
    return render(request, "confirm_delete.html", {"object": nurse, "kind": "nurse"})
