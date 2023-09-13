from django_filters import FilterSet
import django_filters
from .models import Post
class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           'title': ['icontains'],
           'created_at': ['gte'],
           'author__user__username': ['icontains'],
       }