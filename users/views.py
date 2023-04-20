from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy

from django.views.generic.edit import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from products.models import Basket
from django.contrib.auth.views import LoginView
from common.views import TitleMixin
from django.contrib.auth.decorators import login_required


class UserLoginView(TitleMixin, LoginView):
    # Модель уже определена в settings.py:  AUTH_USER_MODEL = 'users.User'
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('index')  # Так не заработало. Тогда прописали в settings.py: LOGIN_REDIRECT_URL = '/'
    title = 'Store - Авторизация'

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)  # заполняем форму полученными данными
#         if form.is_valid():
#             username = request.POST['username']  # получаем данные
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)  # проверка подлинности (существования) пользователя
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(redirect_to=reverse('index'))
#     else:  # request.method == 'GET' запрос
#         form = UserLoginForm()
#     # context = {'form': UserLoginForm()}
#     context = {'form': form}
#     return render(request, 'users/login.html', context=context)

# Класс LogoutView взяли целиком как есть и указали его в users/urls.py.
# Только прописали в settings.py: LOGOUT_REDIRECT_URL = '/'

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(redirect_to=reverse('index'))


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):  # SuccessMessageMixin - создание всплывающего сообщения
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы!'
    title = 'Store - Регистрация'

    # через миксин "TitleMixin"
    # def get_context_data(self, **kwargs):
    #     context = super(UserRegistrationView, self).get_context_data()
    #     context['title'] = 'Store - Регистрация'
    #     return context


# Решение через FBV
# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             # Вывод сообщения об успешной регистрации
#             messages.success(request, 'Вы успешно зарегистрированы!')
#             return HttpResponseRedirect(redirect_to=reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context=context)


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    # Атрибут для LoginRequiredMixin, служащий для перенаправления пользователя который не залогинен
    login_url = reverse_lazy('users:login')
    # success_url = reverse_lazy('users:profile')  # Нет возможности передать <int:pk>
    title = 'Store - Личный кабинет'

    # Переопределяем метод "get_success_url()" для возможности передачи <int:pk> в роут
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))  # "id,))"  - запятая, т.к. это кортеж

    # Возможность извлечения одного объекта для дальнейших манипуляций "class SingleObjectMixin(ContextMixin)".
    # Переопределяем его "метод get_object()"
    # Получаем объект исходя из id пользователя, который сделал запрос.
    # При данной реализации нет необходимости передавать pk в ссылке
    # def get_object(self, queryset=None):
    #     queryset = self.get_queryset()
    #     user = queryset.get(pk=self.request.user.id)
    #     return user

    #  Улучшаем (для исключения двух одинаковых запросов)
    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        # context['title'] = 'Store - Личный кабинет'  # через миксин "TitleMixin"
        context['baskets'] = Basket.objects.filter(user=self.object)  # равнозначный метод
        # context['baskets'] = Basket.objects.filter(user=self.request.user)  # равнозначный метод
        return context



# Декоратор доступа
# Контролер не будет отрабатывать, пока не будет произведена авторизация
# @login_required
# def profile(request):
#     if request.method == "POST":
#         # files=request.FILES   - для загрузки изображений
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(redirect_to=reverse('users:profile'))
#         # Так можно для проверки выводить в консоль ошибки
#         else:
#             print(form.errors)
#     else:
#         # instance= (экземпляр)
#         # instance=request.user передаем объект текущего пользователя
#         form = UserProfileForm(instance=request.user)
#
#     # Получение общей суммы и кол-ва товаров в корзине текущего пользователя через логику контроллера:
#     # Реализация 2-х вариантов. Третий вариант реализован в модели products/models.py -> line 26, 43
#     # baskets = Basket.objects.filter(user=request.user)  # Корзина текущего пользователя
#
#     # 1-й вариант
#     # total_sum = 0
#     # total_quantity = 0
#     # for item in baskets:
#     #     total_sum += item.sum_goods()
#     #     total_quantity += item.quantity
#
#     # 2-й вариант
#     # Используем встроенную python функцию sum()
#     # total_sum = sum(item.sum_goods() for item in baskets)
#     # total_quantity = sum(item.quantity for item in baskets)
#
#     context = {
#         'title': 'Store - Профиль',
#         'form': form,
#         # Внимание !!! При реализации 3-го варианта (в модели products/models.py -> 43) 'objects' переопределен
#         'baskets': Basket.objects.filter(user=request.user),  # Корзина текущего пользователя
#         # 'total_sum': total_sum,
#         # 'total_quantity': total_quantity,
#     }
#     return render(request, 'users/profile.html', context=context)

