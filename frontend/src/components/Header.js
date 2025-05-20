import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/images/logo_header.jpg';
import karol from '../assets/images/karol.jpeg';
import '../assets/styles/header.css';

const Header = ({ isLoggedIn }) => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="custom-header">
      <div className="header-top">
        <div className="logo-burger">
          <Link to="/" className="logo-link">
            <img src={logo} alt="logo" className="logo" />
          </Link>
          <button className="burger-btn" onClick={() => setMenuOpen(!menuOpen)}>
            ☰
          </button>
        </div>
         <div className="header-spacer" />
        <div className="auth-buttons-top">
          {isLoggedIn ? (
            <Link to="/account" className="btn account-btn">Moje konto</Link>
          ) : (
            <>
              <Link to="/login" className="btn login-btn">Zaloguj się</Link>
              <Link to="/register" className="btn register-btn">Zarejestruj się</Link>
            </>
          )}
        </div>
      </div>

      {menuOpen && (
        <nav className="dropdown-menu">
          <Link to="/user-panel">Zakłady</Link>
          <Link to="/live">Na Żywo</Link>
          <Link to="/spin">
            <img src={karol} alt="spin" className="spin-avatar" />
          </Link>
        </nav>
      )}
    </header>
  );
};

export default Header;