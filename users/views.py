from rest_framework.generics import RetrieveUpdateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
