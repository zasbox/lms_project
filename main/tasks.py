from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from main.models import Subscription
from users.models import User


@shared_task
def send_email_about_updating_course(course):

    users = Subscription.objects.filter(course=course, is_signed=True).values('user__email')
    for user in users:
        send_mail(
            subject='Обновление курса',
            message=f'Курс {course} был обновлен {course.updated_at.strftime("%d.%m.%Y %H:%M")}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user['user__email']]
        )


@shared_task
def check_users():
    users = User.objects.filter(is_active=True)
    for user in users:
        if user.last_login is not None and timezone.now() - timedelta(days=30) > user.last_login:
            user.is_active = False
            user.save()






