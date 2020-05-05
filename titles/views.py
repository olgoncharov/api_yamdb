from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import filters
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet

from titles import serializers
from users.permissions import IsAdminOrReadOnly

from .filters import TitleFilter
from .models import Category, Genre, Title

User = get_user_model()


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    filterset_fields = ['category', 'genre', 'year', 'name']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return serializers.TitleSerializer
        return serializers.TitleSerializerDeep


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
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
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise MethodNotAllowed(self.request.method)
