from django import forms
from .models import Post


class UserCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    file = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'file'
        ]
