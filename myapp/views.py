from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.db.models import Count, Sum, Q
from .models import (
    Student, Department, Course, Enrollment, 
    Attendance, Grade, FeePayment
)
from .forms import (
    StudentForm, CourseForm, EnrollmentForm, CustomUserCreationForm,
    AttendanceForm, GradeForm, FeePaymentForm
)



# =========================
# INDEX (DEFAULT PAGE)
# =========================
def index_view(request):
    return render(request, 'myapp/index.html')

# =========================
# DASHBOARD
# =========================
@login_required(login_url='login')

def dashboard(request):
    # Basic statistics
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='active').count()
    total_courses = Course.objects.count()
    total_departments = Department.objects.count()

    # Department-wise student count
    dept_data = Department.objects.annotate(
        student_count=Count('students')
    ).order_by('-student_count')

    # Recent enrollments
    recent_enrollments = Enrollment.objects.select_related(
        'student', 'course'
    ).order_by('-enrollment_date')[:10]

    # Pending fees
    pending_fees = FeePayment.objects.filter(
        status__in=['pending', 'overdue']
    ).count()

    context = {
        'total_students': total_students,
        'active_students': active_students,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'dept_data': dept_data,
        'recent_enrollments': recent_enrollments,
        'pending_fees': pending_fees,
        'PROJECT_NAME': 'StarAdmin',           # Added here
    }

    return render(request, 'myapp/dashboard/dashboard.html', context)


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome {user.username}')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please fill all fields')

    return render(request, 'myapp/auth/login.html')


# =========================
# REGISTER
# =========================
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct errors below')
    else:
        form = CustomUserCreationForm()

    return render(request, 'myapp/auth/register.html', {'form': form})


# =========================
# LOGOUT
# =========================
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


# =========================
# PROFILE
# =========================
@login_required(login_url='login')
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'myapp/auth/profile.html', {'form': form})


# =========================
# CHANGE PASSWORD
# =========================
@login_required(login_url='login')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Fix errors below')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'myapp/auth/change_password.html', {'form': form})


# =========================
# STUDENTS
# =========================
class StudentListView(ListView):
    model = Student
    template_name = 'myapp/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    ordering = ['student_id']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        
        if search:
            queryset = queryset.filter(
                Q(student_id__icontains=search) | 
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'myapp/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Student added successfully!")
        return super().form_valid(form)


class StudentDetailView(DetailView):
    model = Student
    template_name = 'myapp/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollments.select_related('course')
        context['attendance'] = Attendance.objects.filter(student=self.object).order_by('-date')[:10]
        context['grades'] = Grade.objects.filter(student=self.object)
        context['payments'] = FeePayment.objects.filter(student=self.object)
        return context


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'myapp/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Student updated successfully!")
        return super().form_valid(form)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'myapp/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Student deleted successfully!")
        return super().delete(request, *args, **kwargs)


# ====================== COURSE VIEWS ======================
class CourseListView(ListView):
    model = Course
    template_name = 'myapp/course_list.html'
    context_object_name = 'courses'
    paginate_by = 15


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'myapp/course_form.html'
    success_url = reverse_lazy('course_list')


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'myapp/course_form.html'
    success_url = reverse_lazy('course_list')


# ====================== ENROLLMENT VIEWS ======================
class EnrollmentCreateView(CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'myapp/enrollment_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Student enrolled successfully!")
        return super().form_valid(form)


# ====================== ATTENDANCE VIEWS ======================
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance marked successfully!")
            return redirect('mark_attendance')
    else:
        form = AttendanceForm()
    
    context = {'form': form}
    return render(request, 'myapp/mark_attendance.html', context)


# ====================== GRADE VIEWS ======================
class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'myapp/grade_form.html'
    success_url = reverse_lazy('student_list')


# ====================== FEE PAYMENT VIEWS ======================
class FeePaymentCreateView(CreateView):
    model = FeePayment
    form_class = FeePaymentForm
    template_name = 'myapp/fee_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Fee payment recorded successfully!")
        return super().form_valid(form)


# ====================== ADDITIONAL USEFUL VIEWS ======================
@login_required
def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'myapp/student_profile.html', {'student': student})
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully')
        return redirect('student_list')

    return render(request, 'myapp/students/student_delete.html', {'student': student})