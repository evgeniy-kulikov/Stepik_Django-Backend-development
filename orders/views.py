from http import HTTPStatus

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
# from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

from common.views import TitleMixin
from orders.forms import OrderForm

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order
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

    #  Переопределяем метод создания объекта
    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)  # Берем родительский класс ...

        # ... и добавляем в него формирование страницы для оплаты товара
        # Данные номера карты для оплаты (остальное произвольно):  https://stripe.com/docs/checkout/quickstart#testing
        # https://stripe.com/docs/checkout/quickstart#create    (start)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # 'price': '{{PRICE_ID}}',
                    # PRICE_ID берем тут  https://dashboard.stripe.com/test/products/prod_NqW20PDhWuz6OE
                    'price': 'price_1N4p0SCkfBAKr9UHoBg2E03q',
                    'quantity': 1,
                },
            ],
            mode='payment',
            # success_url=YOUR_DOMAIN + '/success.html',
            # cancel_url=YOUR_DOMAIN + '/cancel.html',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        # https://stripe.com/docs/checkout/quickstart#create    (finish)

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    # Для добавления в форму поля со значением инициатора заказа ( initiator )
    def form_valid(self, form):
        form.instance.initiator = self.request.user  # "instance" - значение
        return super(OrderCreateView, self).form_valid(form)


#  https://stripe.com/docs/payments/checkout/fulfill-orders#create-event-handler
# @csrf_exempt
# def stripe_webhook_view(request):
#   payload = request.body  # ответ от stripe
#   # the structure.
#   print(payload)
#   return HttpResponse(status=200)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    print('fulfill_order')
    # order = Order.objects.get(id=order_id)
    # order.update_after_payment()

