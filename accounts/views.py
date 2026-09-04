from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import SignupForm, LoginForm, ProfileEditForm
from .models import Profile


@require_http_methods(["GET", "POST"])
def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email'].lower().strip()
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('home')

            else:
                form.add_error(
                    None,
                    "Invalid email or password."
                )

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def home(request):
    return render(request, 'home.html')


@login_required
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, current_user=request.user)

        if form.is_valid():
            request.user.first_name = form.cleaned_data['name']
            request.user.email = form.cleaned_data['email']
            request.user.username = form.cleaned_data['email']
            request.user.save()

            profile.age = form.cleaned_data.get('age')
            if form.cleaned_data.get('photo'):
                profile.photo = form.cleaned_data['photo']
            profile.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileEditForm(
            initial={
                'name': request.user.first_name,
                'email': request.user.email,
                'age': profile.age,
            },
            current_user=request.user,
        )

    return render(request, 'profile.html', {'form': form, 'profile': profile})