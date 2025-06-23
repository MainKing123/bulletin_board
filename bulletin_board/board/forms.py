from django import forms
from .models import Post, Response
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # WYSIWYG-редактор

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']

class CustomRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']