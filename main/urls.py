from django.urls import path
from rest_framework.routers import DefaultRouter

from main.apps import MainConfig
from main.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView

app_name = MainConfig.name

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='list'),
    path('lessons/<int:pk>', LessonRetrieveAPIView.as_view(), name='detail'),
    path('lessons/create', LessonCreateAPIView.as_view(), name='create'),
    path('lessons/<int:pk>/update', LessonUpdateAPIView.as_view(), name='update'),
    path('lessons/<int:pk>/delete', LessonDestroyAPIView.as_view(), name='delete'),

    path('courses/subscribe', SubscriptionCreateAPIView.as_view(), name='subscribe'),
]

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
urlpatterns += router.urls
