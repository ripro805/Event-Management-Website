from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Home (Public Dashboard)
    path('', views.home, name='home'),
    
    # Public Event Views (Read-Only)
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    
    # Public Category Views (Read-Only)
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    
    # Public Participant Views (Read-Only)
    path('participants/', views.participant_list, name='participant_list'),
    path('participants/<int:pk>/', views.participant_detail, name='participant_detail'),
]
