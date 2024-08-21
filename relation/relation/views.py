from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class Sub(APIView):
    def get(self, request):
        return render(request, "relation/main.html")

# class Signup(APIView):
#     def get(self, request):
#         return render(request, "user/login.html")

class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True  # 이미 로그인된 사용자는 리디렉션
    success_url = reverse_lazy('home')  # 로그인 후 리디렉션할 URL, 'home'을 원하는 대로 변경 가능

    def get_success_url(self):
        return self.success_url




class SignupView(LoginView):
    template_name = 'user/signup.html'
    redirect_authenticated_user = True  # 이미 로그인된 사용자는 리디렉션
    success_url = reverse_lazy('home')  # 로그인 후 리디렉션할 URL, 'home'을 원하는 대로 변경 가능

    def get_success_url(self):
        return self.success_url