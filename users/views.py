from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib import auth, messages
from products.models import Basket
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from common.views import TitleMixin
from users.models import MyUser, EmailVerification
from django.urls import reverse


def login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
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


@login_required
def profile(request):
    form = UserProfileForm(instance=request.user)
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {
        'title': 'Store - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = MyUser.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        return redirect(reverse('index'))
