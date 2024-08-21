# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''  # 모든 필드의 도움말 텍스트 제거
        self.fields['password1'].help_text = ''  # 패스워드 필드의 도움말 텍스트 제거
        self.fields['password2'].help_text = ''  # 패스워드 확인 필드의 도움말 텍스트 제거
