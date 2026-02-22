import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """Validate phone number format: should be 10-15 digits, optionally starting with +"""
    pattern = r'^\+?[0-9]{10,15}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Phone number must be 10-15 digits and can optionally start with +'
        )


class CustomUser(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser
    Includes profile picture and phone number fields
    """
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name="Profile Picture"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[validate_phone_number],
        verbose_name="Phone Number"
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.username
    
    def get_role(self):
        """Returns the user's primary role"""
        if self.is_superuser:
            return 'Admin'
        elif self.groups.filter(name='Admin').exists():
            return 'Admin'
        elif self.groups.filter(name='Organizer').exists():
            return 'Organizer'
        elif self.groups.filter(name='Participant').exists():
            return 'Participant'
        return 'User'
    
    @property
    def profile_picture_url(self):
        """Returns the profile picture URL or default"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/default_avatar.svg'
