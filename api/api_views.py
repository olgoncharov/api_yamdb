from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmailCodeTokenObtainPairSerializer


User = get_user_model()


class EmailCodeTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailCodeTokenObtainPairSerializer


class SendConfirmationCodeView(APIView):
    http_method_names = ['post',]

    def post(self, request):
        email = request.data.get('email', '')
        if not email:
            return Response(
                data={'error': 'Не передан email'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=uuid4(),
                email=email,
                confirmation_code=uuid4()
            )
        success = send_mail(
            'Yamdb registration',
            f'Your confirmation code: {user.confirmation_code}',
            'admin@yamdb.ru',
            (email,)
        )
        if success:
            return Response(
                data={'message': 'Код выслан на email'},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'error': 'Не удалось отправить код на email'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
