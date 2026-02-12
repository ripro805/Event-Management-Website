from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from datetime import date
from .models import Category, Event, Participant


# ==================== Public Views (Read-Only) ====================
# All CRUD operations (Create, Update, Delete) are in organizer app

def home(request):
    """Dashboard with statistics and filtered event list"""
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    filter_param = request.GET.get('filter', 'today')
    
    # Get today's date
    today = date.today()
    
    # Calculate overall statistics
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    total_categories = Category.objects.count()
    
    # Calculate upcoming and past events counts
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    
    # Base queryset with optimizations
    base_queryset = Event.objects.select_related('category').prefetch_related('participants')
    
    # Apply filters
    if search_query:
        events = base_queryset.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        ).order_by('-date', '-time')
        filter_label = "Search Results"
        filter_param = 'search'
    elif filter_param == 'today':
        events = base_queryset.filter(date=today).order_by('time')
        filter_label = "Today's Events"
    elif filter_param == 'upcoming':
        events = base_queryset.filter(date__gte=today).order_by('date', 'time')
        filter_label = "Upcoming Events"
    elif filter_param == 'past':
        events = base_queryset.filter(date__lt=today).order_by('-date', '-time')
        filter_label = "Past Events"
    elif filter_param == 'all':
        events = base_queryset.all().order_by('-date', '-time')
        filter_label = "All Events"
    else:
        events = base_queryset.filter(date=today).order_by('time')
        filter_label = "Today's Events"
        filter_param = 'today'
    
    # Annotate with participant count
    events = events.annotate(participant_count=Count('participants'))
    
    # Get recent categories
    recent_categories = Category.objects.all()[:5]
    
    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'total_categories': total_categories,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'events': events,
        'filter_param': filter_param,
        'filter_label': filter_label,
        'search_query': search_query,
        'recent_categories': recent_categories,
        'title': 'Dashboard - Event Management System'
    }
    return render(request, 'events/home.html', context)


def event_list(request):
    """Public event listing with filters"""
    events = Event.objects.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants')
    )
    
    # Apply filters
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    
    if category_id:
        events = events.filter(category_id=category_id)
    
    if start_date:
        events = events.filter(date__gte=start_date)
    
    if end_date:
        events = events.filter(date__lte=end_date)
    
    categories = Category.objects.all()
    
    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_id,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
        'title': 'Events'
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    """Public event detail view"""
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('participants'),
        pk=pk
    )
    context = {
        'event': event,
        'title': event.name
    }
    return render(request, 'events/event_detail.html', context)


def category_list(request):
    """Public category listing"""
    categories = Category.objects.prefetch_related('events').all()
    context = {
        'categories': categories,
        'title': 'Categories'
    }
    return render(request, 'events/category_list.html', context)


def category_detail(request, pk):
    """Public category detail view"""
    category = get_object_or_404(Category.objects.prefetch_related('events'), pk=pk)
    events = category.events.all()
    context = {
        'category': category,
        'events': events,
        'title': f'Category: {category.name}'
    }
    return render(request, 'events/category_detail.html', context)


def participant_list(request):
    """Public participant listing"""
    participants = Participant.objects.prefetch_related('events').all()
    context = {
        'participants': participants,
        'title': 'Participants'
    }
    return render(request, 'events/participant_list.html', context)


def participant_detail(request, pk):
    """Public participant detail view"""
    participant = get_object_or_404(
        Participant.objects.prefetch_related('events__category'),
        pk=pk
    )
    context = {
        'participant': participant,
        'title': participant.name
    }
    return render(request, 'events/participant_detail.html', context)
