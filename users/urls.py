from django.urls import path

from users.api_views import UserRegAuthAPIView, UserLoginAPIView, UserProfileAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # app routes
    path('phone/login/', UserRegAuthAPIView.as_view(), name='login'),
    path('phone/confirm/', UserLoginAPIView.as_view(), name='auth-login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
