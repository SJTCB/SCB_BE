import requests
import base64
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Comment
from .serializers import ProjectSerializer, ProjectListSerializer, CommentSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        # 기본 메시지 반환
        return Response({"message": "This endpoint is for project creation only."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='list')
    def custom_list(self, request):
        """
        GET: 모든 프로젝트의 팀명, 팀원, 점수, 내용을 반환
        """
        projects = Project.objects.all()
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # 기본 점수 0으로 설정
        score = 0
        project = serializer.save(score=score)
        code_file = project.code

        # 모델 URL로 파일 전송 및 점수 요청
        try:
            with open(code_file.path, 'rb') as file:
                file_data = base64.b64encode(file.read()).decode('utf-8')
                payload = {"code": file_data}
                headers = {'Content-Type': 'application/json'}
                response = requests.post("https://sozerong.pythonanywhere.com/random", json=payload, headers=headers)
            response.raise_for_status()
            score = response.json().get("score", 0)
        except requests.RequestException:
            score = 0  # 요청 실패 시 기본값

        # 점수 저장
        project.score = score
        project.save()

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def project_comments(self, request, pk=None):
        """
        GET: 특정 프로젝트의 댓글 목록 반환
        POST: 특정 프로젝트에 댓글 추가
        """
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            # 특정 프로젝트의 댓글 목록 조회
            comments = project.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            # 특정 프로젝트에 댓글 생성
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
