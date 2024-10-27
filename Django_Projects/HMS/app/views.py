from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Nurse
from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:  
                return redirect('dashboard')
            else:
                return redirect('other_page')  
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful')
        return redirect('login')

    return render(request, 'register.html')


@login_required(login_url="/login")
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url="/login")
def nurses(request):
    all_nurses = Nurse.objects.all()
    return render(request, 'nurses_list.html', {'nurses': all_nurses})

@login_required(login_url="/login")
def add_nurse(request):
    if request.method == 'POST':
        nurse_name = request.POST['nurseName']
        nurse_gender = request.POST['nurseGender']
        nurse_department = request.POST['nurseDepartment']
        nurse_shift = request.POST['nurseShift']
        nurse_care = request.POST['nurseCare']
        nurse_experience = request.POST['nurseExperience']
        nurse_certifications = request.POST['nurseCertifications']
        nurse_contact = request.POST['nurseContact']
        nurse_email = request.POST['nurseEmail']
        nurse_address = request.POST['nurseAddress']
        nurse_profile_picture = request.FILES.get('nurseProfilePicture')

        Nurse.objects.create(
            name=nurse_name,
            gender=nurse_gender,
            department=nurse_department,
            shift=nurse_shift,
            care=nurse_care,
            experience=nurse_experience,
            certifications=nurse_certifications,
            contact_number=nurse_contact,
            email=nurse_email,
            address=nurse_address,
            profile_picture=nurse_profile_picture
        )
        
        messages.success(request, 'Nurse added successfully')
        return redirect('nurses')
    
    return render(request, 'add_nurse.html')

@login_required(login_url="/login")
def update_nurse(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)
    if request.method == 'POST':
        nurse.name = request.POST['nurseName']
        nurse.gender = request.POST['nurseGender']
        nurse.department = request.POST['nurseDepartment']
        nurse.shift = request.POST['nurseShift']
        nurse.care = request.POST['nurseCare']
        nurse.experience = request.POST['nurseExperience']
        nurse.certifications = request.POST['nurseCertifications']
        nurse.contact_number = request.POST['nurseContact']
        nurse.email = request.POST['nurseEmail']
        nurse.address = request.POST['nurseAddress']
        if 'nurseProfilePicture' in request.FILES:
            nurse.profile_picture = request.FILES['nurseProfilePicture']
        nurse.save()
        
        messages.success(request, 'Nurse details updated successfully')
        return redirect('nurses')
    
    return render(request, 'update_nurse.html', {'nurse': nurse})

# def delete_nurse(request,nurse_id):
#     nurse = get_object_or_404(Nurse, id=nurse_id)
#     if request.method == 'POST':
#         nurse.delete()
#         messages.success(request, 'Nurse deleted successfully.')
#     return redirect(reverse('nurses_list'))


def delete_nurse(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)
    if request.method == 'POST':
        nurse.delete()
        return redirect('nurses')
        messages.success(request, 'Nurse deleted successfully.')

    return render(request, 'nurses.html', {'nurses': Nurse.objects.all()})

def logout_view(request):
    logout(request)
    return redirect('login')

