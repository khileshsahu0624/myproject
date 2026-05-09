from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # ======================
    # Public Pages
    # ======================
    path('', views.index_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # ======================
    # Protected Pages
    # ======================
    path('dashboard/', login_required(views.dashboard), name='dashboard'),

    # Profile
    path('profile/', login_required(views.profile_view), name='profile'),
    path('change-password/', login_required(views.change_password_view), name='change_password'),



    # ====================== STUDENT URLs ======================
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('student/add/', views.StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('student/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    # ====================== COURSE URLs ======================
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/add/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_update'),

    # ====================== ENROLLMENT ======================
    path('enroll/', views.EnrollmentCreateView.as_view(), name='enrollment_create'),

    # ====================== ATTENDANCE ======================
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),

    # ====================== GRADE ======================
    path('grade/add/', views.GradeCreateView.as_view(), name='grade_create'),

    # ====================== FEE PAYMENT ======================
    path('fee/add/', views.FeePaymentCreateView.as_view(), name='fee_create'),

    # ====================== EXTRA ======================
    path('student/<int:pk>/profile/', views.student_profile, name='student_profile'),

]