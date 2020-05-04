from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Review, Comment

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    review = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('pub_date',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'last_name', 'username', 'bio', 'email', 'role']
        model = User
