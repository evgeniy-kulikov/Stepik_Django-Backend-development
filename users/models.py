from django.db import models
from django.contrib.auth.models import AbstractUser


# Эту модель нужно создавать самой первой (первая миграция проекта)
# Наследуемся уже от существующей модели пользователя
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    # Далее можно добавить необходимые поля (дата рождения, телефон, должность и т.д)
