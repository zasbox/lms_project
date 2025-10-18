from django.contrib import admin
from django.contrib.admin import ModelAdmin

from main.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ['name', 'owner', 'pk']


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ['name', 'pk', 'owner']
