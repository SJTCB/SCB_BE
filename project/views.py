import requests
import base64
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Comment
from .serializers import ProjectSerializer, ProjectListSerializer,ProjectUpdateSerializer, ProjectDetailSerializer, CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer  # 목록 조회용
        elif self.action == 'retrieve':
            return ProjectDetailSerializer  # 상세 조회용
        elif self.action in ['update', 'partial_update']:
            return ProjectUpdateSerializer  # 수정용
        return ProjectSerializer  # 생성용


    def perform_create(self, serializer):
        # 프로젝트 생성 후 점수 계산 요청
        project = serializer.save()
        self._update_project_score(project)

        

    def _update_project_score(self, project):
        """Flask 모델 서버로 점수를 요청하고 업데이트"""
        try:
            file_data = base64.b64encode(project.code).decode('utf-8')
            payload = {"code": file_data}
            headers = {'Content-Type': 'application/json'}
            response = requests.post("https://sozerong.pythonanywhere.com/random", json=payload, headers=headers)
            response.raise_for_status()
            project.score = response.json().get("score", 0)
        except requests.RequestException:
            project.score = 0
        project.save()

    @action(detail=False, methods=['get'], url_path='list')
    def project_list(self, request):
        # 프로젝트 목록 조회
        queryset = self.get_queryset()
        serializer = ProjectListSerializer(queryset, many=True)  # 올바른 Serializer 사용
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def project_comments(self, request, pk=None):
        project = self.get_object()

        if request.method == 'GET':
            # 댓글 목록 조회
            comments = project.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            # 댓글 추가
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
