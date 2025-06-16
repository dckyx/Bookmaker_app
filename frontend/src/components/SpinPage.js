import React, { useState, useEffect } from 'react';
import '../assets/styles/spinpage.css';
import karol from '../assets/images/karol.jpeg';

const prizes = [0, 2, 5, 10, 20];

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function SpinPage() {
  const [spinning, setSpinning] = useState(false);
  const [result, setResult] = useState(null);
  const [roulettePosition, setRoulettePosition] = useState(0);
  const [karole, setKarole] = useState([]);
  const [karoleVisible, setKaroleVisible] = useState(true);
  const [userAuthenticated, setUserAuthenticated] = useState(true);

  const spin = async () => {
    if (spinning) return;

    setSpinning(true);

    try {
      const response = await fetch('/api/spin/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
      });

      if (response.status === 401 || response.status === 403) {
        setUserAuthenticated(false);
        setResult(null);
        setSpinning(false);
        return;
      }
      if (response.status === 200) {
        const data = await response.json();
        const prize = parseFloat(data.result);
        if (data.message === 'already') {
          setUserAuthenticated(true);
          setResult('already');
          setSpinning(false);
          return;
        }
        // animacja losowania tylko jeśli message !== 'already'
        if (data.message !== 'already') {
          setUserAuthenticated(true);

          const prizeIndex = prizes.indexOf(prize);
          const itemWidth = 120;
          const extraLoops = 4;
          const totalItems = prizes.length * extraLoops;
          const targetPosition = (totalItems + prizeIndex) * itemWidth;

          setRoulettePosition(0);

          setTimeout(() => {
            setRoulettePosition(-targetPosition);
          }, 50);

          setTimeout(() => {
            setResult(prize);
            setSpinning(false);

            const karolki = Array.from({ length: 15 }, (_, i) => ({
              id: i,
              top: Math.random() * 100 + '%',
              left: Math.random() * 100 + '%',
              delay: Math.random() * 2,
            }));
            setKarole(karolki);
            setKaroleVisible(true);

            setTimeout(() => {
              setKaroleVisible(false);
              setTimeout(() => setKarole([]), 700);
            }, 3500);
          }, 5000);
        }
      }
    } catch (error) {
      console.error('Błąd podczas spinowania:', error);
      setSpinning(false);
    }
  };

  return (
    <div className="container text-center spin-page-container">
      <h2>CODZIENNY BONUS</h2>

      <div className="roulette-container">
        <div
          className="roulette"
          style={{ transform: `translateX(${roulettePosition}px)` }}
        >
          {Array.from({ length: 7 }).map((_, loop) =>
            prizes.map((prize, i) => {
              const globalIndex = loop * prizes.length + i;
              const hue = (globalIndex * 47) % 360; // ładnie się rozkłada
              return (
                <div
                  className="prize-item"
                  key={`${loop}-${i}`}
                  style={{
                    backgroundColor: `hsl(${hue}, 85%, 70%)`,
                    font: `solid black`
                  }}
                >
                  {prize} zł
                </div>
              );
            })
          )}
        </div>
        <div className="indicator">▼</div>
      </div>

      {!userAuthenticated ? (
        <div className="alert alert-danger mt-4">
          Musisz być zalogowany, aby skorzystać z tej wspaniałej funkcjonalności.
        </div>
      ) : result === 'already' ? (
        <div className="alert alert-warning mt-4">
          Już dziś kręciłeś! Wróć jutro po więcej szczęścia.
        </div>
      ) : (
        <button className="btn btn-primary mt-4" onClick={spin} disabled={spinning}>
          SPIN
        </button>
      )}

      {!spinning && result !== null && result !== 'already' && (
        result === 0 ? (
          <div className="alert alert-warning mt-3">
            Nic nie wygrałeś...
          </div>
        ) : (
          <div className="alert alert-success mt-3">
            Gratulacje! Wylosowałeś {result} zł!!!
          </div>
        )
      )}

      {karole.map((k) => (
        <img
          key={k.id}
          src={karol}
          alt="karol"
          className={`karol-float-global ${karoleVisible ? 'show' : 'hide'}`}
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