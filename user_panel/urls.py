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
    path('my-rsvps/', views.my_rsvps_view, name='my_rsvps'),

    # Activation
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    
    # RSVP
    path('rsvp/<int:event_id>/', views.rsvp_event, name='rsvp_event'),
]
