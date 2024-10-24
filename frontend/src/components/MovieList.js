import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MovieList() {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/movies/')
            .then(response => setMovies(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
            <h1>Movie List</h1>
            <ul>
                {movies.map(movie => (
                    <li key={movie.id}>{movie.title} - {movie.genre} - {movie.mood}</li>
                ))}
            </ul>
        </div>
    );
}

export default MovieList;
