from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import Category, Event, Participant, RSVP

# RSVP Admin
@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'responded_at')
    search_fields = ('user__username', 'event__name')
    list_filter = ('responded_at',)
    ordering = ('-responded_at',)


# ==================== Custom User Admin ====================

class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User admin with role management"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_roles', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # Use base fieldsets without adding groups again (it's already in BaseUserAdmin)
    filter_horizontal = ('groups', 'user_permissions')
    
    def get_roles(self, obj):
        """Display user's roles"""
        roles = obj.groups.values_list('name', flat=True)
        return ', '.join(roles) if roles else 'No Role'
    get_roles.short_description = 'Roles'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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
