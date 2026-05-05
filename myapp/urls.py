from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard (Protected)
    path('', login_required(views.dashboard), name='dashboard'),
    path('dashboard/', login_required(views.dashboard), name='dashboard'),

    # Auth Routes (Public - Do NOT protect)
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Students CRUD (All Protected)
    path('students/', login_required(views.student_list), name='student_list'),
    path('students/add/', login_required(views.student_create), name='student_add'),
    path('students/edit/<int:id>/', login_required(views.student_update), name='student_edit'),
    path('students/delete/<int:id>/', login_required(views.student_delete), name='student_delete'),

      # User Profile & Settings
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
]

