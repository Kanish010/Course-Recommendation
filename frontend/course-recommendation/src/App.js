import React, { useState } from 'react';
import EntryPage from './components/EntryPage';
import CampusPage from './components/CampusPage';
import Settings from './components/Settings';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [selectedCampus, setSelectedCampus] = useState(null);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleSettings = () => {
    setShowSettings(true);
  };

  const handleCloseSettings = () => {
    setShowSettings(false);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setShowSettings(false);
    setSelectedCampus(null);
  };

  const handleCampusSelection = (campus) => {
    setSelectedCampus(campus);
  };

  return (
    <div className="App">
      {!isLoggedIn ? (
        <EntryPage onLogin={handleLogin} onCampusSelect={handleCampusSelection} />
      ) : showSettings ? (
        <Settings onClose={handleCloseSettings} onLogout={handleLogout} />
      ) : (
        <CampusPage campus={selectedCampus} onSettings={handleSettings} />
      )}
    </div>
  );
}

export default App;