/**
 * Article Progress Component
 * 
 * Task 5.3: Generation Queue
 * Individual article progress tracking
 */

import React, { useState } from 'react'
import './ArticleProgress.css'

const ArticleProgress = ({ article, onClose }) => {
  const [showFullContent, setShowFullContent] = useState(false)
  
  if (!article) return null

  const allStages = [
    { key: 'keyword_analysis', label: 'Keyword Analysis', icon: '🔑' },
    { key: 'research', label: 'Research', icon: '🔬' },
    { key: 'outline', label: 'Outline', icon: '📝' },
    { key: 'content_generation', label: 'Content Generation', icon: '✍️' },
    { key: 'humanization', label: 'Humanization', icon: '🎨' },
    { key: 'ai_detection', label: 'AI Detection', icon: '🤖' },
    { key: 'plagiarism_check', label: 'Plagiarism Check', icon: '📋' },
    { key: 'bias_detection', label: 'Bias Detection', icon: '⚖️' },
    { key: 'fact_verification', label: 'Fact Verification', icon: '✅' },
    { key: 'perspective_analysis', label: 'Perspective Analysis', icon: '👁️' },
    { key: 'seo_optimization', label: 'SEO Optimization', icon: '🔍' },
    { key: 'meta_generation', label: 'Meta Generation', icon: '🏷️' },
    { key: 'image_generation', label: 'Image Generation', icon: '🖼️' },
    { key: 'quality_check', label: 'Quality Check', icon: '✓' },
    { key: 'completed', label: 'Completed', icon: '🎉' }
  ]

  const currentStageIndex = allStages.findIndex(s => s.key === article.workflow_stage)
  
  const getStageStatus = (index) => {
    if (index < currentStageIndex) return 'completed'
    if (index === currentStageIndex) return 'active'
    return 'pending'
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleString()
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content article-progress-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>📊 Article Progress</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          {/* Article Info */}
          <div className="info-section">
            <h3>{article.title || article.keyword?.keyword || 'Untitled Article'}</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Status:</label>
                <span className={`status-badge ${article.status}`}>
                  {article.status}
                </span>
              </div>
              <div className="info-item">
                <label>Template:</label>
                <span>{article.template_type || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Model:</label>
                <span>{article.ai_model_used || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Word Count:</label>
                <span>{article.actual_word_count || 0} / {article.target_word_count || 0}</span>
              </div>
            </div>
          </div>

          {/* Pipeline Stages */}
          <div className="stages-section">
            <h4>Pipeline Progress</h4>
            <div className="stages-list">
              {allStages.map((stage, index) => {
                const status = getStageStatus(index)
                return (
                  <div key={stage.key} className={`stage-row ${status}`}>
                    <div className="stage-icon-circle">
                      {status === 'completed' && '✓'}
                      {status === 'active' && '⟳'}
                      {status === 'pending' && '○'}
                    </div>
                    <div className="stage-info">
                      <span className="stage-name">{stage.icon} {stage.label}</span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Quality Scores */}
          {(article.ai_score || article.plagiarism_score || article.seo_score) && (
            <div className="quality-section">
              <h4>Quality Metrics</h4>
              <div className="quality-grid">
                {article.ai_score !== null && article.ai_score !== undefined && (
                  <div className="quality-item">
                    <label>AI Detection:</label>
                    <div className="score-bar">
                      <div 
                        className="score-fill ai" 
                        style={{ width: `${article.ai_score}%` }}
                      />
                      <span className="score-value">{article.ai_score}%</span>
                    </div>
                  </div>
                )}
                {article.plagiarism_score !== null && article.plagiarism_score !== undefined && (
                  <div className="quality-item">
                    <label>Plagiarism:</label>
                    <div className="score-bar">
                      <div 
                        className="score-fill plagiarism" 
                        style={{ width: `${article.plagiarism_score}%` }}
                      />
                      <span className="score-value">{article.plagiarism_score}%</span>
                    </div>
                  </div>
                )}
                {article.seo_score !== null && article.seo_score !== undefined && (
                  <div className="quality-item">
                    <label>SEO Score:</label>
                    <div className="score-bar">
                      <div 
                        className="score-fill seo" 
                        style={{ width: `${article.seo_score}%` }}
                      />
                      <span className="score-value">{article.seo_score}%</span>
                    </div>
                  </div>
                )}
                {article.readability_score !== null && article.readability_score !== undefined && (
                  <div className="quality-item">
                    <label>Readability:</label>
                    <div className="score-bar">
                      <div 
                        className="score-fill readability" 
                        style={{ width: `${article.readability_score}%` }}
                      />
                      <span className="score-value">{article.readability_score}%</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Generated Content */}
          {article.raw_content && (
            <div className="content-section">
              <div className="content-header">
                <h4>Generated Content</h4>
                <div className="content-stats">
                  <span className="word-count">
                    📝 {article.actual_word_count || article.raw_content.split(/\s+/).length} words
                  </span>
                  {article.raw_content.length > 1000 && (
                    <button 
                      className="toggle-content-btn"
                      onClick={() => setShowFullContent(!showFullContent)}
                    >
                      {showFullContent ? '📖 Show Less' : '📚 Show Full Content'}
                    </button>
                  )}
                </div>
              </div>
              <div className={`content-display ${showFullContent ? 'full' : 'preview'}`}>
                {showFullContent ? (
                  <div className="full-content">
                    {article.raw_content}
                  </div>
                ) : (
                  <div className="preview-content">
                    {article.raw_content.substring(0, 1000)}
                    {article.raw_content.length > 1000 && (
                      <div className="content-fade">
                        <span className="read-more-hint">Click "Show Full Content" to read more...</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Meta Information */}
          {(article.meta_title || article.meta_description) && (
            <div className="meta-section">
              <h4>SEO Meta Tags</h4>
              {article.meta_title && (
                <div className="meta-item">
                  <label>Meta Title:</label>
                  <p>{article.meta_title}</p>
                </div>
              )}
              {article.meta_description && (
                <div className="meta-item">
                  <label>Meta Description:</label>
                  <p>{article.meta_description}</p>
                </div>
              )}
            </div>
          )}

          {/* Error Log */}
          {article.last_error && (
            <div className="error-section">
              <h4>⚠️ Error Log</h4>
              <div className="error-box">
                {article.last_error}
              </div>
            </div>
          )}

          {/* Timestamps */}
          <div className="timestamps-section">
            <h4>Timeline</h4>
            <div className="timestamps-grid">
              <div className="timestamp-item">
                <label>Created:</label>
                <span>{formatDate(article.created_at)}</span>
              </div>
              <div className="timestamp-item">
                <label>Updated:</label>
                <span>{formatDate(article.updated_at)}</span>
              </div>
              {article.generation_started_at && (
                <div className="timestamp-item">
                  <label>Started:</label>
                  <span>{formatDate(article.generation_started_at)}</span>
                </div>
              )}
              {article.generation_completed_at && (
                <div className="timestamp-item">
                  <label>Completed:</label>
                  <span>{formatDate(article.generation_completed_at)}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Close</button>
          {article.slug && (
            <a 
              href={`/admin/news/aiarticle/${article.id}/change/`} 
              target="_blank" 
              rel="noopener noreferrer"
              className="btn btn-primary"
            >
              Edit in Admin
            </a>
          )}
        </div>
      </div>
    </div>
  )
}

export default ArticleProgress