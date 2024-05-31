from django.contrib import admin
from django.urls import path,include
from .views import CustomAuthTokenLogin,CreateNewPlayerView,GetAllPlayersView,GetPlayersByNameView,GetAllTeamsView,GetTeamsByNameView,GetAllCompetitionsView,GetCompetitionByNameView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/',include('rest_framework.urls')),
    path('get_all_players/', GetAllPlayersView.as_view(), name='test'),
    path('get_player_name/', GetPlayersByNameView.as_view(), name='get_player_by_name'),
    path('create_player', CreateNewPlayerView.as_view(), name='create_player'),
    path('get_all_teams', GetAllTeamsView.as_view(), name='get_all_teams'),
    path('get_team_name/<str:name>', GetTeamsByNameView.as_view(), name='get_player_by_name'),
    path('get_all_competitions', GetAllCompetitionsView.as_view(), name='get_all_competitions'),
    path('get_competition_name/<str:name>', GetCompetitionByNameView.as_view(), name='get_competition_by_name'),
    path('', include('player_app.urls')),
    path('api-token-auth/', CustomAuthTokenLogin.as_view())
]
