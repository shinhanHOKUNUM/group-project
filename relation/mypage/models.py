from django.db import models
from django.conf import settings  # 사용자 모델 참조를 위해

class TrackedData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자와 연결
    title = models.CharField(max_length=255, default='No Title')  # 제목
    nodes = models.JSONField()  # 노드 정보 JSON
    edges = models.JSONField()  # 엣지 정보 JSON
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 생성 시간