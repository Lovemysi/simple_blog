from django.test import TestCase
from django.urls import reverse

from users.models import User, BlogUser


class PostsViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user("Test", "Test@test.com", "test123456")
        user.save()
        BlogUser.objects.create(user=user, username=user.username, email=user.email)

    def setUp(self) -> None:
        self.client.post(reverse("login"), {"username": "Test", "password": "test123456"})

        res = self.client.post(reverse("add_post"), {"title": "Global Title", "body": "Global Content"})
        self.assertEqual(res.status_code, 302)

    def test_post_index(self):
        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Test")

    def test_create_post(self):
        res = self.client.get(reverse("add_post"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Test")

        res = self.client.post(reverse("add_post"), {"title": "Have A Title", "body": "Have A Content"})
        self.assertEqual(res.status_code, 302)

        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Have A Title")
        self.assertContains(res, "Have A Content")

    def test_update_post(self):
        res = self.client.get(reverse("update_post", kwargs={"post_id": "1"}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Global Title")
        self.assertContains(res, "Global Content")

        res = self.client.post(reverse("update_post", kwargs={"post_id": "1"}), {"title": "Update Title", "body": "Update Content"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Update Title")
        self.assertContains(res, "Update Content")

    def test_delete_post(self):
        res = self.client.get(reverse("delete_post", kwargs={"post_id": "1"}), follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Global Title")

    def test_logout_access(self):
        res = self.client.get(reverse("logout"))
        self.assertEqual(res.status_code, 302)

        res.client.get(reverse("add_post"))
        self.assertEqual(res.status_code, 302)

        res.client.get(reverse("update_post", kwargs={"post_id": "1"}))
        self.assertEqual(res.status_code, 302)

        res = self.client.post(reverse("update_post", kwargs={"post_id": "1"}), {"title": "Update Title", "body": "Update Content"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Update Title")
        self.assertNotContains(res, "Update Content")

        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)


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
