from modeltranslation.translator import register, TranslationOptions
from .models import Post, Category
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )
@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title','text' )