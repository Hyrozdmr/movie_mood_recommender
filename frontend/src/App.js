import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import SearchMoviesPage from './components/SearchMoviesPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className='App'>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/search" element={<SearchMoviesPage />} />
        </Routes>

      </div>
    </Router>

  );
}

export default App;
