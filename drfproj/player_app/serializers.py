from rest_framework import serializers
from .models import Player,Team,Competition


    # class Meta:
    #     indexes = [models.Index(fields=['name','team','total_goals','total_assists','market_value'])]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'name','country'
        )

class PlayerSerializer(serializers.ModelSerializer):
    team  = TeamSerializer(read_only=True)
    class Meta:
        model = Player
        fields = (
            'name','team','total_goals','total_assists','market_value'
        )

class CompetitionSerializer(serializers.ModelSerializer):
    top_winner = TeamSerializer(read_only=True)
    class Meta:
        model = Competition
        fields = ('name','country','top_winner')
        