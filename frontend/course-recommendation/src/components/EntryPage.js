import React from 'react';
import LoginForm from './LoginForm';
import './EntryPage.css';

const EntryPage = ({ onLogin, onCampusSelect }) => {
  return (
    <div className="entry-page">
      <div className="campus okanagan" onClick={() => onCampusSelect('okanagan')}>
        <h2 className="campus-text">Okanagan</h2>
      </div>
      <div className="campus vancouver" onClick={() => onCampusSelect('vancouver')}>
        <h2 className="campus-text">Vancouver</h2>
      </div>
      <LoginForm onLogin={onLogin} />
    </div>
  );
};

export default EntryPage;