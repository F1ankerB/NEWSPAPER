"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from news.views import (NewsList, NewsDetail, PostCreate,PostUpdate,PostDelete,ArticleCreate,ArticleUpdate,ArticleDelete,become_author, subscribe_to_category
                        )
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', cache_page(60*1)(NewsList.as_view())),
    path('news/<int:pk>/', NewsDetail.as_view(),name='news_detail'),
    path('news/create/', cache_page(60*5)(PostCreate.as_view()), name='post_create'),
    path('news/<int:pk>/update/', cache_page(60*5)(PostUpdate.as_view()), name='post_update'),
    path('news/<int:pk>/delete/', cache_page(60*5)(PostDelete.as_view()), name='post_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('accounts/', include('allauth.urls')),
    path('become_author/', become_author, name='become_author'),
    path('subscribe/<int:category_id>/', subscribe_to_category, name='subscribe_to_category'),

]
