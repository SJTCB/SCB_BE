# from django.urls import path
# from .views import ProfileList, ProfileDetail  # views.py 파일에서 가져옴

# urlpatterns = [
#     path('', ProfileList.as_view(), name='profile-list'),
#     path('<int:school_id>/', ProfileDetail.as_view(), name='profile-detail'),
# ]


from django.urls import path
from .views import RegisterView,LoginView,ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', ProfileView.as_view()),
]