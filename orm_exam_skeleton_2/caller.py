import os
import django
from django.db.models import Q, Count

from main_app.models import TennisPlayer, Tournament, Match

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here
# Create and run your queries within functions

def get_tennis_players(search_name: str = None, search_country: str = None):
    if search_name is None and search_country is None:
        return ''

    q_1 = Q()

    if search_name is not None:
        q_1 &= Q(full_name__icontains=search_name)

    if search_country is not None:
        q_1 &= Q(country__icontains=search_country)

    tennis_players = TennisPlayer.objects.filter(q_1).order_by('ranking')

    if tennis_players.exists():
        return '\n'.join(f'Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}'
                         for player in tennis_players)
    else:
        return ''


def get_top_tennis_player():
    tennis_players = TennisPlayer.objects.get_tennis_players_by_wins_count()

    if tennis_players.exists():
        tennis_player = tennis_players.first()
        return f"Top Tennis Player: {tennis_player.full_name} with {tennis_player.cnt_wins} wins."
    else:
        return ''


def get_tennis_player_by_matches_count():
    tennis_players = (TennisPlayer.objects.annotate(cnt_matches=Count('matches')).filter(cnt_matches__gt=0).
                      order_by('-cnt_matches', 'ranking'))

    if tennis_players.exists():
        tennis_player = tennis_players.first()
        return f"Tennis Player: {tennis_player.full_name} with {tennis_player.cnt_matches} matches played."
    else:
        return ''


def get_tournaments_by_surface_type(surface: str = None):
    if surface is None:
        return ''

    q_1 = Q(surface_type__icontains=surface)

    tournaments = Tournament.objects.annotate(cnt_matches=Count('matches')).filter(q_1).order_by('-start_date')

    if tournaments.exists():
        return '\n'.join(f'Tournament: {tournament.name},'
                         f' start date: {tournament.start_date},'
                         f' matches: {tournament.cnt_matches}'
                         for tournament in tournaments)
    else:
        return ''


def get_latest_match_info():
    matches = Match.objects.prefetch_related('players').order_by('-date_played', '-id')
    if matches.exists():
        match = matches.first()
        players = match.players.order_by('full_name')
        player_1 = players.first().full_name
        player_2 = players.last().full_name
        if match.winner is None:
            winner = 'TBA'
        else:
            winner = match.winner.full_name
        return (
            f"Latest match played on: {match.date_played}, tournament: {match.tournament.name}, score: {match.score},"
            f" players: {player_1} vs {player_2}, winner: {winner},"
            f" summary: {match.summary}")
    else:
        return ''


def get_matches_by_tournament(tournament_name: str = None):
    if tournament_name is None:
        return "No matches found."

    matches = (Match.objects.select_related('tournament', 'winner').filter(tournament__name__exact=tournament_name).
               order_by('-date_played'))

    if matches.exists():
        return '\n'.join(f'Match played on: {match.date_played},'
                         f' score: {match.score}, winner:'
                         f' {"TBA" if match.winner is None else match.winner.full_name}'
                         for match in matches)
    else:
        return "No matches found."
