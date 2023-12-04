from django.db import models
from django.db.models import Count


class CustomAuthor(models.Manager):
    def get_authors_by_article_count(self):
        return self.annotate(count_articles=Count('articles')).order_by('-count_articles', 'email')

        # return self.annotate(count_articles=Count('articles')).
        # filter(count_articles__gt=0).order_by('-count_articles', 'email')
        # """if you want to return the same method but without authors with zero articles"""
