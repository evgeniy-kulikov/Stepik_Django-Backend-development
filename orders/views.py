from django.shortcuts import render
# from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

from common.views import TitleMixin
from orders.forms import OrderForm


# Create your views here.


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')  # Куда перенаправляется пользователь после отправки формы
    title = 'Store - Оформление заказа'

    # Для добавления в форму поля со значением инициатора заказа ( initiator )
    def form_valid(self, form):
        form.instance.initiator = self.request.user  # "instance" - значение
        return super(OrderCreateView, self).form_valid(form)
