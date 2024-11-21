import requests
import base64
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Comment
from .serializers import ProjectSerializer, CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        # 데이터 반환 없이 메시지만 전달
        return Response({"message": "This endpoint is for project creation only."}, status=status.HTTP_200_OK)

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
                serializer.save(project=project)  # project를 URL의 프로젝트로 설정
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
