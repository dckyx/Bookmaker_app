import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SpinPage from './components/SpinPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/spin" element={<SpinPage />} />
      </Routes>
    </Router>
  );
}

export default App;