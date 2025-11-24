
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from main.models import Course, Lesson, Subscription, Payment
from main.paginators import CoursePaginator, LessonPaginator
from main.permissions import IsModerator, IsOwner
from main.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from main.services import make_payment, get_status_payment
from main.tasks import send_email_about_updating_course


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

    def perform_update(self, serializer):
        course = serializer.save()
        send_email_about_updating_course(course)


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

    def perform_update(self, serializer):
        lesson = serializer.save()
        if timezone.now() - timedelta(hours=4) > lesson.course.updated_at:
            send_email_about_updating_course(lesson.course)


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


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


class PaymentCreateAPIView(APIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        user = request.user
        course = Course.objects.get(pk=course_id)
        session, url = make_payment(course.name, course.price).values()
        Payment.objects.create(user=user, course=course, amount=course.price, method='ACCOUNT', payment_session=session)
        return Response({'status': 'OK', 'url': url}, status=status.HTTP_201_CREATED)


class PaymentRealizedAPIView(APIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        payment = Payment.objects.get(payment_session=session_id)
        payment.is_paid = True
        payment.save()
        return Response({'status': 'paid'}, status=status.HTTP_200_OK)


class PaymentStatusAPIView(APIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        data = get_status_payment(session_id)
        return Response({'status': data}, status=status.HTTP_200_OK)
