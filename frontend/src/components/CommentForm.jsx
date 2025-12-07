import React, { useState } from 'react';
import './CommentForm.css';

const CommentForm = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    text: '',
  });
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }

    if (!formData.text.trim()) {
      newErrors.text = 'Comment text is required';
    } else if (formData.text.trim().length < 10) {
      newErrors.text = 'Comment must be at least 10 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      await onSubmit(formData);
      // Reset form on successful submission
      setFormData({ name: '', email: '', text: '' });
      setErrors({});
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <form className="comment-form" onSubmit={handleSubmit}>
      <h3 className="comment-form__title">Leave a Comment</h3>
      
      <div className="comment-form__row">
        <div className="comment-form__field">
          <label htmlFor="name" className="comment-form__label">
            Name *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            className={`comment-form__input ${errors.name ? 'comment-form__input--error' : ''}`}
            value={formData.name}
            onChange={handleChange}
            disabled={isLoading}
          />
          {errors.name && <span className="comment-form__error">{errors.name}</span>}
        </div>

        <div className="comment-form__field">
          <label htmlFor="email" className="comment-form__label">
            Email *
          </label>
          <input
            type="email"
            id="email"
            name="email"
            className={`comment-form__input ${errors.email ? 'comment-form__input--error' : ''}`}
            value={formData.email}
            onChange={handleChange}
            disabled={isLoading}
          />
          {errors.email && <span className="comment-form__error">{errors.email}</span>}
        </div>
      </div>

      <div className="comment-form__field">
        <label htmlFor="text" className="comment-form__label">
          Comment *
        </label>
        <textarea
          id="text"
          name="text"
          className={`comment-form__textarea ${errors.text ? 'comment-form__input--error' : ''}`}
          rows="5"
          value={formData.text}
          onChange={handleChange}
          disabled={isLoading}
        ></textarea>
        {errors.text && <span className="comment-form__error">{errors.text}</span>}
      </div>

      <button 
        type="submit" 
        className="comment-form__submit"
        disabled={isLoading}
      >
        {isLoading ? 'Submitting...' : 'Post Comment'}
      </button>
    </form>
  );
};

export default CommentForm;
