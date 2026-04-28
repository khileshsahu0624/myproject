from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='list'),
    path('create/', views.student_create, name='create'),
    path('update/<int:id>/', views.student_update, name='update'),
    path('delete/<int:id>/', views.student_delete, name='delete'),
]