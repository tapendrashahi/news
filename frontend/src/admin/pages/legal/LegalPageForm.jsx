import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import legalService from '../../services/legalService';
import RichTextEditor from '../../components/common/RichTextEditor';
import './LegalPageForm.css';

const LegalPageForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);
  
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm({
    defaultValues: {
      status: 'draft',
      page_type: 'privacy_policy',
    }
  });

  const [loading, setLoading] = useState(false);
  const [pageTypes, setPageTypes] = useState([]);
  const [jsonContent, setJsonContent] = useState('');
  const [jsonError, setJsonError] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState('');

  const pageTypeValue = watch('page_type');

  // Load available JSON templates from administration folder
  const jsonTemplates = {
    privacy_policy: '/administration/privacy_polity.json',
    terms_of_service: '/administration/terms_of_service.json',
    cookie_policy: '/administration/cookee.json',
    ethics_policy: '/administration/ethics_policy.json',
    editorial_guidelines: '/administration/guidemines.json',
    about: '/administration/about.json',
  };

  useEffect(() => {
    fetchPageTypes();
    if (isEdit) {
      fetchPageData();
    }
  }, [isEdit, id]);

  const fetchPageTypes = async () => {
    try {
      const data = await legalService.getPageTypes();
      setPageTypes(data.page_types || []);
    } catch (error) {
      console.error('Failed to fetch page types:', error);
    }
  };

  const fetchPageData = async () => {
    try {
      setLoading(true);
      const data = await legalService.get(id);
      
      // Set form values
      setValue('page_type', data.page_type);
      setValue('title', data.title);
      setValue('slug', data.slug);
      setValue('status', data.status);
      setValue('version', data.version);
      setValue('effective_date', data.effective_date);
      setValue('meta_description', data.meta_description || '');
      setValue('contact_email', data.contact_email || '');
      
      // Set JSON content
      setJsonContent(JSON.stringify(data.content_json, null, 2));
    } catch (error) {
      console.error('Failed to fetch page data:', error);
      toast.error('Failed to load page data');
    } finally {
      setLoading(false);
    }
  };

  const loadTemplate = async (pageType) => {
    const templatePath = jsonTemplates[pageType];
    if (!templatePath) return;

    try {
      const response = await fetch(templatePath);
      if (response.ok) {
        const json = await response.json();
        setJsonContent(JSON.stringify(json, null, 2));
        toast.success('Template loaded successfully');
      } else {
        toast.error('Template file not found');
      }
    } catch (error) {
      console.error('Failed to load template:', error);
      toast.error('Failed to load template');
    }
  };

  const handleTemplateLoad = () => {
    if (selectedTemplate) {
      loadTemplate(selectedTemplate);
    }
  };

  const validateJSON = (jsonString) => {
    try {
      JSON.parse(jsonString);
      setJsonError('');
      return true;
    } catch (error) {
      setJsonError(`Invalid JSON: ${error.message}`);
      return false;
    }
  };

  const handleJsonChange = (e) => {
    const value = e.target.value;
    setJsonContent(value);
    if (value.trim()) {
      validateJSON(value);
    } else {
      setJsonError('');
    }
  };

  const formatJSON = () => {
    try {
      const parsed = JSON.parse(jsonContent);
      setJsonContent(JSON.stringify(parsed, null, 2));
      setJsonError('');
      toast.success('JSON formatted successfully');
    } catch (error) {
      toast.error('Cannot format invalid JSON');
    }
  };

  const onSubmit = async (data) => {
    // Validate JSON content
    if (!jsonContent.trim()) {
      toast.error('JSON content is required');
      return;
    }

    if (!validateJSON(jsonContent)) {
      toast.error('Please fix JSON errors before submitting');
      return;
    }

    try {
      setLoading(true);
      
      const payload = {
        ...data,
        content_json: JSON.parse(jsonContent),
      };

      if (isEdit) {
        await legalService.update(id, payload);
        toast.success('Legal page updated successfully');
      } else {
        await legalService.create(payload);
        toast.success('Legal page created successfully');
      }
      
      navigate('/admin/legal');
    } catch (error) {
      console.error('Failed to save legal page:', error);
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.message ||
                          'Failed to save legal page';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (loading && isEdit) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading page data...</p>
      </div>
    );
  }

  return (
    <div className="legal-page-form-container">
      <div className="form-header">
        <button onClick={() => navigate('/admin/legal')} className="btn-back">
          <i className="fas fa-arrow-left"></i> Back
        </button>
        <h1>{isEdit ? 'Edit Legal Page' : 'Create New Legal Page'}</h1>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="legal-page-form">
        <div className="form-section">
          <h2>Basic Information</h2>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="page_type">
                Page Type <span className="required">*</span>
              </label>
              <select
                id="page_type"
                {...register('page_type', { required: 'Page type is required' })}
                className={errors.page_type ? 'error' : ''}
              >
                {pageTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
              {errors.page_type && <span className="error-message">{errors.page_type.message}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="status">
                Status <span className="required">*</span>
              </label>
              <select
                id="status"
                {...register('status', { required: 'Status is required' })}
                className={errors.status ? 'error' : ''}
              >
                <option value="draft">Draft</option>
                <option value="published">Published</option>
                <option value="archived">Archived</option>
              </select>
              {errors.status && <span className="error-message">{errors.status.message}</span>}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="title">
              Page Title <span className="required">*</span>
            </label>
            <input
              type="text"
              id="title"
              {...register('title', { required: 'Title is required' })}
              className={errors.title ? 'error' : ''}
              placeholder="e.g., Privacy Policy"
            />
            {errors.title && <span className="error-message">{errors.title.message}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="slug">
              URL Slug <span className="required">*</span>
            </label>
            <input
              type="text"
              id="slug"
              {...register('slug', { 
                required: 'Slug is required',
                pattern: {
                  value: /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
                  message: 'Slug must be lowercase letters, numbers, and hyphens only'
                }
              })}
              className={errors.slug ? 'error' : ''}
              placeholder="e.g., privacy-policy"
            />
            {errors.slug && <span className="error-message">{errors.slug.message}</span>}
            <small>Used in URL: /legal/{watch('slug')}</small>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="version">
                Version <span className="required">*</span>
              </label>
              <input
                type="text"
                id="version"
                {...register('version', { required: 'Version is required' })}
                className={errors.version ? 'error' : ''}
                placeholder="e.g., 1.0"
              />
              {errors.version && <span className="error-message">{errors.version.message}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="effective_date">
                Effective Date <span className="required">*</span>
              </label>
              <input
                type="date"
                id="effective_date"
                {...register('effective_date', { required: 'Effective date is required' })}
                className={errors.effective_date ? 'error' : ''}
              />
              {errors.effective_date && <span className="error-message">{errors.effective_date.message}</span>}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="meta_description">Meta Description</label>
            <textarea
              id="meta_description"
              {...register('meta_description')}
              rows="3"
              placeholder="SEO-friendly description for search engines"
            />
          </div>

          <div className="form-group">
            <label htmlFor="contact_email">Contact Email</label>
            <input
              type="email"
              id="contact_email"
              {...register('contact_email')}
              placeholder="e.g., legal@newsportal.com"
            />
          </div>
        </div>

        <div className="form-section">
          <div className="section-header">
            <h2>Page Content (JSON Structure)</h2>
            <div className="json-actions">
              <select
                value={selectedTemplate}
                onChange={(e) => setSelectedTemplate(e.target.value)}
                className="template-selector"
              >
                <option value="">Select a template...</option>
                {pageTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label} Template
                  </option>
                ))}
              </select>
              <button
                type="button"
                onClick={handleTemplateLoad}
                className="btn-secondary"
                disabled={!selectedTemplate}
              >
                <i className="fas fa-download"></i> Load Template
              </button>
              <button
                type="button"
                onClick={formatJSON}
                className="btn-secondary"
              >
                <i className="fas fa-magic"></i> Format JSON
              </button>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="content_json">
              JSON Content <span className="required">*</span>
            </label>
            <textarea
              id="content_json"
              value={jsonContent}
              onChange={handleJsonChange}
              className={`json-editor ${jsonError ? 'error' : ''}`}
              rows="20"
              placeholder='{"metadata": {...}, "sections": [...]}'
              spellCheck="false"
            />
            {jsonError && <span className="error-message">{jsonError}</span>}
            <small>
              <i className="fas fa-info-circle"></i> Enter the page content as JSON. 
              Use the template selector above to load a pre-defined structure.
            </small>
          </div>

          {jsonContent && !jsonError && (
            <div className="json-preview">
              <h3>JSON Preview</h3>
              <pre>{jsonContent}</pre>
            </div>
          )}
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={() => navigate('/admin/legal')}
            className="btn-cancel"
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn-submit"
            disabled={loading || !!jsonError}
          >
            {loading ? (
              <>
                <span className="spinner-small"></span> Saving...
              </>
            ) : (
              <>
                <i className="fas fa-save"></i> {isEdit ? 'Update Page' : 'Create Page'}
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default LegalPageForm;
