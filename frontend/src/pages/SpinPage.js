import React, { useState } from 'react';
import '../components/SpinPage.css';
import karol from '../assets/images/karol.jpeg';

const prizes = [0, 2, 5, 10, 20];
const tickSound = new Audio('/tick.mp3');

function SpinPage() {
  const [spinning, setSpinning] = useState(false);
  const [result, setResult] = useState(null);
  const [angle, setAngle] = useState(0);
  const [karole, setKarole] = useState([]);

  const spin = () => {
    if (spinning) return;

    const prizeIndex = Math.floor(Math.random() * prizes.length);
    const prize = prizes[prizeIndex];
    const degreesPerPrize = 360 / prizes.length;
    // Obracamy koło tak, by środek wybranego segmentu znalazł się pod wskaźnikiem
    const finalAngle = 360 * 5 + (prizes.length - prizeIndex - 0.5) * degreesPerPrize;

    setSpinning(true);
    setAngle(prev => prev + finalAngle);

    const interval = setInterval(() => {
      tickSound.currentTime = 0;
      tickSound.play();
    }, 150);

    setTimeout(() => {
      clearInterval(interval);
    }, 4500);

    setTimeout(() => {
      setResult(prize);
      setSpinning(false);

      // tworzymy nową falę Karoli z fade-outem
      const karolki = Array.from({ length: 15 }, (_, i) => ({
        id: i,
        top: Math.random() * 100 + '%',
        left: Math.random() * 100 + '%',
        delay: Math.random() * 2,
      }));

      setKarole(karolki);

      // fadeout po czasie (klasa CSS zajmie się opacity)
      setTimeout(() => setKarole([]), 6000); // usuwamy dopiero po animacji
    }, 5000);
  };

  return (
    <div className="container text-center mt-5 spin-page-container">
      <h2>DAILY SPIN</h2>

      <div className="wheel-container mt-4">
        <div className="wheel" style={{ transform: `rotate(${angle}deg)` }}>
          {prizes.map((prize, index) => (
            <div
              key={index}
              className="segment"
              style={{
                transform: `rotate(${index * (360 / prizes.length)}deg)`,
                backgroundColor: `hsl(${index * 72}, 70%, 40%)`,
              }}
            >
              <span className="segment-label">{prize} zł</span>
            </div>
          ))}
        </div>
        <div className="pointer">▼</div>
      </div>

      <button
        className="btn btn-primary mt-4"
        onClick={spin}
        disabled={spinning}
      >
        SPIN
      </button>

      {result !== null && (
        <div className="alert alert-success mt-3">
          Gratulacje! Wylosowałeś {result} zł 🎉
        </div>
      )}

      {karole.map(k => (
        <img
          key={k.id}
          src={karol}
          alt="karol"
          className="karol-float"
          style={{
            top: k.top,
            left: k.left,
            animationDelay: `${k.delay}s`,
          }}
        />
      ))}
    </div>
  );
}

export default SpinPage;