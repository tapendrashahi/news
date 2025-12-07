import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './OptimizedImage.css';

const OptimizedImage = ({
  src,
  alt,
  className = '',
  placeholderSrc = '/placeholder.jpg',
  loading = 'lazy',
  width,
  height,
  onLoad,
  onError,
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);

  const handleLoad = (e) => {
    setIsLoaded(true);
    if (onLoad) onLoad(e);
  };

  const handleError = (e) => {
    setHasError(true);
    if (onError) onError(e);
  };

  const imageSrc = hasError ? placeholderSrc : src;

  return (
    <div className={`optimized-image ${className}`}>
      {!isLoaded && !hasError && (
        <div className="optimized-image__placeholder">
          <div className="optimized-image__skeleton"></div>
        </div>
      )}
      <img
        src={imageSrc}
        alt={alt}
        width={width}
        height={height}
        loading={loading}
        className={`optimized-image__img ${isLoaded ? 'optimized-image__img--loaded' : ''}`}
        onLoad={handleLoad}
        onError={handleError}
      />
    </div>
  );
};

OptimizedImage.propTypes = {
  src: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
  className: PropTypes.string,
  placeholderSrc: PropTypes.string,
  loading: PropTypes.oneOf(['lazy', 'eager']),
  width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  onLoad: PropTypes.func,
  onError: PropTypes.func,
};

export default OptimizedImage;
