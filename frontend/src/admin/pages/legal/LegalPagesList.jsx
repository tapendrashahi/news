import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import legalService from '../../services/legalService';
import './LegalPages.css';

const LegalPagesList = () => {
  const [pages, setPages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchPages();
  }, [filter]);

  const fetchPages = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filter !== 'all') {
        params.status = filter;
      }
      const data = await legalService.getAll(params);
      setPages(Array.isArray(data) ? data : data.results || []);
    } catch (error) {
      console.error('Failed to fetch legal pages:', error);
      toast.error('Failed to load legal pages');
    } finally {
      setLoading(false);
    }
  };

  const handlePublish = async (id) => {
    try {
      await legalService.publish(id);
      toast.success('Page published successfully');
      fetchPages();
    } catch (error) {
      console.error('Failed to publish page:', error);
      toast.error('Failed to publish page');
    }
  };

  const handleUnpublish = async (id) => {
    try {
      await legalService.unpublish(id);
      toast.success('Page unpublished successfully');
      fetchPages();
    } catch (error) {
      console.error('Failed to unpublish page:', error);
      toast.error('Failed to unpublish page');
    }
  };

  const handleDelete = async (id, title) => {
    if (window.confirm(`Are you sure you want to delete "${title}"?`)) {
      try {
        await legalService.delete(id);
        toast.success('Page deleted successfully');
        fetchPages();
      } catch (error) {
        console.error('Failed to delete page:', error);
        toast.error('Failed to delete page');
      }
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      published: 'status-published',
      draft: 'status-draft',
      archived: 'status-archived',
    };
    return badges[status] || 'status-draft';
  };

  return (
    <div className="legal-pages-container">
      <div className="legal-pages-header">
        <div>
          <h1>Legal Pages Management</h1>
          <p>Manage Privacy Policy, Terms of Service, and other legal/administrative pages</p>
        </div>
        <Link to="/admin/legal/create" className="btn-create">
          <i className="fas fa-plus"></i> Create New Page
        </Link>
      </div>

      <div className="legal-pages-filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Pages
        </button>
        <button
          className={`filter-btn ${filter === 'published' ? 'active' : ''}`}
          onClick={() => setFilter('published')}
        >
          Published
        </button>
        <button
          className={`filter-btn ${filter === 'draft' ? 'active' : ''}`}
          onClick={() => setFilter('draft')}
        >
          Drafts
        </button>
        <button
          className={`filter-btn ${filter === 'archived' ? 'active' : ''}`}
          onClick={() => setFilter('archived')}
        >
          Archived
        </button>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading legal pages...</p>
        </div>
      ) : pages.length === 0 ? (
        <div className="empty-state">
          <i className="fas fa-file-contract"></i>
          <h3>No Legal Pages Found</h3>
          <p>Create your first legal page to get started</p>
          <Link to="/admin/legal/create" className="btn-primary">
            Create Page
          </Link>
        </div>
      ) : (
        <div className="legal-pages-grid">
          {pages.map((page) => (
            <div key={page.id} className="legal-page-card">
              <div className="card-header">
                <div>
                  <h3>{page.title}</h3>
                  <p className="page-type">{page.page_type_display}</p>
                </div>
                <span className={`status-badge ${getStatusBadge(page.status)}`}>
                  {page.status_display}
                </span>
              </div>

              <div className="card-body">
                <div className="page-meta">
                  <div className="meta-item">
                    <i className="fas fa-link"></i>
                    <span className="slug">{page.slug}</span>
                  </div>
                  <div className="meta-item">
                    <i className="fas fa-code-branch"></i>
                    <span>Version {page.version}</span>
                  </div>
                  <div className="meta-item">
                    <i className="fas fa-calendar"></i>
                    <span>Effective: {new Date(page.effective_date).toLocaleDateString()}</span>
                  </div>
                  <div className="meta-item">
                    <i className="fas fa-clock"></i>
                    <span>Updated: {new Date(page.last_updated).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>

              <div className="card-actions">
                <Link to={`/admin/legal/${page.id}/edit`} className="btn-action btn-edit">
                  <i className="fas fa-edit"></i> Edit
                </Link>
                
                {page.status === 'draft' && (
                  <button
                    onClick={() => handlePublish(page.id)}
                    className="btn-action btn-publish"
                  >
                    <i className="fas fa-check"></i> Publish
                  </button>
                )}
                
                {page.status === 'published' && (
                  <button
                    onClick={() => handleUnpublish(page.id)}
                    className="btn-action btn-unpublish"
                  >
                    <i className="fas fa-times"></i> Unpublish
                  </button>
                )}
                
                <button
                  onClick={() => handleDelete(page.id, page.title)}
                  className="btn-action btn-delete"
                >
                  <i className="fas fa-trash"></i> Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LegalPagesList;
