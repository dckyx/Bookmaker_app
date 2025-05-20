import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../assets/styles/Login.css'; // jeśli chcesz osobne style
import 'bootstrap/dist/css/bootstrap.min.css';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [errors, setErrors] = useState({});

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();

    // tutaj można dodać walidację lub wywołanie API do logowania
    if (!formData.username || !formData.password) {
      setErrors({ form: 'Wypełnij wszystkie pola!' });
    } else {
      console.log('Loguję z danymi:', formData);
      setErrors({});
      // redirect na dashboard albo wysłanie danych do backendu
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <div className="card shadow p-4" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 className="mb-4 text-center">Logowanie</h2>
        {errors.form && <div className="alert alert-danger">{errors.form}</div>}
        <form onSubmit={handleSubmit} noValidate>
          <div className="mb-3">
            <label className="form-label">Nazwa użytkownika</label>
            <input
              type="text"
              name="username"
              className="form-control"
              value={formData.username}
              onChange={handleChange}
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Hasło</label>
            <input
              type="password"
              name="password"
              className="form-control"
              value={formData.password}
              onChange={handleChange}
            />
          </div>
          <button type="submit" className="btn btn-custom w-100">Zaloguj się</button>
        </form>
        <p className="mt-3 text-center">
          Nie masz konta? <Link to="/register">Zarejestruj się</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;