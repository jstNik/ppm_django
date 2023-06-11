from django import forms
from django.forms import Textarea

from comments.models import Comment


class AddCommentForm(forms.ModelForm):
    body = forms.CharField(max_length=1000, widget=Textarea(attrs={'rows': 1}))

    class Meta:
        model = Comment
        fields = ['body']


class EditCommentForm(forms.Form):
    body = forms.CharField(max_length=1000, widget=Textarea(attrs={'rows': 1}))
    pk = forms.IntegerField()

    class Meta:
        model = Comment
        fields = ['pk', 'body']
