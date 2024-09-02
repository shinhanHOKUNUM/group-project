from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import signup_view, login_view, main_view  # main_view 추가

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
path('main/', main_view, name='main'),  # main_view에 대한 URL 패턴 추가
]