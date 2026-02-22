from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from events.models import Event, Category, Participant
from django.db.models import Count
from functools import wraps

User = get_user_model()


# ==================== Helper Functions ====================

def is_admin(user):
    """Check if user is Admin"""
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name='Admin').exists()


# Custom login_required that works with inactive users (for testing)
def login_required_allow_inactive(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user_panel:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==================== Admin Dashboard ====================

@login_required_allow_inactive
@user_passes_test(is_admin, login_url='/')
def admin_dashboard(request):
    """Admin dashboard with complete system statistics"""
    
    # Get comprehensive statistics
    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    
    # Count only participants who are in Participant group
    participant_group = Group.objects.filter(name='Participant').first()
    total_participants = Participant.objects.filter(
        user__isnull=False,
        user__groups=participant_group
    ).count()
    
    # Role statistics
    admin_count = User.objects.filter(groups__name='Admin').count()
    organizer_count = User.objects.filter(groups__name='Organizer').count()
    participant_count = User.objects.filter(groups__name='Participant').count()
    
    # Get recent users
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Get events with most participants (RSVPs)
    popular_events = Event.objects.annotate(
        participant_count=Count('rsvps')
    ).order_by('-participant_count')[:5]
    
    context = {
        'title': 'Admin Dashboard',
        'total_users': total_users,
        'total_events': total_events,
        'total_categories': total_categories,
        'admin_count': admin_count,
        'organizer_count': organizer_count,
        'participant_count': participant_count,
        'total_participants': total_participants,
        'recent_users': recent_users,
        'popular_events': popular_events,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required_allow_inactive
@user_passes_test(is_admin, login_url='/')
def user_list(request):
    """List all users in the system"""
    users = User.objects.all().order_by('-date_joined')
    
    # Get role counts
    admin_count = User.objects.filter(groups__name='Admin').distinct().count()
    organizer_count = User.objects.filter(groups__name='Organizer').distinct().count()
    participant_count = User.objects.filter(groups__name='Participant').distinct().count()
    
    # Get all available groups for the modal
    all_groups = Group.objects.all().order_by('name')
    
    context = {
        'title': 'User Management',
        'users': users,
        'admin_count': admin_count,
        'organizer_count': organizer_count,
        'participant_count': participant_count,
        'all_groups': all_groups,
    }
    return render(request, 'admin_panel/user_list.html', context)


@login_required_allow_inactive
@user_passes_test(is_admin, login_url='/')
def user_detail(request, pk):
    """View details of a specific user"""
    from django.shortcuts import get_object_or_404
    user = get_object_or_404(User, pk=pk)
    context = {
        'title': f'User: {user.username}',
        'user_detail': user,
    }
    return render(request, 'admin_panel/user_detail.html', context)


@login_required_allow_inactive
@user_passes_test(is_admin, login_url='/')
def system_statistics(request):
    """Comprehensive system statistics and analytics"""
    from datetime import date, timedelta
    from django.db.models import Q
    
    today = date.today()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    # User statistics
    users_last_week = User.objects.filter(date_joined__gte=last_week).count()
    users_last_month = User.objects.filter(date_joined__gte=last_month).count()
    
    # Event statistics
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    events_this_month = Event.objects.filter(
        date__year=today.year,
        date__month=today.month
    ).count()
    
    context = {
        'title': 'System Statistics',
        'users_last_week': users_last_week,
        'users_last_month': users_last_month,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'events_this_month': events_this_month,
    }
    return render(request, 'admin_panel/statistics.html', context)


# ==================== Role Management Views ====================

@login_required_allow_inactive
@user_passes_test(is_admin, login_url='/')
def assign_role(request, user_id):
    """Assign role to a user (Admin only)"""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        
        # Clear all existing roles
        user.groups.clear()
        
        # Assign new role
        if role in ['Admin', 'Organizer', 'Participant']:
            group = Group.objects.get(name=role)
            user.groups.add(group)
            messages.success(request, f'Role "{role}" assigned to {user.username}')
        else:
            messages.error(request, 'Invalid role selected')
        
        return redirect('admin_panel:user_list')
    
    # Get all available roles
    roles = Group.objects.all()
    current_role = user.groups.first()
    
    context = {
        'title': f'Assign Role to {user.username}',
        'user': user,
        'roles': roles,
        'current_role': current_role,
    }
    return render(request, 'admin_panel/assign_role.html', context)


@login_required_allow_inactive
@user_passes_test(is_admin, login_url='/')  
def remove_role(request, user_id):
    """Remove role from a user (Admin only)"""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user.groups.clear()
        messages.success(request, f'All roles removed from {user.username}')
        return redirect('admin_panel:user_list')
    
    context = {
        'title': f'Remove Role from {user.username}',
        'user': user,
    }
    return render(request, 'admin_panel/remove_role.html', context)


@login_required_allow_inactive
@user_passes_test(is_admin, login_url='/')
def manage_groups(request):
    """Manage Django groups (Admin only)"""
    groups = Group.objects.annotate(user_count=Count('user')).all()
    
    context = {
        'title': 'Manage Groups',
        'groups': groups,
    }
    return render(request, 'admin_panel/manage_groups.html', context)
