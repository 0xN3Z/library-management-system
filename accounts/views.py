from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import SignupForm, LoginForm


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