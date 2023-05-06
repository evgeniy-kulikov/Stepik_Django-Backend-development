from http import HTTPStatus

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
# from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

from common.views import TitleMixin
from orders.forms import OrderForm

import stripe
from django.conf import settings
from products.models import Basket

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/cancled.html'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')  # Куда перенаправляется пользователь после отправки формы
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        # baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1N4p0SCkfBAKr9UHoBg2E03q',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    # Для добавления в форму поля со значением инициатора заказа ( initiator )
    def form_valid(self, form):
        form.instance.initiator = self.request.user  # "instance" - значение
        return super(OrderCreateView, self).form_valid(form)
