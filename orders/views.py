from django.shortcuts import render
# from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

from common.views import TitleMixin


# Create your views here.


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    # form_class = OrderForm
    # success_url = reverse_lazy('orders:order_create')
    # title = 'Store - Оформление заказа'

