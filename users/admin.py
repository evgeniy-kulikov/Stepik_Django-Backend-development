from django.contrib import admin
from users.models import User

from products.admin import BasketAdmin


# Register your models here.
# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    exclude = ('password', 'last_login')  # исключить поле
    filter_horizontal = ('groups', 'user_permissions')  # отображение полей "многие ко многим"
    ordering = ('username',)
    inlines = (BasketAdmin,)  # У пользователя будут отображены его корзины. !!! Из другой модели (через внешний ключ)
