# ==================== Imports ====================
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from functools import wraps

from events.models import Event, Participant, RSVP
from .forms import UserSignupForm, UserLoginForm, EditProfileForm, CustomPasswordResetForm, CustomSetPasswordForm

User = get_user_model()


# ==================== Profile Views ====================

class ProfileView(LoginRequiredMixin, TemplateView):
    """View user profile - dynamic based on role"""
    template_name = 'user_panel/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['role'] = user.get_role()
        
        # Role-specific context
        if context['role'] == 'Admin':
            context['admin_stats'] = {
                'total_users': User.objects.count(),
                'total_events': Event.objects.count(),
            }
        elif context['role'] == 'Organizer':
            # Add organizer-specific stats if needed
            context['organizer_stats'] = {
                'events_created': Event.objects.count(),
            }
        elif context['role'] == 'Participant':
            # Add participant-specific stats
            context['participant_stats'] = {
                'rsvp_count': RSVP.objects.filter(user=user).count(),
            }
        
        return context


# ==================== Edit Profile View ====================

class EditProfileView(LoginRequiredMixin, UpdateView):
    """Edit user profile using UpdateView CBV"""
    model = User
    form_class = EditProfileForm
    template_name = 'user_panel/edit_profile.html'
    success_url = reverse_lazy('user_panel:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


# ==================== Change Password View ====================

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    """Change password view using CBV"""
    template_name = 'user_panel/change_password.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        # Add styling to form fields
        for field in form.fields.values():
            field.widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('user_panel:profile')
        # Add styling to form fields
        for field in form.fields.values():
            field.widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        return render(request, self.template_name, {'form': form})


# ==================== Password Reset Views ====================

class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view"""
    template_name = 'user_panel/password_reset.html'
    email_template_name = 'user_panel/password_reset_email.html'
    subject_template_name = 'user_panel/password_reset_subject.txt'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('user_panel:password_reset_done')
    
    def form_valid(self, form):
        messages.info(self.request, 'Password reset email has been sent. Please check your inbox.')
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Custom password reset done view"""
    template_name = 'user_panel/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view"""
    template_name = 'user_panel/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('user_panel:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Custom password reset complete view"""
    template_name = 'user_panel/password_reset_complete.html'


# ==================== Helper Functions ====================

# Custom login_required that works with inactive users (for testing)
def login_required_allow_inactive(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user_panel:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==================== Account Activation ====================

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated! You can now log in.')
            return redirect('user_panel:login')
        else:
            messages.info(request, 'Account already activated. Please log in.')
            return redirect('user_panel:login')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('events:home')


# ==================== Authentication Views ====================

def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('user_panel:dashboard')
    
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User must activate via email link
            user.save()
            
            messages.success(
                request, 
                f'✓ Account created successfully! Please check your email ({user.email}) for an activation link to complete your registration.'
            )
            return redirect('user_panel:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserSignupForm()
    
    return render(request, 'user_panel/signup.html', {
        'form': form,
        'title': 'Sign Up - Create Your Account'
    })


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('user_panel:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate user (only active users can login)
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Role-based redirect
                if user.is_superuser or user.groups.filter(name='Admin').exists():
                    return redirect('admin_panel:admin_dashboard')
                elif user.groups.filter(name='Organizer').exists():
                    return redirect('organizer:dashboard')
                else:
                    return redirect('user_panel:dashboard')
            else:
                # Check if user exists but is inactive
                try:
                    inactive_user = User.objects.get(username=username)
                    if not inactive_user.is_active:
                        messages.warning(request, '⚠️ Your account is not activated yet. Please check your email for the activation link.')
                    else:
                        messages.error(request, 'Invalid username or password. Please try again.')
                except User.DoesNotExist:
                    messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    
    return render(request, 'user_panel/login.html', {
        'form': form,
        'title': 'Login - Access Your Account'
    })


def logout_view(request):
    """User logout view"""
    username = request.user.username if request.user.is_authenticated else None
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return render(request, 'user_panel/logout.html', {
        'title': 'Logged Out',
        'username': username
    })


# ==================== Dashboard Views ====================

@login_required_allow_inactive
def dashboard_view(request):
    """Participant dashboard"""
    user = request.user
    from datetime import date
    
    # Get user's RSVP'd events
    rsvp_events = []
    if user.is_authenticated:
        rsvps = RSVP.objects.filter(user=user).select_related('event', 'event__category').order_by('-event__date')
        rsvp_events = [rsvp.event for rsvp in rsvps]
    
    # Get upcoming events
    today = date.today()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date', 'time')[:6]
    
    context = {
        'title': 'My Dashboard',
        'rsvp_events': rsvp_events,
        'upcoming_events': upcoming_events,
        'total_rsvps': len(rsvp_events),
    }
    return render(request, 'user_panel/dashboard.html', context)


@login_required_allow_inactive
def rsvp_event(request, event_id):
    """RSVP to an event"""
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    
    # Check if user already RSVP'd
    existing_rsvp = RSVP.objects.filter(event=event, user=user).first()
    
    if existing_rsvp:
        messages.warning(request, f'You have already RSVP\'d to "{event.name}".')
    else:
        # Create RSVP
        RSVP.objects.create(
            event=event,
            user=user
        )
        messages.success(request, f'✓ Successfully RSVP\'d to "{event.name}"!')
    
    return redirect('events:event_detail', pk=event_id)


@login_required_allow_inactive
def my_rsvps_view(request):
    """View user's RSVPs"""
    user = request.user
    my_rsvps = RSVP.objects.filter(user=user).select_related('event', 'event__category').order_by('-event__date')
    
    context = {
        'title': 'My RSVPs',
        'my_rsvps': my_rsvps,
        'total_rsvps': my_rsvps.count(),
    }
    return render(request, 'user_panel/my_rsvps.html', context)

