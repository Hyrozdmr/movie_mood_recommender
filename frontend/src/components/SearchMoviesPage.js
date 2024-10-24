import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import debounce from "lodash.debounce"; //Debounce search requests to reduce API Call.


function SearchMoviesPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const searchMovies = debounce(async (searchTerm) => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/search/', {
        params: { query: searchTerm }
      });
      setResults(response.data.results);
    } catch (error) {
      console.error('Error searching movies:', error);
    }
  }, 500); // 500ms debounce time to prevent excessive API requests.

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    if (value.trim()) {
      searchMovies(value);
    }
  };

  return (
    <div className="SearchMoviesPage">
      <input
        type="text"
        value={query}
        onChange={handleInputChange}
        placeholder="Search for movies (e.g., Inception, Avatar, The Matrix)..."
      />
      <div className="results">
        {results.map((movie) => (
          <div key={movie.id} className="movie-item">
            <Link to={`/movie/${movie.id}`}>{movie.title}</Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchMoviesPage;





















