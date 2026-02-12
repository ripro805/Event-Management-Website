from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Admin Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # User Management
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    
    # Role Management (Admin Only)
    path('users/<int:user_id>/assign-role/', views.assign_role, name='assign_role'),
    path('users/<int:user_id>/remove-role/', views.remove_role, name='remove_role'),
    path('groups/', views.manage_groups, name='manage_groups'),
    
    # System Statistics
    path('statistics/', views.system_statistics, name='statistics'),
]
