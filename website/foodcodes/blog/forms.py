from django import forms
from .models import Post, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class ContactForm(forms.Form):
    full_name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)
