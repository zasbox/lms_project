from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, ListAPIView

from main.models import Payment
from users.models import User
from users.serializers import UserSerializer, PaymentSerializer


class UserUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['method']
    ordering_fields = ['date']
    filterset_fields = ['course', 'lesson']




