from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Home (Public Dashboard)
    path('', views.home, name='home'),
    
    # Public Event Views (Read-Only) - Using Class-Based Views
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    
    # Public Category Views (Read-Only) - Using Class-Based Views
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Public Participant Views (Read-Only) - Using Class-Based Views
    path('participants/', views.ParticipantListView.as_view(), name='participant_list'),
    path('participants/<int:pk>/', views.participant_detail, name='participant_detail'),
]
