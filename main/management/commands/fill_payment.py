import random
from datetime import datetime, date

from django.core.management import BaseCommand

from main.models import Course, Payment, Lesson
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        Payment.objects.all().delete()
        users = list(User.objects.all().values_list('pk', flat=True))
        courses = list(Course.objects.all().values_list('pk', flat=True))
        lessons = list(Lesson.objects.all().values_list('pk', flat=True))
        for user in users:
            for i in range(random.randint(1, 5)):
                payment = Payment()
                payment.user_id = user
                payment.date = date(2025, random.randint(1, 12), random.randint(1, 28))
                target_pay = random.choice([1, 2])
                if target_pay == 1:
                    payment.course_id = random.choice(courses)
                else:
                    payment.lesson_id = random.choice(lessons)
                payment.amount = random.randint(1000, 3000)
                payment.method = random.choice(['CASH', 'ACCOUNT'])
                payment.save()
