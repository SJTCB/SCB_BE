from django.urls import path
from .views import BoardViewSet

board_list = BoardViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

board_detail = BoardViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

board_comments = BoardViewSet.as_view({
    'get': 'list_comments',
    'post': 'add_comment'
})

board_comment_delete = BoardViewSet.as_view({
    'delete': 'delete_comment'
})

urlpatterns = [
    path('', board_list, name='board_list'),  # 게시글 목록 및 생성
    path('<int:pk>/', board_detail, name='board_detail'),  # 특정 게시글 조회, 수정, 삭제
    path('<int:pk>/comments/', board_comments, name='board_comments'),  # 특정 게시글 댓글 조회, 추가
    path('<int:pk>/comments/<int:comment_id>/', board_comment_delete, name='board_comment_delete'),  # 특정 댓글 삭제
]
