from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
#from player_app.authentication import ExpiringTokenAuthentication
from drfproj.settings import TOKEN_EXPIRE_TIME
from player_app.authentication import ExpiringTokenAuthentication
from player_app.models import Player,Team,Competition
from player_app.pagination import CustomPageNumberPag
from player_app.serializers import TeamSerializer,CompetitionSerializer,PlayerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
import pytz
from django.core.cache import cache
import datetime
from asgiref.sync import sync_to_async


class CustomAuthTokenLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        utc_now = datetime.datetime.now()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        result = Token.objects.filter(user=user, created__lt = utc_now - TOKEN_EXPIRE_TIME).delete()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
# class CustomObtainToken(APIView):
#     permission_classes = []

#     def post(self, request, *args, **kwargs):
#         token = create_custom_token(request.user)
#         return Response({'token': token.key})

# class SomeSecuredView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         return Response({'message': 'You are authenticated!'})


@authentication_classes([ExpiringTokenAuthentication])
@permission_classes([IsAuthenticated])
class GetAllPlayersView(generics.ListAPIView):
    queryset = Player.objects.all().order_by('total_goals')
    serializer_class = PlayerSerializer
    pagination_class = CustomPageNumberPag
    # def get_queryset(self):
    #     cached_players = cache.get('all_players')
    #     if not cached_players:
    #         cached_players = queryset = Player.objects.select_related('team').order_by('total_goals')
    #         cache.set('all_players', cached_players, timeout=60*15)  # Cache for 15 minutes
    #     return cached_players
    
    

@authentication_classes([ExpiringTokenAuthentication])
@permission_classes([IsAuthenticated])
class GetAllTeamsView(generics.ListAPIView):
    #permission_classes = (IsAuthenticated, )
    #print("ENTERED...")
    queryset = Team.objects.all().order_by('country')
    serializer_class = TeamSerializer
    pagination_class = CustomPageNumberPag

    # def get(self,request, *args, **kwargs):
    #     queryset = Team.objects.all().order_by('name').values()
    #     serializer = TeamSerializer(queryset,many=True)
    #     return Response(serializer.data)


@authentication_classes([ExpiringTokenAuthentication])
@permission_classes([IsAuthenticated])
class GetAllCompetitionsView(APIView):
    def get(self,request, *args, **kwargs):
        queryset = Competition.objects.all().order_by('name')
        serializer = CompetitionSerializer(queryset,many=True)
        return Response(serializer.data)




class CreateNewPlayerView(APIView):
    #permission_classes = (IsAuthenticated, )

    def post(self,request,*args,**kwargs):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

@authentication_classes([ExpiringTokenAuthentication])
@permission_classes([IsAuthenticated])
class GetPlayersByNameView(APIView):
    #permission_classes = (IsAuthenticated, )
    def get(self,request, *args, **kwargs):
        name = request.query_params.get('name')
        if name:
            queryset = Player.objects.filter(name__icontains=name)
            serializer = PlayerSerializer(queryset,many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    

@authentication_classes([ExpiringTokenAuthentication])
@permission_classes([IsAuthenticated])
class GetTeamsByNameView(APIView):
    #permission_classes = (IsAuthenticated, )
    def get(self,request,name, *args, **kwargs):
        queryset = Team.objects.filter(name__icontains=name)
        serializer = TeamSerializer(queryset,many=True)
        return Response(serializer.data)


@authentication_classes([ExpiringTokenAuthentication])
@permission_classes([IsAuthenticated])
class GetCompetitionByNameView(APIView):
    def get(self,request,name, *args, **kwargs):
        queryset = Competition.objects.filter(name__icontains=name)
        serializer = CompetitionSerializer(queryset,many=True)
        return Response(serializer.data)