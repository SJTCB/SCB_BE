import zipfile
import requests
import io
import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Project, Comment
from .serializers import (
    ProjectSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    CommentSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    def get_serializer_class(self):
        """Serializer 반환"""
        if self.action == 'list':
            return ProjectListSerializer  # 목록 조회
        elif self.action in ['retrieve', 'list_detail']:
            return ProjectDetailSerializer  # 세부사항 조회
        return ProjectSerializer  # 생성/수정용

    def perform_create(self, serializer):
        """프로젝트 생성"""
        # ZIP 파일 데이터 저장
        code_file = serializer.validated_data['code_file']  # 업로드된 ZIP 파일
        zip_data = code_file.read()  # ZIP 파일의 바이너리 데이터를 읽음

        project = serializer.save(code=zip_data)  # 원본 데이터를 code 필드에 저장

        try:
            # ZIP 파일 처리
            with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zf:
                # ZIP 파일의 최상위 디렉토리 추출
                if zf.namelist():
                    top_level = zf.namelist()[0].split('/')[0]  # 최상위 디렉토리 이름
                else:
                    top_level = "Unknown"

                # 최상위 디렉토리 이름을 zip_name 필드에 저장
                project.zip_name = top_level
                project.save()

        except zipfile.BadZipFile:
            project.delete()  # 잘못된 ZIP 파일인 경우 삭제
            raise ValueError("Invalid ZIP file uploaded.")

        # AI 모델에 점수 업데이트 요청
        self._update_project_score(project)





    def _update_project_score(self, project):
        """AI 모델로 점수 계산 및 업데이트"""
        try:
            file_data = project.code.hex()  # BinaryField 데이터를 HEX로 변환
            payload = {"code": file_data}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                "https://sozerong.pythonanywhere.com/random",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            project.score = response.json().get("score", 0.0)
        except requests.RequestException:
            project.score = 0.0
        project.save()

    @action(detail=False, methods=['get'], url_path='list')
    def project_list(self, request):
        """프로젝트 목록 조회"""
        queryset = self.get_queryset()
        serializer = ProjectListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list/(?P<id>[^/.]+)')
    def list_detail(self, request, id=None):
        """특정 프로젝트 세부사항 조회"""
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        comments = project.comments.all()
        comment_serializer = CommentSerializer(comments, many=True)

        response_data = {
            "id": project.id,
            "team_name": project.team_name,
            "team_members": project.team_members,
            "score": project.score,
            "code": project.zip_name,  # 최상위 디렉토리 이름 반환
            "comment": project.comment,
            "comments": comment_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)






    @action(detail=False, methods=['get', 'post'], url_path='list/(?P<id>[^/.]+)/comments')
    def list_comments(self, request, id=None):
        """댓글 조회 및 추가"""
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            comments = project.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='list/(?P<id>[^/.]+)/code-preview')
    def code_preview(self, request, id=None):
        """ZIP 파일의 텍스트 파일 내용 미리보기"""
        try:
            project = Project.objects.get(id=id)

            zip_data = io.BytesIO(project.code)  # BinaryField에서 ZIP 파일 데이터를 가져오기
            code_contents = {}
            with zipfile.ZipFile(zip_data, 'r') as zf:
                for file_name in zf.namelist():
                    if file_name.endswith(('.py', '.java', '.js', '.html', '.txt')):
                        with zf.open(file_name) as file:
                            code_contents[file_name] = file.read().decode('utf-8')

            return Response(code_contents, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
        except zipfile.BadZipFile:
            return Response({"error": "Invalid ZIP file format."}, status=status.HTTP_400_BAD_REQUEST)

