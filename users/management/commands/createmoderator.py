from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        group = Group.objects.get_or_create(name='moderator')[0]

        user = User.objects.get_or_create(
            last_name="Федоров",
            first_name="Федор",
            middle_name="Иванович",
            email="fedorov@mail.ru",
            phone_number="+79605837382",
            location="Москва",
            password="12345"
        )[0]
        group.user_set.add(user)
        print(f'Создан модератор {user}\nЛогин: {user.email}\nПароль: {user.password}')

