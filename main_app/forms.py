from django import forms
from .models import ProductReview
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,SetPasswordForm)
from django.forms import ModelForm

class ReviewForm(ModelForm):
    title = forms.CharField(
        label='Title',
        min_length=10,
        max_length=50,
        required=True,
        )
    content = forms.CharField(
        label='Content',
        min_length=15,
        max_length=400,
        required=True,
    )
    rating = forms.IntegerField(
        label='Rating',
        min_value=1,
        max_value=5,
        required=False,
    )
    
    class Meta:
        model = ProductReview
        fields = ['title', 'content']
        
        labels = {
            'title': 'Title',
            'content': 'Content',
            'rating': 'Rating',
        }
        help_texts = {
            'title': 'Enter a title for your review',
            'content': 'Enter your review',
            'rating': 'Enter a rating for your review',
        }
        error_messages = {
            'title': {
                'max_length': "Title cannot be more than 50 characters",
                'min_length': "Title cannot be less than 10 characters",
                'required': "Title is required",
            },
            'content': {
                'min_length': "Content cannot be less than 15 characters",
                'required': "Content is required",
            },
            'rating': {
                'min_value': "Rating cannot be less than 1",
                'max_value': "Rating cannot be more than 5",
                'required': "Rating is required",
            },
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'block w-full px-4 py-2 rounded-lg border border-gray-300 placeholder-gray-500 focus:outline-none focus:border-gray-500 focus:shadow-outline-blue transition duration-150 ease-in-out', 'placeholder': 'Title'})
        self.fields['content'].widget.attrs.update({'class': 'block w-full px-4 py-2 rounded-lg border border-gray-300 placeholder-gray-500 focus:outline-none focus:border-gray-500 focus:shadow-outline-blue transition duration-150 ease-in-out', 'placeholder': 'Body Content'})
        
    
 