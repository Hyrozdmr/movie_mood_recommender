import tmdbsimple as tmdb
from django.conf import settings

tmdb.API_KEY = settings.TMDB_API_KEY

def get_movie_details(movie_id):
    movie = tmdb.Movies(movie_id)
    return movie.info()

def get_movie_recommendations(movie_id):
    movie = tmdb.Movies(movie_id)
    return movie.recommendations()

def search_movies(query):
    search = tmdb.Search()
    response = search.movie(query=query)
    return response['results']
