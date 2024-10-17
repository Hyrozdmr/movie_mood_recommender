import tmdbsimple as tmdb
from django.conf import settings
from .models import Movie

# Set the TMDb API key
tmdb.API_KEY = settings.TMDB_API_KEY

def get_movie_details(movie_id):
    """Fetches movie details from TMDb by movie ID, without caching."""
    try:
        movie = tmdb.Movies(movie_id)
        movie_details = movie.info()  # Get movie details from TMDb
        return movie_details
    except Exception as e:
        # Return an error message if the API call fails
        return {'error': 'Could not fetch movie details. Please try again later.', 'details': str(e)}

def get_movie_recommendations(movie_id):
    """Fetches movie recommendations from TMDb based on the given movie ID, without caching."""
    try:
        movie = tmdb.Movies(movie_id)
        recommendations = movie.recommendations()  # Get movie recommendations
        return recommendations
    except Exception as e:
        # Return an error message if the API call fails
        return {'error': 'Could not fetch movie recommendations. Please try again later.', 'details': str(e)}

def search_movies(query):
    """Searches for movies in TMDb by a query string, without caching."""
    try:
        search = tmdb.Search()
        response = search.movie(query=query)  # Search movies by query
        return response['results']  # Return the search results
    except Exception as e:
        # Return an error message if the search fails
        return {'error': 'Could not perform search. Please try again later.', 'details': str(e)}


def save_movie_from_tmdb(movie_id):
    movie_data = get_movie_details(movie_id)
    
    if 'error' in movie_data:
        return {'error': 'Failed to fetch movie details from TMDb'}

    title = movie_data.get('title')
    genres = ', '.join([genre['name'] for genre in movie_data.get('genres', [])])
    mood = movie_data.get('overview')  # Mapping overview to mood

    movie = Movie(
        id=movie_data.get('id'),
        title=title,
        genre=genres,
        mood=mood,
    )
    movie.save()

    return movie