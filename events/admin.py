from django.contrib import admin
from .models import Category, Event, Participant, RSVP

# RSVP Admin
@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'responded_at')
    search_fields = ('user__username', 'event__name')
    list_filter = ('responded_at',)
    ordering = ('-responded_at',)


# ==================== Category Admin ====================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    list_display = ('name', 'description', 'event_count')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 20
    
    def event_count(self, obj):
        """Display number of events in this category"""
        return obj.events.count()
    event_count.short_description = 'Number of Events'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin configuration for Event model"""
    list_display = ('name', 'category', 'date', 'time', 'location', 'participant_count', 'created_at')
    list_filter = ('category', 'date', 'created_at')
    search_fields = ('name', 'description', 'location')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    list_per_page = 20
    autocomplete_fields = ['category']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Schedule', {
            'fields': ('date', 'time', 'location')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def participant_count(self, obj):
        """Display number of participants (RSVPs)"""
        return obj.rsvps.count()
    participant_count.short_description = 'Participants'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    """Admin configuration for Participant model"""
    list_display = ('name', 'email', 'event_count', 'registered_at')
    search_fields = ('name', 'email')
    list_filter = ('registered_at',)
    date_hierarchy = 'registered_at'
    ordering = ('name',)
    list_per_page = 20
    filter_horizontal = ('events',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email')
        }),
        ('Events', {
            'fields': ('events',)
        }),
        ('Registration Info', {
            'fields': ('registered_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('registered_at',)
    
    def event_count(self, obj):
        """Display number of events participant is registered for"""
        return obj.events.count()
    event_count.short_description = 'Events Registered'
