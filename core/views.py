from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm
from tickets.models import Ticket
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'  # Force role to customer
            user.save()
            login(request, user)
            messages.success(request, "✅ Registration successful. Welcome to your Dashboard!")
            return redirect('dashboard')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard or any page
        else:
            messages.error(request, 'Please enter valid credentials')
            return redirect('login')

    return render(request, 'core/login.html')


@login_required
def dashboard_view(request):
    user = request.user

    if user.role == 'admin':
        tickets = Ticket.objects.all()
    elif user.role == 'agent':
        tickets = Ticket.objects.filter(assigned_to=user)
    else:
        tickets = Ticket.objects.filter(created_by=user)

    stats = {
        'total': tickets.count(),
        'open': tickets.filter(status='open').count(),
        'in_progress': tickets.filter(status='in_progress').count(),
        'resolved': tickets.filter(status='resolved').count(),
        'closed': tickets.filter(status='closed').count(),
        'high_priority': tickets.filter(priority='high').count(),
        'urgent': tickets.filter(priority='urgent').count(),
    }

    return render(request, 'core/dashboard.html', {
        'stats': stats,
        'tickets': tickets,
    })


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def terms_of_service(request):
    """Render the Terms of Service page"""
    return render(request, 'core/terms_of_service.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # 👇 Construct a clearly formatted email body
        email_body = f"""
Name: {name}
Email: {email}
Subject: {subject}
Message:
{message}
"""

        send_mail(
            subject=subject,
            message=email_body,
            from_email=email,
            recipient_list=['ganamunna143@gmail.com'],
        )

        # Optional: Clear previous messages & add success message
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, '✅ Your message has been sent successfully. We will contact you soon!')

        return redirect('contact')
    return render(request, 'core/contact.html')
