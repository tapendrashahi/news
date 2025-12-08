import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import adminTeamService from '../../services/adminTeamService';
import './TeamForm.css';

const TeamEdit = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue, formState: { errors } } = useForm();

  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const [photoPreview, setPhotoPreview] = useState(null);
  const [existingPhotoUrl, setExistingPhotoUrl] = useState(null);

  const roleChoices = adminTeamService.getRoleChoices();

  useEffect(() => {
    fetchMemberData();
  }, [id]);

  const fetchMemberData = async () => {
    try {
      setFetching(true);
      const data = await adminTeamService.getTeamMemberById(id);
      
      // Pre-populate form fields
      setValue('name', data.name);
      setValue('role', data.role);
      setValue('bio', data.bio || '');
      setValue('email', data.email || '');
      setValue('twitter_url', data.twitter_url || '');
      setValue('linkedin_url', data.linkedin_url || '');
      setValue('order', data.order || 0);
      setValue('is_active', data.is_active);
      
      // Set existing photo
      if (data.photo) {
        setExistingPhotoUrl(data.photo);
      }
    } catch (error) {
      console.error('Failed to fetch team member:', error);
      toast.error('Failed to load team member');
      navigate('/admin/team');
    } finally {
      setFetching(false);
    }
  };

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast.error('Photo size must be less than 5MB');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result);
        setExistingPhotoUrl(null); // Clear existing photo when new one is selected
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemovePhoto = () => {
    setPhotoPreview(null);
    setExistingPhotoUrl(null);
    const photoInput = document.getElementById('photo');
    if (photoInput) photoInput.value = '';
  };

  const onSubmit = async (data) => {
    try {
      setLoading(true);

      const formData = new FormData();
      formData.append('name', data.name);
      formData.append('role', data.role);
      formData.append('bio', data.bio || '');
      formData.append('email', data.email || '');
      formData.append('twitter_url', data.twitter_url || '');
      formData.append('linkedin_url', data.linkedin_url || '');
      formData.append('order', data.order || 0);
      formData.append('is_active', data.is_active);

      // Only append photo if a new one is selected
      if (data.photo && data.photo[0]) {
        formData.append('photo', data.photo[0]);
      }

      await adminTeamService.updateTeamMember(id, formData);
      toast.success('Team member updated successfully!');
      navigate('/admin/team');
    } catch (error) {
      console.error('Error updating team member:', error);
      toast.error(error.response?.data?.error || 'Failed to update team member');
    } finally {
      setLoading(false);
    }
  };

  if (fetching) {
    return (
      <div className="team-form-wrapper">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading team member...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="team-form-wrapper">
      {/* Header */}
      <div className="team-form-header">
        <div className="header-left">
          <button onClick={() => navigate('/admin/team')} className="btn-back">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"/>
            </svg>
            Back
          </button>
          <h1>Edit Team Member</h1>
        </div>
        <div className="header-actions">
          <button type="submit" form="teamForm" className="btn-primary" disabled={loading}>
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"/>
            </svg>
            {loading ? 'Updating...' : 'Update Member'}
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} id="teamForm">
        <div className="team-form-container">
          
          {/* Photo Upload */}
          <div className="form-card">
            <h2 className="form-section-title">Profile Photo</h2>
            <div className="photo-upload-section">
              {(photoPreview || existingPhotoUrl) ? (
                <div className="photo-preview">
                  <img src={photoPreview || existingPhotoUrl} alt="Preview" />
                  <button type="button" className="photo-remove" onClick={handleRemovePhoto}>
                    <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
              ) : (
                <div className="photo-preview">
                  <div className="photo-placeholder">
                    <svg width="64" height="64" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd"/>
                    </svg>
                  </div>
                </div>
              )}

              <label htmlFor="photo" className="upload-btn">
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                </svg>
                <span>{(photoPreview || existingPhotoUrl) ? 'Change Photo' : 'Upload Photo'}</span>
              </label>
              <input 
                type="file"
                id="photo"
                {...register('photo')}
                accept="image/jpeg,image/png,image/jpg,image/webp"
                onChange={handlePhotoChange}
                style={{ display: 'none' }}
              />
              <span className="upload-hint">Max 5MB, square images recommended</span>
            </div>
          </div>

          {/* Basic Information */}
          <div className="form-card">
            <h2 className="form-section-title">Basic Information</h2>
            
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">
                  Full Name<span className="required-star">*</span>
                </label>
                <input 
                  type="text"
                  {...register('name', { 
                    required: 'Name is required',
                    minLength: { value: 2, message: 'Name must be at least 2 characters' }
                  })}
                  className={`form-input ${errors.name ? 'error' : ''}`}
                  placeholder="John Doe"
                  maxLength="100"
                />
                {errors.name && <span className="error-text">{errors.name.message}</span>}
              </div>

              <div className="form-group">
                <label className="form-label">
                  Role<span className="required-star">*</span>
                </label>
                <select 
                  {...register('role', { required: 'Role is required' })}
                  className={`form-select ${errors.role ? 'error' : ''}`}
                >
                  <option value="">Select role...</option>
                  {roleChoices.map(choice => (
                    <option key={choice.value} value={choice.value}>
                      {choice.label}
                    </option>
                  ))}
                </select>
                {errors.role && <span className="error-text">{errors.role.message}</span>}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Email</label>
              <input 
                type="email"
                {...register('email', {
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address'
                  }
                })}
                className={`form-input ${errors.email ? 'error' : ''}`}
                placeholder="john@example.com"
              />
              {errors.email && <span className="error-text">{errors.email.message}</span>}
            </div>

            <div className="form-group">
              <label className="form-label">Bio</label>
              <textarea 
                {...register('bio')}
                className="form-textarea"
                placeholder="Brief description about the team member..."
                rows="4"
              />
              <span className="field-hint">A short bio will be displayed on the team page</span>
            </div>
          </div>

          {/* Social Links */}
          <div className="form-card">
            <h2 className="form-section-title">Social Media</h2>
            
            <div className="form-group">
              <label className="form-label">Twitter/X URL</label>
              <input 
                type="url"
                {...register('twitter_url', {
                  pattern: {
                    value: /^https?:\/\/.+/,
                    message: 'Must be a valid URL starting with http:// or https://'
                  }
                })}
                className={`form-input ${errors.twitter_url ? 'error' : ''}`}
                placeholder="https://twitter.com/username"
              />
              {errors.twitter_url && <span className="error-text">{errors.twitter_url.message}</span>}
            </div>

            <div className="form-group">
              <label className="form-label">LinkedIn URL</label>
              <input 
                type="url"
                {...register('linkedin_url', {
                  pattern: {
                    value: /^https?:\/\/.+/,
                    message: 'Must be a valid URL starting with http:// or https://'
                  }
                })}
                className={`form-input ${errors.linkedin_url ? 'error' : ''}`}
                placeholder="https://linkedin.com/in/username"
              />
              {errors.linkedin_url && <span className="error-text">{errors.linkedin_url.message}</span>}
            </div>
          </div>

          {/* Settings */}
          <div className="form-card">
            <h2 className="form-section-title">Settings</h2>
            
            <div className="form-group">
              <label className="form-label">Display Order</label>
              <input 
                type="number"
                {...register('order')}
                className="form-input"
                placeholder="0"
                min="0"
              />
              <span className="field-hint">Lower numbers appear first</span>
            </div>

            <div className="checkbox-group">
              <input 
                type="checkbox"
                id="is_active"
                {...register('is_active')}
              />
              <label htmlFor="is_active">Active (visible on website)</label>
            </div>
          </div>

        </div>
      </form>
    </div>
  );
};

export default TeamEdit;
