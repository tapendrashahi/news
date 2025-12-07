import React from 'react';
import { Link } from 'react-router-dom';
import './NotFound.css';

const NotFound = () => {
  return (
    <div className="not-found">
      <div className="not-found__content">
        <div className="not-found__animation">
          <span className="not-found__number">4</span>
          <span className="not-found__icon">🔍</span>
          <span className="not-found__number">4</span>
        </div>
        
        <h1 className="not-found__title">Page Not Found</h1>
        
        <p className="not-found__message">
          Oops! The page you're looking for doesn't exist or has been moved.
        </p>
        
        <div className="not-found__suggestions">
          <p className="not-found__suggestions-title">Here are some helpful links instead:</p>
          <div className="not-found__links">
            <Link to="/" className="not-found__link">
              <span className="not-found__link-icon">🏠</span>
              Home
            </Link>
            <Link to="/search" className="not-found__link">
              <span className="not-found__link-icon">🔎</span>
              Search
            </Link>
            <Link to="/about" className="not-found__link">
              <span className="not-found__link-icon">ℹ️</span>
              About
            </Link>
          </div>
        </div>
        
        <Link to="/" className="not-found__button">
          Go Back Home
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
