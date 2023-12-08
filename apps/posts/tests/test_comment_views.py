from django.test import TestCase
from django.urls import reverse

from users.models import User, BlogUser


class CommentViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user("Test", "Test@test.com", "test123456")
        user.save()
        BlogUser.objects.create(user=user, username=user.username, email=user.email)

    def setUp(self) -> None:
        self.client.post(reverse("login"), {"username": "Test", "password": "test123456"})

        res = self.client.post(reverse("add_post"), {"title": "Global Title", "body": "Global Content"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Global Title")

    def test_add_comment(self):
        res = self.client.post(reverse("add_comment", kwargs={"post_id": "1"}), {"body": "Add a Comment"}, follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Add a Comment")

    def test_logout_access(self):
        res = self.client.get(reverse("logout"), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Test")

        res = self.client.post(reverse("add_comment", kwargs={"post_id": "1"}), {"body": "Logout Add"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, '"Logout Add"')
