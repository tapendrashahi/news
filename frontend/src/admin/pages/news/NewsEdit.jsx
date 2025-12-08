import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import adminNewsService from '../../services/adminNewsService';
import api from '../../../services/api';
import './NewsForm.css';

const NewsEdit = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm();

  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const [teamMembers, setTeamMembers] = useState([]);
  const [tags, setTags] = useState([]);
  const [tagInput, setTagInput] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const [existingImageUrl, setExistingImageUrl] = useState(null);
  const [slugEdited, setSlugEdited] = useState(true); // Don't auto-generate when editing
  const [newsData, setNewsData] = useState(null);

  const titleValue = watch('title');
  const categories = adminNewsService.getCategoryChoices();
  const visibilityOptions = adminNewsService.getVisibilityChoices();

  useEffect(() => {
    fetchNewsData();
    fetchTeamMembers();
  }, [id]);

  const fetchNewsData = async () => {
    try {
      setFetching(true);
      const data = await adminNewsService.getNewsById(id);
      setNewsData(data);
      
      // Pre-populate form fields
      setValue('title', data.title);
      setValue('slug', data.slug);
      setValue('content', data.content);
      setValue('excerpt', data.excerpt || '');
      setValue('category', data.category);
      setValue('author', data.author?.id || data.author);
      setValue('meta_description', data.meta_description || '');
      setValue('visibility', data.visibility || 'public');
      
      // Handle publish date
      if (data.publish_date) {
        // Convert from "2024-12-08T10:30:00Z" to "2024-12-08T10:30"
        const dateStr = data.publish_date.slice(0, 16);
        setValue('publish_date', dateStr);
      }
      
      // Set existing image
      if (data.image) {
        setExistingImageUrl(data.image);
      }
      
      // Parse tags from comma-separated string
      if (data.tags) {
        const tagList = data.tags.split(',').map(t => t.trim()).filter(t => t);
        setTags(tagList);
      }
    } catch (error) {
      console.error('Failed to fetch news:', error);
      toast.error('Failed to load article');
      navigate('/admin/news');
    } finally {
      setFetching(false);
    }
  };

  const fetchTeamMembers = async () => {
    try {
      const response = await api.get('/admin/team/', {
        params: { page_size: 100 } // Get all team members
      });
      
      // Handle both paginated and non-paginated responses
      const members = response.data.results || response.data;
      
      // Filter only active members for the dropdown
      const activeMembers = Array.isArray(members) ? members.filter(m => m.is_active) : [];
      
      setTeamMembers(activeMembers);
    } catch (error) {
      console.error('Failed to fetch team members:', error);
      toast.error('Failed to load team members');
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast.error('Image size must be less than 5MB');
        e.target.value = ''; // Clear the input
        return;
      }
      
      // Update react-hook-form value
      setValue('image', e.target.files);
      
      // Create preview and clear existing image
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
        setExistingImageUrl(null); // Clear existing image when new one is selected
      };
      reader.readAsDataURL(file);
      
      console.log('📸 Image selected:', {
        name: file.name,
        size: file.size,
        type: file.type
      });
    }
  };

  const handleRemoveImage = () => {
    setImagePreview(null);
    setExistingImageUrl(null);
    setValue('image', null);
    const imageInput = document.getElementById('image');
    if (imageInput) imageInput.value = '';
  };

  const handleTagAdd = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const tag = tagInput.trim();
      if (tag && !tags.includes(tag)) {
        setTags([...tags, tag]);
        setTagInput('');
      }
    }
  };

  const handleTagRemove = (index) => {
    setTags(tags.filter((_, i) => i !== index));
  };

  const onSubmit = async (data) => {
    try {
      setLoading(true);

      console.log('📝 Form data received:', data);
      console.log('🖼️ Image file:', data.image?.[0]);
      console.log('🖼️ Existing image URL:', existingImageUrl);

      const formData = new FormData();
      formData.append('title', data.title);
      formData.append('slug', data.slug);
      formData.append('content', data.content);
      formData.append('excerpt', data.excerpt || '');
      formData.append('category', data.category);
      formData.append('tags', tags.join(', '));
      formData.append('author_id', data.author);
      formData.append('meta_description', data.meta_description || '');
      formData.append('visibility', data.visibility);
      
      if (data.publish_date) {
        formData.append('publish_date', data.publish_date);
      }

      // Only append image if a new one is selected
      if (data.image && data.image[0]) {
        formData.append('image', data.image[0]);
        console.log('✅ New image added to FormData:', {
          name: data.image[0].name,
          size: data.image[0].size,
          type: data.image[0].type
        });
      } else if (!existingImageUrl && !imagePreview) {
        console.log('⚠️ No image (new or existing)');
      } else {
        console.log('ℹ️ Keeping existing image:', existingImageUrl);
      }

      // Log FormData contents
      console.log('📦 FormData contents:');
      for (let [key, value] of formData.entries()) {
        if (value instanceof File) {
          console.log(`  ${key}:`, { name: value.name, size: value.size, type: value.type });
        } else {
          console.log(`  ${key}:`, value);
        }
      }

      const response = await adminNewsService.updateNews(id, formData);
      console.log('🎉 Article updated successfully:', response);
      console.log('🖼️ Image path saved:', response.image);
      
      toast.success('Article updated successfully!');
      navigate('/admin/news');
    } catch (error) {
      console.error('Error updating article:', error);
      toast.error(error.response?.data?.error || 'Failed to update article');
    } finally {
      setLoading(false);
    }
  };

  if (fetching) {
    return (
      <div className="editor-wrapper">
        <div style={{ padding: '40px', textAlign: 'center' }}>
          <div className="loading-spinner"></div>
          <p>Loading article...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="editor-wrapper">
      {/* Header */}
      <div className="editor-header">
        <div className="header-left">
          <button onClick={() => navigate('/admin/news')} className="btn-back">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"/>
            </svg>
            Back
          </button>
          <h1>Edit Article</h1>
        </div>
        <div className="header-actions">
          <button 
            type="button" 
            onClick={() => window.open(`/news/${newsData?.slug}/`, '_blank')}
            className="btn-secondary"
          >
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            Preview
          </button>
          <button type="submit" form="articleForm" className="btn-primary" disabled={loading}>
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"/>
            </svg>
            {loading ? 'Updating...' : 'Update'}
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} id="articleForm">
        <div className="editor-layout">
          {/* Main Editor Area */}
          <div className="editor-main">
            
            {/* Title */}
            <div className="form-group">
              <input 
                type="text"
                {...register('title', { 
                  required: 'Title is required',
                  minLength: { value: 10, message: 'Title must be at least 10 characters' }
                })}
                className="title-input" 
                placeholder="Article title..."
                maxLength="200"
              />
              {errors.title && <div className="error-text">{errors.title.message}</div>}
            </div>

            {/* Permalink */}
            <div className="permalink-box">
              <span className="permalink-label">URL:</span>
              <input 
                type="text"
                {...register('slug', { 
                  required: 'Slug is required',
                  pattern: {
                    value: /^[a-z0-9\-]+$/,
                    message: 'Only lowercase letters, numbers, and hyphens allowed'
                  }
                })}
                className="slug-input" 
                placeholder="article-url-slug"
              />
              {errors.slug && <div className="error-text" style={{marginTop: '4px'}}>{errors.slug.message}</div>}
              <button type="button" className="btn-edit" onClick={() => setSlugEdited(true)}>
                <svg width="12" height="12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                </svg>
              </button>
            </div>

            {/* Content Editor */}
            <div className="form-group">
              <label className="label-text">Content *</label>
              <textarea 
                {...register('content', { 
                  required: 'Content is required',
                  minLength: { value: 50, message: 'Content must be at least 50 characters' }
                })}
                className="content-textarea"
                placeholder="Start writing your content..."
                rows="15"
              />
              {errors.content && <div className="error-text">{errors.content.message}</div>}
              <div className="field-hint">
                <svg width="12" height="12" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"/>
                </svg>
                Write your article content with proper formatting
              </div>
            </div>

            {/* Excerpt */}
            <div className="form-group">
              <label className="label-text">Excerpt</label>
              <textarea 
                {...register('excerpt')}
                className="excerpt-textarea"
                rows="2"
                placeholder="Brief summary (optional)..."
                maxLength="300"
              />
              <div className="field-hint">Brief summary for article previews (max 300 chars)</div>
            </div>

            {/* SEO Meta */}
            <div className="form-group">
              <label className="label-text">
                <svg width="14" height="14" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"/>
                </svg>
                SEO Meta Description
              </label>
              <textarea 
                {...register('meta_description')}
                className="meta-textarea"
                rows="2"
                placeholder="Description for search engines..."
                maxLength="160"
              />
              <div className="field-hint">Optimal: 150-160 characters</div>
            </div>

          </div>

          {/* Compact Sidebar */}
          <div className="editor-sidebar">
            
            {/* Publish Panel */}
            <div className="panel">
              <div className="panel-header">
                <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <span>Settings</span>
              </div>
              
              <div className="panel-body">
                <div className="field-compact">
                  <label className="label-sm">Visibility</label>
                  <select {...register('visibility')} className="select-sm">
                    {visibilityOptions.map(option => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </select>
                </div>

                <div className="field-compact">
                  <label className="label-sm">Publish Date</label>
                  <input 
                    type="datetime-local"
                    {...register('publish_date')}
                    className="input-sm"
                  />
                </div>

                <div className="field-compact">
                  <label className="label-sm">Author *</label>
                  <select {...register('author', { required: 'Author is required' })} className="select-sm">
                    <option value="">Select author...</option>
                    {teamMembers.map(member => (
                      <option key={member.id} value={member.id}>
                        {member.name}
                      </option>
                    ))}
                  </select>
                  {errors.author && <div className="error-text">{errors.author.message}</div>}
                </div>
              </div>
            </div>

            {/* Category Panel */}
            <div className="panel">
              <div className="panel-header">
                <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
                </svg>
                <span>Category</span>
              </div>
              <div className="panel-body">
                <div className="radio-list">
                  {categories.map(cat => (
                    <label key={cat.value} className="radio-label">
                      <input 
                        type="radio"
                        {...register('category', { required: true })}
                        value={cat.value}
                      />
                      <span>{cat.label}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            {/* Tags Panel */}
            <div className="panel">
              <div className="panel-header">
                <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
                <span>Tags</span>
              </div>
              <div className="panel-body">
                <div className="tags-display">
                  {tags.map((tag, index) => (
                    <span key={index} className="tag-chip">
                      {tag}
                      <button type="button" className="tag-del" onClick={() => handleTagRemove(index)}>
                        <svg width="10" height="10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                      </button>
                    </span>
                  ))}
                </div>
                <input 
                  type="text"
                  className="input-sm"
                  placeholder="Add tag (press Enter)"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyDown={handleTagAdd}
                  autoComplete="off"
                />
              </div>
            </div>

            {/* Featured Image Panel */}
            <div className="panel">
              <div className="panel-header">
                <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                <span>Featured Image</span>
              </div>
              
              <div className="panel-body">
                {(imagePreview || existingImageUrl) && (
                  <div className="image-preview">
                    <img src={imagePreview || existingImageUrl} alt="Preview" />
                    <button type="button" className="image-remove" onClick={handleRemoveImage}>
                      <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </div>
                )}
                
                <label htmlFor="image" className="upload-btn">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                  </svg>
                  <span>{(imagePreview || existingImageUrl) ? 'Change' : 'Upload'}</span>
                </label>
                <input 
                  type="file"
                  id="image"
                  name="image"
                  accept="image/jpeg,image/png,image/jpg,image/webp"
                  onChange={handleImageChange}
                  style={{ display: 'none' }}
                />
                <div className="field-hint" style={{ marginTop: '8px' }}>Max 5MB, 1200×630px recommended</div>
              </div>
            </div>

          </div>
        </div>
      </form>
    </div>
  );
};

export default NewsEdit;
