# user/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# 기존 등록 해제 부분 제거
# admin.site.unregister(User)

# User 모델을 관리자 사이트에 등록
admin.site.register(User, UserAdmin)