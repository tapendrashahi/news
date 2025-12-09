import React, { useState, useEffect } from 'react'
import { getArticles, approveArticle, rejectArticle, publishArticle } from '../../../services/aiContentService'
import QualityMetrics from './QualityMetrics'
import './ReviewQueue.css'

const ReviewQueue = () => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedArticle, setSelectedArticle] = useState(null)
  const [actionLoading, setActionLoading] = useState(false)
  const [showRejectModal, setShowRejectModal] = useState(false)
  const [rejectNotes, setRejectNotes] = useState('')
  const [regenerateOnReject, setRegenerateOnReject] = useState(false)
  const [showFullContent, setShowFullContent] = useState(false)

  useEffect(() => {
    fetchReviewQueue()
    const interval = setInterval(fetchReviewQueue, 5000) // Poll every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchReviewQueue = async () => {
    try {
      // Fetch articles with status 'reviewing' or 'approved'
      // We need to fetch both statuses separately since the API doesn't support comma-separated values
      const [reviewingResponse, approvedResponse] = await Promise.all([
        getArticles({ status: 'reviewing' }),
        getArticles({ status: 'approved' })
      ])
      
      const reviewingArticles = reviewingResponse.data.results || reviewingResponse.data || []
      const approvedArticles = approvedResponse.data.results || approvedResponse.data || []
      
      // Combine and sort by created_at descending
      const allArticles = [...reviewingArticles, ...approvedArticles]
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      
      setArticles(allArticles)
      
      // Update selected article if it's in the list
      if (selectedArticle) {
        const updated = allArticles.find(a => a.id === selectedArticle.id)
        if (updated) setSelectedArticle(updated)
      }
    } catch (error) {
      console.error('Failed to fetch review queue:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async () => {
    if (!selectedArticle) return
    
    setActionLoading(true)
    try {
      await approveArticle(selectedArticle.id, 'Approved for publishing')
      await fetchReviewQueue()
      alert('Article approved! You can now publish it.')
    } catch (error) {
      console.error('Failed to approve article:', error)
      alert('Failed to approve article: ' + (error.response?.data?.detail || error.message))
    } finally {
      setActionLoading(false)
    }
  }

  const handlePublish = async () => {
    if (!selectedArticle) return
    
    if (!confirm(`Publish "${selectedArticle.title}" to live site?`)) return
    
    setActionLoading(true)
    try {
      const response = await publishArticle(selectedArticle.id, 'public')
      await fetchReviewQueue()
      setSelectedArticle(null)
      alert(`Article published successfully!\n\nView at: ${response.data.article_url}`)
    } catch (error) {
      console.error('Failed to publish article:', error)
      alert('Failed to publish article: ' + (error.response?.data?.detail || error.message))
    } finally {
      setActionLoading(false)
    }
  }

  const handleReject = async () => {
    if (!selectedArticle) return
    
    if (!rejectNotes.trim()) {
      alert('Please provide rejection notes')
      return
    }
    
    setActionLoading(true)
    try {
      await rejectArticle(selectedArticle.id, rejectNotes, regenerateOnReject)
      await fetchReviewQueue()
      setSelectedArticle(null)
      setShowRejectModal(false)
      setRejectNotes('')
      setRegenerateOnReject(false)
      alert(regenerateOnReject ? 'Article rejected. New generation started.' : 'Article rejected.')
    } catch (error) {
      console.error('Failed to reject article:', error)
      alert('Failed to reject article: ' + (error.response?.data?.detail || error.message))
    } finally {
      setActionLoading(false)
    }
  }

  const getQualityColor = (score) => {
    if (score >= 80) return '#28a745'
    if (score >= 60) return '#ffc107'
    return '#dc3545'
  }

  const getStatusBadge = (status) => {
    const badges = {
      'reviewing': { label: 'Ready for Review', color: '#007bff' },
      'approved': { label: 'Approved', color: '#28a745' }
    }
    const badge = badges[status] || { label: status, color: '#6c757d' }
    return <span className="status-badge" style={{ background: badge.color }}>{badge.label}</span>
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) return <div className="loading">Loading review queue...</div>

  return (
    <div className="review-queue-container">
      <div className="page-header">
        <h1>📋 Article Review Queue</h1>
        <p>{articles.length} article(s) ready for review</p>
      </div>

      <div className="review-grid">
        <div className="articles-list">
          {articles.map(article => (
            <div
              key={article.id}
              className={`review-card ${selectedArticle?.id === article.id ? 'selected' : ''}`}
              onClick={() => setSelectedArticle(article)}
            >
              <div className="card-header">
                <h3>{article.title}</h3>
                {getStatusBadge(article.status)}
              </div>
              
              <div className="article-meta">
                <div className="meta-item">
                  <strong>Keyword:</strong> {article.keyword?.keyword || 'N/A'}
                </div>
                <div className="meta-item">
                  <strong>Created:</strong> {formatDate(article.created_at)}
                </div>
                <div className="meta-item">
                  <strong>Word Count:</strong> {article.word_count || 0}
                </div>
              </div>

              {article.overall_quality_score !== null && (
                <div className="quality-preview">
                  <div 
                    className="quality-badge" 
                    style={{ background: getQualityColor(article.overall_quality_score) }}
                  >
                    Quality: {Math.round(article.overall_quality_score)}%
                  </div>
                  {article.seo_score !== null && (
                    <div 
                      className="quality-badge" 
                      style={{ background: getQualityColor(article.seo_score) }}
                    >
                      SEO: {Math.round(article.seo_score)}%
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
          
          {articles.length === 0 && (
            <div className="empty-state">
              <p>🎉 No articles in review queue</p>
              <small>Articles will appear here when generation is completed</small>
            </div>
          )}
        </div>

        {selectedArticle && (
          <div className="review-panel">
            <div className="panel-header">
              <h2>{selectedArticle.title}</h2>
              <div className="header-actions">
                {getStatusBadge(selectedArticle.status)}
                <button 
                  className="btn-close" 
                  onClick={() => setSelectedArticle(null)}
                  title="Close"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="panel-content">
              {/* Article Details */}
              <div className="article-details">
                <div className="detail-row">
                  <span className="label">Keyword:</span>
                  <span className="value">{selectedArticle.keyword?.keyword}</span>
                </div>
                <div className="detail-row">
                  <span className="label">Category:</span>
                  <span className="value">{selectedArticle.keyword?.category?.name || 'N/A'}</span>
                </div>
                <div className="detail-row">
                  <span className="label">Word Count:</span>
                  <span className="value">{selectedArticle.word_count || 0}</span>
                </div>
                <div className="detail-row">
                  <span className="label">AI Model:</span>
                  <span className="value">{selectedArticle.ai_model_used || 'N/A'}</span>
                </div>
              </div>

              {/* Quality Metrics */}
              <QualityMetrics article={selectedArticle} />

              {/* Meta Information */}
              {(selectedArticle.meta_title || selectedArticle.meta_description) && (
                <div className="meta-section">
                  <h3>SEO Metadata</h3>
                  {selectedArticle.meta_title && (
                    <div className="meta-field">
                      <strong>Meta Title:</strong>
                      <p>{selectedArticle.meta_title}</p>
                    </div>
                  )}
                  {selectedArticle.meta_description && (
                    <div className="meta-field">
                      <strong>Meta Description:</strong>
                      <p>{selectedArticle.meta_description}</p>
                    </div>
                  )}
                  {selectedArticle.focus_keywords && selectedArticle.focus_keywords.length > 0 && (
                    <div className="meta-field">
                      <strong>Focus Keywords:</strong>
                      <div className="keywords-list">
                        {selectedArticle.focus_keywords.map((kw, idx) => (
                          <span key={idx} className="keyword-tag">{kw}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Content Preview/Full */}
              <div className="article-content">
                <div className="content-header">
                  <h3>Article Content</h3>
                  <button 
                    className="btn-toggle-content"
                    onClick={() => setShowFullContent(!showFullContent)}
                  >
                    {showFullContent ? 'Show Preview' : 'Show Full Content'}
                  </button>
                </div>
                
                <div className={`content-display ${showFullContent ? 'full' : 'preview'}`}>
                  {selectedArticle.raw_content ? (
                    <div 
                      className="content-html"
                      dangerouslySetInnerHTML={{ __html: selectedArticle.raw_content }} 
                    />
                  ) : (
                    <p className="no-content">No content available</p>
                  )}
                </div>
                
                {!showFullContent && selectedArticle.raw_content && (
                  <div className="content-fade"></div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="review-actions">
              {selectedArticle.status === 'reviewing' && (
                <button 
                  className="btn btn-success"
                  onClick={handleApprove}
                  disabled={actionLoading}
                >
                  ✓ Approve for Publishing
                </button>
              )}
              
              {selectedArticle.status === 'approved' && (
                <button 
                  className="btn btn-primary"
                  onClick={handlePublish}
                  disabled={actionLoading}
                >
                  🚀 Publish to Live Site
                </button>
              )}
              
              <button 
                className="btn btn-danger"
                onClick={() => setShowRejectModal(true)}
                disabled={actionLoading}
              >
                ✕ Reject Article
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Reject Modal */}
      {showRejectModal && (
        <div className="modal-overlay" onClick={() => setShowRejectModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Reject Article</h3>
              <button onClick={() => setShowRejectModal(false)}>✕</button>
            </div>
            
            <div className="modal-body">
              <p>Please provide a reason for rejecting this article:</p>
              <textarea
                value={rejectNotes}
                onChange={(e) => setRejectNotes(e.target.value)}
                placeholder="Explain why this article is being rejected..."
                rows={5}
              />
              
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={regenerateOnReject}
                  onChange={(e) => setRegenerateOnReject(e.target.checked)}
                />
                <span>Regenerate article with new content</span>
              </label>
            </div>
            
            <div className="modal-footer">
              <button 
                className="btn btn-secondary"
                onClick={() => setShowRejectModal(false)}
              >
                Cancel
              </button>
              <button 
                className="btn btn-danger"
                onClick={handleReject}
                disabled={actionLoading || !rejectNotes.trim()}
              >
                {actionLoading ? 'Processing...' : 'Reject Article'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ReviewQueue
