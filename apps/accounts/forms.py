from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')})
    )
    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Company name')})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'company_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm password')})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username or email')})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')})
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'avatar',
            'company_name', 'vat_number', 'address', 'city', 'country', 'postal_code',
            'language', 'timezone'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vat_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
            'timezone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StripeSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['stripe_publishable_key', 'stripe_secret_key']
        widgets = {
            'stripe_publishable_key': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'pk_live_...'
            }),
            'stripe_secret_key': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'sk_live_...'
            }),
        }
        help_texts = {
            'stripe_publishable_key': _('Your Stripe publishable key for accepting payments from your customers'),
            'stripe_secret_key': _('Your Stripe secret key (kept secure and never displayed)'),
        }


class ResendSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['resend_api_key', 'resend_from_email', 'resend_from_name']
        widgets = {
            'resend_api_key': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 're_...'
            }),
            'resend_from_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'noreply@yourdomain.com'
            }),
            'resend_from_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Company Name'
            }),
        }
        help_texts = {
            'resend_api_key': _('Your Resend API key from resend.com (kept secure and never displayed)'),
            'resend_from_email': _('Email address to send from (must be verified in your Resend account)'),
            'resend_from_name': _('Name to display in the "from" field of emails'),
        }

