from django.urls import path
from . import views

app_name = 'user_panel'

urlpatterns = [
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
