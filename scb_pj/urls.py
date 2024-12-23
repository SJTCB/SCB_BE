from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger 설정
schema_view = get_schema_view(
    openapi.Info(
        title="SCB Project API",
        default_version="v1",
        description="SCB 프로젝트 API 문서",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin 페이지
    path('admin/', admin.site.urls),

    # 앱별 엔드포인트
    path('api/project/', include('project.urls')),  # Project 앱 URL
    path('api/user/', include('users.urls')),       # Users 앱 URL 포함
    path('api/board/', include('board.urls')),      # Board 앱 URL 포함

    # Swagger 문서
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# DEBUG 모드일 때 MEDIA_URL 경로 추가
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
