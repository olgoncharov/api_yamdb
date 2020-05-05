from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views


urlpatterns = [
    path(
        'v1/auth/token/',
        views.EmailCodeTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh',
        views.EmailCodeTokenObtainPairView.as_view(),
        name='token_refresh'
    ),
    path(
        'v1/auth/email/',
        views.SendConfirmationCodeView.as_view(),
        name='send_confirmation_code'
    ),
    path('v1/users/me/', views.PersonalUserView.as_view(), name='profile'),
]

v1_router = DefaultRouter()
v1_router.register('users', views.UsersViewSet, basename='users')

urlpatterns += [
    path('v1/', include(v1_router.urls)),
]