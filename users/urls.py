from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserRetrieveAPIView, PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('<int:pk>/update', UserUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='detail'),
    path('payments/', PaymentListAPIView.as_view(), name='list'),
]
