from django.urls import path

from .api_views import EmailCodeTokenObtainPairView, SendConfirmationCodeView


urlpatterns = [
    path(
        'v1/auth/token/',
        EmailCodeTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh',
        EmailCodeTokenObtainPairView.as_view(),
        name='token_refresh'
    ),
    path(
        'v1/auth/email/',
        SendConfirmationCodeView.as_view(),
        name='send_confirmation_code'
    )
]
