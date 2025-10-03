from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from main.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonForCourseSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'description', 'preview', 'video_url']


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonForCourseSerializer(source='lesson_set', many=True)

    def get_lessons_count(self, instance):
        return Lesson.objects.filter(course=instance).count()

    class Meta:
        model = Course
        fields = '__all__'
