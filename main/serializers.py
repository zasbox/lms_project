from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from main.models import Course, Lesson, Subscription
from main.validators import VideoURLValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoURLValidator('video_url')]


class LessonForCourseSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'description', 'preview', 'video_url']
        validators = [VideoURLValidator('video_url')]


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonForCourseSerializer(source='lesson_set', many=True, read_only=True)
    is_signed = SerializerMethodField()

    def get_lessons_count(self, instance):
        return Lesson.objects.filter(course=instance).count()

    def get_is_signed(self, instance):
        return bool(Subscription.objects.filter(course=instance, user=self.context.get('user'))
                    .values('is_signed').first())

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
