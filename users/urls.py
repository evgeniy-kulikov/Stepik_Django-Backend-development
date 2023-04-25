from django.urls import path
from users.views import UserRegistrationView, UserProfileView, UserLoginView, \
    EmailVerificationView  # login, logout, registration, profile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    # path('login/', login, name='login'),

    path('registration/', UserRegistrationView.as_view(), name='registration'),
    # path('registration/', registration, name='registration'),

    # Подключаем декоратор доступа (перебрасывает на 'login' при попытке зайти в профиль не авторизированному
    # пользователю), но авторизованный пользователь еще может зайти на чужой профиль с доступом к корзине.
    # Вместо использования LoginRequiredMixin в UserProfileView
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    # path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    # path('profile/', profile, name='profile'),

    path('logout/', LogoutView.as_view(), name='logout'),
    # path('logout/', logout, name='logout'),

    # Параметры email и uuid нужны для однозначной идентификации пользователя при создании ссылки в для его почты
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
