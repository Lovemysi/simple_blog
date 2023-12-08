from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.fields import CharField, EmailField, ImageField

from .models import BlogUser


class BlogUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email",  "password1", "password2"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            current_field: CharField | EmailField = field
            current_field.widget.attrs.update({'class': 'bg-gray-200 rounded-md p-2 my-4 outline-none text-gray-600 w-full'})

        username: CharField = self.fields['username']
        email: EmailField = self.fields['email']
        password1: CharField = self.fields['password1']
        password2: CharField = self.fields['password2']

        username.widget.attrs.update({'placeholder': '用户名', 'autocomplete': 'bloguser'})
        email.widget.attrs.update({'placeholder': '邮箱', 'autocomplete': 'blogemail'})
        password1.widget.attrs.update({'placeholder': '密码'})
        password2.widget.attrs.update({'placeholder': '确认密码'})


class BlogUserHomeForm(ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            current_field: CharField | EmailField | ImageField = field

            current_field.widget.attrs.update({'class': 'bg-gray-200 rounded-md p-2 my-4 outline-none text-gray-600 w-full'})

    class Meta:
        model = BlogUser
        fields = ['username', 'email']
