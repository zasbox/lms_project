from django.contrib.auth.models import Group
from rest_framework import status

from main.models import Lesson, Course
from users.models import User
from rest_framework.test import APITestCase


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(last_name="Федоров",
                                             first_name="Федор",
                                             middle_name="Иванович",
                                             email="fedorov@mail.ru",
                                             phone_number="+79605837382",
                                             location="Москва",
                                             password="12345")

        self.client.force_authenticate(user=self.user)

        self.lesson1 = Lesson.objects.create(
            name='Экономика',
            description='Экономическая теория',
            video_url='http://youtube.com/eco'
        )
        self.lesson2 = Lesson.objects.create(
            name='Основы Python',
            description='Основы языка python',
            video_url='http://youtube.com/py'
        )
        self.course = Course.objects.create(
            name="Программирование на языке python",
            description="Экспресс курс языка python"
        )

    def tearDown(self) -> None:
        pass

    def test_subscribe(self):
        """Тестирование подписки на курс"""
        data = {'course': self.course.pk}
        response = self.client.post('/courses/subscribe', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_signed'], True)

        response = self.client.post('/courses/subscribe', data=data, format='json')
        self.assertEqual(response.data['is_signed'], False)

    def test_create_course(self):
        """Тестирование создания курса"""
        course = {
            'name': "Программирование на языке Java",
            'description': "Экспресс курс языка Java",
        }
        response = self.client.post('/courses/', data=course, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name='Экономика').exists())
        self.assertEqual(response.json(),
                         {'id': response.data['id'],
                          'lessons_count': 0,
                          'lessons': [],
                          'is_signed': False,
                          'name': 'Программирование на языке Java', 'preview': None,
                          'description': 'Экспресс курс языка Java', 'owner': None}
                         )

    def test_update_course_by_not_moderator(self):
        """Тестирование обновления курса не модератором"""

        new_course = {
            'name': "Программирование на языке Java",
            'description': "Экспресс курс языка Java"
        }

        response = self.client.put(f'/courses/{self.course.pk}/', data=new_course, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_by_moderator(self):
        """Тестирование обновления курса модератором"""
        group = Group.objects.create(name='moderator')
        group.user_set.add(self.user)

        new_course = {
            'name': "Программирование на языке Java",
            'description': "Экспресс курс языка Java"
        }

        response = self.client.put(f'/courses/{self.course.pk}/', data=new_course, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_course(self):
        """Тестирование получения списка курсов"""

        response = self.client.get(f'/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_course_by_moderator(self):
        """Тестирование получения одного курса модератором"""
        group = Group.objects.create(name='moderator')
        group.user_set.add(self.user)

        response = self.client.get(f'/courses/{self.course.pk}/',  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        """Тестирование удаления курса"""

        response = self.client.delete(f'/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
