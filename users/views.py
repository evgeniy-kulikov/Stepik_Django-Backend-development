from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # заполняем форму полученными данными
        if form.is_valid():
            username = request.POST['username']  # получаем данные
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)  # проверка подлинности (существования) пользователя
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_to=reverse('index'))
    else:  # request.method == 'GET' запрос
        form = UserLoginForm()
    # context = {'form': UserLoginForm()}
    context = {'form': form}
    return render(request, 'users/login.html', context=context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context=context)
