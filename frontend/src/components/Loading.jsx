import React from 'react';
import PropTypes from 'prop-types';
import './Loading.css';

const Loading = ({ 
  size = 'medium', 
  text = 'Loading...', 
  fullScreen = false,
  overlay = false 
}) => {
  const containerClass = `loading ${fullScreen ? 'loading--fullscreen' : ''} ${overlay ? 'loading--overlay' : ''}`;
  const spinnerClass = `loading__spinner loading__spinner--${size}`;

  return (
    <div className={containerClass}>
      <div className="loading__content">
        <div className={spinnerClass}>
          <div className="loading__spinner-circle"></div>
          <div className="loading__spinner-circle"></div>
          <div className="loading__spinner-circle"></div>
          <div className="loading__spinner-circle"></div>
        </div>
        {text && <p className="loading__text">{text}</p>}
      </div>
    </div>
  );
};

Loading.propTypes = {
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  text: PropTypes.string,
  fullScreen: PropTypes.bool,
  overlay: PropTypes.bool,
};

export default Loading;
