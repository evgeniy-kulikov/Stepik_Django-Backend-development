from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from products.models import Basket
from django.contrib.auth.decorators import login_required


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
            # Вывод сообщения об успешной регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return HttpResponseRedirect(redirect_to=reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context=context)


# Декоратор доступа
# Контролер не будет отрабатывать, пока не будет произведена авторизация
@login_required
def profile(request):
    if request.method == "POST":
        # files=request.FILES   - для загрузки изображений
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to=reverse('users:profile'))
        # Так можно для проверки выводить в консоль ошибки
        else:
            print(form.errors)
    else:
        # instance= (экземпляр)
        # instance=request.user передаем объект текущего пользователя
        form = UserProfileForm(instance=request.user)

    # Получение общей суммы и кол-ва товаров в корзине текущего пользователя через логику контроллера:
    # Реализация 2-х вариантов. Третий вариант реализован в модели products/models.py -> line 26, 43
    # baskets = Basket.objects.filter(user=request.user)  # Корзина текущего пользователя

    # 1-й вариант
    # total_sum = 0
    # total_quantity = 0
    # for item in baskets:
    #     total_sum += item.sum_goods()
    #     total_quantity += item.quantity

    # 2-й вариант
    # Используем встроенную python функцию sum()
    # total_sum = sum(item.sum_goods() for item in baskets)
    # total_quantity = sum(item.quantity for item in baskets)

    context = {
        'title': 'Store - Профиль',
        'form': form,
        # Внимание !!! При реализации 3-го варианта (в модели products/models.py -> 43) 'objects' переопределен
        'baskets': Basket.objects.filter(user=request.user),  # Корзина текущего пользователя
        # 'total_sum': total_sum,
        # 'total_quantity': total_quantity,
    }
    return render(request, 'users/profile.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(redirect_to=reverse('index'))
