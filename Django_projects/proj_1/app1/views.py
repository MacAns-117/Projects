# views.py
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.utils.html import format_html
from .models import Patient

def display(request, Name):
    AllPost = Patient.objects.filter(Name=Name)
    context = {"AllPost": AllPost}
    return render(request, "index.html", context)

def details(request):
    if request.method == "POST":
        Name = request.POST.get("Name")
        Blood_group = request.POST.get("Blood_group")
        Age = request.POST.get("Age")
        Disease = request.POST.get("Disease")
        Location = request.POST.get("Location")
        query = Patient(Name=Name, Blood_group=Blood_group, Age=Age, Disease=Disease, Location=Location)
        query.save()

        # Build the response HTML
        response_html = format_html('''
            Successfully Saved<br><br>
            <a href="{}" class="btn btn-primary">Add Patient</a>
            <a href="{}" class="btn btn-secondary">View Saved Details</a>
            ''',
            reverse('add_patient'),  # URL to add another patient
            reverse('view_patient', kwargs={'Name': Name})  # URL to view this patient's details
        )
        return HttpResponse(response_html)
    return render(request, "details.html")


def view_all_patients(request):
    patients = Patient.objects.all()
    return render(request, "all_patients.html", {"patients": patients})

def filter_patients(request):
    query = request.GET.get('query', '')

    # Trying to convert query to an integer to filter by ID, if possible
    try:
        query_id = int(query)
        patients = Patient.objects.filter(id=query_id)
    except ValueError:
        # If conversion fails, filter by name
        patients = Patient.objects.filter(Name__icontains=query)

    return render(request, 'all_patients.html', {'patients': patients})


def update_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        patient.Name = request.POST.get("Name", "")
        patient.Blood_group = request.POST.get("Blood_group", "")
        patient.Age = request.POST.get("Age", "")
        patient.Disease = request.POST.get("Disease", "")
        patient.Location = request.POST.get("Location", "")
        patient.save()
        return redirect('view_all_patients')
    return render(request, "patient_form.html", {"patient": patient})

def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        patient.delete()
        return redirect('view_all_patients')
    return render(request, "confirm_delete.html", {"patient": patient})

def base(request):
    return render(request, 'base.html')

from django.shortcuts import render

# Create your views here.
def base_login_signup(request):
    return render(request, 'base_login_signup.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')
