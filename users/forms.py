from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from users.models import User, EmailVerification

# Перенесено в users/tasks.py
# # для атрибута 'record' функции 'save()' из 'UserRegistrationForm'
# import uuid
# from datetime import timedelta
# from django.utils.timezone import now

from users.tasks import send_email_verification


# Наследуемся от встроенного класса AuthenticationForm
class UserLoginForm(AuthenticationForm):
    # Переопределяем поля формы. Кастомизация полей формы.
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


class UserRegistrationForm(UserCreationForm):
    # Переопределяем поля формы. Кастомизация полей формы.
    first_name = forms.CharField(widget=forms.TextInput({
        'class': 'form-control py-4',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput({
        'class': 'form-control py-4',
        'placeholder': 'Введите фамилию'
    }))
    username = forms.CharField(widget=forms.TextInput({
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя'
    }))
    email = forms.CharField(widget=forms.EmailInput({
        'class': 'form-control py-4',
        'placeholder': 'Введите адрес эл. почты'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control py-4',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    # Расширяем метод save() где будет реализованна логика подтверждения эл. почты
    # def save(self, commit=True):
    #     user = super(UserRegistrationForm, self).save(commit=True)
    #     expiration = now() + timedelta(hours=48)  # длительность ожидания 48 часов
    #     record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    #     record.send_verification_email()
    #     return user

    # Расширяем метод save() где будет реализованна логика подтверждения эл. почты с использованием Celery
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        # send_email_verification()  # Так сработает, но параллельно выполняться не будет
        send_email_verification.delay(user.id)  # Параллельное выполнение задачи
        return user


class UserProfileForm(UserChangeForm):
    # Переопределяем поля формы. Кастомизация полей формы.
    first_name = forms.CharField(widget=forms.TextInput({'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput({'class': 'form-control py-4'}))
    # required=False - поле необязательно к заполнению
    image = forms.ImageField(widget=forms.FileInput({'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput({'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput({'class': 'form-control py-4', 'readonly': True}))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')
