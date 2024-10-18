from django.test import TestCase
from unittest.mock import patch, MagicMock
from recommender.services import get_movie_details, get_movie_recommendations, search_movies, save_movie_from_tmdb
from recommender.models import Movie
from rest_framework.exceptions import ValidationError

class TmdbServiceTests(TestCase):

    @patch('recommender.services.tmdb.Movies')
    def test_get_movie_details_success(self, mock_tmdb_movies):
        """Test get_movie_details correctly fetches and returns movie details."""
        mock_movie_instance = MagicMock()
        mock_movie_instance.info.return_value = {
            'id': 27205,
            'title': 'Inception',
            'overview': 'Cobb, a skilled thief who commits corporate espionage...',
            'genres': [{'id': 28, 'name': 'Action'}, {'id': 878, 'name': 'Science Fiction'}],
            'release_date': '2010-07-15',
            'vote_average': 8.368
        }
        mock_tmdb_movies.return_value = mock_movie_instance
        result = get_movie_details(27205)

        self.assertEqual(result['id'], 27205)
        self.assertEqual(result['title'], 'Inception')

    @patch('recommender.services.tmdb.Movies')
    def test_get_movie_recommendations_success(self, mock_tmdb_movies):
        """Test get_movie_recommendations correctly fetches movie recommendations."""
        mock_movie_instance = MagicMock()
        mock_movie_instance.recommendations.return_value = {
            'results': [
                {'id': 27205, 'title': 'Inception'},
                {'id': 157336, 'title': 'Interstellar'}
            ]
        }
        mock_tmdb_movies.return_value = mock_movie_instance
        result = get_movie_recommendations(27205)

        self.assertEqual(len(result['results']), 2)
        self.assertEqual(result['results'][0]['id'], 27205)
        self.assertEqual(result['results'][1]['id'], 157336)

    @patch('recommender.services.tmdb.Search')
    def test_search_movies_success(self, mock_tmdb_search):
        """Test search_movies fetches movies based on a query string."""
        mock_search_instance = MagicMock()
        mock_search_instance.movie.return_value = {
            'results': [{'id': 157336, 'title': 'Interstellar'}]
        }
        mock_tmdb_search.return_value = mock_search_instance
        result = search_movies('Interstellar')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 157336)

class SaveMovieFromTMDbTests(TestCase):

    @patch('recommender.services.get_movie_details')
    def test_save_movie_from_tmdb_success(self, mock_get_movie_details):
        """Test saving movie details fetched from TMDb."""
        mock_get_movie_details.return_value = {
            'id': 123,
            'title': 'Inception',
            'genres': [{'id': 28, 'name': 'Action'}, {'id': 878, 'name': 'Science Fiction'}],
            'overview': 'A mind-bending thriller',
        }

        # Call the function to save movie details
        movie = save_movie_from_tmdb(123)
        
        # Check if the movie was saved correctly
        print(f"Saved movie: {movie}")

        # Retrieve the saved movie from the database
        try:
            saved_movie = Movie.objects.get(id=123)
            print(f"Saved Movie: {saved_movie}")
            self.assertEqual(saved_movie.id, 123)
            self.assertEqual(saved_movie.title, 'Inception')
            self.assertEqual(saved_movie.genre, 'Action, Science Fiction')
            self.assertEqual(saved_movie.mood, 'A mind-bending thriller')
        except Movie.DoesNotExist:
            print("Movie does not exist in the database!")
            raise

    @patch('recommender.services.get_movie_details')
    def test_save_movie_from_tmdb_validation_error(self, mock_get_movie_details):
        """Test save_movie_from_tmdb raises validation error when data is invalid."""
        mock_get_movie_details.return_value = {
            'id': 123,
            'title': '',  # Invalid title
            'genres': [{'id': 28, 'name': 'Action'}],
            'overview': 'A mind-bending thriller',
        }

        # Call the function expecting it to raise a ValidationError
        result = save_movie_from_tmdb(123)
        self.assertIn('error', result)

    @patch('recommender.services.get_movie_details')
    def test_save_movie_from_tmdb_api_failure(self, mock_get_movie_details):
        """Test save_movie_from_tmdb handles API failure correctly."""
        mock_get_movie_details.return_value = {'error': 'API failed'}

        result = save_movie_from_tmdb(123)
        self.assertEqual(result, {'error': 'Failed to fetch movie details from TMDb'})
