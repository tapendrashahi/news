import { useState, useEffect } from 'react';
import advertisementService from '../services/advertisementService';
import './Advertisement.css';

const Advertisement = ({ position = 'sidebar' }) => {
  const [ads, setAds] = useState([]);
  const [currentAdIndex, setCurrentAdIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAds = async () => {
      try {
        const response = await advertisementService.getAdvertisements(position);
        console.log('Advertisement API response:', response);
        console.log('Position requested:', position);
        
        // Handle both paginated and non-paginated responses
        const adsData = response.results || response.data || response;
        console.log('Processed ads data:', adsData);
        
        setAds(Array.isArray(adsData) ? adsData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching advertisements:', error);
        console.error('Error response:', error.response);
        setLoading(false);
      }
    };

    fetchAds();
  }, [position]);

  useEffect(() => {
    if (Array.isArray(ads) && ads.length > 0 && currentAdIndex < ads.length) {
      const currentAd = ads[currentAdIndex];
      advertisementService.trackImpression(currentAd.id).catch(error => {
        console.error('Error tracking impression:', error);
      });
    }
  }, [ads, currentAdIndex]);

  useEffect(() => {
    if (Array.isArray(ads) && ads.length > 1) {
      const interval = setInterval(() => {
        setCurrentAdIndex((prevIndex) => (prevIndex + 1) % ads.length);
      }, 10000); // Rotate every 10 seconds

      return () => clearInterval(interval);
    }
  }, [ads]);

  const handleAdClick = async (ad) => {
    try {
      await advertisementService.trackClick(ad.id);
      if (ad.link_url) {
        window.open(ad.link_url, '_blank', 'noopener,noreferrer');
      }
    } catch (error) {
      console.error('Error tracking click:', error);
    }
  };

  if (loading) {
    return (
      <div className="advertisement advertisement--loading">
        <div className="advertisement__skeleton"></div>
      </div>
    );
  }

  if (!Array.isArray(ads) || !ads.length) {
    return null;
  }

  const currentAd = ads[currentAdIndex];

  return (
    <div className={`advertisement advertisement--${position}`}>
      <div className="advertisement__label">Advertisement</div>
      <div
        className="advertisement__content"
        onClick={() => handleAdClick(currentAd)}
        role="button"
        tabIndex={0}
        onKeyPress={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            handleAdClick(currentAd);
          }
        }}
        aria-label={currentAd.alt_text || currentAd.title}
      >
        <img
          src={currentAd.image}
          alt={currentAd.alt_text || currentAd.title}
          className="advertisement__image"
        />
        {currentAd.title && (
          <div className="advertisement__title">{currentAd.title}</div>
        )}
      </div>
      {ads.length > 1 && (
        <div className="advertisement__dots">
          {ads.map((_, index) => (
            <button
              key={index}
              className={`advertisement__dot ${
                index === currentAdIndex ? 'advertisement__dot--active' : ''
              }`}
              onClick={() => setCurrentAdIndex(index)}
              aria-label={`View advertisement ${index + 1}`}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Advertisement;
