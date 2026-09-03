from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):

    name = forms.CharField(
        max_length=150,
        strip=True,
        error_messages={'required': 'Full name is required.'}
    )

    email = forms.EmailField(
        max_length=254,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
        error_messages={'required': 'Password is required.'}
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
        error_messages={'required': 'Please confirm your password.'}
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "Unable to create account with this email."
            )

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):

    email = forms.EmailField(
        max_length=254,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
        error_messages={'required': 'Password is required.'}
    )