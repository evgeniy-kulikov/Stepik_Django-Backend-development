from django.contrib import admin
from users.models import User, EmailVerification

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


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
