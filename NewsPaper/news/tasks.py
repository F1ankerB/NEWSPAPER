from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_to_subscriber(user_id, post_id):
    from .models import User, Post  # Импортируем модели здесь, чтобы избежать циклического импорта

    user = User.objects.get(id=user_id)
    post = Post.objects.get(id=post_id)

    subject = post.title
    message = f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!\n\n"
    message += f"<h2>{post.title}</h2>\n<p>{post.text[:50]}...</p>"
    post_url = post.get_absolute_url()
    red_post_url=f'http://127.0.0.1:8000{post_url}'
    message += f"<p><a href='{red_post_url}'>Читать полностью</a></p>"

    send_mail(subject, "", "te4kkaunt@yandex.ru", [user.email], html_message=message)

from django.utils import timezone
from datetime import timedelta

@shared_task
def send_weekly_email():
    from .models import Category, Post
    subject = 'Новые сообщения в вашей категории'
    from_email = 'te4kkaunt@yandex.ru'

    categories_with_subscribers = Category.objects.filter(subscribers__isnull=False)

    for category in categories_with_subscribers:
        subscribers = category.subscribers.all()

        week_ago = timezone.now() - timedelta(days=7)
        articles = Post.objects.filter(categories=category, created_at__gte=week_ago)

        if not articles.exists():
            continue

        articles_info = []
        for index, article in enumerate(articles, 1):
            article_text = f"{index}. {article.title}\nТекст: {article.text[:50]}...\nСсылка: http://127.0.0.1:8000{article.get_absolute_url()}\n"
            articles_info.append(article_text)

        message_body = f'Здравствуйте, {subscribers[0].username},\n\nЗа прошедшую неделю были опубликованы следующие статьи:\n\n' + '\n'.join(articles_info)

        recipient_list = [user.email for user in subscribers]
        send_mail(subject, message_body, from_email, recipient_list)