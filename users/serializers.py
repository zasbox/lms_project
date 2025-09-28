from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'phone_number', 'location', 'avatar']
