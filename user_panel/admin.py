from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register the custom user model so you can manage users in the admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin configuration"""
    model = CustomUser
    
    # Fields for the user detail/edit view
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('profile_picture', 'phone_number')}),
    )
    
    # Fields for creating a new user
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'phone_number')}),
    )
    
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('username',)
