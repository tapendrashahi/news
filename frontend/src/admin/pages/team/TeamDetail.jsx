import { useState, useEffect } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import adminTeamService from '../../services/adminTeamService';
import './TeamDetail.css';

const TeamDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [member, setMember] = useState(null);
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMemberData();
    fetchMemberArticles();
  }, [id]);

  const fetchMemberData = async () => {
    try {
      const data = await adminTeamService.getTeamMemberById(id);
      setMember(data);
    } catch (error) {
      console.error('Failed to fetch team member:', error);
      toast.error('Failed to load team member');
      navigate('/admin/team');
    } finally {
      setLoading(false);
    }
  };

  const fetchMemberArticles = async () => {
    try {
      const data = await adminTeamService.getMemberArticles(id);
      setArticles(data.results || data);
    } catch (error) {
      console.error('Failed to fetch member articles:', error);
      setArticles([]);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Are you sure you want to delete ${member.name}? This action cannot be undone.`)) {
      return;
    }

    try {
      await adminTeamService.deleteTeamMember(id);
      toast.success('Team member deleted successfully');
      navigate('/admin/team');
    } catch (error) {
      console.error('Failed to delete team member:', error);
      toast.error('Failed to delete team member');
    }
  };

  if (loading) {
    return (
      <div className="team-detail-page">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (!member) {
    return null;
  }

  return (
    <div className="team-detail-page">
      {/* Header */}
      <div className="detail-header">
        <button onClick={() => navigate('/admin/team')} className="btn-back">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Back to Team
        </button>
        
        <div className="header-actions">
          <Link to={`/admin/team/${id}/edit`} className="btn-secondary">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            Edit
          </Link>
          <button onClick={handleDelete} className="btn-danger">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            Delete
          </button>
        </div>
      </div>

      {/* Member Info Card */}
      <div className="member-info-card">
        <div className="member-photo-section">
          {member.photo ? (
            <img src={member.photo} alt={member.name} className="member-photo" />
          ) : (
            <div className="member-photo-placeholder">
              <svg width="80" height="80" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd"/>
              </svg>
            </div>
          )}
          
          {!member.is_active && (
            <span className="inactive-badge">Inactive</span>
          )}
        </div>

        <div className="member-details">
          <h1 className="member-name">{member.name}</h1>
          <p className="member-role">{member.role}</p>
          
          {member.email && (
            <div className="member-contact">
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <a href={`mailto:${member.email}`}>{member.email}</a>
            </div>
          )}

          {member.bio && (
            <div className="member-bio">
              <h3>Bio</h3>
              <p>{member.bio}</p>
            </div>
          )}

          {(member.twitter_url || member.linkedin_url) && (
            <div className="member-social">
              <h3>Social Links</h3>
              <div className="social-links">
                {member.twitter_url && (
                  <a href={member.twitter_url} target="_blank" rel="noopener noreferrer" className="social-link">
                    <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"/>
                    </svg>
                    Twitter/X
                  </a>
                )}
                {member.linkedin_url && (
                  <a href={member.linkedin_url} target="_blank" rel="noopener noreferrer" className="social-link">
                    <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/>
                      <circle cx="4" cy="4" r="2"/>
                    </svg>
                    LinkedIn
                  </a>
                )}
              </div>
            </div>
          )}

          <div className="member-meta">
            <div className="meta-item">
              <span className="meta-label">Display Order:</span>
              <span className="meta-value">{member.order}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Status:</span>
              <span className={`status-badge ${member.is_active ? 'active' : 'inactive'}`}>
                {member.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Articles Section */}
      <div className="articles-section">
        <h2 className="section-title">
          Articles by {member.name}
          <span className="article-count">{articles.length} {articles.length === 1 ? 'article' : 'articles'}</span>
        </h2>

        {articles.length === 0 ? (
          <div className="empty-articles">
            <svg width="48" height="48" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <p>No articles published yet</p>
          </div>
        ) : (
          <div className="articles-list">
            {articles.map((article) => (
              <div key={article.id} className="article-item">
                {article.image && (
                  <div className="article-thumbnail">
                    <img src={article.image} alt={article.title} />
                  </div>
                )}
                
                <div className="article-content">
                  <h3 className="article-title">{article.title}</h3>
                  {article.excerpt && <p className="article-excerpt">{article.excerpt}</p>}
                  
                  <div className="article-meta">
                    <span className="category-badge">{article.category}</span>
                    <span className="article-date">
                      {new Date(article.publish_date).toLocaleDateString()}
                    </span>
                    <span className="article-views">
                      {article.views || 0} views
                    </span>
                  </div>
                </div>

                <div className="article-actions">
                  <a href={`/news/${article.slug}/`} target="_blank" rel="noopener noreferrer" className="btn-icon" title="View">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                  </a>
                  <Link to={`/admin/news/${article.id}/edit`} className="btn-icon" title="Edit">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TeamDetail;
