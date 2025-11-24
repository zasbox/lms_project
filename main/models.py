from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    preview = models.ImageField(upload_to='preview_courses/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)
    price = models.PositiveIntegerField(default=85000, verbose_name="Цена")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время последнего обновления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='preview_lessons/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='URL видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата оплаты', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    METHOD_CHOICES = (('CASH', 'Наличные'), ('ACCOUNT', 'Перевод на счет'))
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, verbose_name='Способ оплаты')
    payment_session = models.CharField(max_length=100, verbose_name="Сессия оплаты", **NULLABLE)
    is_paid = models.BooleanField(default=False, verbose_name="Статус оплаты")

    def __str__(self):
        return f'{self.amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    is_signed = models.BooleanField(default=True, verbose_name="Подписан")

    def __str__(self):
        return f'{self.user} {self.course} {self.is_signed}'

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ('user', 'course')
