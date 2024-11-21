from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, CommentViewSet  # CommentViewSet 추가

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'comments', CommentViewSet)  # 댓글 라우터 추가

urlpatterns = [
    path('', include(router.urls)),
]
