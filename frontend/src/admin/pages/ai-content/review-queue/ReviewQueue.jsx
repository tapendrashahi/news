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

      <div className="review-layout">
        {/* Left Sidebar - Topics List */}
        <div className="topics-sidebar">
          <div className="sidebar-header">
            <h3>Review Topics ({articles.length})</h3>
          </div>
          
          <div className="topics-list">
            {articles.map(article => (
              <div
                key={article.id}
                className={`topic-item ${selectedArticle?.id === article.id ? 'active' : ''}`}
                onClick={() => setSelectedArticle(article)}
              >
                <div className="topic-header">
                  <h4>{article.title}</h4>
                </div>
              </div>
            ))}
            
            {articles.length === 0 && (
              <div className="empty-state">
                <p>🎉 No articles ready</p>
                <small>Articles will appear here when generation completes</small>
              </div>
            )}
          </div>
        </div>

        {/* Main Content Area */}
        {selectedArticle ? (
          <div className="article-detail-view">
            <div className="detail-header">
              <div className="detail-title">
                <h1>{selectedArticle.title}</h1>
                {getStatusBadge(selectedArticle.status)}
              </div>
              <button 
                className="btn-close-detail" 
                onClick={() => setSelectedArticle(null)}
                title="Close Detail View"
              >
                ✕ Close
              </button>
            </div>

            <div className="detail-content">
              {/* Article Metadata */}
              <div className="metadata-grid">
                <div className="metadata-card">
                  <span className="metadata-label">Keyword</span>
                  <span className="metadata-value">{selectedArticle.keyword_text || 'N/A'}</span>
                </div>
                <div className="metadata-card">
                  <span className="metadata-label">Category</span>
                  <span className="metadata-value">{selectedArticle.category_display || 'N/A'}</span>
                </div>
                <div className="metadata-card">
                  <span className="metadata-label">Word Count</span>
                  <span className="metadata-value">{selectedArticle.actual_word_count || 0}</span>
                </div>
                <div className="metadata-card">
                  <span className="metadata-label">AI Model</span>
                  <span className="metadata-value">{selectedArticle.ai_model_used || 'N/A'}</span>
                </div>
                <div className="metadata-card">
                  <span className="metadata-label">Created</span>
                  <span className="metadata-value">{formatDate(selectedArticle.created_at)}</span>
                </div>
                <div className="metadata-card">
                  <span className="metadata-label">Updated</span>
                  <span className="metadata-value">{formatDate(selectedArticle.updated_at)}</span>
                </div>
              </div>

              {/* Quality Metrics */}
              <div className="section-card">
                <h3 className="section-title">Quality Metrics</h3>
                <QualityMetrics article={selectedArticle} />
              </div>

              {/* SEO Metadata */}
              {(selectedArticle.meta_description || (selectedArticle.focus_keywords && selectedArticle.focus_keywords.length > 0)) && (
                <div className="section-card">
                  <h3 className="section-title">SEO Metadata</h3>
                  {selectedArticle.meta_description && (
                    <div className="seo-field">
                      <label>Meta Description</label>
                      <p>{selectedArticle.meta_description}</p>
                    </div>
                  )}
                  {selectedArticle.focus_keywords && selectedArticle.focus_keywords.length > 0 && (
                    <div className="seo-field">
                      <label>Focus Keywords</label>
                      <div className="keywords-list">
                        {selectedArticle.focus_keywords.map((kw, idx) => (
                          <span key={idx} className="keyword-tag">{kw}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Generated Content */}
              <div className="section-card content-card">
                <div className="content-card-header">
                  <h3 className="section-title">Generated Content</h3>
                  <button 
                    className="btn-toggle-content"
                    onClick={() => setShowFullContent(!showFullContent)}
                  >
                    {showFullContent ? '📖 Show Preview' : '📄 Show Full Content'}
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

              {/* Action Buttons */}
              <div className="detail-actions">
                {selectedArticle.status === 'reviewing' && (
                  <button 
                    className="btn btn-success btn-large"
                    onClick={handleApprove}
                    disabled={actionLoading}
                  >
                    ✓ Approve for Publishing
                  </button>
                )}
                
                {selectedArticle.status === 'approved' && (
                  <button 
                    className="btn btn-primary btn-large"
                    onClick={handlePublish}
                    disabled={actionLoading}
                  >
                    🚀 Publish to Live Site
                  </button>
                )}
                
                <button 
                  className="btn btn-danger btn-large"
                  onClick={() => setShowRejectModal(true)}
                  disabled={actionLoading}
                >
                  ✕ Reject Article
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="no-selection">
            <div className="no-selection-icon">📋</div>
            <h2>Select an Article to Review</h2>
            <p>Choose an article from the topics list on the left to view details and take action</p>
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
