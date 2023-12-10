from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import BlogUser


class BlogUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super_user = User.objects.create_user(username="Admin", email="Admin@fack.com", password="test123456", is_superuser=True)
        user = User.objects.create_user(username="Test", email="Test@fack.com", password="test123456")
        blog_user = BlogUser.objects.create(
            user=user,
            username=user.username,
            email=user.email,
        )

    def test_bloguser_exists(self):
        user = User.objects.get(username="Test")
        blog_user = BlogUser.objects.get(username="Test")
        self.assertIs(user.pk, blog_user.user.pk)

    def test_register_bloguser(self):
        res = self.client.get(reverse("register"))
        self.assertEqual(res.status_code, 200)

        res = self.client.post(reverse("register"), data={"username": "Test2", "email": "Test2@fack.com", "password1": "test123456", "password2": "test123456"})

        blog_user = BlogUser.objects.get(username="Test2")
        user = User.objects.get(username="Test2")
        self.assertEqual(res.status_code, 302)

        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Test2")

    def test_login_bloguser(self):
        res = self.client.post(reverse("login"), {"username": "Test", "password": "test123456"})
        self.assertRedirects(res, reverse("home"))

        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Test")

    def test_superuser_not_register(self):
        """
        测试博客用户未注册, 但注册了超管用户
        """
        res = self.client.post(reverse("login"), {"username": "Admin", "password": "test123456"}, follow=True)
        self.assertEqual(res.status_code, 200)

        user = User.objects.get(username="Admin")
        blog_user = BlogUser.objects.get(user=user)

        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Admin")

    def test_logout(self):
        res = self.client.post(reverse("login"), {"username": "Test", "password": "test123456"})
        self.assertEqual(res.status_code, 302)

        res = self.client.get(reverse("logout"), follow=True)
        self.assertRedirects(res, reverse("login"))
        self.assertNotContains(res, "Test")
