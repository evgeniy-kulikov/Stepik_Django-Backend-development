from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now


# Эту модель нужно создавать самой первой (первая миграция проекта)
# Наследуемся уже от существующей модели пользователя
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    # Далее можно добавить необходимые поля (дата рождения, телефон, должность и т.д)

    # Проверка подтверждения адреса электронной почты
    is_verified_email = models.BooleanField(default=False)


# Создание ссылки для подтверждения адреса электронной почты
class EmailVerification(models.Model):
    # Уникальный идентификатор пользователя
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()  # ограничение существования ссылки

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        """Письмо на почту зарегистрированному новому пользователю"""
        # Ссылка пользователю для подтверждения указанной почты
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        # полный адрес ссылки (с корневым адресом 'http://127.0.0.1:8000')
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        # Заголовок письма пользователю
        subject = f'Подверждение учетной записи для {self.user.username}'
        # Сообщение пользователю. Используем format() а не f строку, т.к. не уместится на одной строчке кода
        message = 'Для подверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )

        # Метод отправки письма
        send_mail(
            subject=subject,
            message=message,
            from_email="from@example.com",
            recipient_list=[self.user.email],
            fail_silently=False,
        )

        # send_mail(
        #     "Subject here",
        #     "проверка send_verification_email",
        #     "from@example.com",
        #     [self.user.email],
        # )

    def is_expired(self):
        """Проверка срока действия ссылки"""
        return True if now() >= self.expiration else False

