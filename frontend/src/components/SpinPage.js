import React, { useState } from 'react';
import './SpinPage.css';

const prizes = [0, 2, 5, 10, 20];

function SpinPage() {
  const [spinning, setSpinning] = useState(false);
  const [result, setResult] = useState(null);
  const [angle, setAngle] = useState(0);
  const [canSpin, setCanSpin] = useState(() => {
    const lastSpin = localStorage.getItem('lastSpin');
    const today = new Date().toDateString();
    return lastSpin == today;
    // powinno być !== żeby działało
  });

  const spin = () => {
    if (!canSpin || spinning) return;

    const prizeIndex = Math.floor(Math.random() * prizes.length);
    const newAngle = 360 * 5 + prizeIndex * (360 / prizes.length);

    setSpinning(true);
    setAngle(newAngle);

    setTimeout(() => {
      setResult(prizes[prizeIndex]);
      setSpinning(false);
      setCanSpin(false);
      localStorage.setItem('lastSpin', new Date().toDateString());
    }, 4500);
  };

  return (
    <div className="container text-center mt-5">
      <h2>DAILY SPIN</h2>
      <div className="wheel-container mt-4">
        <div className="wheel" style={{ transform: `rotate(${angle}deg)` }}>
          {prizes.map((prize, index) => (
            <div
              key={index}
              className="segment"
              style={{ transform: `rotate(${index * (360 / prizes.length)}deg)` }}
            >
              {prize} zł
            </div>
          ))}
        </div>
        <div className="pointer">▼</div>
      </div>
      <button
        className="btn btn-primary mt-4"
        onClick={spin}
        disabled={!canSpin || spinning}
      >
        {canSpin ? 'SPIN' : 'koniec gamblowania'}
      </button>

      {result !== null && (
        <div className="alert alert-success mt-3">
          Gratulacje! Wylosowałeś {result} zł 🎉
        </div>
      )}
    </div>
  );
}

export default SpinPage;