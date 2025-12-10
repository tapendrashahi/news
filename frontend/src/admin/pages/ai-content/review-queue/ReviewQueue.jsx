import React, { useState, useEffect } from 'react'
import { getArticles, updateArticle, uploadArticleImage, approveArticle, rejectArticle, publishArticle } from '../../../services/aiContentService'
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
  const [showFullContent, setShowFullContent] = useState(true)
  const [editableContent, setEditableContent] = useState('')
  const [isEditingContent, setIsEditingContent] = useState(false)
  const [newImageUrl, setNewImageUrl] = useState('')
  const [isUploadingImage, setIsUploadingImage] = useState(false)

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
        if (updated) {
          // Preserve image_url if it exists in current state but not in fetched data
          const mergedArticle = {
            ...updated,
            image_url: updated.image_url || selectedArticle.image_url
          }
          setSelectedArticle(mergedArticle)
          setEditableContent(mergedArticle.raw_content || '')
        }
      }
    } catch (error) {
      console.error('Failed to fetch review queue:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectArticle = (article) => {
    setSelectedArticle(article)
    setEditableContent(article.raw_content || '')
    setIsEditingContent(false)
    setNewImageUrl('')
  }

  const handleSaveContent = async () => {
    if (!selectedArticle) return
    
    try {
      await updateArticle(selectedArticle.id, { raw_content: editableContent })
      setIsEditingContent(false)
      await fetchReviewQueue()
      alert('✅ Content updated successfully!')
    } catch (error) {
      console.error('Failed to update content:', error)
      alert('❌ Failed to update content')
    }
  }

  const handleImageUpload = async (file) => {
    if (!selectedArticle || !file) return
    
    setIsUploadingImage(true)
    try {
      console.log('Uploading image file:', file.name, 'Size:', file.size)
      const response = await uploadArticleImage(selectedArticle.id, file)
      console.log('Image upload response:', response.data)
      
      // Update the selected article with the server-returned image URL
      const updatedArticle = {
        ...selectedArticle,
        image_url: response.data.image_url
      }
      setSelectedArticle(updatedArticle)
      
      // Update in articles list too
      setArticles(prev => prev.map(a => 
        a.id === selectedArticle.id ? updatedArticle : a
      ))
      
      alert('✅ Image uploaded successfully!')
    } catch (error) {
      console.error('Failed to upload image:', error)
      alert('❌ Failed to upload image: ' + (error.response?.data?.detail || error.message))
    } finally {
      setIsUploadingImage(false)
    }
  }

  const handleImageUrlChange = async () => {
    if (!selectedArticle || !newImageUrl.trim()) return
    
    try {
      await updateArticle(selectedArticle.id, { image_url: newImageUrl })
      setNewImageUrl('')
      await fetchReviewQueue()
      alert('✅ Image URL updated!')
    } catch (error) {
      console.error('Failed to update image URL:', error)
      alert('❌ Failed to update image URL')
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
                onClick={() => handleSelectArticle(article)}
              >
                {article.image_url && (
                  <div className="topic-thumbnail">
                    <img src={article.image_url} alt={article.title} />
                  </div>
                )}
                <div className="topic-header">
                  <h4>{article.title}</h4>
                  <div className="topic-meta">
                    <span className="topic-wordcount">📝 {article.actual_word_count || 0} words</span>
                    {article.overall_quality_score && (
                      <span className="topic-quality">⭐ {Math.round(article.overall_quality_score)}%</span>
                    )}
                  </div>
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
                  <span className="metadata-label">Template</span>
                  <span className="metadata-value">{selectedArticle.template_type || 'N/A'}</span>
                </div>
                <div className="metadata-card">
                  <span className="metadata-label">Word Count</span>
                  <span className="metadata-value">{selectedArticle.actual_word_count || 0} / {selectedArticle.target_word_count || 0}</span>
                </div>
                <div className="metadata-card">
                  <span className="metadata-label">AI Model</span>
                  <span className="metadata-value">{selectedArticle.ai_model_used || 'N/A'}</span>
                </div>
                <div className="metadata-card">
                  <span className="metadata-label">Generation Time</span>
                  <span className="metadata-value">{selectedArticle.generation_time ? `${Math.round(selectedArticle.generation_time)}s` : 'N/A'}</span>
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

              {/* Comprehensive Quality Metrics */}
              <div className="section-card">
                <h3 className="section-title">📊 Comprehensive Quality Metrics</h3>
                <div className="comprehensive-metrics">
                  {/* Overall Scores */}
                  <div className="metrics-row">
                    <div className="metric-item large">
                      <span className="metric-icon">⭐</span>
                      <div className="metric-details">
                        <span className="metric-label">Overall Quality</span>
                        <span className="metric-value">{selectedArticle.overall_quality_score != null ? `${Math.round(selectedArticle.overall_quality_score)}%` : 'N/A'}</span>
                      </div>
                      {selectedArticle.overall_quality_score != null && (
                        <div className="metric-bar">
                          <div className="metric-bar-fill" style={{ width: `${selectedArticle.overall_quality_score}%` }}></div>
                        </div>
                      )}
                    </div>
                    <div className="metric-item large">
                      <span className="metric-icon">🎯</span>
                      <div className="metric-details">
                        <span className="metric-label">SEO Score</span>
                        <span className="metric-value">{selectedArticle.seo_score != null ? `${Math.round(selectedArticle.seo_score)}%` : 'N/A'}</span>
                      </div>
                      {selectedArticle.seo_score != null && (
                        <div className="metric-bar">
                          <div className="metric-bar-fill" style={{ width: `${selectedArticle.seo_score}%` }}></div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Content Analysis */}
                  <div className="metrics-section">
                    <h4 className="metrics-section-title">Content Analysis</h4>
                    <div className="metrics-row">
                      <div className="metric-item">
                        <span className="metric-icon">🤖</span>
                        <div className="metric-details">
                          <span className="metric-label">AI Detection</span>
                          <span className="metric-value">{selectedArticle.ai_score != null ? `${Math.round(selectedArticle.ai_score)}%` : 'N/A'}</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">📋</span>
                        <div className="metric-details">
                          <span className="metric-label">Plagiarism</span>
                          <span className="metric-value">{selectedArticle.plagiarism_score != null ? `${Math.round(selectedArticle.plagiarism_score)}%` : 'N/A'}</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">⚖️</span>
                        <div className="metric-details">
                          <span className="metric-label">Bias Score</span>
                          <span className="metric-value">{selectedArticle.bias_score != null ? `${Math.round(selectedArticle.bias_score)}%` : 'N/A'}</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">✅</span>
                        <div className="metric-details">
                          <span className="metric-label">Fact Check</span>
                          <span className="metric-value">{selectedArticle.fact_check_score != null ? `${Math.round(selectedArticle.fact_check_score)}%` : 'N/A'}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Readability & Quality */}
                  <div className="metrics-section">
                    <h4 className="metrics-section-title">Readability & Quality</h4>
                    <div className="metrics-row">
                      <div className="metric-item">
                        <span className="metric-icon">📖</span>
                        <div className="metric-details">
                          <span className="metric-label">Readability</span>
                          <span className="metric-value">{selectedArticle.readability_score != null ? `${Math.round(selectedArticle.readability_score)}%` : 'N/A'}</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">📝</span>
                        <div className="metric-details">
                          <span className="metric-label">Word Count</span>
                          <span className="metric-value">{selectedArticle.actual_word_count || 0}</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">⏱️</span>
                        <div className="metric-details">
                          <span className="metric-label">Gen Time</span>
                          <span className="metric-value">{selectedArticle.generation_time ? `${Math.round(selectedArticle.generation_time)}s` : 'N/A'}</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">🤖</span>
                        <div className="metric-details">
                          <span className="metric-label">AI Model</span>
                          <span className="metric-value" style={{fontSize: '11px'}}>{selectedArticle.ai_model_used || 'N/A'}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Technical SEO */}
                  <div className="metrics-section">
                    <h4 className="metrics-section-title">Technical SEO</h4>
                    <div className="metrics-row">
                      <div className="metric-item">
                        <span className="metric-icon">📰</span>
                        <div className="metric-details">
                          <span className="metric-label">Title Length</span>
                          <span className="metric-value">{selectedArticle.title ? selectedArticle.title.length : 0} chars</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">📝</span>
                        <div className="metric-details">
                          <span className="metric-label">Meta Length</span>
                          <span className="metric-value">{selectedArticle.meta_description ? selectedArticle.meta_description.length : 0} chars</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">🔑</span>
                        <div className="metric-details">
                          <span className="metric-label">Focus Keywords</span>
                          <span className="metric-value">{selectedArticle.focus_keywords?.length || 0}</span>
                        </div>
                      </div>
                      <div className="metric-item">
                        <span className="metric-icon">🖼️</span>
                        <div className="metric-details">
                          <span className="metric-label">Image</span>
                          <span className="metric-value">{selectedArticle.image_url ? '✓' : '✗'}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
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

              {/* Featured Image - Main Article Image */}
              <div className="section-card featured-image-card-large">
                <div className="featured-image-header">
                  <h3 className="section-title">📸 Article Featured Image</h3>
                  <button 
                    className="btn-edit-image"
                    onClick={() => document.getElementById('imageInput').click()}
                    disabled={isUploadingImage}
                  >
                    {isUploadingImage ? '⏳ Uploading...' : '📤 Upload New'}
                  </button>
                  <input 
                    id="imageInput" 
                    type="file" 
                    accept="image/*" 
                    style={{display: 'none'}}
                    onChange={(e) => e.target.files[0] && handleImageUpload(e.target.files[0])}
                  />
                </div>
                
                {selectedArticle.image_url && selectedArticle.image_url.trim() ? (
                  <div className="featured-image-container-large">
                    <img 
                      src={selectedArticle.image_url} 
                      alt={selectedArticle.title}
                      onError={(e) => {
                        console.error('Image load error:', selectedArticle.image_url)
                        e.target.style.display = 'none'
                        e.target.parentElement.innerHTML = '<p style="text-align:center;color:#dc3545;">❌ Failed to load image</p>'
                      }}
                    />
                    {selectedArticle.image_alt_text && (
                      <p className="image-alt-text">Alt: {selectedArticle.image_alt_text}</p>
                    )}
                  </div>
                ) : (
                  <div className="no-image-placeholder">
                    <p>📷 No image uploaded</p>
                  </div>
                )}
                
                <div className="image-url-editor">
                  <input 
                    type="text" 
                    placeholder="Or paste image URL..."
                    value={newImageUrl}
                    onChange={(e) => setNewImageUrl(e.target.value)}
                    className="image-url-input"
                  />
                  <button 
                    className="btn-update-url"
                    onClick={handleImageUrlChange}
                    disabled={!newImageUrl.trim()}
                  >
                    Update URL
                  </button>
                </div>
              </div>

              {/* Generated Content */}
              <div className="section-card content-card">
                <div className="content-card-header">
                  <h3 className="section-title">📝 Article Content</h3>
                  <div className="content-actions">
                    {isEditingContent ? (
                      <>
                        <button 
                          className="btn-save-content"
                          onClick={handleSaveContent}
                        >
                          💾 Save Changes
                        </button>
                        <button 
                          className="btn-cancel-edit"
                          onClick={() => {
                            setIsEditingContent(false)
                            setEditableContent(selectedArticle.raw_content || '')
                          }}
                        >
                          ✖ Cancel
                        </button>
                      </>
                    ) : (
                      <button 
                        className="btn-edit-content"
                        onClick={() => setIsEditingContent(true)}
                      >
                        ✏️ Edit Content
                      </button>
                    )}
                  </div>
                </div>
                
                <div className="content-display full">
                  {isEditingContent ? (
                    <textarea
                      className="content-editor"
                      value={editableContent}
                      onChange={(e) => setEditableContent(e.target.value)}
                      rows={25}
                    />
                  ) : (
                    selectedArticle.raw_content ? (
                      <div 
                        className="content-html"
                        dangerouslySetInnerHTML={{ __html: selectedArticle.raw_content }} 
                      />
                    ) : (
                      <p className="no-content">No content available</p>
                    )
                  )}
                </div>
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
