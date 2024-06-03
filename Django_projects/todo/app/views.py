from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from .models import Task
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Updated log view
def log(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to a success page.
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

@login_required
def index(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})

def logout_view(request):
    logout(request)
    return redirect('log')

# @login_required
# def add_task(request):
#     if request.method == 'POST':
#         task_name = request.POST['task_name']
#         description = request.POST['description']
#         status = request.POST['status']
#         Task.objects.create(task_name=task_name, description=description, status=status)
#         return redirect('index')
#     return render(request, 'add_task.html')

@login_required
def add_task(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        description = request.POST['description']
        status = request.POST['status']
        Task.objects.create(task_name=task_name, description=description, status=status)
        return redirect('index')
    return render(request, 'add_task.html')


@login_required
def view_tasks(request):
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = Task.objects.filter(status=status_filter)
    else:
        tasks = Task.objects.all()
    return render(request, 'view_tasks.html', {'tasks': tasks})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('index')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.task_name = request.POST['task_name']
        task.description = request.POST['description']
        task.status = request.POST['status']
        task.save()
        return redirect('index')
    return render(request, 'edit_task.html', {'task': task})



@login_required
def change_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == 'Pending':
        task.status = 'Completed'
    else:
        task.status = 'Pending'
    task.save()
    return JsonResponse({'success': True, 'new_status': task.status})

