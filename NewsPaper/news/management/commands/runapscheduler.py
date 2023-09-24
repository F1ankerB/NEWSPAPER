import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)

from django.core.mail import send_mail
from news.models import Category

def send_email_job():
    subject = 'Новые сообщения в вашей категории'
    message = 'Здравствуйте, новые сообщения доступны в вашей категории.'
    from_email = 'te4kkaunt@yandex.ru'

    # Получите все категории с подписчиками
    categories_with_subscribers = Category.objects.filter(subscribers__isnull=False)

    # Отправьте сообщение каждому подписчику в каждой категории
    for category in categories_with_subscribers:
        subscribers = category.subscribers.all()
        recipient_list = [user.email for user in subscribers]
        send_mail(subject, message, from_email, recipient_list)
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
            send_email_job,
            trigger=CronTrigger(second="0"),
            id="send_email_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_email_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")