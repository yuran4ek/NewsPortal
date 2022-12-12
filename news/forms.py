from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    header = forms.CharField(min_length=20,
                             label='Заголовок публикации')
    text = forms.CharField(label='Текст публикации',
                           widget=forms.Textarea)
    postCategories = forms.ModelMultipleChoiceField(label='Категория публикации',
                                                    queryset=Category.objects.all(),
                                                    widget=forms.SelectMultiple)
    postsOrNews = forms.ChoiceField(label='Тип публикации',
                                    choices=Post.TYPES)

    class Meta:
        model = Post
        fields = [
            'header',
            'text',
            'postCategories',
            'postsOrNews',

        ]

    def clean(self):
        cleaned_data = super(PostForm, self).clean()

        header = cleaned_data.get('header')
        if header[0].islower():
            raise ValidationError(
                'Заголовок должен начинаться с заглавной буквы.'
            )

        text = cleaned_data.get('text')
        if text is None:
            raise ValidationError(
                'Поле не может быть пустым.'
            )
        if text[0].islower():
            raise ValidationError(
                'Текст публикации должен начинаться с заглавной буквы.'
            )
        if text is not None and text == header:
            raise ValidationError(
                'Текст публикации не должен быть идентичен заголовку публикации.'
            )

        return cleaned_data


class CommentForm(forms.ModelForm):
    comments = forms.CharField(max_length=80,
                               label='Ваш комментарий',
                               )

    class Meta:
        model = Comment
        fields = [
            'comments',
        ]

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()

        comments = cleaned_data.get('comments')
        if comments is None:
            raise ValidationError(
                'Поле не может быть пустым.'
            )
        if comments[0].islower():
            raise ValidationError(
                'Текст публикации должен начинаться с заглавной буквы.'
            )

        return cleaned_data
