import logging
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
