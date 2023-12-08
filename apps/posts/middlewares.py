from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User, AbstractBaseUser
from django.http.request import HttpRequest

from users.models import BlogUser


class CheckUserExists(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if request.user.is_authenticated:
            user: User = User.objects.get(pk=request.user.pk)
            try:
                BlogUser.objects.get(user=user)
            except BlogUser.DoesNotExist:
                blog_user = BlogUser(user=user, username=user.username, email=user.email)
                blog_user.save()
