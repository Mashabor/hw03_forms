from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')


def clean_text(self):
    data = self.cleaned_data['text']
    # Если пользователь ничего не написал в теле поста
    if data == '':
        raise forms.ValidationError(
            'Вы ничего не написали, заполните поле!'
        )
    return data
