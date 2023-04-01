from django.contrib.auth.forms import AuthenticationForm
from users.models import User


# Наследуемся от встроенного класса AuthenticationForm
class UserLoginForm(AuthenticationForm):
    class Meta:  # class Meta отвечает за выбор модели и отображаемых полей
        model = User
        fields = ('username', 'password')
