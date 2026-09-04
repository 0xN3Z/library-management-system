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
    from django.contrib.auth.models import User


class ProfileEditForm(forms.Form):

    name = forms.CharField(max_length=150, strip=True)

    email = forms.EmailField(max_length=254)

    age = forms.IntegerField(required=False, min_value=1, max_value=120)

    photo = forms.ImageField(required=False)

    def __init__(self, *args, current_user=None, **kwargs):
        self.current_user = current_user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()

        # Allow keeping the same email, but block switching to someone else's.
        if User.objects.filter(username=email).exclude(pk=self.current_user.pk).exists():
            raise forms.ValidationError("This email is already in use by another account.")

        return email