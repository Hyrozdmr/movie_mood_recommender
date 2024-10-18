from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

class MovieViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_home_view(self):
        """
        Test the home view.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Welcome to the Movie Mood Recommender API!")

    @patch('recommender.views.tmdb_search_movies')
    def test_search_movies(self, mock_search):
        """
        Test the search_movies view with a query parameter.
        """
        mock_search.return_value = [{"title": "Inception", "id": 123}]
        response = self.client.get(reverse('search_movies'), {'query': 'Inception'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'results': [{"title": "Inception", "id": 123}]})
    
    @patch('recommender.views.tmdb_search_movies')
    def test_search_movies_no_query(self, mock_search):
        """
        Test search_movies view with no query (should return empty results).
        """
        response = self.client.get(reverse('search_movies'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'results': []})

    @patch('recommender.views.get_movie_details')
    def test_movie_details(self, mock_get_movie_details):
        """
        Test movie_details view.
        """
        mock_get_movie_details.return_value = {"title": "Inception", "id": 123}
        response = self.client.get(reverse('movie_details', args=[123]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"title": "Inception", "id": 123})

    @patch('recommender.views.get_movie_details')
    def test_movie_details_error(self, mock_get_movie_details):
        """
        Test movie_details view when an error is returned.
        """
        mock_get_movie_details.return_value = {"error": "Movie not found"}
        response = self.client.get(reverse('movie_details', args=[999]))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Movie not found"})

    @patch('recommender.views.get_movie_recommendations')
    def test_recommend_movies(self, mock_get_recommendations):
        """
        Test recommend_movies view.
        """
        mock_get_recommendations.return_value = [{"title": "Interstellar", "id": 456}]
        response = self.client.get(reverse('recommend_movies', args=[123]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'recommendations': [{"title": "Interstellar", "id": 456}]})

    @patch('recommender.views.get_movie_recommendations')
    def test_recommend_movies_error(self, mock_get_recommendations):
        """
        Test recommend_movies view when an error is returned.
        """
        mock_get_recommendations.return_value = {"error": "Recommendations not available"}
        response = self.client.get(reverse('recommend_movies', args=[999]))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Recommendations not available"})

    @patch('recommender.views.get_movie_recommendations')
    def test_recommend_movie_post(self, mock_get_recommendations):
        """
        Test recommend_movie view with a POST request.
        """
        mock_get_recommendations.return_value = [{"title": "Interstellar", "id": 456}]
        response = self.client.post(reverse('recommend_movie'), {'movie_id': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'recommendations': [{"title": "Interstellar", "id": 456}]})

    def test_recommend_movie_missing_movie_id(self):
        """
        Test recommend_movie view with POST request missing movie_id.
        """
        response = self.client.post(reverse('recommend_movie'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'movie_id is required'})

    def test_recommend_movie_invalid_method(self):
        """
        Test recommend_movie view with a GET request (expecting POST).
        """
        response = self.client.get(reverse('recommend_movie'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Post request required'})
