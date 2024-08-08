import React, { useState } from 'react';
import EntryPage from './components/EntryPage';
import CampusPage from './components/CampusPage';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [selectedCampus, setSelectedCampus] = useState(null);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleCampusSelection = (campus) => {
    setSelectedCampus(campus);
  };

  return (
    <div className="App">
      {!isLoggedIn ? (
        <EntryPage onLogin={handleLogin} onCampusSelect={handleCampusSelection} />
      ) : (
        <CampusPage campus={selectedCampus} />
      )}
    </div>
  );
}

export default App;