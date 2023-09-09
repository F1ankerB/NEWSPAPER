from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList

urlpatterns = [

   path('news/', NewsList.as_view()),

]