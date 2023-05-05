from products.models import Basket


# Отображаем переменную baskets по пользователю, который авторизован (см.  def basket_add(request, product_id) )
# Эта переменная становится глобальной для всего проекта. Доступна везде.
def baskets(request):
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
