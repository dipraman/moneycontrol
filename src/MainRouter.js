import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import App from './App';
import LandingPage from './landingPage'; // Ensure the import paths match your file structure

function MainRouter() {
  return (
    <Router>
      <Routes>
        {/* Route for the Landing Page */}
        <Route path="/" element={<LandingPage />} />
        
        {/* Route for the main App Page */}
        <Route path="/app" element={<App />} />
        
        {/* Navigate for unmatched routes, directing users to the landing page */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default MainRouter;