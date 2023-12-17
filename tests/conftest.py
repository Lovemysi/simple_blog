import pytest

from django.test.client import Client
from django.test.utils import setup_test_environment


# 测?
# TODO 1.解决测试数据库的创建和使用
# TODO 2.先创建用户, 普通用户和超管用户
def create_test_user():
    pass


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def client():
    return Client()
