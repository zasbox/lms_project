from rest_framework.serializers import ModelSerializer

from main.models import Payment
from users.models import User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'date', 'amount', 'method', 'course', 'lesson']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {key: value for key, value in representation.items() if value is not None}


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name', 'middle_name', 'email', 'phone_number', 'location', 'avatar', 'payments']
