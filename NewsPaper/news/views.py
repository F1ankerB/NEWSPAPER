# views.py
from __future__ import print_function
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,DeleteView
)
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
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

class PostCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm

    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    success_url = '/news'
    def form_valid(self, form):
        form.instance.post_type = 'news'  # Установка post_type как "article"
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news'
    def form_valid(self, form):
        form.instance.post_type = 'news'  # Установка post_type как "article"
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news'

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news'
    def form_valid(self, form):
        form.instance.post_type = 'article'  # Установка post_type как "article"
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = '/news'
    def form_valid(self, form):
        form.instance.post_type = 'article'  # Установка post_type как "article"
        return super().form_valid(form)

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news'
