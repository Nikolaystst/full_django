from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models

from main_app.custom_managers import CustomAuthor


# Create your models here.
class PublishedOn(models.Model):
    published_on = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2005)])
    website = models.URLField(null=True, blank=True)

    objects = CustomAuthor()


class Article(PublishedOn):
    CATEGORY_CHOICES = (
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Education', 'Education')
    )
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0])
    authors = models.ManyToManyField(to=Author, related_name='articles')
    # published_on = models.DateTimeField(auto_now_add=True, editable=False)


class Review(PublishedOn):
    content = models.TextField(validators=[MinLengthValidator(10)])
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='reviews')
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name='reviews')
    # published_on = models.DateTimeField(auto_now_add=True, editable=False)
