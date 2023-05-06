from django.urls import path

from orders.views import OrderCreateView, CanceledTemplateView, SuccessTemplateView

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    # path('', OrderListView.as_view(), name='orders_list'),
    # path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),  # http://127.0.0.1:8000/orders/order-success/
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]
