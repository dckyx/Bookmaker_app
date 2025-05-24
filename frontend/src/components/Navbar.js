import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => (
  <nav>
    <Link to="/">Strona główna</Link> |
    <Link to="/spin">Koło fortuny</Link>
  </nav>
);

export default Navbar;