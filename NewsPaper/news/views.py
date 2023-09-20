# views.py
from __future__ import print_function
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,DeleteView
)
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
@login_required
def become_author(request):
    author_group = Group.objects.get(name='authors')
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

class PostCreate(PermissionRequiredMixin,CreateView):
    permission_required='news.add_post'
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
