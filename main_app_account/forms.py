from django import forms
from .models import UserBase
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,SetPasswordForm)

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w-full px-4 py-2 mt-2 border rounded-md border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-600', 'placeholder': 'Email', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'w-full px-4 py-2 mt-2 border rounded-md border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-600',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        min_length=2,
        max_length=50,
        # help_text='required',
        required=False,
    )
    
    last_name = forms.CharField(
        label='Last Name',
        min_length=2,
        max_length=50,
        # help_text='required',
        required=False,
    )
    
    user_name = forms.CharField(
        label='Username',
        min_length=4,
        max_length=50,
        required=True,
        # help_text='Required'
    )
    email = forms.EmailField(
        max_length=100,
        required=False,
        # help_text='Required',
        error_messages={
        'required': 'Email is required',}
    )
    password = forms.CharField(
        min_length=8,
        label='Password', 
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        min_length=8,
        label='Confirm Password', 
        widget=forms.PasswordInput
    )

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email address is already in use.')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-md border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-600', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-md border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-600', 'placeholder': 'Email', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-md border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-600', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-md border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-600', 'placeholder': 'Repeat Password'})