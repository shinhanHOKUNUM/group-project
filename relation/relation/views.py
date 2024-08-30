from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required  # 추가

from relation.forms import CustomUserCreationForm

# 사용자 로그인 뷰
class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True  # 이미 로그인된 사용자는 리디렉션
    success_url = reverse_lazy('main')  # 로그인 후 루트 URL로 리디렉션

    def get_success_url(self):
        return self.success_url

# 사용자 회원가입 뷰
class SignupView(CreateView):
    form_class = CustomUserCreationForm  # 기본 폼 대신 커스텀 폼 사용
    template_name = 'user/signup.html'
    success_url = reverse_lazy('login')  # 회원가입 후 로그인 페이지로 리디렉션

    def get_success_url(self):
        return self.success_url

# Welcome 페이지 뷰
def welcome_view(request):
    return render(request, 'relation/welcome.html')

# 메인 페이지 뷰, 로그인된 사용자만 접근 가능
@login_required
def main_view(request):
    return render(request, 'relation/main.html')
