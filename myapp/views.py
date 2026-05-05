from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm
from .models import Student
from .forms import StudentForm


# =========================
# Dashboard
# =========================
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'myapp/dashboard/dashboard.html', {
        "PROJECT_NAME": "StarAdmin"
    })


# =========================
# Auth System
# =========================
# ================= LOGIN =================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'✅ Welcome back, {user.get_full_name() or user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, '❌ Invalid username or password.')

    return render(request, 'myapp/auth/login.html')


# ================= REGISTER =================
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '🎉 Account created successfully! Please login with your credentials.')
            return redirect('login')
        else:
            # Show clean error messages
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'myapp/auth/register.html', {'form': form})


# ================= LOGOUT =================
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, '👋 You have been logged out successfully.')
    return redirect('login')


# ================= PROFILE UPDATE =================
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'myapp/auth/profile.html', {'form': form})


# ================= CHANGE PASSWORD =================
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'myapp/auth/change_password.html', {'form': form})




# =========================
# Student CRUD
# =========================
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'myapp/students/student_list.html', {'students': students})


@login_required
def student_create(request):
    form = StudentForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully!')
        return redirect('student_list')

    return render(request, 'myapp/students/student_form.html', {'form': form})


@login_required
def student_update(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)

    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')

    return render(request, 'myapp/students/student_form.html', {'form': form})


@login_required
def student_delete(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')

    return render(request, 'myapp/students/student_delete.html', {'student': student})