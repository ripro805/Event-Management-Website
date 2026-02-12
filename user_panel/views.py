from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, UserLoginForm


def signup_view(request):
    """User signup view"""
    if request.user.is_authenticated:
        return redirect('user_panel:dashboard')
    
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('user_panel:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserSignupForm()
    
    return render(request, 'user_panel/signup.html', {
        'form': form,
        'title': 'Sign Up - Create Your Account'
    })


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('user_panel:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('user_panel:dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    
    return render(request, 'user_panel/login.html', {
        'form': form,
        'title': 'Login - Access Your Account'
    })


def logout_view(request):
    """User logout view"""
    username = request.user.username if request.user.is_authenticated else None
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return render(request, 'user_panel/logout.html', {
        'title': 'Logged Out',
        'username': username
    })


@login_required
def dashboard_view(request):
    """User dashboard showing their profile and registered events"""
    from events.models import Event, Participant
    from django.db.models import Count
    
    # Get user's participant record if exists
    try:
        participant = Participant.objects.prefetch_related('events__category').get(
            email=request.user.email
        )
        registered_events = participant.events.all()
    except Participant.DoesNotExist:
        participant = None
        registered_events = []
    
    # Get upcoming events
    from datetime import date
    upcoming_events = Event.objects.filter(date__gte=date.today()).order_by('date', 'time')[:5]
    
    context = {
        'title': 'User Dashboard',
        'participant': participant,
        'registered_events': registered_events,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'user_panel/dashboard.html', context)

