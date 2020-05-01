from django.urls import path

from .api_views import EmailCodeTokenObtainPairView


urlpatterns = [
    path('v1/token/', EmailCodeTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh', EmailCodeTokenObtainPairView.as_view(), name='token_refresh'),
]
