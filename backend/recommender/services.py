import tmdbsimple as tmdb
from django.conf import settings
from .models import Movie
from .serializers import MovieSerializer
import logging
from rest_framework.exceptions import ValidationError

# Set the TMDb API key
tmdb.API_KEY = settings.TMDB_API_KEY

def handle_tmdb_errors(func):
    """Decorator to handle TMDb API errors and provide consistent error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"TMDB API Error: {e}")
            return {'error': 'Failed to perform the operation. Please try again later.', 'details': str(e)}
    return wrapper 

@handle_tmdb_errors
def get_movie_details(movie_id):
    """Fetches movie details from TMDb by movie ID"""
    movie = tmdb.Movies(movie_id)
    movie_details = movie.info()  # Get movie details from TMDb
    return movie_details

@handle_tmdb_errors
def get_movie_recommendations(movie_id):
    """Fetches movie recommendations from TMDb based on the given movie ID"""
    movie = tmdb.Movies(movie_id)
    recommendations = movie.recommendations()  # Get movie recommendations
    return recommendations

@handle_tmdb_errors
def search_movies(query):
    """Searches for movies in TMDb by a query string"""
    search = tmdb.Search()
    response = search.movie(query=query)  # Search movies by query
    return response['results']  # Return the search results

@handle_tmdb_errors
def save_movie_from_tmdb(movie_id):
    """Fetches movie details from TMDb and saves them into the database."""
    movie_data = get_movie_details(movie_id)
    
    if 'error' in movie_data:
        return {'error': 'Failed to fetch movie details from TMDb'}

    # Extract movie data and map to model fields
    mapped_data = {
        'id': movie_data.get('id'),
        'title': movie_data.get('title'),
        'genre': ', '.join([genre['name'] for genre in movie_data.get('genres', [])]),
        'mood': movie_data.get('overview'),  # Mapping overview to mood
    }

    print(f"Mapped Data: {mapped_data}")
    # Use the MovieSerializer to validate and save the data
    serializer = MovieSerializer(data=mapped_data)
    if serializer.is_valid():
        movie = serializer.save()
        print(f"Movie saved: {movie}")  # Debugging: Check if the movie is saved
        print(f"Movie ID: {movie.id}, Title: {movie.title}")
        return movie
    else:
        logging.error(f"Validation Error: {serializer.errors}")
        raise ValidationError(serializer.errors)  # Raise ValidationError if it fails