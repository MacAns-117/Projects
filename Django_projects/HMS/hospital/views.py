from django.shortcuts import render

# Create your views here.
def base_login_signup(request):
    return render(request, 'base_login_signup.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')
