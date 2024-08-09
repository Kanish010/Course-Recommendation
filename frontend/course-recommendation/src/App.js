import React, { useState } from 'react';
import EntryPage from './components/EntryPage';
import CampusPage from './components/CampusPage';
import Settings from './components/Settings';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userId, setUserId] = useState(null); // Store userId after login
  const [showSettings, setShowSettings] = useState(false);

  const handleLogin = (id) => {
    setIsLoggedIn(true);
    setUserId(id); // Save userId
  };

  const handleSettings = () => {
    setShowSettings(true);
  };

  const handleCloseSettings = () => {
    setShowSettings(false);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserId(null); // Clear userId on logout
    setShowSettings(false);
  };

  return (
    <div className="App">
      {!isLoggedIn ? (
        <EntryPage onLogin={handleLogin} />
      ) : showSettings ? (
        <Settings onClose={handleCloseSettings} onLogout={handleLogout} userId={userId} />
      ) : (
        <CampusPage onSettings={handleSettings} />
      )}
    </div>
  );
}

export default App;