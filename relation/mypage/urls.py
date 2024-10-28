from django.urls import path
from . import views

urlpatterns = [
    path('word-directory/', views.word_directory, name='word_directory'),
    path('delete/<int:pk>/', views.delete_tracked_data, name='delete_tracked_data'),  # pk 전달
]
