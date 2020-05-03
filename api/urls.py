from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views


urlpatterns = [
    path('v1/users/me/', views.PersonalUserView.as_view(), name='profile'),
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
    )
]

v1_router = DefaultRouter()
v1_router.register('users', views.UsersViewSet, basename='users')
v1_router.register('titles', views.TitleViewSet, basename='titles')
v1_router.register('categories', views.CategoryViewSet)
v1_router.register('genres', views.GenreViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', views.CommentViewSet, basename='comments')


urlpatterns += [
    path('v1/', include(v1_router.urls)),
]
