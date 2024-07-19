from django import forms


class PostForm(forms.Form):
    author = forms.CharField(max_length=50, label='Автор')
    title = forms.CharField(max_length=200, label='Заголовок')
    text = forms.CharField(label='Текст поста', widget=forms.Textarea())
