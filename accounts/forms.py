import os
from io import BytesIO

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from PIL import Image


ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_UPLOAD_SIZE_MB = 3


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

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
            return photo

        # 1. Reject oversized files before doing any further processing.
        max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if photo.size > max_bytes:
            raise forms.ValidationError(
                f"Image is too large. Maximum allowed size is {MAX_UPLOAD_SIZE_MB}MB."
            )

        # 2. Reject anything whose declared MIME type isn't an allowed image type.
        # This blocks obvious mismatches like a .php file renamed to .jpg.
        content_type = getattr(photo, 'content_type', None)
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise forms.ValidationError("Only JPEG, PNG, and WEBP images are allowed.")

        # 3. Reject extensions that don't match an allowed image extension,
        # even if the MIME type header was spoofed.
        ext = os.path.splitext(photo.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise forms.ValidationError("Unsupported file extension.")

        # 4. Actually open and decode the image with Pillow. This is the real
        # check — it forces the file to be parsed as a genuine image. A
        # disguised script or corrupted/malicious file will fail here even if
        # it passed the MIME type and extension checks above.
        try:
            photo.seek(0)
            img = Image.open(photo)
            img.verify()  # raises if the file isn't a valid, complete image
        except Exception:
            raise forms.ValidationError("This file is not a valid image.")

        # 5. Guard against decompression-bomb style images (huge pixel
        # dimensions that are cheap to store but expensive to process).
        photo.seek(0)
        img = Image.open(photo)
        max_pixels = 20_000_000  # ~20 megapixels
        if img.width * img.height > max_pixels:
            raise forms.ValidationError("Image resolution is too large.")

        # Reset the file pointer so Django can actually save it afterwards.
        photo.seek(0)
        return photo