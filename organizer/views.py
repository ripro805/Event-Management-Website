from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from datetime import date

from events.models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm


# ==================== Helper Functions ====================

def is_admin_or_organizer(user):
    """Check if user is Admin or Organizer"""
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name__in=['Admin', 'Organizer']).exists()


# ==================== Organizer Dashboard ====================

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def organizer_dashboard(request):
    """Organizer dashboard with event management statistics"""
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    total_participants = Participant.objects.count()
    
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

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def category_list(request):
    """Display list of all categories"""
    categories = Category.objects.prefetch_related('events').all()
    context = {
        'categories': categories,
        'title': 'Categories Management'
    }
    return render(request, 'organizer/category_list.html', context)


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def category_detail(request, pk):
    """Redirect to public category detail page"""
    return redirect('events:category_detail', pk=pk)


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
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


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
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


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
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

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def event_list(request):
    """Display list of all events with filters"""
    events = Event.objects.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants')
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


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def event_detail(request, pk):
    """Redirect to public event detail page"""
    return redirect('events:event_detail', pk=pk)


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def event_create(request):
    """Create a new event"""
    if request.method == 'POST':
        form = EventForm(request.POST)
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


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def event_update(request, pk):
    """Update an existing event"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
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


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
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

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def participant_list(request):
    """Display list of all participants"""
    participants = Participant.objects.prefetch_related('events').all()
    context = {
        'participants': participants,
        'title': 'Participants Management'
    }
    return render(request, 'organizer/participant_list.html', context)


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def participant_detail(request, pk):
    """Redirect to public participant detail page"""
    return redirect('events:participant_detail', pk=pk)


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
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


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
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


@login_required
@user_passes_test(is_admin_or_organizer, login_url='/')
def participant_delete(request, pk):
    """Delete a participant"""
    participant = get_object_or_404(Participant, pk=pk)
    
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

