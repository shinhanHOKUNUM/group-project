from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path('directory/', lambda request: render(request, 'mypage/word-diretory.html'), name='mypage'),
]
