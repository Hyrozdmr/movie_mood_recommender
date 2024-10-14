from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer
from django.shortcuts import render
from django.conf import settings
import tmdbsimple as tmdb
from django.http import JsonResponse

# Set the TMDb API key
tmdb.API_KEY = settings.TMDB_API_KEY

class MovieViewSet(viewsets.ModelViewSet):
    # Get all Movie objects from the database
    queryset = Movie.objects.all()
    # Use MovieSerializer for serialization/deserialization
    serializer_class = MovieSerializer

def home(request):
    # Render the home.html template
    return render(request, 'home.html')

def search_movies(request):
    query = request.GET.get('query', '')
    if query:
        # Create a TMDb Search object
        search = tmdb.Search()
        # Search for movies using the query
        response = search.movie(query=query)
        # Extract the results from the response
        results = response['results']
    else:
        results = []
    # Return the search results as JSON
    return JsonResponse({'results': results})

def movie_details(request, movie_id):
    # Create a TMDb Movies object with the given ID
    movie = tmdb.Movies(movie_id)
    # Get the movie info
    info = movie.info()
    # Get movie credits (cast and crew)
    credits = movie.credits()
    # Combine movie info and credits
    details = {**info, **credits}
    # Return the movie details as JSON
    return JsonResponse(details)

def recommend_movies(request, movie_id):
    # Create a TMDb Movies object with the given ID
    movie = tmdb.Movies(movie_id)
    # Get movie recommendations
    recommendations = movie.recommendations()
    # Extract the results from the recommendations
    results = recommendations['results']
    # Return the recommendations as JSON
    return JsonResponse({'recommendations': results})

def recommend_movie(request):
    if request.method == 'POST':
        # Get the movie ID from the POST data
        movie_id = request.POST.get('movie_id')
        # Create a TMDb Movies object with the given ID
        movie = tmdb.Movies(movie_id)
        # Get movie recommendations
        recommendations = movie.recommendations()
        # Extract the results from the recommendations
        results = recommendations['results']
        # Render the recommend.html template with the recommendations
        return render(request, 'recommend.html', {'recommendations': results})
    # If it's a GET request, just render the empty form
    return render(request, 'recommend_form.html')