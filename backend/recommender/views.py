from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer
from .services import get_movie_details, get_movie_recommendations, search_movies as tmdb_search_movies
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Movie model.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

def search_movies(request):
    """
    Searches for movies using a query string from the TMDb API.
    """
    query = request.GET.get('query', '')
    if query:
        results = tmdb_search_movies(query)
        if 'error' in results:
            # Return 500 if there's an error in the API response
            return HttpResponseServerError(results['error'])
    else:
        results = []
    return JsonResponse({'results': results}, status=200)

def movie_details(request, movie_id):
    """
    Fetches movie details from the TMDb API by movie ID.
    """
    details = get_movie_details(movie_id)
    if 'error' in details:
        # Return 500 if there's an error in the API response
        return HttpResponseServerError(details['error'])
    return JsonResponse(details, status=200)

def recommend_movies(request, movie_id):
    """
    Fetches movie recommendations from the TMDb API by movie ID.
    """
    recommendations = get_movie_recommendations(movie_id)
    if 'error' in recommendations:
        # Return 500 if there's an error in the API response
        return HttpResponseServerError(recommendations['error'])
    return JsonResponse({'recommendations': recommendations}, status=200)

def recommend_movie(request):
    """
    Recommends movies via POST request, expects a movie ID in the body.
    """
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        if not movie_id:
            # Return 400 if the movie_id is missing in the POST data
            return HttpResponseBadRequest("movie_id is required.")
        recommendations = get_movie_recommendations(movie_id)
        if 'error' in recommendations:
            # Return 500 if there's an error in the API response
            return HttpResponseServerError(recommendations['error'])
        return JsonResponse({'recommendations': recommendations}, status=200)
    return JsonResponse({'error': 'Post request required'}, status=400)
