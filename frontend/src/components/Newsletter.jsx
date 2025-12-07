import React, { useState } from 'react';
import { useSubscribe } from '../hooks';
import './Newsletter.css';

const Newsletter = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState({ text: '', type: '' });
  const subscribeMutation = useSubscribe();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email.trim()) {
      setMessage({ text: 'Please enter your email', type: 'error' });
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setMessage({ text: 'Please enter a valid email', type: 'error' });
      return;
    }

    try {
      await subscribeMutation.mutateAsync(email);
      setMessage({ text: 'Successfully subscribed to newsletter!', type: 'success' });
      setEmail('');
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to subscribe. Please try again.';
      setMessage({ text: errorMessage, type: 'error' });
    }
  };

  return (
    <div className="newsletter">
      <div className="newsletter__content">
        <h3 className="newsletter__title">📰 Subscribe to Newsletter</h3>
        <p className="newsletter__description">
          Get the latest news delivered directly to your inbox.
        </p>
        
        <form className="newsletter__form" onSubmit={handleSubmit}>
          <input
            type="email"
            className="newsletter__input"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={subscribeMutation.isLoading}
          />
          <button 
            type="submit" 
            className="newsletter__button"
            disabled={subscribeMutation.isLoading}
          >
            {subscribeMutation.isLoading ? 'Subscribing...' : 'Subscribe'}
          </button>
        </form>

        {message.text && (
          <p className={`newsletter__message newsletter__message--${message.type}`}>
            {message.text}
          </p>
        )}
      </div>
    </div>
  );
};

export default Newsletter;
