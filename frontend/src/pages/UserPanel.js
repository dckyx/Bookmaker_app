// src/pages/UserPanel.js
import React from 'react';
import '../assets/styles/UserPanel.css';

const mockZaklady = [
  { id: 1, nazwa: 'Mecz 1', stawka: 50, status: 'Wygrany' },
  { id: 2, nazwa: 'Mecz 2', stawka: 20, status: 'Przegrany' },
];

const mockTransakcje = [
  { id: 1, typ: 'Wpłata', wartosc: 100, data: '2025-05-18 12:00' },
  { id: 2, typ: 'Wypłata', wartosc: 50, data: '2025-05-19 09:30' },
];

const UserPanel = () => {
  const username = 'JanKowalski';
  const saldo = 130;

  return (
    <div className="container mt-5 pt-5">
      <div className="custom-card p-4">
        <h1 className="mb-4 text-center">Witaj, {username}!</h1>
        <h2 className="mb-3 text-center">💰 Saldo: {saldo} zł</h2>

        <div className="d-flex flex-column align-items-center mb-4 gap-3">
          <a href="/deposit" className="btn btn-danger w-100">💸 Wpłata</a>
          <a href="/withdraw" className="btn btn-danger w-100">🏧 Wypłata</a>
        </div>

        <h3>🎯 Twoje zakłady:</h3>
        <ul className="list-group mb-4">
          {mockZaklady.length > 0 ? (
            mockZaklady.map(z => (
              <li key={z.id} className="list-group-item bg-transparent text-dark border-light" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
                <strong>{z.nazwa}</strong><br />
                Stawka: {z.stawka} zł<br />
                Status: {z.status}
              </li>
            ))
          ) : (
            <li className="list-group-item bg-transparent text-dark border-light">Nie masz żadnych zakładów.</li>
          )}
        </ul>

        <h3>📜 Twoje transakcje:</h3>
        <ul className="list-group">
          {mockTransakcje.length > 0 ? (
            mockTransakcje.map(t => (
              <li key={t.id} className="list-group-item bg-transparent text-dark border-light" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
                {t.typ} – Kwota: {t.wartosc} zł – Data: {t.data}
              </li>
            ))
          ) : (
            <li className="list-group-item bg-transparent text-dark border-light">Brak transakcji.</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default UserPanel;