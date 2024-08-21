from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin  # 로그인 여부를 확인하는 믹스인
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from relation.forms import CustomUserCreationForm


# 메인 페이지 뷰, 로그인된 사용자만 접근 가능
class Sub(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "relation/main.html")

# 사용자 로그인 뷰
class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True  # 이미 로그인된 사용자는 리디렉션
    success_url = reverse_lazy('main')  # 로그인 후 메인 페이지로 리디렉션

    def get_success_url(self):
        return self.success_url

# 사용자 회원가입 뷰
class SignupView(LoginView):
    template_name = 'user/signup.html'
    redirect_authenticated_user = True  # 이미 로그인된 사용자는 리디렉션
    success_url = reverse_lazy('main')  # 회원가입 후 메인 페이지로 리디렉션

    def get_success_url(self):
        return self.success_url

# views.py 예시 (사용자가 로그인되어 있을 경우 강제로 로그아웃 시키는 방법)
from django.contrib.auth import logout
from django.shortcuts import redirect

def force_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('main')

def main_view(request):
    return render(request, 'relation/main.html')

class SignupView(CreateView):
    form_class = CustomUserCreationForm  # 기본 폼 대신 커스텀 폼 사용
    template_name = 'user/signup.html'
    success_url = reverse_lazy('login')