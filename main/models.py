from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    preview = models.ImageField(upload_to='preview_courses/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='preview_lessons/', verbose_name='Превью')
    video_url = models.URLField(verbose_name='URL видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс')

    def __str__(self):
        return f'{self.name} ({self.course.name})'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
