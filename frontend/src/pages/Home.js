// src/pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => (
  <div className="container text-center mt-5">
    <h1>Strona Główna</h1>
    <Link to="/spin" className="btn btn-success mt-3">Przejdź do Koła Fortuny</Link>
  </div>
);

export default Home;