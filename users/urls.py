from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserRetrieveAPIView, PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('<int:pk>/update', UserUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='detail'),
    path('payments/', PaymentListAPIView.as_view(), name='list'),
]
