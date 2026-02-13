from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import date

from events.models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm


# ==================== Helper Functions ====================


# Custom permission decorator for organizer views
from functools import wraps
def organizer_permission_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        # Check if user is authenticated (skip is_active check for testing)
        if not user.is_authenticated:
            return redirect('user_panel:login')
        # Check if user has organizer or admin permissions
        if not (user.is_superuser or user.groups.filter(name__in=['Admin', 'Organizer']).exists()):
            return render(request, 'nopermission.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==================== Organizer Dashboard ====================

@organizer_permission_required
def organizer_dashboard(request):
    """Organizer dashboard with event management statistics"""
    from django.contrib.auth.models import Group
    
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    
    # Count only participants who are in Participant group
    participant_group = Group.objects.filter(name='Participant').first()
    total_participants = Participant.objects.filter(
        user__isnull=False,
        user__groups=participant_group
    ).count()
    
    upcoming_events = Event.objects.filter(date__gte=date.today()).count()
    
    recent_events = Event.objects.select_related('category').order_by('-date')[:5]
    
    context = {
        'title': 'Organizer Dashboard',
        'total_events': total_events,
        'total_categories': total_categories,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'recent_events': recent_events,
    }
    return render(request, 'organizer/dashboard.html', context)


# ==================== Category Views ====================

@organizer_permission_required
def category_list(request):
    """Display list of all categories"""
    categories = Category.objects.prefetch_related('events').all()
    context = {
        'categories': categories,
        'title': 'Categories Management'
    }
    return render(request, 'organizer/category_list.html', context)


@organizer_permission_required
def category_detail(request, pk):
    """Redirect to public category detail page"""
    return redirect('events:category_detail', pk=pk)


@organizer_permission_required
def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('organizer:category_detail', pk=category.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Create Category',
        'button_text': 'Create Category'
    }
    return render(request, 'organizer/category_form.html', context)


@organizer_permission_required
def category_update(request, pk):
    """Update an existing category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('organizer:category_detail', pk=category.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': f'Update Category: {category.name}',
        'button_text': 'Update Category'
    }
    return render(request, 'organizer/category_form.html', context)


@organizer_permission_required
def category_delete(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('organizer:category_list')
    
    context = {
        'category': category,
        'title': f'Delete Category: {category.name}'
    }
    return render(request, 'organizer/category_confirm_delete.html', context)


# ==================== Event Views ====================

@organizer_permission_required
def event_list(request):
    """Display list of all events with filters"""
    events = Event.objects.select_related('category').prefetch_related('rsvps').annotate(
        participant_count=Count('rsvps')
    )
    
    # Apply filters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    
    if category_id:
        events = events.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'title': 'Events Management'
    }
    return render(request, 'organizer/event_list.html', context)


@organizer_permission_required
def event_detail(request, pk):
    """Redirect to public event detail page"""
    return redirect('events:event_detail', pk=pk)


@organizer_permission_required
def event_create(request):
    """Create a new event"""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" created successfully!')
            return redirect('organizer:event_detail', pk=event.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'title': 'Create Event',
        'button_text': 'Create Event'
    }
    return render(request, 'organizer/event_form.html', context)


@organizer_permission_required
def event_update(request, pk):
    """Update an existing event"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" updated successfully!')
            return redirect('organizer:event_detail', pk=event.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'title': f'Update Event: {event.name}',
        'button_text': 'Update Event'
    }
    return render(request, 'organizer/event_form.html', context)


@organizer_permission_required
def event_delete(request, pk):
    """Delete an event"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'Event "{event_name}" deleted successfully!')
        return redirect('organizer:event_list')
    
    context = {
        'event': event,
        'title': f'Delete Event: {event.name}'
    }
    return render(request, 'organizer/event_confirm_delete.html', context)


# ==================== Participant Views ====================

@organizer_permission_required
def participant_list(request):
    """Display list of all participants"""
    from django.db.models import Count
    from django.contrib.auth.models import Group
    
    # Get Participant group
    participant_group = Group.objects.filter(name='Participant').first()
    
    # Filter participants who have a user and are in Participant group
    participants = Participant.objects.filter(
        user__isnull=False,
        user__groups=participant_group
    ).annotate(
        rsvp_count=Count('user__rsvp')
    ).select_related('user').order_by('name')
    
    context = {
        'participants': participants,
        'title': 'Participants Management'
    }
    return render(request, 'organizer/participant_list.html', context)


@organizer_permission_required
def participant_detail(request, pk):
    """Redirect to public participant detail page"""
    return redirect('events:participant_detail', pk=pk)


@organizer_permission_required
def participant_create(request):
    """Create a new participant"""
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'Participant "{participant.name}" created successfully!')
            return redirect('organizer:participant_detail', pk=participant.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ParticipantForm()
    
    context = {
        'form': form,
        'title': 'Create Participant',
        'button_text': 'Create Participant'
    }
    return render(request, 'organizer/participant_form.html', context)


@organizer_permission_required
def participant_update(request, pk):
    """Update an existing participant"""
    participant = get_object_or_404(Participant, pk=pk)
    
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'Participant "{participant.name}" updated successfully!')
            return redirect('organizer:participant_detail', pk=participant.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ParticipantForm(instance=participant)
    
    context = {
        'form': form,
        'participant': participant,
        'title': f'Update Participant: {participant.name}',
        'button_text': 'Update Participant'
    }
    return render(request, 'organizer/participant_form.html', context)


@organizer_permission_required
def participant_delete(request, pk):
    """Delete a participant"""
    from django.db.models import Count
    
    participant = get_object_or_404(
        Participant.objects.annotate(rsvp_count=Count('user__rsvp')),
        pk=pk
    )
    
    if request.method == 'POST':
        participant_name = participant.name
        participant.delete()
        messages.success(request, f'Participant "{participant_name}" deleted successfully!')
        return redirect('organizer:participant_list')
    
    context = {
        'participant': participant,
        'title': f'Delete Participant: {participant.name}'
    }
    return render(request, 'organizer/participant_confirm_delete.html', context)

