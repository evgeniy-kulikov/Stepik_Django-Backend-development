from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.mail import send_mail


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
        send_mail(
            "Subject here",
            "проверка send_verification_email",
            "from@example.com",
            [self.user.email],
            fail_silently=False,
        )

