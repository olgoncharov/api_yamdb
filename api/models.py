from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_year, validate_score


User = get_user_model()


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
