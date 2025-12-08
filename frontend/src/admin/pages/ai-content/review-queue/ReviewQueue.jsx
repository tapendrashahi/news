import React, { useState, useEffect } from 'react'
import { getArticles } from '../../../services/aiContentService'
import QualityMetrics from './QualityMetrics'
import './ReviewQueue.css'

const ReviewQueue = () => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedArticle, setSelectedArticle] = useState(null)

  useEffect(() => {
    fetchReviewQueue()
  }, [])

  const fetchReviewQueue = async () => {
    try {
      const response = await getArticles({ status: 'completed' })
      setArticles(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch review queue:', error)
    } finally {
      setLoading(false)
    }
  }

  const getQualityColor = (score) => {
    if (score >= 80) return '#28a745'
    if (score >= 60) return '#ffc107'
    return '#dc3545'
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="review-queue-container">
      <div className="page-header">
        <h1>Article Review Queue</h1>
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
              <h3>{article.title}</h3>
              <div className="article-meta">
                <span>Keyword: {article.keyword?.keyword}</span>
                <span>Created: {new Date(article.created_at).toLocaleDateString()}</span>
              </div>
              {article.overall_quality_score && (
                <div className="quality-badge" style={{ background: getQualityColor(article.overall_quality_score) }}>
                  Quality: {article.overall_quality_score}%
                </div>
              )}
            </div>
          ))}
          {articles.length === 0 && <div className="empty-state">No articles ready for review</div>}
        </div>

        {selectedArticle && (
          <div className="review-panel">
            <h2>{selectedArticle.title}</h2>
            <QualityMetrics article={selectedArticle} />
            <div className="article-content">
              <h3>Content Preview</h3>
              <div dangerouslySetInnerHTML={{ __html: selectedArticle.raw_content || 'No content' }} />
            </div>
            <div className="review-actions">
              <button className="btn btn-success">Approve & Publish</button>
              <button className="btn btn-warning">Request Revision</button>
              <button className="btn btn-danger">Reject</button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ReviewQueue
