from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings
from .models import RSVP, Event
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

# 1. Send account activation email after user registration
@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    """Send activation email only when user is created and not active"""
    if created and not instance.is_active:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)
        activation_link = f"{settings.SITE_URL}/user/activate/{uid}/{token}/"
        
        subject = 'Activate Your Account - Event Management System'
        message = f'''
Hi {instance.username},

Welcome to Event Management System!

Please click the link below to activate your account:
{activation_link}

This link will expire in 24 hours.

Thank you!
Event Management Team
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending activation email: {e}")

# 2. Send RSVP confirmation email after RSVP
@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation(sender, instance, created, **kwargs):
    """Send RSVP confirmation email when user RSVPs"""
    if created:
        event = instance.event
        user = instance.user
        
        subject = f'RSVP Confirmation - {event.name}'
        message = f'''
Hi {user.username},

You have successfully RSVP'd to the following event:

Event: {event.name}
Date: {event.date}
Time: {event.time}
Location: {event.location}

We look forward to seeing you there!

Thank you!
Event Management Team
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending RSVP confirmation email: {e}")


# 3. Auto-assign Participant role to new users
@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    """Automatically assign Participant group to newly created users"""
    if created:
        # Get or create Participant group
        participant_group, group_created = Group.objects.get_or_create(name='Participant')
        # Add user to Participant group
        instance.groups.add(participant_group)
        # Note: No need to call instance.save() as groups are ManyToMany


# 4. Create Participant record for new users
@receiver(post_save, sender=User)
def create_participant_record(sender, instance, created, **kwargs):
    """Create a Participant record when a new user registers"""
    from .models import Participant
    
    if created:
        # Check if Participant record already exists
        if not Participant.objects.filter(email=instance.email).exists():
            # Create Participant record
            Participant.objects.create(
                name=instance.get_full_name() or instance.username,
                email=instance.email,
                user=instance
            )
