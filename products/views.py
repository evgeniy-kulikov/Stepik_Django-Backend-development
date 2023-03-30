from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'title': 'Store',
        'is_promotion': True,
    }
    return render(request, 'products/index.html', context=context)


dic_product = [
    {
        "image": "/static/vendor/img/products/Adidas-hoodie.png",
        "name": "Худи черного цвета с монограммами adidas Originals",
        "price": 6090,
        "descroption": "Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.",
    },
    {
        "image": "/static/vendor/img/products/Blue-jacket-The-North-Face.png",
        "name": "Синяя куртка The North Face",
        "price": 23725,
        "descroption": "Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.",
    },
    {
        "image": "/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png",
        "name": "Коричневый спортивный oversized-топ ASOS DESIGN",
        "price": 3390,
        "descroption": "Материал с плюшевой текстурой. Удобный и мягкий.",
    },
    {
        "image": "/static/vendor/img/products/Black-Nike-Heritage-backpack.png",
        "name": "Черный рюкзак Nike Heritage",
        "price": 2340,
        "descroption": "Плотная ткань. Легкий материал.",
    },
    {
        "image": "/static/vendor/img/products/Black-Dr-Martens-shoes.png",
        "name": "Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex",
        "price": 13590,
        "descroption": "Гладкий кожаный верх. Натуральный материал.",
    },
    {
        "image": "/static/vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png",
        "name": "Темно-синие широкие строгие брюки ASOS DESIGN",
        "price": 2890,
        "descroption": "Легкая эластичная ткань сирсакер Фактурная ткань.",
    },
]


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': dic_product,
    }
    return render(request, 'products/products.html', context=context)
