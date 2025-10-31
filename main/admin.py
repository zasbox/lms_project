from django.contrib import admin
from django.contrib.admin import ModelAdmin

from main.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ['name', 'owner', 'pk']


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ['name', 'pk', 'owner']


@admin.register(Subscription)
class LessonAdmin(ModelAdmin):
    list_display = ['pk', 'user', 'course', 'is_signed']
