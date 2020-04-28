from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators
import datetime as dt

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[validators.MinValueValidator(0, message="Год должен быть больше нуля"), validators.MaxValueValidator(
        int(dt.datetime.today().year), message="Год должен быть меньше текущего")])
    genre = models.ManyToManyField(
        Genre, on_delete=models.SET_NULL, blank=True, null=True, related_name="title")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="title")
    description = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review")
    pub_date = models.DateTimeField("date of review", auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="review")


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField(
        "date of comment", auto_now_add=True, db_index=True)
