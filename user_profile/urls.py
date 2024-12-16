from django.urls import path
from .views import ProfileList, ProfileDetail  # views.py 파일에서 가져옴

urlpatterns = [
    path('', ProfileList.as_view(), name='profile-list'),
    path('<int:school_id>/', ProfileDetail.as_view(), name='profile-detail'),
]
