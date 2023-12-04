import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Avg
from main_app.models import Author, Article


# Import your models here
# Create and run your queries within functions

def get_authors(search_name: str = None, search_email: str = None) -> str:
    if search_name is None and search_email is None:
        return ''

    q_search = Q()

    if search_name is not None:
        q_search &= Q(full_name__icontains=search_name)

    if search_email is not None:
        q_search &= Q(email__icontains=search_email)

    authors = Author.objects.filter(q_search).order_by('-full_name')
    if authors.exists():
        return '\n'.join(f'Author: {author.full_name}, email: {author.email},'
                         f' status: {"Banned" if author.is_banned else "Not Banned"}' for author in authors)
    else:
        return ''


def get_top_publisher():
    authors = Author.objects.get_authors_by_article_count()
    if authors.exists():
        author = authors[0]
        if author.count_articles == 0:
            return ''
        return f"Top Author: {author.full_name} with {author.count_articles} published articles."
    else:
        return ''

    # authors = return (self.annotate(count_articles=Count('articles')).
    #                   filter(count_articles__gt=0).order_by('-count_articles', 'email'))
    # if authors.exists():
    #     author = authors[0]
    # else:
    #     return ''
    # """if you don't want to use the method of the custom manager for the Author class use the 2nd method"""


def get_top_reviewer():
    authors = (Author.objects.annotate(count_reviews=Count('reviews')).
               filter(count_reviews__gt=0).order_by('-count_reviews', 'email'))
    if authors.exists():
        author = authors[0]
        return f'Top Reviewer: {author.full_name} with {author.count_reviews} published reviews.'
    else:
        return ''


def get_latest_article():
    articles = (Article.objects.annotate(count_reviews=Count('reviews'), avg_rating=Avg('reviews__rating')).
                order_by('published_on')).prefetch_related('authors', 'reviews')

    if articles.exists():
        article = articles.last()
        authors = ', '.join(author.full_name for author in article.authors.all().order_by('full_name'))

        return (f"The latest article is: {article.title}."
                f" Authors: {authors}."
                f" Reviewed: {article.count_reviews} times. Average Rating: {(article.avg_rating or 0):.2f}.")

    else:
        return ''


def get_top_rated_article():
    articles = (Article.objects.annotate(count_reviews=Count('reviews'), avg_rating=Avg('reviews__rating')).
                filter(avg_rating__gt=0).order_by('-avg_rating', 'title')).prefetch_related('reviews')

    if articles.exists():
        article = articles.first()
        return (f'The top-rated article is: {article.title},'
                f' with an average rating of {article.avg_rating:.2f},'
                f' reviewed {article.count_reviews} times.')

    else:
        return ''


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.prefetch_related('reviews').get(email__exact=email, is_banned=False)
    except Author.DoesNotExist:
        return "No authors banned."

    num_reviews = author.reviews.count()

    if author is not None:
        author.is_banned = True
        author.reviews.all().delete()
        author.save()
        return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."
    else:
        return "No authors banned."
