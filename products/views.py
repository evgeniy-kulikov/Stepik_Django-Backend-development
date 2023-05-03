# from django.http import HttpResponseRedirect
from users.models import User
from django.core.paginator import Paginator

from common.views import TitleMixin
from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Basket

# Декоратор доступа
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

# Использование кэша
# from django.core.cache import cache


# Для передачи контекста, отказались от переопределения метода "get_context_data"
# Вместо него задействовали собственный миксин TitleMixin
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


# class IndexView(TemplateView):
#     template_name = 'products/index.html'
#
#     # Для передачи контекста используем метод "get_context_data"
#     def get_context_data(self, **kwargs):
#         context = super(IndexView, self).get_context_data()  # для сохранения функционала метода родительского класса
#         context['title'] = 'Store'  # переопределение (расширение) метода родительского класса
#         return context

# Решение через FBV
# def index(request):
#     context = {
#         'title': 'Store',
#         'is_promotion': True,
#     }
#     return render(request, 'products/index.html', context=context)


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    # Переопределяем "context" на свое имя. Можно в шаблоне все заменить на "object_list" - имя контекста по умолчанию
    # context_object_name = 'products'

# Формируем queryset для category
    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category = self.kwargs.get('category_val')  # 'category' это <int:category_val>
        return queryset.filter(category_id=category) if category else queryset

    # Формируем необходимый контекст
    def get_context_data(self, *, object_list=None, **kwargs):

        # Без использования кеширования категорий в шаблоне
        context = super(ProductsListView, self).get_context_data(**kwargs)

        # для работы кеширования категорий в шаблоне
        # context = super().get_context_data(**kwargs)

        # context['title'] = 'Store - Каталог'  # Получаем через миксин "TitleMixin"

        # # Организуем cache
        # categories = cache.get('categories')
        # if not categories:  # Если кеш пуст, то создаем его
        #     context['categories'] = ProductCategory.objects.all()
        #     cache.set('categories', context['categories'], 30)
        # else:  # Иначе получаем контекст их кеша
        #     context['categories'] = categories

        context['categories'] = ProductCategory.objects.all()

        # Контекст для работы кеширования категорий в шаблоне "products.html"
        context['category_cache'] = self.kwargs.get('category')

        return context


# Решение через FBV
# Если категория не указана, тогда 'category_id=None'  и отработает роут "path('', products, name='index')"
# def products(request, category_val=None, page_number=1):
#     products = Product.objects.filter(category_id=category_val) if category_val else Product.objects.all()
#     per_page = 3  # кол-во страниц для пагинации
#     paginator = Paginator(products, per_page)  # Весь список, разделенный на страницы
#     products_paginator = paginator.page(page_number)  # Страница из этого списка
#     context = {
#         'title': 'Store - Каталог',
#         'products': products_paginator,
#         'categories': ProductCategory.objects.all(),
#     }
#     return render(request, 'products/products.html', context=context)


# Декоратор доступа
# Контролер не будет отрабатывать, пока не будет произведена авторизация
@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)  # Продукт, который будет добавлен в корзину.
    # baskets = Basket.objects.filter(user=request.user, product=product)

    # Получаем все корзины, где есть данный продукт, и берем из них корзину текущего авторизованного пользователя.
    # Возьмутся все корзины текущего авторизованного пользователя, где есть данный продукт.
    # Возвращается только одно значение
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():  # Если корзина с таким товаром не существует
        Basket.objects.create(user=request.user, product=product, quantity=1)  # То создаем ее
    else:
        basket = baskets.first()  # Если корзина с таким товаром существует, то получаем ее (возвращается только одно значение)
        basket.quantity += 1  # Увеличиваем свойство 'quantity' на единицу
        basket.save()  # Сохраняем
    # Возврат на текущую страницу (т.е. остаемся здесь же )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
