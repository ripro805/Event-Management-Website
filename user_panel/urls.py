
from django.urls import path
from . import views

app_name = 'user_panel'

urlpatterns = [
    # Profile URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Password Reset URLs
    path('reset-password/', views.CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset-password/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-rsvps/', views.my_rsvps_view, name='my_rsvps'),

    # Activation
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    
    # RSVP
    path('rsvp/<int:event_id>/', views.rsvp_event, name='rsvp_event'),
]
