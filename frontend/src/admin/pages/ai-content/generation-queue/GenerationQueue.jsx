import React, { useState, useEffect } from 'react'
import { getArticles, retryStage, cancelGeneration } from '../../../services/aiContentService'
import './GenerationQueue.css'

const GenerationQueue = () => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    fetchArticles()
    const interval = setInterval(fetchArticles, 5000)
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
      console.error('Failed to retry:', error)
    }
  }

  const handleCancel = async (id) => {
    if (!window.confirm('Cancel generation?')) return
    try {
      await cancelGeneration(id)
      fetchArticles()
    } catch (error) {
      console.error('Failed to cancel:', error)
    }
  }

  if (loading) return <div className="loading">Loading...</div>

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
          {['all', 'queued', 'generating', 'completed', 'failed'].map(f => (
            <button key={f} className={filter === f ? 'active' : ''} onClick={() => setFilter(f)}>
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="queue-grid">
        {articles.map(article => (
          <div key={article.id} className={`queue-card ${article.status}`}>
            <div className="card-header">
              <h3>{article.title || article.keyword?.keyword || 'Untitled'}</h3>
            </div>
            <div className="card-meta">
              <span>Status: {article.status}</span>
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
                <button className="btn btn-sm btn-warning" onClick={() => handleRetry(article.id, article.workflow_stage)}>Retry</button>
              )}
              {(article.status === 'queued' || article.status === 'generating') && (
                <button className="btn btn-sm btn-danger" onClick={() => handleCancel(article.id)}>Cancel</button>
              )}
              {article.status === 'completed' && (
                <button className="btn btn-sm btn-primary">View</button>
              )}
            </div>
            {article.error_log && (
              <div className="error-message"><small>{article.error_log}</small></div>
            )}
          </div>
        ))}
      </div>
      {articles.length === 0 && <div className="empty-state">No articles in queue</div>}
    </div>
  )
}

export default GenerationQueue
