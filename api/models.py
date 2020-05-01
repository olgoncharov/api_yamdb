from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_year, validate_score


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(unique=True)


    USER_ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Обычный пользователь'),
    ]

    confirmation_code = models.CharField(
        max_length=36,
        blank=True,
        editable=False,
        null=True,
        unique=True
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    bio = models.TextField(blank=True)

    @property
    def is_admin(self):
        return (self.role == 'admin' or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[validate_year])
    genre = models.ManyToManyField(
        Genre, blank=True, null=True, related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="titles")
    description = models.TextField()


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(validators=[validate_score])
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    pub_date = models.DateTimeField("date of review", auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews")


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField(
        "date of comment", auto_now_add=True, db_index=True)

