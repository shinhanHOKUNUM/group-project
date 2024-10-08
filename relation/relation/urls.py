from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import main_view, CustomLoginView, SignupView, welcome_view  # welcome_view를 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_view, name='welcome'),  # 기본 URL을 welcome.html로 설정
    path('main/', main_view, name='main'),  # 로그인 후 메인 페이지로 리디렉션
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('user/', include('user.urls')),
    path('mypage/', include('mypage.urls')),
    path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'),  # 로그아웃 후 welcome으로 이동
]
