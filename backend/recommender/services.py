import tmdbsimple as tmdb
from django.conf import settings
from django.core.cache import cache

# Set the TMDb API key
tmdb.API_KEY = settings.TMDB_API_KEY

def get_movie_details(movie_id):
    """Fetches and caches movie details from TMDb by movie ID."""
    cache_key = f'movie_details_{movie_id}'
    movie_details = cache.get(cache_key)
    
    if movie_details is None:
        try:
            movie = tmdb.Movies(movie_id)
            movie_details = movie.info()  # Get movie details from TMDb
            cache.set(cache_key, movie_details, timeout=60*60)  # Cache for 1 hour
        except Exception as e:
            # Return an error message if the API call fails
            return {'error': 'Could not fetch movie details. Please try again later.', 'details': str(e)}
    
    return movie_details

def get_movie_recommendations(movie_id):
    """Fetches movie recommendations from TMDb based on the given movie ID."""
    try:
        movie = tmdb.Movies(movie_id)
        recommendations = movie.recommendations()  # Get movie recommendations
        return recommendations
    except Exception as e:
        # Return an error message if the API call fails
        return {'error': 'Could not fetch movie recommendations. Please try again later.', 'details': str(e)}

def search_movies(query):
    """Searches for movies in TMDb by a query string."""
    try:
        search = tmdb.Search()
        response = search.movie(query=query)  # Search movies by query
        return response['results']  # Return the search results
    except Exception as e:
        # Return an error message if the search fails
        return {'error': 'Could not perform search. Please try again later.', 'details': str(e)}
