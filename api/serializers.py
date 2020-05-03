from django.contrib.auth import authenticate, get_user_model
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, Genre, Genre_Title, Review, Title


User = get_user_model()


class ConfirmationCodeField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'confirmation_code'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class EmailCodeTokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = ConfirmationCodeField()

    def validate(self, attrs):
        email = attrs.get('email', '')
        confirmation_code = attrs.get('confirmation_code', '')

        users = User.objects.filter(
            email=email,
            confirmation_code=confirmation_code
        )
        if users.exists():
            self.user = users.first()
            return {}

        raise exceptions.AuthenticationFailed(
            self.error_messages['no_active_account'],
            'no_active_account',
        )


    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class EmailCodeTokenObtainPairSerializer(EmailCodeTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'slug','name'
        model = Category

   # def to_representation(self, value):
   #     serializer=CategorySerializer.save(self.value)
   #     return serializer.data


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'slug','name'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genres = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all())

    # вариант с PrimaryKeyRelatedField
    # genre = serializers.PrimaryKeyRelatedField(many=True, allow_null=True,read_only=True)
    # еще такой вариант
    # genre=GenreSerializer(read_only=True, many=True)
    # category =CategorySerializer(read_only=True)
    # Если вы явно указываете реляционное поле, указывающее на ManyToManyFieldсквозную модель, обязательно установите read_only значение True.

    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=self.context['request'].title)
        rating = round(reviews.aggregate(Avg('score'), 2))
        return rating

    class Meta:
        #fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('pub_date',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['first_name', 'last_name', 'username', 'bio', 'email', 'role']
        model = User
