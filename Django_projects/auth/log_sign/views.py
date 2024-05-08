from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

# Updated log view
def log(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to a success page.
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

# Updated signup view
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                User.objects.create_user(username=username, email=email, password=password1)
                return redirect('log')  # Redirect after successful signup.
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'signup.html')
