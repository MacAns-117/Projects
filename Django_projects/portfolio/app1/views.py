from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # For example, send an email
            send_mail(
                f'Message from {name}',
                message,
                email,
                ['maqsood.a.ansari@gmail.com'],  # Replace with your email
            )
            
            # Add a success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')  # Redirect to the same page to clear the form
    else:
        form = ContactForm()

    return render(request, 'index.html', {'form': form})
