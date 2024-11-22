
// LandingPage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './landingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();

  const handleOptionClick = (option) => {
    switch (option) {
      case 'Water Bottle':
        navigate('/app');
        break;
      case 'Marker Pen':
        navigate('/app1');
        break;
      case 'Pamphlets':
        navigate('/app2');
        break;
      default:
        break;
    }
  };

  return (
    <div className="landing-container">
      <h1>Select an Option</h1>
      <div className="options-container">
        <div className="option-box" onClick={() => handleOptionClick('Water Bottle')}>
          Water Bottle
        </div>
        <div className="option-box" onClick={() => handleOptionClick('Marker Pen')}>
          Marker Pen
        </div>
        <div className="option-box" onClick={() => handleOptionClick('Pamphlets')}>
          Pamphlets
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
