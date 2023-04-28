"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# для возможности отображения медиафайлов
from django.conf.urls.static import static
from django.conf import settings
# from store import settings # Так тоже работает, но строчка выше будет лучше, т.к. загрузятся все настройки проекта

from products.views import IndexView  # index, products

urlpatterns = [
    path('admin/', admin.site.urls),

    # Контекст можно передать через "extra_context="
    # path('', IndexView.as_view(extra_context={'title': 'Store'}), name='index'),

    # path('', index, name='index'),  # FBV
    path('', IndexView.as_view(), name='index'),  # CBV

    path("products/", include("products.urls", namespace='products')),
    path("users/", include("users.urls", namespace='users')),
    # http://127.0.0.1:8000/accounts/github/login/
    path('accounts/', include('allauth.urls')),
]

# для возможности отображения медиафайлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
