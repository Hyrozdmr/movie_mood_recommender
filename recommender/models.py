from django.db import models

class Movie(models.Model):
    title = models.CharField(max_lenght=200)
    genre = models.CharField(max_lenght=100)
    mood = models.CharField(max_lenght=100)

    def __str__(self):
        return self.title


# This defines a new class called Movie, which inherits from models.Model. 
# In Django, all models inherit from models.Model, 
# which is part of Django’s ORM (Object-Relational Mapping). 
# This allows Django to automatically handle interactions between the Python code and the database

# The field is a CharField, which means it will store text data.
# The max_length=200 specifies that the maximum number of characters for the movie title is 200. 
# This helps prevent excessively long titles from being stored in the database.