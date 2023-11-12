# views.py
from __future__ import print_function
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,DeleteView
)
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .models import Post,Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Category
from django.core.mail import send_mail
from django.shortcuts import render
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from news.tasks import send_email_to_subscriber
from django.core.cache import cache

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.user not in category.subscribers.all():
        category.subscribers.add(request.user)
    else:
        # Если пользователь уже подписан, вы можете решить, отписывать его при повторном нажатии или оставить без изменений.
        # Для отписки используйте следующий код:
        # category.subscribers.remove(request.user)
        pass
    return redirect('/news')
@login_required
def become_author(request):
    author_group = Group.objects.get(name='authors')
    author, created = Author.objects.get_or_create(user=request.user)
    author_group.user_set.add(request.user)
    return redirect('/news')
class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    def get_queryset(self):
        queryset = Post.objects.filter(post_type='news').order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # Вычисляем количество всех новостей
        context['news_count'] = self.get_queryset().count()

        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj

from datetime import datetime, timedelta
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news'

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)

        # Определяем начало и конец текущего дня
        today_start = datetime.combine(datetime.now(), datetime.min.time())
        today_end = datetime.combine(datetime.now(), datetime.max.time())

        # Подсчитываем количество постов пользователя за текущий день
        post_count = Post.objects.filter(author=author, created_at__range=(today_start, today_end)).count()

        # Устанавливаем максимальное количество постов в день (3)
        max_posts_per_day = 3

        # Проверяем, не превысил ли пользователь максимальное количество постов
        if post_count >= max_posts_per_day:
            return HttpResponseForbidden("Вы не можете опубликовать больше трех постов в день.")

        # Устанавливаем автора поста в текущего пользователя перед сохранением
        form.instance.author = author

        form.instance.post_type = 'news'
        response = super().form_valid(form)  # Сначала вызываем родительский метод
        self.send_emails_for_new_post(self.object)  # Затем отправляем письма
        return response

    def send_emails_for_new_post(self, post):
        for category in post.categories.all():
            for subscriber in category.subscribers.all():
                send_email_to_subscriber.delay(subscriber.id,post.id)  # Используйте .delay для асинхронного вызова задачи Celery

    def send_email_to_subscriber(self, user, post):
        subject = post.title
        message = f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!\n\n"
        message += f"<h2>{post.title}</h2>\n<p>{post.text[:50]}...</p>"
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        message += f"<p><a href='{post_url}'>Читать полностью</a></p>"

        send_mail(subject, "", "te4kkaunt@yandex.ru", [user.email], html_message=message)

class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news'
    def form_valid(self, form):
        form.instance.post_type = 'news'  # Установка post_type как "article"
        return super().form_valid(form)

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news'

class ArticleCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news'
    def form_valid(self, form):
        form.instance.post_type = 'article'  # Установка post_type как "article"
        return super().form_valid(form)

class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = '/news'
    def form_valid(self, form):
        form.instance.post_type = 'article'  # Установка post_type как "article"
        return super().form_valid(form)

class ArticleDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news'
