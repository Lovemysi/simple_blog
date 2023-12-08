from django.forms import ModelForm
from django.db.models import ImageField, CharField, TextField

from .models import Post


class PostForm(ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        title: CharField = self.fields['title']
        body: TextField = self.fields['body']

        title.widget.attrs.update({'class': 'bg-gray-200 rounded-md p-2 my-4 outline-none text-gray-600 w-full', 'placeholder': '标题'})
        body.widget.attrs.update(
            {'class': 'bg-white rounded-md p-2 my-4 outline-none text-gray-600 border-blue-100 border-2 h-52',
             'cols': '80'})

    class Meta:
        model = Post
        fields = ['title', 'body', ]
