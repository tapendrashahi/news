import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import adminCommentService from '../../services/adminCommentService';
import './CommentsList.css';

const CommentsList = () => {
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchComments();
  }, [searchQuery, statusFilter]);

  const fetchComments = async () => {
    try {
      setLoading(true);
      const params = {};
      
      if (searchQuery) {
        params.search = searchQuery;
      }
      
      if (statusFilter !== 'all') {
        params.status = statusFilter;
      }

      const data = await adminCommentService.getCommentsList(params);
      setComments(data.results || data);
    } catch (error) {
      console.error('Failed to fetch comments:', error);
      toast.error('Failed to load comments');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id) => {
    try {
      await adminCommentService.approveComment(id);
      toast.success('Comment approved');
      fetchComments();
    } catch (error) {
      console.error('Failed to approve comment:', error);
      toast.error('Failed to approve comment');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this comment?')) {
      return;
    }

    try {
      await adminCommentService.deleteComment(id);
      toast.success('Comment deleted');
      fetchComments();
    } catch (error) {
      console.error('Failed to delete comment:', error);
      toast.error('Failed to delete comment');
    }
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterChange = (filter) => {
    setStatusFilter(filter);
  };

  // Calculate stats
  const stats = {
    total: comments.length,
    approved: comments.filter(c => c.is_approved).length,
    pending: comments.filter(c => !c.is_approved).length,
  };

  return (
    <div className="comments-list-page">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Comments</h1>
          <p className="page-subtitle">Moderate and manage user comments</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon all">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total Comments</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon pending">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.pending}</div>
            <div className="stat-label">Pending Review</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon approved">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.approved}</div>
            <div className="stat-label">Approved</div>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="filter-tabs">
        <button
          className={`tab-btn ${statusFilter === 'all' ? 'active' : ''}`}
          onClick={() => handleFilterChange('all')}
        >
          All ({stats.total})
        </button>
        <button
          className={`tab-btn ${statusFilter === 'pending' ? 'active' : ''}`}
          onClick={() => handleFilterChange('pending')}
        >
          Pending ({stats.pending})
        </button>
        <button
          className={`tab-btn ${statusFilter === 'approved' ? 'active' : ''}`}
          onClick={() => handleFilterChange('approved')}
        >
          Approved ({stats.approved})
        </button>
      </div>

      {/* Search */}
      <div className="search-box">
        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input
          type="text"
          placeholder="Search by author or comment text..."
          value={searchQuery}
          onChange={handleSearch}
          className="search-input"
        />
      </div>

      {/* Comments List */}
      {loading ? (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading comments...</p>
        </div>
      ) : comments.length === 0 ? (
        <div className="empty-state">
          <svg width="64" height="64" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          <h3>No comments found</h3>
          <p>
            {statusFilter === 'pending' ? 'No pending comments to review' : 
             statusFilter === 'approved' ? 'No approved comments yet' :
             'No comments available'}
          </p>
        </div>
      ) : (
        <div className="comments-table-container">
          <table className="comments-table">
            <thead>
              <tr>
                <th>Author</th>
                <th>Comment</th>
                <th>Article</th>
                <th>Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {comments.map((comment) => (
                <tr key={comment.id}>
                  <td>
                    <div className="author-info">
                      <div className="author-name">{comment.author_name}</div>
                      {comment.author_email && (
                        <div className="author-email">{comment.author_email}</div>
                      )}
                    </div>
                  </td>
                  <td>
                    <div className="comment-text">{comment.text}</div>
                  </td>
                  <td>
                    <Link to={`/news/${comment.news_slug || comment.news?.slug}/`} target="_blank" className="article-link">
                      {comment.news_title || comment.news?.title}
                    </Link>
                  </td>
                  <td>
                    <div className="comment-date">
                      {new Date(comment.created_at).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    </div>
                    <div className="comment-time">
                      {new Date(comment.created_at).toLocaleTimeString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </td>
                  <td>
                    <span className={`status-badge ${comment.is_approved ? 'approved' : 'pending'}`}>
                      {comment.is_approved ? 'Approved' : 'Pending'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      {!comment.is_approved && (
                        <button
                          onClick={() => handleApprove(comment.id)}
                          className="btn-action approve"
                          title="Approve"
                        >
                          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"/>
                          </svg>
                        </button>
                      )}
                      <button
                        onClick={() => handleDelete(comment.id)}
                        className="btn-action delete"
                        title="Delete"
                      >
                        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CommentsList;
