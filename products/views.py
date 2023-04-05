# from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect

from products.models import Product, ProductCategory, Basket
from users.models import User


def index(request):
    context = {
        'title': 'Store',
        'is_promotion': True,
    }
    return render(request, 'products/index.html', context=context)


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context=context)


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


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
