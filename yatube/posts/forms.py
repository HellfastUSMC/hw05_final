from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        exclude = ('author',)
        labels = {
            "text": 'Текст поста',
            "group": "Группа поста"
        }
        help_texts = {
            'text': 'Введите текст поста в поле выше',
            'group': 'Выберите группу, к которой будет относиться пост',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
        exclude = ('author', 'post', )
        labels = {
            "text": 'Текст комментария',
        }
        help_texts = {
            'text': 'Введите текст комментария в поле выше',
        }
