import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Settings.css';

const Settings = ({ onClose, onLogout, userId }) => {
  const navigate = useNavigate();

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1>SETTINGS</h1>
      </div>
      <div className="settings-content">
        <button onClick={() => navigate('/search-history')}>View Search History</button>
        {/* Other buttons */}
        <button onClick={onClose}>Close</button>
        <button onClick={onLogout}>Logout</button>
      </div>
    </div>
  );
};

export default Settings;