# user/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser  # 기존 User 대신 CustomUser를 사용
        fields = ['username', 'email', 'password1', 'password2']
