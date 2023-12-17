import pytest

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


def test_client(client: Client):
    res = client.get(reverse("home"))

    assert res.status_code == 200
