"""
URL configuration for movie_mood_recommender project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recommender import views

# a router and reegister MovieViewSets with it.
router = DefaultRouter()
router.register(r'movies', views.MovieViewSet, basename='movie')

urlpatterns = [
    # django admin route
    path('admin/', admin.site.urls),

    # API routes  
    path('api/', include(router.urls)), # Registers the viewset for MovieViewSet

    # Custom search and recommendation routes

     # Search movies from TMDb API
    path('api/search/', views.search_movies, name='search_movies'),
    # Get movie details from TMDb API
    path('api/movie/<int:movie_id>/', views.movie_details, name='movie_details'),
    # Recommend movies from TMDb API
    path('api/movie/<int:movie_id>/recommend/', views.recommend_movies, name='recommend_movies'),
    # Recommend movies via POST request
    path('api/movie/recommend/', views.recommend_movie, name='recommend_movie'),
]

