from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer
from django.shortcuts import render


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def home(request):
        return render(request, 'home.html')
    
    def recommend_movie(request):
        # recommendation logic 
        return render(request, 'recommend.html')
