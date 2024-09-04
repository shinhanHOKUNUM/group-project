from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required  # 추가

import os
import pandas as pd
from django.http import JsonResponse
from django.conf import settings
import networkx as nx

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

# AI_dictionary.csv로 노드랑 엣지 만들기
def get_network_data(request):
    # AI_dictionary.csv 파일 경로 지정
    file_path = os.path.join(settings.BASE_DIR, 'relation', 'static', 'AI_dictionary.csv')

    # CSV 파일 읽기
    df = pd.read_csv(file_path)

    # 그래프 객체 생성
    G = nx.Graph()

    # 노드 추가 (term-kor 기준)
    for index, row in df.iterrows():
        G.add_node(index, label=row['term-kor'])

    # 엣지 추가 (연결 조건은 필요에 따라 조정)
    for i, row in df.iterrows():
        current_term = row['term']
        current_content = f"{row['mean']} {row['detail_mean']}"

        for j, other_row in df.iterrows():
            if i != j:
                other_term = other_row['term']
                term_en = other_row['term-en']
                term_kor = other_row['term-kor']

                # term-en 또는 term-kor이 mean이나 detail_mean에 등장하는 경우 엣지 추가
                if term_en in current_content or term_kor in current_content:
                    G.add_edge(i, j)

    # Kamada-Kawai 레이아웃 적용 (노드 좌표 계산)
    pos = nx.kamada_kawai_layout(G)

    # 노드 데이터 (좌표 포함)
    nodes = [{'id': n, 'label': G.nodes[n]['label'], 'x': pos[n][0], 'y': pos[n][1]} for n in G.nodes()]

    # 엣지 데이터
    edges = [{'from': u, 'to': v} for u, v in G.edges()]

    # JSON 형태로 노드와 엣지를 반환
    data = {
        'nodes': nodes,
        'edges': edges
    }

    return JsonResponse(data)
