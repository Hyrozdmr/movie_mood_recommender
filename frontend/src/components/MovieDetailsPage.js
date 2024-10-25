import React, { useEffect, useState} from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function MovieDetailsPage() {
    const{ id } = useParams();
    const [movieDetails, setMovieDetails] = useState(null);

    useEffect(() => {
        const fetchMovieDetails = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/movie/${id}/`);
                setMovieDetails(response.data);
            } catch (error) {
                console.error('Error fetching movie details:', error);
            }
        };
        fetchMovieDetails();
    }, [id]);

    if (!movieDetails) {
        return <div>Loading...</div>;
    }

    return (
        <div className="MovieDetailsPage">
            <h2>{movieDetails.title}</h2>
            <p>Genre: {movieDetails.genre}</p>
            <p>Mood: {movieDetails.mood}</p>
        </div>
    );
}

export default MovieDetailsPage;