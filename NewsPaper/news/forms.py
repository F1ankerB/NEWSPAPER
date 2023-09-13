from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['rating','post_type']  # Исключаем поле 'rating' из формы

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        instance.rating = 0.0  # Устанавливаем значение 'rating' в 0.0
        if commit:
            instance.save()
        return instance