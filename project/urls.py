from django.urls import path
from .views import ProjectViewSet,UserProjectListView

project_list = ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

project_detail = ProjectViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

project_code_preview = ProjectViewSet.as_view({
    'get': 'code_preview'
})

project_comments = ProjectViewSet.as_view({
    'get': 'list_comments',
    'post': 'add_comment'
})

project_comment_delete = ProjectViewSet.as_view({
    'delete': 'delete_comment'
})

urlpatterns = [
    path('', project_list, name='project_list'),  # 프로젝트 목록 및 생성
    path('<int:pk>/', project_detail, name='project_detail'),  # 특정 프로젝트 조회, 수정, 삭제
    path('<int:pk>/code-preview/', project_code_preview, name='project_code_preview'),  # 코드 미리보기
    path('<int:pk>/comments/', project_comments, name='project_comments'),  # 특정 프로젝트 댓글 조회, 추가
    path('<int:pk>/comments/<int:comment_id>/', project_comment_delete, name='project_comment_delete'),  # 특정 댓글 삭제
    path('user/', UserProjectListView.as_view(), name='user_projects'),

]
