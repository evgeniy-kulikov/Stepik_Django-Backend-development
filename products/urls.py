from django.urls import path
from products.views import basket_add, basket_remove, ProductsListView

from django.views.decorators.cache import cache_page

app_name = 'products'

urlpatterns = [
    # path('', cache_page(30)(ProductsListView.as_view()), name='index'),  # cache_page на 30 сек (вся страница)
    path('', ProductsListView.as_view(), name='index'),  # все продукты
    # path('', products, name='index'),  # все продукты  через FBV

    path('category/<int:category_val>', ProductsListView.as_view(), name='category'),  # сортировка по категориям
    # path('category/<int:category_val>', products, name='category'),  # сортировка по категориям  через FBV

    # Для окончательной версии templates/products/paginator.html этот путь можно убрать
    # path('page/<int:page_val>', ProductsListView.as_view(), name='paginator'),  # для работы пагинации
    # path('page/<int:page_number>', products, name='paginator'),  # для работы пагинации через FBV

    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
