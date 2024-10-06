from django.urls import path
from mypage.views import word_directory
from mypage.views import delete_tracked_data

urlpatterns = [
    path('word-directory/', word_directory, name='mypage'),
    path('word-directory/delete_tracked_data/', delete_tracked_data, name='delete_tracked_data'),
]
