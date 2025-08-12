from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from materials.models import Course, Lesson, Subscription


class LessonCRUDTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create(
            email='test@test.com',
            password='testpass'
        )
        self.moderator = User.objects.create(
            email='moderator@test.com',
            password='modpass'
        )
        self.moderator.groups.create(name='moderators')

        # Создаем курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            owner=self.user
        )

        # URL для уроков
        self.list_url = reverse('materials:lessons_list')
        self.create_url = reverse('materials:lessons_create')
        self.detail_url = reverse('materials:lessons_retrieve', kwargs={'pk': self.lesson.pk})
        self.update_url = reverse('materials:lessons_update', kwargs={'pk': self.lesson.pk})
        self.delete_url = reverse('materials:lessons_delete', kwargs={'pk': self.lesson.pk})

    def test_lesson_list(self):
        """Тест получения списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_lesson_create_by_user(self):
        """Тест создания урока обычным пользователем"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.pk
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_by_moderator(self):
        """Тест запрета создания урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.pk
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_by_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Title')

    def test_lesson_update_by_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        data = {'title': 'Updated by Moderator'}
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated by Moderator')

    def test_lesson_delete_by_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_delete_by_moderator(self):
        """Тест запрета удаления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.user1 = User.objects.create(
            email='user1@test.com',
            password='testpass1'
        )
        self.user2 = User.objects.create(
            email='user2@test.com',
            password='testpass2'
        )

        # Создаем курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user1
        )

        # URL для подписок
        self.subscription_url = reverse('materials:subscriptions')

    def test_subscription_flow(self):
        """Тест полного цикла подписки/отписки"""
        self.client.force_authenticate(user=self.user1)

        # Первый запрос - подписаться
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_subscribed'], True)
        self.assertEqual(Subscription.objects.count(), 1)

        # Второй запрос - отписаться
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_subscribed'], False)
        self.assertEqual(Subscription.objects.count(), 0)

    def test_subscription_by_another_user(self):
        """Тест подписки другим пользователем"""
        self.client.force_authenticate(user=self.user2)

        # Первый пользователь подписывается
        Subscription.objects.create(user=self.user1, course=self.course)

        # Второй пользователь подписывается
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_subscribed'], True)
        self.assertEqual(Subscription.objects.count(), 2)

    def test_subscription_unauthorized(self):
        """Тест подписки неавторизованным пользователем"""
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseSubscriptionInfoTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='user@test.com',
            password='testpass'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.course_url = reverse('materials:courses-detail', kwargs={'pk': self.course.pk})

    def test_is_subscribed_field(self):
        """Тест поля is_subscribed в курсе"""
        self.client.force_authenticate(user=self.user)

        # Проверка без подписки
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_subscribed'], False)

        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        # Проверка с подпиской
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_subscribed'], True)
