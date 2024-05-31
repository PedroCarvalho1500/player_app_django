from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token as AuthToken
#from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
#python3 manage.py makemigrations
# python3 manage.py migrate
#python3 manage.py createsuperuser
# Create your models here.





class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    pass
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team,related_name='players', on_delete=models.CASCADE)
    total_goals = models.IntegerField(default=False,db_index=True)
    total_assists = models.IntegerField(default=False,db_index=True)
    market_value = models.CharField(max_length=200,db_index=True)

    def __str__(self) -> str:
        return self.name
    
    # class Meta:
    #     indexes = [models.Index(fields=['name','team','total_goals','total_assists','market_value'])]


class Competition(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    top_winner = models.ForeignKey(Team,related_name='competitions', on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return self.name


# class CustomToken(models.Model):
#     key = models.CharField(max_length=40, primary_key=True)
#     user = models.OneToOneField(AbstractBaseUser, related_name='auth_token', on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     expiration = models.DateTimeField()

#     def is_expired(self):
#         return self.expiration < timezone.now()