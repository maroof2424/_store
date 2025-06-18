# products/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=Feedback.RATING_CHOICES,
                attrs={
                    'class': 'form-select form-select-lg mb-3',
                    'style': 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'
                }
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this product...',
                'style': 'border-radius: 15px; border: 2px solid #e3f2fd;'
            })
        }

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Choose a username',
            'style': 'border-radius: 25px; padding: 15px 20px; border: 2px solid #e3f2fd;'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email',
            'style': 'border-radius: 25px; padding: 15px 20px; border: 2px solid #e3f2fd;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Create a password',
            'style': 'border-radius: 25px; padding: 15px 20px; border: 2px solid #e3f2fd;'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm your password',
            'style': 'border-radius: 25px; padding: 15px 20px; border: 2px solid #e3f2fd;'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords don't match!")
        
        return cleaned_data

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your username',
            'style': 'border-radius: 25px; padding: 15px 20px; border: 2px solid #e3f2fd;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password',
            'style': 'border-radius: 25px; padding: 15px 20px; border: 2px solid #e3f2fd;'
        })
    )