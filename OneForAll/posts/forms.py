from django import forms
from django.db.models import fields
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption','image')

class CommentModelForm(forms.ModelForm):
    text = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Comment'}))
    class Meta:
        model = Comment
        fields = ('text',)