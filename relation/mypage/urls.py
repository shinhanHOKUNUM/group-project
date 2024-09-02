from django.urls import path
from .views import word_directory_view

urlpatterns = [
    path('word-directory/', word_directory_view, name='mypage'),
]