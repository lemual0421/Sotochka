from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Profile
from .forms import UserRegisterForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)  # Авторизация пользователя после регистрации
            messages.success(request, "Registration successful.")
            return redirect('accounts:profile')  # Перенаправление на страницу профиля
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileUpdateForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'profile': request.user.profile})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('accounts:profile')  # Убедитесь, что namespace 'accounts' указан
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('accounts:login')  # Убедитесь, что namespace 'accounts' указан
