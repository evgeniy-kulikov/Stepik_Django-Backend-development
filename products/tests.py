from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

# from users.models import User
from products.models import Product, ProductCategory


# Запуск всех тестов проекта
# python manage.py test
# ./manage.py test .


class IndexViewTestCase(TestCase):
    def test_view(self):
        # Сначала указываем путь к тестируемой странице
        path = reverse('index')  # http://127.0.0.1:8000/
        # И формируем от нее ответ
        # client вспомогательный класс позволяющий обратиться к разным методам
        response = self.client.get(path)

        # Сначала обычно всегда проверяем статус кода
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Далее обычно получаем верность получаемого шаблона страницы
        self.assertTemplateUsed(response, 'products/index.html')
        # Проверка получаемого QuerySet
        self.assertEqual(response.context_data['title'], 'Store')

        # print(response)

        # # При тесте запускается своя база данных, отличная от реальной. Проверим это:
        # #  ...  Creating test database for alias 'default'...
        # print(f'Products: {Product.objects.all()}')  # Products: <QuerySet []>
        # print(f'User: {User.objects.all()}')  # User: <QuerySet []>


# Запуск теста через терминал
# ./manage.py test products.tests.IndexViewTestCase.test_view


class ProductsListViewTestCase(TestCase):
    # Заполняем тестовую БД
    fixtures = ['categories.json', 'goods.json']

    # Используем встроенный метод setUp() для использования одинаковых переменных. Например, для "products".
    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        # products = Product.objects.all()  # Вынесли в метод setUp()

        # Отобразим в терминале выборки товаров
        # print(response.context_data['object_list'])
        # print(products[:3])
        # # print(response.context_data['object_list'] == products[:3])  # False
        # print(list(response.context_data['object_list']) == list(products[:3]))  # True

        # self.assertEqual(response.status_code, HTTPStatus.OK)  # Вынесли в метод _common_tests()
        # self.assertTemplateUsed(response, 'products/products.html')  # Вынесли в метод _common_tests()
        # self.assertEqual(response.context_data['title'], 'Store - Каталог')  # Вынесли в метод _common_tests()
        self._common_tests(response)

        # self.assertEqual(response.context_data['object_list'], products[:3])
        # Отображение на странице 3-х карточек товара. Но сравниваем не <QuerySet> а list()
        # self.assertEqual(list(response.context_data['object_list']), list(products[:3]))
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_val': category.id})
        response = self.client.get(path)

        # products = Product.objects.all()  # Вынесли в метод setUp()

        # self.assertEqual(response.status_code, HTTPStatus.OK)  # Вынесли в метод _common_tests()
        # self.assertTemplateUsed(response, 'products/products.html')  # Вынесли в метод _common_tests()
        # self.assertEqual(response.context_data['title'], 'Store - Каталог')  # Вынесли в метод _common_tests()
        self._common_tests(response)

        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id)[:3])
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')

# Запуск всех тестов проекта
# python manage.py test
# ./manage.py test .
