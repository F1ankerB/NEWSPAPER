# views.py
from __future__ import print_function
from django.views.generic import ListView,DetailView
from .models import Post

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем список новостей
        news = Post.objects.filter(post_type='news')

        # Сортируем новости по дате создания (самые новые сначала)
        news = news.order_by('-created_at')  # Обратный порядок

        context['news'] = news

        # Вычисляем количество всех новостей
        context['news_count'] = news.count()

        return context
class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'