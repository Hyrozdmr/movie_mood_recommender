from django.test import TestCase
from recommender.serializers import MovieSerializer
from recommender.models import Movie

class MovieSerializerTest(TestCase):

    def setUp(self):
        # Set up a sample movie object for testing serialization
        self.movie = Movie.objects.create(
            id=123,
            title="Inception",
            genre="Action, Science Fiction",
            mood="A mind-bending thriller"
        )

        # Valid data for testing deserialization
        self.valid_data = {
            'id': 124,
            'title': 'Interstellar',
            'genre': 'Science Fiction, Drama',
            'mood': 'A thrilling space exploration'
        }

        # Invalid data for testing validation errors (missing title)
        self.invalid_data = {
            'id': 125,
            'title': '',
            'genre': 'Adventure',
            'mood': 'An adventure beyond the stars'
        }

    def test_movie_serializer_serialization(self):
        """
        Test the MovieSerializer correctly serializes a Movie object.
        """
        serializer = MovieSerializer(instance=self.movie)
        data = serializer.data

        # Assert that the serialized data matches the movie object
        self.assertEqual(data['id'], self.movie.id)
        self.assertEqual(data['title'], self.movie.title)
        self.assertEqual(data['genre'], self.movie.genre)
        self.assertEqual(data['mood'], self.movie.mood)

    def test_movie_serializer_deserialization_valid(self):
        """
        Test the MovieSerializer correctly deserializes valid data.
        """
        serializer = MovieSerializer(data=self.valid_data)

        # Assert that the serializer is valid
        self.assertTrue(serializer.is_valid())

        # Save and check if the deserialized data is correct
        movie = serializer.save()
        self.assertEqual(movie.id, self.valid_data['id'])
        self.assertEqual(movie.title, self.valid_data['title'])
        self.assertEqual(movie.genre, self.valid_data['genre'])
        self.assertEqual(movie.mood, self.valid_data['mood'])

    def test_movie_serializer_deserialization_invalid(self):
        """
        Test the MovieSerializer handles invalid data correctly.
        """
        serializer = MovieSerializer(data=self.invalid_data)

        # Assert that the serializer is not valid due to the missing title
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)  # Check that there's a validation error on title
        self.assertEqual(serializer.errors['title'][0], 'This field may not be blank.')
