import React from 'react';
import '../styles.css';

// Tip : Always keep your components small and focused on a single responsibility.
function HomePage() {
  return (
    <div className="HomePage">
      <header className="HomePage-header">
        <h1>Welcome to the Movie Mood Recommender!</h1>
        <p>Discover movies that suit your mood. 
            Start by searching for your favorite movies 
            or pick a mood to see recommendations curated for you.</p>
        <div className="HomePage-actions">
          <button className="HomePage-button" onClick={() => 
            window.location.href = '/search'}>Search Movies</button>
          <button className="HomePage-button" onClick={() => 
            window.location.href = '/mood-recommendations'}>Recommend by Mood</button>
        </div>
      </header>
    </div>
  );
}

export default HomePage;