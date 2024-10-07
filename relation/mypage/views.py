from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TrackedData
import json


@login_required
def word_directory(request):
    # 로그인한 사용자와 연관된 데이터만 가져옴
    tracked_data = TrackedData.objects.filter(user=request.user)

    return render(request, 'mypage/word-directory.html', {'tracked_data': tracked_data})

@csrf_exempt
def delete_tracked_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tracked_data_id = data.get('id')
            # DB에서 해당 데이터를 삭제
            tracked_data = TrackedData.objects.get(id=tracked_data_id, user=request.user)
            tracked_data.delete()
            return JsonResponse({'status': 'success'})
        except TrackedData.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Data not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)