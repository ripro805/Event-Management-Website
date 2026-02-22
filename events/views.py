from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from datetime import date
from .models import Category, Event, Participant


# ==================== Public Views (Read-Only) ====================
# All CRUD operations (Create, Update, Delete) are in organizer app

def home(request):
    """Dashboard with statistics and filtered event list"""
    from django.contrib.auth.models import Group
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    filter_param = request.GET.get('filter', 'today')
    
    # Get today's date
    today = date.today()
    
    # Calculate overall statistics
    total_events = Event.objects.count()
    
    # Count only participants who are in Participant group
    participant_group = Group.objects.filter(name='Participant').first()
    total_participants = Participant.objects.filter(
        user__isnull=False,
        user__groups=participant_group
    ).count()
    
    total_categories = Category.objects.count()
    
    # Calculate upcoming and past events counts
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    
    # Base queryset with optimizations
    base_queryset = Event.objects.select_related('category').prefetch_related('rsvps')
    
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
    
    # Annotate with RSVP count
    events = events.annotate(rsvp_count=Count('rsvps'))
    
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


class EventListView(ListView):
    """Public event listing with filters (Converted to CBV)"""
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        """Apply filters and annotations to queryset"""
        queryset = Event.objects.select_related('category').prefetch_related('rsvps').annotate(
            rsvp_count=Count('rsvps')
        )
        
        # Apply filters
        search_query = self.request.GET.get('search', '').strip()
        category_id = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(location__icontains=search_query)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['search_query'] = self.request.GET.get('search', '').strip()
        context['title'] = 'Events'
        return context


class EventDetailView(DetailView):
    """Public event detail view (Converted to CBV)"""
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        """Optimize queryset with select_related and prefetch_related"""
        return Event.objects.select_related('category').prefetch_related('rsvps')
    
    def get_context_data(self, **kwargs):
        """Add user RSVP status to context"""
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Check if user already RSVP'd
        user_rsvp = False
        if self.request.user.is_authenticated:
            from .models import RSVP
            user_rsvp = RSVP.objects.filter(user=self.request.user, event=event).exists()
        
        context['user_rsvp'] = user_rsvp
        context['title'] = event.name
        return context


class CategoryListView(ListView):
    """Public category listing (Converted to CBV)"""
    model = Category
    template_name = 'events/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        """Optimize queryset with prefetch_related"""
        return Category.objects.prefetch_related('events').all()
    
    def get_context_data(self, **kwargs):
        """Add title to context"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categories'
        return context


class CategoryDetailView(DetailView):
    """Public category detail view (Converted to CBV)"""
    model = Category
    template_name = 'events/category_detail.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        """Optimize queryset with prefetch_related"""
        return Category.objects.prefetch_related('events')
    
    def get_context_data(self, **kwargs):
        """Add events and title to context"""
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['events'] = category.events.all()
        context['title'] = f'Category: {category.name}'
        return context


class ParticipantListView(ListView):
    """Public participant listing (Converted to CBV)"""
    model = Participant
    template_name = 'events/participant_list.html'
    context_object_name = 'participants'
    
    def get_queryset(self):
        """Filter participants who are in Participant group with RSVP count"""
        from django.contrib.auth.models import Group
        
        # Get Participant group
        participant_group = Group.objects.filter(name='Participant').first()
        
        # Filter participants who have a user and are in Participant group
        return Participant.objects.filter(
            user__isnull=False,
            user__groups=participant_group
        ).annotate(
            rsvp_count=Count('user__rsvp')
        ).select_related('user').order_by('name')
    
    def get_context_data(self, **kwargs):
        """Add title to context"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Participants'
        return context


def participant_detail(request, pk):
    """Public participant detail view"""
    from django.db.models import Count
    
    participant = get_object_or_404(
        Participant.objects.annotate(
            rsvp_count=Count('user__rsvp')
        ).select_related('user'),
        pk=pk
    )
    
    # Get RSVP'd events
    rsvp_events = []
    if participant.user:
        from .models import RSVP
        rsvps = RSVP.objects.filter(user=participant.user).select_related('event', 'event__category').order_by('-event__date')
        rsvp_events = [rsvp.event for rsvp in rsvps]
    
    context = {
        'participant': participant,
        'rsvp_events': rsvp_events,
        'title': participant.name
    }
    return render(request, 'events/participant_detail.html', context)
