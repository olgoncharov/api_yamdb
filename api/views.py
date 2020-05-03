from uuid import uuid4

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import Http404
from rest_framework import filters, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import EmailCodeTokenObtainPairSerializer, UserSerializer, CategorySerializer, GenreSerializer
from .models import Category, Genre


User = get_user_model()


class EmailCodeTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailCodeTokenObtainPairSerializer
    permission_classes = []


class SendConfirmationCodeView(APIView):
    http_method_names = ['post', ]
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


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise MethodNotAllowed(self.request.method)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise MethodNotAllowed(self.request.method)
