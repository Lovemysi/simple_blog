import pytest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import BlogUser

# TODO 视图测试用pytest 单元测试用 Django
# TODO 先参数化测试用户
# TODO 1.为pytest创建统一的测试数据库, 测试后删除
# TODO 2.创建测试用户对象


# TODO 检测重定向使用 self.assertRedirects()
