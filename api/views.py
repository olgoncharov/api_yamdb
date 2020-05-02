from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (
    EmailCodeTokenObtainPairSerializer,
    UserSerializer,
    TitleSerializer,
    TitleSerializerDeep
)
from .models import Title, Category, Genre

User = get_user_model()


class EmailCodeTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailCodeTokenObtainPairSerializer
    permission_classes = []


class SendConfirmationCodeView(APIView):
    http_method_names = ['post',]
    permission_classes = []

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


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    permission_classes = [IsAdmin]


class PersonalUserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    filterset_fields = ['category', 'genre', 'year', 'name']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        print(self.action)
        if self.action in ('create', 'partial_update'):
            return TitleSerializer

        return TitleSerializerDeep
