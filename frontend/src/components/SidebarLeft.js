import React, { useEffect, useState } from 'react';

const Sidebar = () => {
  const [dyscypliny, setDyscypliny] = useState([]);

useEffect(() => {
  fetch('http://localhost:8000/api/dyscypliny/')
    .then(res => res.json())
    .then(data => setDyscypliny(data))
    .catch(err => console.error('Błąd ładowania dyscyplin:', err));
}, []);

  return (
    <aside className="left-panel" style={{ height: '100vh', overflowY: 'auto' }}>
      {dyscypliny.length > 0 ? (
        dyscypliny.map((d, i) => (
          <button key={i} className="btn btn-lg btn-custom link_but_button w-100 mb-2">
            {d}
          </button>
        ))
      ) : (
        <p className="text-muted px-2">Brak dostępnych dyscyplin.</p>
      )}
    </aside>
  );
};

export default Sidebar;