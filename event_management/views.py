from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail

def about(request):
    return render(request, 'about.html')

def contact(request):
    success = False
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = f"Contact Form Submission from {first_name} {last_name}"
        body = f"Name: {first_name} {last_name}\nMobile: {mobile}\nEmail: {email}\n\nMessage:\n{message}"
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        success = True
    return render(request, 'contact.html', {"success": success})
