import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)

from django.urls import reverse
from django.core.mail import send_mail
from news.models import Category,Post
from datetime import timedelta
from django.utils import timezone

def send_email_job():
    subject = 'Новые сообщения в вашей категории'
    from_email = 'te4kkaunt@yandex.ru'

    # Получите все категории с подписчиками
    categories_with_subscribers = Category.objects.filter(subscribers__isnull=False)

    for category in categories_with_subscribers:
        subscribers = category.subscribers.all()

        # Получите все статьи за прошедшую неделю для этой категории
        week_ago = timezone.now() - timedelta(days=7)
        articles = Post.objects.filter(categories=category, created_at__gte=week_ago)

        # Если статей нет, то пропускаем этот шаг
        if not articles.exists():
            continue

        # Сформируйте сообщение
        articles_info = []
        for index, article in enumerate(articles, 1):
            article_text = f"{index}. {article.title}\nТекст: {article.text[:50]}...\nСсылка: http://127.0.0.1:8000{article.get_absolute_url()}\n"
            articles_info.append(article_text)

        message_body = f'Здравствуйте, {subscribers[0].username},\n\nЗа прошедшую неделю были опубликованы следующие статьи:\n\n' + '\n'.join(articles_info)

        recipient_list = [user.email for user in subscribers]
        send_mail(subject, message_body, from_email, recipient_list)
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
            trigger=CronTrigger(day_of_week="sun", hour="12", minute="0"),
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