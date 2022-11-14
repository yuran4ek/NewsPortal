from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    postAuthor = forms.ModelChoiceField(queryset=Author.objects.all(),
                                        label='Автор публикации')
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
            'postAuthor',
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
