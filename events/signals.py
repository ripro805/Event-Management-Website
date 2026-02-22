from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import RSVP, Event
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

User = get_user_model()

# 1. Send account activation email after user registration
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_activation_email(sender, instance, created, **kwargs):
    """
    Send activation email when user is created and not active
    User must click the activation link to activate their account
    """
    if created and not instance.is_active:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)
        activation_link = f"{settings.SITE_URL}/user/activate/{uid}/{token}/"
        
        subject = '✉️ Activate Your Account - Event Management System'
        message = f'''
Hi {instance.get_full_name() or instance.username},

🎉 Welcome to Event Management System!

Thank you for signing up. To complete your registration, please activate your account by clicking the link below:

🔗 Activation Link:
{activation_link}

⚠️ Important: This link will expire in 24 hours.

Once activated, you can:
✓ Browse and RSVP to exciting events
✓ Manage your RSVPs from your dashboard
✓ Receive event notifications and updates

If you did not create this account, please ignore this email.

Best regards,
Event Management Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated email. Please do not reply to this message.
Event Management System - {settings.SITE_URL}
        '''
        
        try:
            print(f"[RenderLog] Attempting to send activation email to {instance.email}")
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
            print(f"[RenderLog] Activation email send attempted to {instance.email}")
        except Exception as e:
            print(f"❌ Error sending activation email to {instance.email}: {e}")

# 2. Send RSVP confirmation email after RSVP
@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation(sender, instance, created, **kwargs):
    """Send RSVP confirmation email when user RSVPs"""
    if created:
        event = instance.event
        user = instance.user
        
        # Format date and time nicely
        event_date = event.date.strftime("%B %d, %Y")  # e.g., "January 15, 2026"
        event_time = event.time.strftime("%I:%M %p")   # e.g., "02:30 PM"
        
        subject = f'✓ RSVP Confirmation - {event.name}'
        message = f'''
Hi {user.get_full_name() or user.username},

Great news! You have successfully RSVP'd to the following event:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVENT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Event Name: {event.name}
📂 Category: {event.category.name}
📅 Date: {event_date}
⏰ Time: {event_time}
📍 Location: {event.location}

{event.description[:200]}{'...' if len(event.description) > 200 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Total Participants: {event.rsvp_set.count()} (including you!)

We look forward to seeing you there!

📧 If you need to cancel your RSVP, please log in to your account at:
{settings.SITE_URL}/user/dashboard/

Best regards,
Event Management Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated email. Please do not reply to this message.
Event Management System - {settings.SITE_URL}
        '''
        
        try:
            print(f"[RenderLog] Attempting to send RSVP confirmation email to {user.email} for event '{event.name}'")
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            print(f"[RenderLog] RSVP confirmation email send attempted to {user.email} for event '{event.name}'")
        except Exception as e:
            print(f"✗ Error sending RSVP confirmation email to {user.email}: {e}")


# 2b. Handle ManyToMany field direct manipulation (event.rsvps.add(user))
@receiver(m2m_changed, sender=Event.rsvps.through)
def send_rsvp_email_on_m2m_add(sender, instance, action, pk_set, **kwargs):
    """
    Send RSVP confirmation email when user is added directly to event.rsvps
    This handles: event.rsvps.add(user) 
    Separate from post_save signal which handles: RSVP.objects.create()
    """
    if action == "post_add" and pk_set:
        # instance is Event, pk_set contains User IDs
        event = instance
        
        for user_id in pk_set:
            try:
                user = User.objects.get(pk=user_id)
                
                # Format date and time nicely
                event_date = event.date.strftime("%B %d, %Y")
                event_time = event.time.strftime("%I:%M %p")
                
                subject = f'✓ RSVP Confirmation - {event.name}'
                message = f'''
Hi {user.get_full_name() or user.username},

Great news! You have successfully RSVP'd to the following event:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVENT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Event Name: {event.name}
📂 Category: {event.category.name}
📅 Date: {event_date}
⏰ Time: {event_time}
📍 Location: {event.location}

{event.description[:200]}{'...' if len(event.description) > 200 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Total Participants: {event.rsvp_set.count()} (including you!)

We look forward to seeing you there!

📧 If you need to cancel your RSVP, please log in to your account at:
{settings.SITE_URL}/user/dashboard/

Best regards,
Event Management Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated email. Please do not reply to this message.
Event Management System - {settings.SITE_URL}
                '''
                
                print(f"[RenderLog] Attempting to send M2M RSVP confirmation email to {user.email} for event '{event.name}'")
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                print(f"[RenderLog] M2M RSVP confirmation email send attempted to {user.email} for event '{event.name}'")
                
            except User.DoesNotExist:
                print(f"✗ User with ID {user_id} not found")
            except Exception as e:
                print(f"✗ Error sending M2M RSVP email: {e}")


# 3. Auto-assign Participant role to new users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_default_role(sender, instance, created, **kwargs):
    """Automatically assign Participant group to newly created users"""
    if created:
        # Get or create Participant group
        participant_group, group_created = Group.objects.get_or_create(name='Participant')
        # Add user to Participant group
        instance.groups.add(participant_group)
        # Note: No need to call instance.save() as groups are ManyToMany


# 4. Create Participant record for new users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
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

