# from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect

from products.models import Product, ProductCategory, Basket
from users.models import User
from django.core.paginator import Paginator

# Декоратор доступа
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'products/index.html'

    # Для передачи контекста используем метод "get_context_data"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Store'
        return context




# def index(request):
#     context = {
#         'title': 'Store',
#         'is_promotion': True,
#     }
#     return render(request, 'products/index.html', context=context)


# Если категория не указана, тогда 'category_id=None'  и отработает роут "path('', products, name='index')"
def products(request, category_id=None, page_number=1):

    # if category_id:
    # Если категория указана, то фильтруем продукты по этой категории.
    # Вариант 1________________________category_id это внешний ключ 'category' таблицы 'Product'
    #     products = Product.objects.filter(category_id=category_id)
    # else:
    #     #  Иначе отображаем все продукты.
    #     products = Product.objects.all()

    # Вариант 2 то же что и в варианте 1, но через тернарный оператор
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    per_page = 3  # кол-во страниц для пагинации
    paginator = Paginator(products, per_page)  # Весь список, разделенный на страницы
    products_paginator = paginator.page(page_number)  # Страница из этого списка

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Store - Каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),

        # 'page_obj': page_obj,
    }

    return render(request, 'products/products.html', context=context)


# Декоратор доступа
# Контролер не будет отрабатывать, пока не будет произведена авторизация
@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)  # Продукт, который будет добавлен в корзину.

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
