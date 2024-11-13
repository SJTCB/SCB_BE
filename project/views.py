import requests
import base64
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project
from .serializers import ProjectSerializer, ProjectListSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        # 임시로 score 기본값 0 설정
        score = 0

        # Project 인스턴스를 생성하여 코드 파일을 가져옵니다.
        project = serializer.save(score=score)
        code_file = project.code

        # 모델 URL에 JSON 형식으로 파일을 전송하여 점수 요청
        try:
            with open(code_file.path, 'rb') as file:
                # 파일 내용을 base64로 인코딩하여 "code" 키로 전송
                file_data = base64.b64encode(file.read()).decode('utf-8')
                payload = {
                    "code": file_data  # Flask 서버가 기대하는 "code" 키로 수정
                }
                headers = {'Content-Type': 'application/json'}
                response = requests.post("https://sozerong.pythonanywhere.com/random", json=payload, headers=headers)
            response.raise_for_status()
            score = response.json().get("score", 0)
        except requests.RequestException:
            score = 0  # 요청 실패 시 기본값 0 설정

        # 업데이트된 점수로 다시 저장
        project.score = score
        project.save()

    @action(detail=False, methods=['get'], url_path='list')
    def project_list(self, request):
        # 목록 조회 시 필요한 필드만 반환하기 위해 ProjectListSerializer 사용
        queryset = self.get_queryset()
        serializer = ProjectListSerializer(queryset, many=True)
        return Response(serializer.data)
