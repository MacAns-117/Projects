from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RequestForm
from .models import smtp
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required



def send_email(request):
    subject = 'Subject'
    message = 'Message.'
    from_email = 'f@example.com'
    recipient_list = ['to@example.com']
    
    send_mail(subject, message, from_email, recipient_list)
    
    return HttpResponse('Email sent successfully!')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        
        if password != cpassword:
            messages.error(request, "Passwords do not match. Please retry.")
            return redirect("/signup")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("/signup")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("/signup")
        
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.save()       
        return redirect("/login")
    
    else:
        messages.info(request, "Please sign up.")
        
    return render(request, "signup.html")



def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        myuser = authenticate(username=username, password=password)
        
        if myuser is not None:
            login(request, myuser)
            if myuser.is_superuser:  # Check if the user is an admin
                messages.success(request, 'Admin login successful')
                return redirect('adminpanel')  # Redirect to admin panel
            else:
                messages.success(request, 'User login successful')
                return redirect('request_form')  # Redirect to request form
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
        
    return render(request, "login.html")

@login_required(login_url="/login")
def adminpanel(request):
   # pending_requests = smtp.objects.filter(status='pending')
    pending_requests = smtp.objects.all() 
    context = {'pending_requests': pending_requests}
    return render(request, 'adminpanel.html', context)

@login_required(login_url="/login")
def approved(request, req_id):
    req = smtp.objects.get(pk=req_id)
    subject = 'Request Approved'
    context = {'request': req}
    html_message = render_to_string('approved.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'your_email@example.com'
    recipient_list = [req.Email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return HttpResponse('Request approved and email sent successfully!')

@login_required(login_url="/login")
def rejected(request, req_id):
    req = smtp.objects.get(pk=req_id)
    subject = 'Request Rejected'
    context = {'request': req}
    html_message = render_to_string('rejected.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'your_email@example.com'
    recipient_list = [req.Email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return HttpResponse('Request rejected and email sent successfully!')


@login_required(login_url="/login")
def newrequest(request):
    subject = 'New Request Submitted'
    message = 'A new request has been submitted. Please log in to the admin panel to review it.'
    
    # Assuming the user's email is stored in the User model's email field
    from_email = request.user.email  
    
    recipient_list = ['abc@gmail.com']  # Replace with admin's email
    send_mail(subject, message, from_email, recipient_list)

@login_required(login_url="/login")
def request_form(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            # Send email notification to admin
            newrequest(request)
            messages.success(request, 'Request submitted successfully.')
            return redirect('login')
    else:
        form = RequestForm()
    return render(request, 'request_form.html', {'form': form})

def base(request):
    return render(request, "base.html")

def send_verification_email(user):
    subject = 'Verify your email address'
    message = 'Please click the link below to verify your email address.'
    from_email = 'abc@gmail.com'
    to_email = user.email
    send_mail(subject, message, from_email, [to_email])






