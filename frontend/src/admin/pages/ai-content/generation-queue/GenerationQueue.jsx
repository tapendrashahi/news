import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getArticles, retryStage, cancelGeneration, startGeneration, deleteArticle } from '../../../services/aiContentService'
import ArticleProgress from './ArticleProgress'
import DebugModal from './DebugModal'
import './GenerationQueue.css'

const GenerationQueue = () => {
  const navigate = useNavigate()
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all') // Show all by default so filters work
  const [selectedArticle, setSelectedArticle] = useState(null)
  const [openMenuId, setOpenMenuId] = useState(null)
  const [debugArticle, setDebugArticle] = useState(null)
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

  // Close dropdown menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (openMenuId && !event.target.closest('.header-right')) {
        setOpenMenuId(null)
      }
    }
    document.addEventListener('click', handleClickOutside)
    return () => document.removeEventListener('click', handleClickOutside)
  }, [openMenuId])

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
      published: articles.filter(a => a.status === 'published').length,
      failed: articles.filter(a => a.status === 'failed').length,
      byStage,
      byTemplate
    })
  }

  const fetchArticles = async () => {
    try {
      const params = {}
      // Apply filter if not 'all'
      if (filter !== 'all') {
        params.status = filter
      }
      
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

  const handleStart = async (id) => {
    try {
      await startGeneration(id)
      fetchArticles()
      alert('✅ Article generation started! Check progress in a few moments.')
    } catch (error) {
      console.error('Failed to start generation:', error)
      alert('❌ Failed to start generation: ' + (error.response?.data?.detail || error.message))
    }
  }

  const handleCancel = async (id) => {
    if (!window.confirm('Cancel generation?')) return
    try {
      await cancelGeneration(id)
      fetchArticles()
      // Optional: Show success message
      console.log('✅ Generation cancelled successfully')
    } catch (error) {
      console.error('Failed to cancel:', error)
      alert('Failed to cancel generation. Please try again.')
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this article? This action cannot be undone.')) return
    try {
      await deleteArticle(id)
      fetchArticles()
      setOpenMenuId(null)
      alert('✅ Article deleted successfully')
    } catch (error) {
      console.error('Failed to delete article:', error)
      alert('❌ Failed to delete article: ' + (error.response?.data?.detail || error.message))
    }
  }

  const handleRemoveFromPipeline = async (id) => {
    if (!window.confirm('Remove this article from the pipeline? The article will be cancelled and marked as failed.')) return
    try {
      await cancelGeneration(id)
      fetchArticles()
      setOpenMenuId(null)
      alert('✅ Article removed from pipeline')
    } catch (error) {
      console.error('Failed to remove from pipeline:', error)
      alert('❌ Failed to remove from pipeline: ' + (error.response?.data?.detail || error.message))
    }
  }

  const toggleMenu = (id) => {
    setOpenMenuId(openMenuId === id ? null : id)
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
        <div className="stat-card approved">
          <div className="stat-content">
            <div className="stat-value">{stats.approved}</div>
            <div className="stat-label">Approved</div>
          </div>
        </div>
        <div className="stat-card published">
          <div className="stat-content">
            <div className="stat-value">{stats.published}</div>
            <div className="stat-label">Published</div>
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
          {['all', 'queued', 'generating', 'reviewing', 'approved', 'published', 'failed'].map(f => (
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
                <div className="header-left">
                  <h3>{article.title || article.keyword?.keyword || 'Untitled'}</h3>
                  <span className={`status-badge ${article.status}`}>
                    {article.status}
                  </span>
                </div>
                <div className="header-right">
                  <button className="menu-button" onClick={() => toggleMenu(article.id)}>
                    ⋮
                  </button>
                  {openMenuId === article.id && (
                    <div className="dropdown-menu">
                      <button onClick={() => handleRemoveFromPipeline(article.id)}>
                        🚫 Remove from Pipeline
                      </button>
                      <button className="danger" onClick={() => handleDelete(article.id)}>
                        🗑️ Delete Article
                      </button>
                    </div>
                  )}
                </div>
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
                  <div className="progress-fill" style={{ width: `${article.progress_percentage || 0}%` }} />
                  <span className="progress-text">{article.progress_percentage || 0}%</span>
                </div>
              )}

              <div className="card-actions">
                {article.status === 'queued' && (
                  <button className="btn btn-sm btn-success" onClick={() => handleStart(article.id)}>
                    🚀 Start Generation
                  </button>
                )}
                {article.status === 'failed' && (
                  <>
                    <button className="btn btn-sm btn-warning" onClick={() => handleRetry(article.id, article.workflow_stage)}>
                      🔄 Retry
                    </button>
                    <button className="btn btn-sm btn-error" onClick={() => setDebugArticle(article)}>
                      🐛 Debug
                    </button>
                  </>
                )}
                {article.status === 'generating' && (
                  <button className="btn btn-sm btn-info" onClick={() => setDebugArticle(article)}>
                    🐛 Debug
                  </button>
                )}
                {(article.status === 'queued' || article.status === 'generating') && (
                  <button className="btn btn-sm btn-danger" onClick={() => handleCancel(article.id)}>
                    ✕ Cancel
                  </button>
                )}
                {(article.status === 'reviewing' || article.workflow_stage === 'completed') && (
                  <button 
                    className="btn btn-sm btn-success" 
                    onClick={() => navigate('/admin/ai-content/review-queue')}
                  >
                    📝 Review Article
                  </button>
                )}
                {article.status === 'approved' && (
                  <button className="btn btn-sm btn-primary" onClick={() => setSelectedArticle(article)}>
                    👁️ View
                  </button>
                )}
                {article.status === 'published' && article.published_article && (
                  <a 
                    href={`/news/${article.published_article.slug || article.slug}/`} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="btn btn-sm btn-success"
                  >
                    🌐 View Live Article
                  </a>
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
      
      {selectedArticle && (
        <ArticleProgress
          article={selectedArticle}
          onClose={() => setSelectedArticle(null)}
        />
      )}
      
      {debugArticle && (
        <DebugModal
          article={debugArticle}
          onClose={() => setDebugArticle(null)}
        />
      )}
    </div>
  )
}

export default GenerationQueue
