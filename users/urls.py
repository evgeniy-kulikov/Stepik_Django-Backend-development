from django.urls import path
from users.views import login, UserRegistrationView, logout, UserProfileView  # registration, profile

from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),

    path('registration/', UserRegistrationView.as_view(), name='registration'),
    # path('registration/', registration, name='registration'),

    # Так по словам автора должен был отработать декоратор доступа, но реально не получилось
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    # path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    # path('profile/', profile, name='profile'),

    path('logout/', logout, name='logout'),
]
