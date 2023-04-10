from django.urls import path
from products.views import products, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),  # все продукты
    path('category/<int:category_id>', products, name='category'),  # сортировка по категориям
    path('page/<int:page_number>', products, name='paginator'),  # пагинация
    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
