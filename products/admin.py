from django.contrib import admin
from products.models import ProductCategory, Product, Basket

# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', 'category', ('price', 'quantity'), 'image')
    readonly_fields = ('quantity',)
    search_fields = ('name', 'price')
    ordering = ('category',)


# Так отобразятся все корзины всех пользователей
# @admin.register(Basket)
# class BasketAdmin(admin.ModelAdmin):
#     pass


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp', )
    extra = 0  # Убираем ненужные дополнительные поля (значение по умолчанию = 3)
