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
from relation.models import AIDictionary  # 모델을 불러옴


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

def get_network_data(request):
    # 데이터베이스에서 데이터를 가져오기
    ai_terms = AIDictionary.objects.all()

    # 그래프 객체 생성
    G = nx.Graph()

    # 노드 추가 (term-kor와 searchkeyword 기준)
    for term in ai_terms:
        G.add_node(term.id, label=term.term_kor, searchkeyword=term.term)  # 각 노드에 searchkeyword로 term 추가

    # 엣지 추가 (연결 조건은 필요에 따라 조정)
    for i, current_term in enumerate(ai_terms):
        current_content = f"{current_term.mean} {current_term.detail_mean}"

        for j, other_term in enumerate(ai_terms):
            if i != j:
                term_en = other_term.term_en
                term_kor = other_term.term_kor

                # term-en 또는 term-kor이 mean이나 detail_mean에 등장하는 경우 엣지 추가
                if term_en in current_content or term_kor in current_content:
                    G.add_edge(current_term.id, other_term.id)

    # Kamada-Kawai 레이아웃 적용 (노드 좌표 계산)
    pos = nx.kamada_kawai_layout(G)

    # 노드 데이터 (좌표 포함)
    nodes = [{'id': n, 'label': G.nodes[n]['label'], 'searchkeyword': G.nodes[n]['searchkeyword'], 'x': pos[n][0], 'y': pos[n][1]} for n in G.nodes()]

    # 엣지 데이터
    edges = [{'from': u, 'to': v} for u, v in G.edges()]

    # JSON 형태로 노드와 엣지를 반환
    data = {
        'nodes': nodes,
        'edges': edges
    }

    return JsonResponse(data)
