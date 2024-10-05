from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import main_view, CustomLoginView, SignupView, welcome_view  # welcome_view를 추가
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_view, name='welcome'),  # 기본 URL을 welcome.html로 설정
    path('main/', main_view, name='main'),  # 로그인 후 메인 페이지로 리디렉션
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('user/', include('user.urls')),
    path('mypage/', include('mypage.urls')),
    path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'),  # 로그아웃 후 welcome으로 이동
    path('get_network_data/', views.get_network_data, name='get_network_data'),
    path('get_node_data/<str:node_label>/', views.get_node_data, name='get_node_data'),  # node_id를 node_label로 변경
    path('save_tracked_data/', views.save_tracked_data, name='save_tracked_data'),
    path('word-directory/', views.word_directory, name='word_directory'),
]
