import requests
import base64
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Project, Comment
from .serializers import (
    ProjectSerializer,
    ProjectListSerializer,
    ProjectUpdateSerializer,
    ProjectDetailSerializer,
    CommentSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    def get_serializer_class(self):
        """Swagger의 fake_view를 처리하여 적절한 serializer 반환"""
        if getattr(self, "swagger_fake_view", False):
            # Swagger를 위한 기본 serializer 반환
            return ProjectSerializer

        if self.action == "list":
            return ProjectListSerializer  # 목록 조회용
        elif self.action == "retrieve":
            return ProjectDetailSerializer  # 상세 조회용
        elif self.action in ["update", "partial_update"]:
            return ProjectUpdateSerializer  # 수정용
        return ProjectSerializer  # 생성용



    @swagger_auto_schema(auto_schema=None)  # Swagger 문서에서 제외
    def list(self, request, *args, **kwargs):
        return Response(
            {"message": "This endpoint is not available."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def perform_create(self, serializer):
        """프로젝트 생성 후 점수 계산 요청"""
        project = serializer.save()
        self._update_project_score(project)

    def _update_project_score(self, project):
        """Flask 모델 서버로 점수를 요청하고 업데이트"""
        try:
            file_data = base64.b64encode(project.code).decode("utf-8")
            payload = {"code": file_data}
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                "https://sozerong.pythonanywhere.com/random",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            project.score = response.json().get("score", 0)
        except requests.RequestException:
            project.score = 0
        project.save()

    @swagger_auto_schema(
        operation_summary="프로젝트 목록 조회",
        operation_description="등록된 모든 프로젝트 목록을 반환합니다.",
        responses={200: ProjectListSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="list")
    def project_list(self, request):
        """프로젝트 목록 조회"""
        queryset = self.get_queryset()
        serializer = ProjectListSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="get",
        operation_summary="특정 프로젝트 댓글 조회",
        operation_description="특정 프로젝트의 댓글 목록을 반환합니다.",
        responses={200: CommentSerializer(many=True)},
    )
    @swagger_auto_schema(
        method="post",
        operation_summary="특정 프로젝트 댓글 추가",
        operation_description="특정 프로젝트에 댓글을 추가합니다.",
        request_body=CommentSerializer,
        responses={201: "댓글 추가 성공", 400: "유효하지 않은 데이터"},
    )
    @action(detail=True, methods=["get", "post"], url_path="comments")
    def project_comments(self, request, pk=None):
        """특정 프로젝트 댓글 처리"""
        project = self.get_object()

        if request.method == "GET":
            comments = project.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
