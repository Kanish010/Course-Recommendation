import React from 'react';
import './CampusPage.css';

const ChooseCampus = ({ onCampusSelect }) => {
  return (
    <div className="choose-campus">
      <div className="campus okanagan" onClick={() => onCampusSelect('okanagan')}>
        <h2 className="campus-text">Okanagan</h2>
      </div>
      <div className="prompt">
        <h2>Which campus are you interested in?</h2>
      </div>
      <div className="campus vancouver" onClick={() => onCampusSelect('vancouver')}>
        <h2 className="campus-text">Vancouver</h2>
      </div>
    </div>
  );
};

export default ChooseCampus;