import React, { useState } from 'react';
import './Settings.css';
import SearchHistoryModal from './SearchHistoryModal';

const Settings = ({ onClose, onLogout, userId }) => {
  const [showSearchHistory, setShowSearchHistory] = useState(false);

  const handleViewSearchHistory = () => {
    setShowSearchHistory(true);
  };

  const handleCloseSearchHistory = () => {
    setShowSearchHistory(false);
  };

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1>SETTINGS</h1>
      </div>
      <div className="settings-content">
        <button onClick={handleViewSearchHistory}>View Search History</button>
        <button onClick={onClose}>Close</button>
        <button onClick={onLogout}>Logout</button>
      </div>
      {showSearchHistory && (
        <SearchHistoryModal userId={userId} onClose={handleCloseSearchHistory} />
      )}
    </div>
  );
};

export default Settings;