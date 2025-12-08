import React, { useState, useEffect } from 'react'
import { getArticles, retryStage, cancelGeneration } from '../../../services/aiContentService'
import ArticleProgress from './ArticleProgress'
import './GenerationQueue.css'

const GenerationQueue = () => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all') // all, queued, generating, completed, failed
  const [selectedArticle, setSelectedArticle] = useState(null)

  useEffect(() => {
    fetchArticles()
    const interval = setInterval(fetchArticles, 5000) // Poll every 5 seconds
    return () => clearInterval(interval)
  }, [filter])

  const fetchArticles = async () => {
    try {
      const params = {}
      if (filter !== 'all') params.status = filter
      
      const response = await getArticles(params)
      setArticles(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch articles:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRetry = async (id, stage) => {
    try {
      await retryStage(id, stage)
      fetchArticles()
    } catch (error) {
      console.error('Failed to retry article:', error)
      alert('Failed to retry article')
    }
  }

  const handleCancel = async (id) => {
    if (!window.confirm('Are you sure you want to cancel this generation?')) return
    
    try {
      await cancelGeneration(id)
      fetchArticles()
      console.log('✅ Generation cancelled successfully')
    } catch (error) {
      console.error('Failed to cancel generation:', error)
      alert('Failed to cancel generation. Please try again.')
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      queued: '#6c757d',
      generating: '#007bff',
      completed: '#28a745',
      failed: '#dc3545'
    }
    return colors[status] || '#6c757d'
  }

  const getStatusIcon = (status) => {
    const icons = {
      queued: '⏳',
      generating: '⚙️',
      completed: '✅',
      failed: '❌'
    }
    return icons[status] || '•'
  }

  if (loading) return <div className="loading">Loading generation queue...</div>

  return (
    <div className="generation-queue-container">
      <div className="page-header">
        <h1>AI Generation Queue</h1>
        <div className="queue-stats">
          <span>Queued: {articles.filter(a => a.status === 'queued').length}</span>
          <span>Generating: {articles.filter(a => a.status === 'generating').length}</span>
          <span>Completed: {articles.filter(a => a.status === 'completed').length}</span>
          <span>Failed: {articles.filter(a => a.status === 'failed').length}</span>
        </div>
      </div>

      <div className="filters-bar">
        <div className="filter-group">
          <button className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>
            All
          </button>
          <button className={filter === 'queued' ? 'active' : ''} onClick={() => setFilter('queued')}>
            Queued
          </button>
          <button className={filter === 'generating' ? 'active' : ''} onClick={() => setFilter('generating')}>
            Generating
          </button>
          <button className={filter === 'completed' ? 'active' : ''} onClick={() => setFilter('completed')}>
            Completed
          </button>
          <button className={filter === 'failed' ? 'active' : ''} onClick={() => setFilter('failed')}>
            Failed
          </button>
        </div>
      </div>

      <div className="queue-grid">
        {articles.map(article => (
          <div
            key={article.id}
            className={`queue-card ${article.status}`}
            onClick={() => setSelectedArticle(article)}
          >
            <div className="card-header">
              <span className="status-icon" style={{ color: getStatusColor(article.status) }}>
                {getStatusIcon(article.status)}
              </span>
              <h3>{article.title || article.keyword?.keyword || 'Untitled'}</h3>
            </div>

            <div className="card-meta">
              <span>Template: {article.template_type}</span>
              <span>Stage: {article.workflow_stage || 'N/A'}</span>
              {article.ai_model_used && <span>Model: {article.ai_model_used}</span>}
            </div>

            {article.status === 'generating' && (
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${article.progress || 0}%` }} />
              </div>
            )}

            <div className="card-actions">
              {article.status === 'failed' && (
                <button
                  className="btn btn-sm btn-warning"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleRetry(article.id, article.workflow_stage)
                  }}
                >
                  Retry
                </button>
              )}
              {(article.status === 'queued' || article.status === 'generating') && (
                <button
                  className="btn btn-sm btn-danger"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleCancel(article.id)
                  }}
                >
                  Cancel
                </button>
              )}
              {article.status === 'completed' && (
                <button className="btn btn-sm btn-primary">View</button>
              )}
            </div>

            {article.error_log && (
              <div className="error-message">
                <small>{article.error_log}</small>
              </div>
            )}
          </div>
        ))}
      </div>

      {articles.length === 0 && (
        <div className="empty-state">
          <p>No articles in the queue</p>
        </div>
      )}

      {selectedArticle && (
        <ArticleProgress
          article={selectedArticle}
          onClose={() => setSelectedArticle(null)}
        />
      )}
    </div>
  )
}

export default GenerationQueue
