from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .api_views import EmailCodeTokenObtainPairView, CategoryViewSet, GenreViewSet


v1_router = DefaultRouter()
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/token/', EmailCodeTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh', EmailCodeTokenObtainPairView.as_view(),
         name='token_refresh'),
    path('v1/', include(v1_router.urls)),
]
