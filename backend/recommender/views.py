from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer
from .services import get_movie_details, get_movie_recommendations, search_movies as tmdb_search_movies
from django.http import JsonResponse


class MovieViewSet(viewsets.ModelViewSet):
    # Get all Movie objects from the database
    queryset = Movie.objects.all()
    # Use MovieSerializer for serialization/deserialization
    serializer_class = MovieSerializer

def search_movies(request):
    query = request.GET.get('query', '')
    if query:
        # search movie function from services.py
        results = tmdb_search_movies(query)
    else:
        results = []
    # Return the search results as JSON
    return JsonResponse({'results': results})

def movie_details(request, movie_id):
    details = get_movie_details(movie_id)
    return JsonResponse(details)

def recommend_movies(request, movie_id):
    recommendations = get_movie_recommendations(movie_id)
    return JsonResponse({'recommendations': recommendations})

def recommend_movie(request):
    if request.method == 'POST':
        # Get the movie ID from the POST data
        movie_id = request.POST.get('movie_id')
        # Get movie recommendations
        recommendations = get_movie_recommendations(movie_id)
        return JsonResponse({'recommendations': recommendations})
    return JsonResponse({'error': 'Post request required'}, status=400)