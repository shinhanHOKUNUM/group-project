from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required  # 추가
from relation.forms import CustomUserCreationForm
import pandas as pd
import torch
from .kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from django.http import JsonResponse
from .models import ITKeyword
import os
from django.conf import settings
import json

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


# Django view 함수 - JSON 파일을 불러오는 방식으로 수정
def get_network_data(request):
    # JSON 파일 경로 설정
    json_file_path = os.path.join(settings.BASE_DIR, 'relation/static/network_data.json')

    # JSON 파일을 읽어서 반환
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            network_data = json.load(f)  # JSON 파일을 파싱
    except FileNotFoundError:
        return JsonResponse({'error': 'network_data.json file not found'}, status=404)

    return JsonResponse(network_data)


def get_node_data(request, node_label):
    try:
        # ITKeyword에서 해당 노드를 term_ko 필드로 검색 (대소문자 구분 없이 정확한 일치 검색)
        node = ITKeyword.objects.get(term_ko__iexact=node_label)
        data = {
            'id': node.id,
            'label': node.term_ko,  # 'term_ko' 필드를 label로 사용
            'mean': node.mean       # 설명을 mean으로 반환
        }
        return JsonResponse(data)
    except ITKeyword.DoesNotExist:
        # 노드를 찾지 못했을 경우 에러 반환
        return JsonResponse({'error': 'Node not found'}, status=404)

