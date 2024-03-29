from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.core.cache import cache
from django.db.models import Sum


class Author(models.Model):
    rating = models.IntegerField(default=0)
    users = models.OneToOneField(User,
                                 on_delete=models.CASCADE)

    def update_rating(self):
        postRait = sum(Post.objects.filter(postAuthor=self).values_list('rating', flat=True))
        if postRait is None:
            postRait = 0

        commentRait = sum(Comment.objects.filter(userComment__username=self).values_list('rating', flat=True))
        if commentRait is None:
            commentRait = 0

        commentPostRait = sum(Comment.objects.filter(postComment__postAuthor=self).values_list('rating', flat=True))
        if commentPostRait is None:
            commentPostRait = 0

        self.rating = postRait * 3 + commentRait + commentPostRait
        self.save()

    def __str__(self):
        return f'{self.users}'


class Category(models.Model):
    categories = models.CharField(max_length=255,
                                  unique=True)
    subscribers = models.ManyToManyField(User,
                                         related_name='sub_categories',
                                         through='SubscribeCategories')

    def __str__(self):
        return f'{self.categories}'

    def get_subscribers(self):
        return ",\n".join([str(p) for p in self.subscribers.all()])


class Post(models.Model):
    posts = 'PT'
    news = 'NS'

    TYPES = [
        (posts, 'Статья'),
        (news, 'Новость')
    ]

    postsOrNews = models.CharField(max_length=2,
                                   choices=TYPES,
                                   default=posts)
    timeIn = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    postAuthor = models.ForeignKey(Author,
                                   on_delete=models.CASCADE)
    postCategories = models.ManyToManyField(Category,
                                            through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:128] + '...'

    def __str__(self):
        return f'{self.text}'

    def get_absolute_url(self):
        return reverse('news_list')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)


class SubscribeCategories(models.Model):
    subscriber = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    subCategory = models.ForeignKey(Category,
                                    on_delete=models.CASCADE)


class Comment(models.Model):
    comments = models.CharField(max_length=255)
    timeIn = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    postComment = models.ForeignKey(Post,
                                    on_delete=models.CASCADE)
    userComment = models.ForeignKey(User,
                                    on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
