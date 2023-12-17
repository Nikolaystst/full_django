from django.db import models
from django.db.models import Count


class CustomTennisPlayer(models.Manager):
    def get_tennis_players_by_wins_count(self):
        return self.annotate(cnt_wins=Count('matches_won')).order_by('-cnt_wins', 'full_name')
