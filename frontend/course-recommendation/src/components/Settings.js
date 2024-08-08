import React from 'react';
import './Settings.css';

const Settings = ({ onClose, onLogout }) => {
  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1>SETTINGS</h1>
        <button onClick={onClose}>Close</button>
      </div>
      <div className="settings-content">
        <button>Manage Favorites</button>
        <button>Set Preferences</button>
        <button>View Search History</button>
        <button onClick={onLogout}>Logout</button>
      </div>
    </div>
  );
};

export default Settings;