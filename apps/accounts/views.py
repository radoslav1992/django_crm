from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, StripeSettingsForm, ResendSettingsForm
from apps.subscriptions.models import Subscription


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('crm:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create free subscription for new user
            Subscription.objects.create(
                user=user,
                plan='free',
                status='active'
            )
            login(request, user)
            messages.success(request, _('Welcome! Your account has been created successfully.'))
            return redirect('crm:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('crm:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Welcome back!'))
                return redirect('crm:dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, _('You have been logged out successfully.'))
    return redirect('accounts:login')


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated successfully.'))
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def stripe_settings(request):
    """Stripe settings view for user's payment processing"""
    if request.method == 'POST':
        form = StripeSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your Stripe settings have been updated successfully.'))
            return redirect('accounts:stripe_settings')
    else:
        form = StripeSettingsForm(instance=request.user)
    
    return render(request, 'accounts/stripe_settings.html', {'form': form})


@login_required
def resend_settings(request):
    """Resend email settings view"""
    if request.method == 'POST':
        form = ResendSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your Resend email settings have been updated successfully.'))
            return redirect('accounts:resend_settings')
    else:
        form = ResendSettingsForm(instance=request.user)
    
    return render(request, 'accounts/resend_settings.html', {
        'form': form,
        'has_resend_configured': request.user.has_resend_configured()
    })


def landing_page(request):
    """Landing page for the CRM"""
    if request.user.is_authenticated:
        return redirect('crm:dashboard')
    
    from django.conf import settings
    plans = settings.SUBSCRIPTION_PLANS
    
    return render(request, 'accounts/landing.html', {'plans': plans})

