from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SignUpForm, TaskForm
from .models import Task


def home(request):
    if request.user.is_authenticated:
        return redirect("index")
    return redirect("login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Log in.")
            return redirect("login")
        for error in form.errors.values():
            messages.error(request, error.as_text().lstrip("* ").strip())
    else:
        form = SignUpForm()
    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def index(request):
    tasks = Task.objects.filter(owner=request.user)
    pending = tasks.filter(status=Task.PENDING).count()
    completed = tasks.filter(status=Task.COMPLETED).count()
    return render(
        request,
        "index.html",
        {
            "tasks": tasks,
            "pending_count": pending,
            "completed_count": completed,
            "form": TaskForm(),
        },
    )


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect("index")
    else:
        form = TaskForm()
    return render(request, "add_task.html", {"form": form})


@login_required
def view_tasks(request):
    tasks = Task.objects.filter(owner=request.user)
    status_filter = request.GET.get("status")
    if status_filter in {Task.PENDING, Task.COMPLETED}:
        tasks = tasks.filter(status=status_filter)
    return render(request, "view_tasks.html", {"tasks": tasks})


@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.delete()
    return redirect("index")


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = TaskForm(instance=task)
    return render(request, "edit_task.html", {"form": form, "task": task})


@login_required
@require_POST
def change_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.status = Task.COMPLETED if task.status == Task.PENDING else Task.PENDING
    task.save(update_fields=["status"])
    return JsonResponse({"success": True, "new_status": task.status})
