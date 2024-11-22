import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Import global CSS
import MainApp from './MainApp'; // Make sure to import your routing setup correctly
import reportWebVitals from './reportWebVitals'; // Optional, only use if you're interested in measuring performance

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <MainApp /> {/* Use MainApp or whichever main component handles routing */}
  </React.StrictMode>
);

reportWebVitals(); // Optional: Can be removed if performance tracking isn't needed
