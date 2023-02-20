from celery import shared_task
from datetime import datetime, timedelta

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from news.models import Post, Category


@shared_task
def new_posts_per_week():
    last_week = datetime.now() - timedelta(weeks=1)
    posts_per_week = Post.objects.filter(timeIn__gte=last_week)
    posts_per_week_category = set(posts_per_week.values_list('postCategories__categories', flat=True))
    posts_per_week_category_subscribers = set(Category.objects.filter(
        categories__in=posts_per_week_category).values_list('subscribers__email', flat=True))
    # print(f'cat: {", ".join(list(posts_per_week_category))}'
    #       )

    html_content = render_to_string(
        'account/email/email_notify_week_category.html',
        {
            'posts_per_week': posts_per_week,
            'link': f'{settings.SITE_URL}/news/',
            'category': ", ".join(list(posts_per_week_category)),
            'choices': len(list(posts_per_week_category)) == 1
        }
        #        'preview': "<br>".join(posts_per_week.values_list('text', flat=True)),
        #        'header': "<br>".join(posts_per_week.values_list('header', flat=True)),
    )

    msg = EmailMultiAlternatives(
        subject='Информация об изменении в разделе "Категории"',
        body='',
        from_email='yuran4ek37@yandex.ru',
        to=posts_per_week_category_subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_notify_category_email(instance):
    inst = Post.objects.get(pk=instance)
    categories = inst.postCategories.all()
    subscribers = []
    category = []
    for cat in categories:
        subscribers += cat.subscribers.values_list('email', flat=True)
        category.append(cat.categories)
    html_content = render_to_string(
        'account/email/email_notify_category.html',
        {
            'link': f'{settings.SITE_URL}/news/',
            'category': ", ".join(category),
            'preview': inst.preview(),
            'header': inst.header,
            'detail': f'{settings.SITE_URL}/news/{instance}',
        }
    )

    msg = EmailMultiAlternatives(
        subject='Информация об изменении в разделе "Категории"',
        body='',
        from_email='yuran4ek37@yandex.ru',
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

