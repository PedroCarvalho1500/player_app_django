from .models import Team,Player
from django.shortcuts import render, redirect
import csv
import pandas as pd


def home(request):
    with open('players.csv') as f:
        f_csv = csv.reader(f) 
        headers = next(f_csv) 
        for row in f_csv:
            print(row)
            player = Player.objects.create(name=row[0], team=row[1],total_goals=row[2], total_assists=row[3],market_value=row[4])
            #player.save()

    return (request,'<h1> CREATE PLAYERS </h1>')

    # with open('soccer_teams.csv') as f:
    #     f_csv = csv.reader(f) 
    #     headers = next(f_csv) 
    #     for row in f_csv:
    #         print(row)
    #         team = Team.objects.create(name=row[0], country=row[1])
    #         team.save()

    # return (request,'<h1> CREATE TEAMS </h1>')