from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm  # 이미 CustomUser를 사용하도록 수정된 폼

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')  # 회원가입 후 메인 페이지로 리디렉션
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')  # 로그인 후 메인 페이지로 이동
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

# 기존의 signup_view와 login_view 이후에 추가
def main_view(request):
    return render(request, 'relation/main.html')