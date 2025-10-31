from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from main.models import Course, Lesson, Subscription
from main.paginators import CoursePaginator, LessonPaginator
from main.permissions import IsModerator, IsOwner
from main.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes_by_action = {'create': [IsAuthenticated, IsOwner],
                                    'list': [IsAuthenticated],
                                    'retrieve': [IsAuthenticated, IsOwner | IsModerator],
                                    'update': [IsAuthenticated, IsOwner | IsModerator],
                                    'partial_update': [IsAuthenticated, IsOwner | IsModerator],
                                    'delete': [IsAuthenticated, IsOwner]}
    pagination_class = CoursePaginator

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [])]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        instance = (Subscription.objects.filter(user=request.user) &
                    Subscription.objects.filter(course_id=request.data['course'])).first()
        serializer = None
        if instance is None:
            serializer = self.get_serializer(data=request.data | {'user': request.user.pk})
        else:
            instance.is_signed = not instance.is_signed
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
