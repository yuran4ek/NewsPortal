from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from NewsPortal import settings
from news.models import PostCategory
from news.tasks import send_notify_category_email


@receiver(m2m_changed, sender=PostCategory)
def notify_category_email(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        send_notify_category_email.delay(instance.pk)
