"""
URLs do password_app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-password/', views.add_password_view, name='add_password'),
    path('edit-password/<int:password_id>/', views.edit_password_view, name='edit_password'),
    path('delete-password/<int:password_id>/', views.delete_password_view, name='delete_password'),
]

