from django.contrib.auth.forms import AuthenticationForm
from django import forms
from users.models import User


# Наследуемся от встроенного класса AuthenticationForm
class UserLoginForm(AuthenticationForm):
    # Переопределяем поля формы. Кастомизация формы.
    username = forms.CharField(widget=forms.TextInput({
    'class': 'form-control py-4',
    'placeholder': 'Введите имя пользователя',
    }))
    password = forms.CharField(widget=forms.PasswordInput({
    'class': 'form-control py-4',
    'placeholder': 'Введите пароль',
    }))

    class Meta:  # class Meta отвечает за выбор модели и отображаемых полей
        model = User
        fields = ('username', 'password')
