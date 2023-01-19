from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from NewsPortal import settings
from news.models import PostCategory


def send_notify_category_email(subscribers, category, preview, header, pk):
    html_content = render_to_string(
        'account/email/email_notify_category.html',
        {
            'link': f'{settings.SITE_URL}/news/',
            'category': ", ".join(category),
            'preview': preview,
            'header': header,
            'detail': f'{settings.SITE_URL}/news/{pk}',
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


@receiver(m2m_changed, sender=PostCategory)
def notify_category_email(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategories.all()
        subscribers = []
        category = []
        for cat in categories:
            subscribers += cat.subscribers.values_list('email', flat=True)
            category.append(cat.categories)

        send_notify_category_email(set(subscribers), category, instance.preview(), instance.header, instance.pk)

