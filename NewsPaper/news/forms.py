from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # или widget=forms.SelectMultiple, в зависимости от вашего предпочтения
        required=False,
        label="Категории"
    )

    class Meta:
        model = Post
        exclude = ['rating', 'post_type','author']

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        instance.rating = 0.0
        if commit:
            instance.save()
            self.save_m2m()  # Это сохраняет связанные объекты ManyToMany
        return instance
