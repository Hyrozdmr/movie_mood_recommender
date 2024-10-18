from django.test import TestCase
from ..models import Movie

class MovieModelTest(TestCase):

    def setUp(self):
        # Set up a sample movie object for use in tests
        self.movie = Movie.objects.create(
            title="Inception",
            genre="Sci-Fi",
            mood="Thrilling"
        )

    def test_movie_creation(self):
        """Test if the movie is created correctly with the given attributes"""
        self.assertEqual(self.movie.title, "Inception")
        self.assertEqual(self.movie.genre, "Sci-Fi")
        self.assertEqual(self.movie.mood, "Thrilling")

    def test_movie_str_method(self):
        """Test the __str__ method of the Movie model"""
        self.assertEqual(str(self.movie), "Inception")

    def test_movie_title_max_length(self):
        """Test the max_length constraint of the title field"""
        max_length = self.movie._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_movie_genre_max_length(self):
        """Test the max_length constraint of the genre field"""
        max_length = self.movie._meta.get_field('genre').max_length
        self.assertEqual(max_length, 100)

    def test_movie_mood_max_length(self):
        """Test the max_length constraint of the mood field"""
        max_length = self.movie._meta.get_field('mood').max_length
        self.assertEqual(max_length, 100)
