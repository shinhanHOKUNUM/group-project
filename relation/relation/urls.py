"""
URL configuration for relation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from relation.views import Sub
from relation.views import CustomLoginView
from relation.views import SignupView
from .views import main_view, CustomLoginView, SignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main'),  # 메인 페이지를 루트 URL로 설정

    path('login/', CustomLoginView.as_view(), name='login'),

    path('signup/', SignupView.as_view(), name='signup'),

    path('user/', include('user.urls')),

    # mypage 앱의 URL을 포함시킵니다.
    path('mypage/', include('mypage.urls')),

    path('logout/', LogoutView.as_view(), name='logout'),
]
