from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('users/', include('users.urls')),
    path('schema/', SpectacularAPIView.as_view(permission_classes=[AllowAny]), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]), name='swagger-ui'),
]