from django.db import models

from users.models import BlogUser


class Post(models.Model):
    """
    OneToMany: user -> post | post -> comment
    """

    id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE)
    cover = models.ImageField(
        upload_to="covers/", default="covers/cover-default.png", null=True, blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """
    OneToMany: user -> comment | post -> comment
    """

    id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.body)
