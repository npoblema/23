from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CustomTokenObtainPairView, RegisterView

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]