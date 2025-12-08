import React, { useState, useEffect } from 'react'
import { getArticles, retryStage, cancelGeneration } from '../../../services/aiContentService'
import './GenerationQueue.css'

const GenerationQueue = () => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [stats, setStats] = useState({
    total: 0,
    queued: 0,
    generating: 0,
    reviewing: 0,
    approved: 0,
    failed: 0,
    byStage: {},
    byTemplate: {},
    recentActivity: []
  })

  // Define all workflow stages (15 total stages)
  const KEY_STAGES = [
    { key: 'keyword_analysis', label: 'Keyword', icon: '🔑' },
    { key: 'research', label: 'Research', icon: '🔬' },
    { key: 'outline', label: 'Outline', icon: '📝' },
    { key: 'content_generation', label: 'Content', icon: '✍️' },
    { key: 'humanization', label: 'Humanize', icon: '🎨' },
    { key: 'ai_detection', label: 'AI Check', icon: '🤖' },
    { key: 'plagiarism_check', label: 'Plagiarism', icon: '📋' },
    { key: 'bias_detection', label: 'Bias', icon: '⚖️' },
    { key: 'fact_verification', label: 'Facts', icon: '✅' },
    { key: 'perspective_analysis', label: 'Perspective', icon: '👁️' },
    { key: 'seo_optimization', label: 'SEO', icon: '🔍' },
    { key: 'meta_generation', label: 'Meta', icon: '🏷️' },
    { key: 'image_generation', label: 'Image', icon: '🖼️' },
    { key: 'quality_check', label: 'Quality', icon: '✓' },
    { key: 'completed', label: 'Done', icon: '🎉' }
  ]

  const getStageProgress = (currentStage) => {
    const allStages = [
      'keyword_analysis', 'research', 'outline', 'content_generation', 'humanization',
      'ai_detection', 'plagiarism_check', 'bias_detection', 'fact_verification',
      'perspective_analysis', 'seo_optimization', 'meta_generation', 'image_generation',
      'quality_check', 'completed'
    ]
    const currentIndex = allStages.indexOf(currentStage)
    
    return KEY_STAGES.map(stage => ({
      ...stage,
      completed: currentIndex >= allStages.indexOf(stage.key),
      active: currentStage === stage.key
    }))
  }

  useEffect(() => {
    fetchArticles()
    const interval = setInterval(fetchArticles, 5000)
    return () => clearInterval(interval)
  }, [filter])

  useEffect(() => {
    calculateStats()
  }, [articles])

  const calculateStats = () => {
    const byStage = {}
    const byTemplate = {}
    
    articles.forEach(article => {
      // Count by stage
      const stage = article.workflow_stage || 'unknown'
      byStage[stage] = (byStage[stage] || 0) + 1
      
      // Count by template
      const template = article.template_type || 'unknown'
      byTemplate[template] = (byTemplate[template] || 0) + 1
    })

    setStats({
      total: articles.length,
      queued: articles.filter(a => a.status === 'queued').length,
      generating: articles.filter(a => a.status === 'generating').length,
      reviewing: articles.filter(a => a.status === 'reviewing').length,
      approved: articles.filter(a => a.status === 'approved').length,
      failed: articles.filter(a => a.status === 'failed').length,
      byStage,
      byTemplate
    })
  }

  const fetchArticles = async () => {
    try {
      const params = {}
      if (filter !== 'all') params.status = filter
      const response = await getArticles(params)
      setArticles(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch articles:', error)
      setArticles([])
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

  if (loading) return <div className="loading">⏳ Loading generation queue...</div>

  return (
    <div className="generation-queue-container">
      <div className="page-header">
        <h1>🤖 AI Generation Queue</h1>
        <div className="header-actions">
          <button className="btn btn-refresh" onClick={fetchArticles}>
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Dashboard Stats */}
      <div className="dashboard-stats">
        <div className="stat-card total">
          <div className="stat-content">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total Articles</div>
          </div>
        </div>
        <div className="stat-card queued">
          <div className="stat-content">
            <div className="stat-value">{stats.queued}</div>
            <div className="stat-label">Queued</div>
          </div>
        </div>
        <div className="stat-card generating">
          <div className="stat-content">
            <div className="stat-value">{stats.generating}</div>
            <div className="stat-label">Generating</div>
          </div>
        </div>
        <div className="stat-card reviewing">
          <div className="stat-content">
            <div className="stat-value">{stats.reviewing}</div>
            <div className="stat-label">Reviewing</div>
          </div>
        </div>
        <div className="stat-card reviewing">
          <div className="stat-content">
            <div className="stat-value">{stats.reviewing}</div>
            <div className="stat-label">Reviewing</div>
          </div>
        </div>
        <div className="stat-card approved">
          <div className="stat-content">
            <div className="stat-value">{stats.approved}</div>
            <div className="stat-label">Approved</div>
          </div>
        </div>
        <div className="stat-card failed">
          <div className="stat-content">
            <div className="stat-value">{stats.failed}</div>
            <div className="stat-label">Failed</div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-card">
          <h3>Progress by Stage</h3>
          <div className="chart-bars">
            {Object.entries(stats.byStage).map(([stage, count]) => (
              <div key={stage} className="bar-row">
                <div className="bar-label">{stage.replace(/_/g, ' ')}</div>
                <div className="bar-container">
                  <div 
                    className="bar-fill" 
                    style={{ width: `${(count / stats.total) * 100}%` }}
                  />
                  <span className="bar-count">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="chart-card">
          <h3>Articles by Template</h3>
          <div className="chart-bars">
            {Object.entries(stats.byTemplate).map(([template, count]) => (
              <div key={template} className="bar-row">
                <div className="bar-label">{template.replace(/_/g, ' ')}</div>
                <div className="bar-container">
                  <div 
                    className="bar-fill template" 
                    style={{ width: `${(count / stats.total) * 100}%` }}
                  />
                  <span className="bar-count">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="filters-bar">
        <div className="filter-group">
          {['all', 'queued', 'generating', 'reviewing', 'approved', 'failed'].map(f => (
            <button key={f} className={filter === f ? 'active' : ''} onClick={() => setFilter(f)}>
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="queue-grid">
        {articles.map(article => {
          const stageProgress = getStageProgress(article.workflow_stage)
          
          return (
            <div key={article.id} className={`queue-card ${article.status}`}>
              <div className="card-header">
                <h3>{article.title || article.keyword?.keyword || 'Untitled'}</h3>
                <span className={`status-badge ${article.status}`}>
                  {article.status}
                </span>
              </div>

              {/* Stage Progress Indicators */}
              <div className="stage-progress">
                {stageProgress.map((stage, idx) => (
                  <div 
                    key={stage.key} 
                    className={`stage-item ${stage.completed ? 'completed' : ''} ${stage.active ? 'active' : ''}`}
                    title={stage.label}
                  >
                    <div className="stage-icon">
                      {stage.completed ? '✓' : (idx + 1)}
                    </div>
                    <div className="stage-label">{stage.label}</div>
                  </div>
                ))}
              </div>

              <div className="card-meta">
                <span className="meta-item">
                  <strong>Current:</strong> {article.workflow_stage?.replace(/_/g, ' ') || 'N/A'}
                </span>
                {article.ai_model_used && (
                  <span className="meta-item">
                    <strong>Model:</strong> {article.ai_model_used}
                  </span>
                )}
              </div>

              {article.status === 'generating' && (
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${article.progress || 0}%` }} />
                </div>
              )}

              <div className="card-actions">
                {article.status === 'failed' && (
                  <button className="btn btn-sm btn-warning" onClick={() => handleRetry(article.id, article.workflow_stage)}>
                    🔄 Retry
                  </button>
                )}
                {(article.status === 'queued' || article.status === 'generating') && (
                  <button className="btn btn-sm btn-danger" onClick={() => handleCancel(article.id)}>
                    ✕ Cancel
                  </button>
                )}
                {(article.status === 'reviewing' || article.status === 'approved') && (
                  <button className="btn btn-sm btn-primary">👁️ View</button>
                )}
              </div>

              {article.error_log && (
                <div className="error-message">
                  <small>⚠️ {article.error_log}</small>
                </div>
              )}
            </div>
          )
        })}
      </div>
      {articles.length === 0 && <div className="empty-state">No articles in queue</div>}
    </div>
  )
}

export default GenerationQueue
