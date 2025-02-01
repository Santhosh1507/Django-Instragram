# forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']  # Field for user to input a comment
        widgets = {
            'comment_text': forms.TextInput(attrs={'placeholder': 'Write a comment...'}),
        }
