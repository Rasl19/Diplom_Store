from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib import auth, messages


def login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # username = request.POST['username']
            # password = request.POST['password']
            user = auth.authenticate(**form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect('index')
    return render(request, 'users/login.html', {'form': form})


def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за регистрацию!')
            return redirect('login')
    return render(request, 'users/register.html', {'form': form})


def profile(request):
    form = UserProfileForm(instance=request.user)
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {
        'title': 'Store - Профиль',
        'form': form
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')
