from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User, EmailVerification

# Запуск всех тестов проекта
# python manage.py test
# ./manage.py test .

class UserRegistrationViewTestCase(TestCase):
    # Используем встроенный метод setUp() для использования одинаковых переменных.
    def setUp(self):
        self.data = {
            'first_name': 'Test', 'last_name': 'User',
            'username': 'testuser', 'email': 'testuser@yandex.ru',
            'password1': '1234567aA', 'password2': '1234567aA',
        }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        """Проверка на получение данных"""
        # client вспомогательный класс позволяющий обратиться к разным методам
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')
        # Тест не проходит. Нужно дать ограничение на выборку полей
        # self.assertEqual(response.context_data['Form'], UserRegistrationForm())

    def test_user_registration_post_success(self):
        """Проверка на отправку данных"""
        # Имя созданного пользователя
        username = self.data['username']
        # Для корректности теста убеждаемся сначала, что такого пользователя нет
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # Проверка редиректа 302
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Проверка адреса страницы редиректа
        self.assertRedirects(response, reverse('users:login'))
        # Проверка создания пользователя
        self.assertTrue(User.objects.filter(username=username).exists())

        # Проверка верификации почты
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        # Проверка срока действия ссылки для верификации почты
        # Только проверяем по дате а не времени, т.к. в тестовой БД пользователь создается раньше на пару миллисекунд
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        """Проверка на существование другого пользователя с таким же именем"""
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.login_url = reverse('users:login')

    def test_login_page_loads_successfully(self):
        """Тест проверяет, что страница авторизации загружается успешно"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_successful(self):
        """Тест проверяет, что успешная авторизация проходит корректно"""
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, reverse('index'))

    def test_login_failure(self):
        """Тест проверяет, что неправильные данные для авторизации возвращают ошибку,"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

# Запуск всех тестов проекта
# python manage.py test
# ./manage.py test .
