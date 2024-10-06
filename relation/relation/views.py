from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required  # 추가
from django.views.decorators.csrf import csrf_exempt
from relation.forms import CustomUserCreationForm
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
        # 데이터베이스에서 term_ko 필드를 기준으로 해당 노드를 찾음
        node = ITKeyword.objects.get(term_ko__iexact=node_label)

        # JSON 파일 경로 설정 (connected_labels 정보를 가져오기 위한 network_data.json)
        json_file_path = os.path.join(settings.BASE_DIR, 'relation/static/network_data.json')

        # JSON 파일을 읽어서 파싱
        with open(json_file_path, 'r', encoding='utf-8') as f:
            network_data = json.load(f)

        # network_data.json에서 해당 노드를 찾고 connected_labels를 가져옴
        json_node = next((n for n in network_data['nodes'] if n['label_ko'] == node_label), None)
        connected_labels = json_node.get('connected_labels', []) if json_node else []

        # 반환할 데이터 (label_full, label_en, label_kor, mean은 데이터베이스에서, connected_labels는 JSON에서)
        data = {
            'label_full': node.term,  # 데이터베이스에서 term을 label_full로 사용
            'label_en': node.term_en,  # 데이터베이스에서 term_en을 label_en으로 사용
            'label_kor': node.term_ko,  # 데이터베이스에서 term_ko를 label_kor으로 사용
            'mean': node.mean,  # 데이터베이스에서 mean을 사용
            'connected_labels': connected_labels  # JSON에서 가져온 connected_labels
        }

        return JsonResponse(data)

    except ITKeyword.DoesNotExist:
        return JsonResponse({'error': 'Node not found'}, status=404)

    except FileNotFoundError:
        return JsonResponse({'error': 'network_data.json file not found'}, status=404)

@csrf_exempt  # CSRF 보호 비활성화 (Ajax POST 요청)
def save_tracked_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # 제목을 포함하여 데이터를 받음
            title = data.get('title', 'No Title')  # 제목을 받지 않았을 때 기본값으로 'No Title'

            # 세션에 저장된 데이터와 함께 mean 값을 추가
            nodes_with_mean = []
            for node in data['nodes']:
                try:
                    node_data = ITKeyword.objects.get(term_ko__iexact=node['label_kor'])
                    node['mean'] = node_data.mean  # mean 값을 추가
                except ITKeyword.DoesNotExist:
                    node['mean'] = 'Mean not found'  # 해당 노드가 없으면 기본 메시지

                nodes_with_mean.append(node)

            # 추적된 데이터로 세션을 업데이트
            request.session['tracked_data'] = {
                'title': title,  # 세션에 제목 추가
                'nodes': nodes_with_mean,
                'edges': data['edges']
            }

            return JsonResponse({'message': 'Data saved successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def word_directory(request):
    # 세션에서 추적한 데이터와 제목을 가져옴
    tracked_data = request.session.get('tracked_data', {'title': '', 'nodes': [], 'edges': []})
    return render(request, 'mypage/word-directory.html', {'tracked_data': json.dumps(tracked_data)})


