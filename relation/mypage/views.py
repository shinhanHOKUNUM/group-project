from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TrackedData
import json


@login_required
def word_directory(request):
    # 로그인한 사용자와 연관된 데이터만 가져옴
    tracked_data = TrackedData.objects.filter(user=request.user)

    # QuerySet을 리스트 형태로 변환하여 직렬화 가능하게 처리
    tracked_data_list = []
    for data in tracked_data:
        # 이미 리스트 형태인 nodes와 edges를 그대로 사용
        nodes = data.nodes  # 그대로 사용
        edges = data.edges  # 그대로 사용

        tracked_data_list.append({
            'id': data.id,  # 여기서 id 값을 추가
            'title': data.title,
            'nodes': nodes,  # 직렬화된 nodes
            'edges': edges   # 직렬화된 edges
        })

    # 리스트를 JSON으로 직렬화
    tracked_data_json = json.dumps(tracked_data_list)

    # JSON 데이터를 템플릿으로 전달
    return render(request, 'mypage/word-directory.html', {'tracked_data': tracked_data_json})


@csrf_exempt
@login_required
def delete_tracked_data(request, pk):
    if request.method == 'POST':
        try:
            # DB에서 해당 데이터를 삭제
            tracked_data = get_object_or_404(TrackedData, pk=pk, user=request.user)
            tracked_data.delete()
            return JsonResponse({'status': 'success'})
        except TrackedData.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Data not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
