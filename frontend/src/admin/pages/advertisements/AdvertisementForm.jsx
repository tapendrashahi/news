import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import adminAdvertisementService from '../../services/adminAdvertisementService';
import './AdvertisementForm.css';

const AdvertisementForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  
  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm();
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(isEdit);
  const [imagePreview, setImagePreview] = useState(null);
  const [existingImageUrl, setExistingImageUrl] = useState(null);

  useEffect(() => {
    if (isEdit) {
      fetchAdvertisement();
    }
  }, [id]);

  const fetchAdvertisement = async () => {
    try {
      setFetching(true);
      const data = await adminAdvertisementService.getAdvertisement(id);
      
      // Set form values
      Object.keys(data).forEach(key => {
        if (key !== 'image') {
          setValue(key, data[key]);
        }
      });
      
      if (data.image) {
        setExistingImageUrl(data.image);
      }
    } catch (error) {
      console.error('Error fetching advertisement:', error);
      toast.error('Failed to load advertisement');
      navigate('/admin/advertisements');
    } finally {
      setFetching(false);
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setValue('image', e.target.files);
      
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
        setExistingImageUrl(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setImagePreview(null);
    setExistingImageUrl(null);
    setValue('image', null);
    document.getElementById('image').value = '';
  };

  const onSubmit = async (data) => {
    try {
      setLoading(true);

      const formData = new FormData();
      formData.append('title', data.title);
      formData.append('position', data.position);
      formData.append('size', data.size);
      formData.append('link_url', data.link_url);
      formData.append('alt_text', data.alt_text);
      formData.append('is_active', data.is_active);
      formData.append('start_date', data.start_date);
      formData.append('order', data.order || 0);
      
      if (data.end_date) {
        formData.append('end_date', data.end_date);
      }

      if (data.image && data.image[0]) {
        formData.append('image', data.image[0]);
      }

      if (isEdit) {
        await adminAdvertisementService.updateAdvertisement(id, formData);
        toast.success('Advertisement updated successfully!');
      } else {
        await adminAdvertisementService.createAdvertisement(formData);
        toast.success('Advertisement created successfully!');
      }
      
      navigate('/admin/advertisements');
    } catch (error) {
      console.error('Error saving advertisement:', error);
      toast.error(error.response?.data?.error || 'Failed to save advertisement');
    } finally {
      setLoading(false);
    }
  };

  if (fetching) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading advertisement...</p>
      </div>
    );
  }

  return (
    <div className="advertisement-form-page">
      <div className="form-header">
        <button onClick={() => navigate('/admin/advertisements')} className="btn-back">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Back
        </button>
        <h1>{isEdit ? 'Edit Advertisement' : 'New Advertisement'}</h1>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="advertisement-form">
        <div className="form-grid">
          <div className="form-section">
            <h2>Basic Information</h2>
            
            <div className="form-group">
              <label htmlFor="title">Title *</label>
              <input
                type="text"
                id="title"
                {...register('title', { required: 'Title is required' })}
                placeholder="Internal title for this advertisement"
              />
              {errors.title && <span className="error">{errors.title.message}</span>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="position">Position *</label>
                <select id="position" {...register('position', { required: true })}>
                  <option value="sidebar">Sidebar</option>
                  <option value="header">Header</option>
                  <option value="footer">Footer</option>
                  <option value="inline">Inline Content</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="size">Size *</label>
                <select id="size" {...register('size', { required: true })}>
                  <option value="300x250">Medium Rectangle (300x250)</option>
                  <option value="728x90">Leaderboard (728x90)</option>
                  <option value="160x600">Wide Skyscraper (160x600)</option>
                  <option value="300x600">Half Page (300x600)</option>
                  <option value="320x50">Mobile Banner (320x50)</option>
                  <option value="custom">Custom Size</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="link_url">Target URL *</label>
              <input
                type="url"
                id="link_url"
                {...register('link_url', { required: 'URL is required' })}
                placeholder="https://example.com"
              />
              {errors.link_url && <span className="error">{errors.link_url.message}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="alt_text">Alt Text *</label>
              <input
                type="text"
                id="alt_text"
                {...register('alt_text', { required: 'Alt text is required' })}
                placeholder="Descriptive text for accessibility"
              />
              {errors.alt_text && <span className="error">{errors.alt_text.message}</span>}
            </div>
          </div>

          <div className="form-section">
            <h2>Image</h2>
            
            <div className="form-group">
              <label htmlFor="image">Advertisement Image {!isEdit && '*'}</label>
              <input
                type="file"
                id="image"
                accept="image/*"
                onChange={handleImageChange}
              />
              {!isEdit && errors.image && <span className="error">Image is required</span>}
            </div>

            {(imagePreview || existingImageUrl) && (
              <div className="image-preview-container">
                <img
                  src={imagePreview || existingImageUrl}
                  alt="Preview"
                  className="image-preview"
                />
                <button type="button" onClick={handleRemoveImage} className="btn-remove">
                  Remove Image
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="form-grid">
          <div className="form-section">
            <h2>Schedule</h2>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="start_date">Start Date & Time *</label>
                <input
                  type="datetime-local"
                  id="start_date"
                  {...register('start_date', { required: 'Start date is required' })}
                />
                {errors.start_date && <span className="error">{errors.start_date.message}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="end_date">End Date & Time</label>
                <input
                  type="datetime-local"
                  id="end_date"
                  {...register('end_date')}
                />
                <small>Leave empty for indefinite</small>
              </div>
            </div>
          </div>

          <div className="form-section">
            <h2>Settings</h2>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="order">Display Order</label>
                <input
                  type="number"
                  id="order"
                  {...register('order')}
                  placeholder="0"
                  min="0"
                />
                <small>Lower numbers appear first</small>
              </div>

              <div className="form-group checkbox-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    {...register('is_active')}
                    defaultChecked={!isEdit}
                  />
                  <span>Active</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" onClick={() => navigate('/admin/advertisements')} className="btn-secondary">
            Cancel
          </button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Saving...' : (isEdit ? 'Update' : 'Create')} Advertisement
          </button>
        </div>
      </form>
    </div>
  );
};

export default AdvertisementForm;
