import csv
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drfproj.settings')
django.setup()

from player_app.models import Team,Player

# Create mock data
# teams = [
#     {'name': 'Team A', 'country': 'Country A'},
#     {'name': 'Team B', 'country': 'Country B'},
#     {'name': 'Team C', 'country': 'Country C'},
# ]

# # Create teams in the database
# for team_data in teams:
#     Team.objects.get_or_create(name=team_data['name'], country=team_data['country'])

# Example players data
players = [
    {'name': 'Player 1', 'total_goals': 10, 'total_assists': 5, 'market_value': '50m', 'team': 'Team A', 'team_country':'Country A'},
    {'name': 'Player 2', 'total_goals': 15, 'total_assists': 7, 'market_value': '70m', 'team': 'Team B', 'team_country':'Country A'},
    {'name': 'Player 3', 'total_goals': 20, 'total_assists': 10, 'market_value': '1000m', 'team': 'Team A', 'team_country':'Country D'},
]


with open('players_data.csv') as f:
    f_csv = csv.reader(f) 
    headers = next(f_csv) 
    for row in f_csv:
        #print(row)
        team, created = Team.objects.get_or_create(name=row[1], defaults={'country': row[2]})
        player = Player.objects.create(name=row[0], team=team,total_goals=row[3], total_assists=row[4],market_value=row[5])


# for player_data in players:
#     team, created = Team.objects.get_or_create(name=player_data['team'], defaults={'country': player_data['team_country']})
#     Player.objects.get_or_create(name=player_data['name'], team=team, total_goals=player_data["total_goals"],total_assists=player_data["total_assists"],market_value=player_data["market_value"])
