from products.models import Basket


# Отображаем переменную baskets по пользователю, который авторизован (см.  def basket_add(request, product_id) )
def baskets(request):
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
