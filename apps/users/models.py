import uuid
from django.db import models
from django.contrib.auth.models import User


class BlogUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(
        upload_to="profiles/", default="profiles/user-default.png", null=True, blank=True,)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username
