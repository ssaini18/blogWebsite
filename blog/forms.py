from .models import Post
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PostForm(forms.ModelForm):
	date = forms.DateField(widget=forms.SelectDateWidget)

	class Meta:
		model = Post
		fields = ['title', 'body', 'date']

