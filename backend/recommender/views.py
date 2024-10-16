from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer
from .services import get_movie_details, get_movie_recommendations, search_movies as tmdb_search_movies
from django.http import JsonResponse
from django.http import HttpResponse

class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Movie model.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

def home(request):
    return HttpResponse("Welcome to the Movie Mood Recommender API!")

def search_movies(request):
    """
    Searches for movies using a query string from the TMDb API.
    """
    query = request.GET.get('query', '')
    if query:
        results = tmdb_search_movies(query)
        if isinstance(results, dict) and 'error' in results:
            return JsonResponse({'error': results['error']}, status=500)
    else:
        results = []
    return JsonResponse({'results': results}, status=200)

def movie_details(request, movie_id):
    """
    Fetches movie details from the TMDb API by movie ID.
    """
    details = get_movie_details(movie_id)
    if 'error' in details:
        return JsonResponse({'error': details['error']}, status=500)
    return JsonResponse(details, status=200)

def recommend_movies(request, movie_id):
    """
    Fetches movie recommendations from the TMDb API by movie ID.
    """
    recommendations = get_movie_recommendations(movie_id)
    if 'error' in recommendations:
        # Return JSON response in case of error
        return JsonResponse({'error': recommendations['error']}, status=500)
    return JsonResponse({'recommendations': recommendations}, status=200)

def recommend_movie(request):
    """
    Recommends movies via POST request, expects a movie ID in the body.
    """
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        if not movie_id:
            # Return 400 if the movie_id is missing in the POST data
            return JsonResponse({'error': 'movie_id is required'}, status=400)
        recommendations = get_movie_recommendations(movie_id)
        if 'error' in recommendations:
            return JsonResponse({'error': recommendations['error']}, status=500)
        return JsonResponse({'recommendations': recommendations}, status=200)
    return JsonResponse({'error': 'Post request required'}, status=400)
