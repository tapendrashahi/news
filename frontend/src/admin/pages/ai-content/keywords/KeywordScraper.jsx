import React, { useState, useEffect } from 'react'
import { 
  createNewsSource, 
  getNewsSources, 
  triggerScrape,
  getScrapedArticles,
  approveScrapedArticle,
  rejectScrapedArticle,
  bulkApproveArticles
} from '../../../services/aiContentService'

export default function KeywordScraper({ onKeywordsAdded, showModal, setShowModal, showFullUI = true }) {
  const [activeTab, setActiveTab] = useState('scrape')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })
  
  // News Source Setup state
  const [setupData, setSetupData] = useState({
    name: '',
    keywords: '',
    source_websites: '',
    category: 'Politics',
    max_articles_per_scrape: 20,
    scrape_frequency_hours: 24,
    notes: ''
  })
  
  // Existing configurations
  const [newsSourceConfigs, setNewsSourceConfigs] = useState([])
  
  // Scraped articles state
  const [scrapedArticles, setScrapedArticles] = useState([])
  const [selectedArticles, setSelectedArticles] = useState([])
  const [articleFilter, setArticleFilter] = useState('pending')
  
  // Scraping progress state
  const [scrapingProgress, setScrapingProgress] = useState({})

  const categories = [
    'Politics', 'Business', 'Technology', 'Health', 'Education',
    'Entertainment', 'Sports', 'Science', 'Environment', 'Culture'
  ]

  useEffect(() => {
    if (activeTab === 'scrape') {
      loadNewsSourceConfigs()
    } else if (activeTab === 'review') {
      loadScrapedArticles()
    }
  }, [activeTab, articleFilter])

  const loadNewsSourceConfigs = async () => {
    try {
      const response = await getNewsSources()
      setNewsSourceConfigs(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to load news source configs:', error)
    }
  }

  const loadScrapedArticles = async () => {
    setLoading(true)
    try {
      const params = articleFilter !== 'all' ? { status: articleFilter } : {}
      const response = await getScrapedArticles(params)
      setScrapedArticles(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to load scraped articles:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSetupSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ type: '', text: '' })

    try {
      // Handle both comma-separated and newline-separated input
      const keywords = setupData.keywords
        .split(/[,\n]+/)  // Split by comma or newline
        .map(k => k.trim())
        .filter(k => k.length > 0)

      const websites = setupData.source_websites
        .split(/[,\n]+/)  // Split by comma or newline
        .map(w => w.trim())
        .filter(w => w.length > 0)

      if (!setupData.name) {
        setMessage({ type: 'error', text: 'Please enter a configuration name' })
        setLoading(false)
        return
      }

      if (keywords.length === 0) {
        setMessage({ type: 'error', text: 'Please enter at least one keyword' })
        setLoading(false)
        return
      }

      if (websites.length === 0) {
        setMessage({ type: 'error', text: 'Please enter at least one news website URL' })
        setLoading(false)
        return
      }

      const data = {
        name: setupData.name,
        keywords: keywords,
        source_websites: websites,
        category: setupData.category,
        max_articles_per_scrape: parseInt(setupData.max_articles_per_scrape),
        scrape_frequency_hours: parseInt(setupData.scrape_frequency_hours),
        notes: setupData.notes,
        status: 'active'
      }
      
      await createNewsSource(data)
      
      setMessage({ 
        type: 'success', 
        text: `Configuration "${setupData.name}" created successfully!` 
      })
      
      setSetupData({
        name: '',
        keywords: '',
        source_websites: '',
        category: 'Politics',
        max_articles_per_scrape: 20,
        scrape_frequency_hours: 24,
        notes: ''
      })
      
      loadNewsSourceConfigs()
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to create configuration' 
      })
    } finally {
      setLoading(false)
    }
  }

  const handleScrapeAll = async () => {
    const activeConfigs = newsSourceConfigs.filter(c => c.status === 'active')
    
    if (activeConfigs.length === 0) {
      setMessage({ type: 'error', text: 'No active configurations to scrape' })
      return
    }

    setMessage({ type: 'info', text: `Starting bulk scrape for ${activeConfigs.length} sources...` })
    
    // Initialize progress for all configs
    const initialProgress = {}
    activeConfigs.forEach(config => {
      initialProgress[config.id] = { status: 'queued', progress: 0, message: 'Queued...' }
    })
    setScrapingProgress(initialProgress)

    // Process all configs sequentially
    for (const config of activeConfigs) {
      await handleTriggerScrape(config.id, config.name)
      // Small delay between sources
      await new Promise(resolve => setTimeout(resolve, 500))
    }
    
    setMessage({ type: 'success', text: `Bulk scraping completed for ${activeConfigs.length} sources!` })
  }

  const handleTriggerScrape = async (configId, configName) => {
    setMessage({ type: '', text: '' })
    
    // Set initial progress
    setScrapingProgress(prev => ({
      ...prev,
      [configId]: { status: 'starting', progress: 0, message: 'Initializing scraper...' }
    }))
    
    try {
      // Update progress to scraping
      setScrapingProgress(prev => ({
        ...prev,
        [configId]: { status: 'scraping', progress: 30, message: 'Scraping articles from websites...' }
      }))
      
      await triggerScrape(configId)
      
      // Update progress to processing
      setScrapingProgress(prev => ({
        ...prev,
        [configId]: { status: 'processing', progress: 70, message: 'Processing scraped content...' }
      }))
      
      // Simulate processing time
      setTimeout(() => {
        setScrapingProgress(prev => ({
          ...prev,
          [configId]: { status: 'complete', progress: 100, message: 'Scraping completed!' }
        }))
        
        setMessage({ 
          type: 'success', 
          text: `Scraping completed for "${configName}". Check Review tab to see results.` 
        })
        
        // Reload scraped articles if on review tab
        if (activeTab === 'review') {
          loadScrapedArticles()
        }
        
        // Clear progress after 3 seconds
        setTimeout(() => {
          setScrapingProgress(prev => {
            const newProgress = { ...prev }
            delete newProgress[configId]
            return newProgress
          })
        }, 3000)
      }, 2000)
      
    } catch (error) {
      setScrapingProgress(prev => ({
        ...prev,
        [configId]: { status: 'error', progress: 0, message: 'Scraping failed!' }
      }))
      
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to trigger scraping' 
      })
      
      // Clear error progress after 3 seconds
      setTimeout(() => {
        setScrapingProgress(prev => {
          const newProgress = { ...prev }
          delete newProgress[configId]
          return newProgress
        })
      }, 3000)
    }
  }

  const handleApproveArticle = async (articleId) => {
    setLoading(true)
    try {
      await approveScrapedArticle(articleId, { auto_generate: true })
      setMessage({ 
        type: 'success', 
        text: 'Article approved and sent to generation pipeline!' 
      })
      loadScrapedArticles()
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to approve article' 
      })
    } finally {
      setLoading(false)
    }
  }

  const handleRejectArticle = async (articleId) => {
    const reason = prompt('Rejection reason (optional):')
    if (reason === null) return
    
    setLoading(true)
    try {
      await rejectScrapedArticle(articleId, reason || 'Not relevant')
      setMessage({ 
        type: 'success', 
        text: 'Article rejected' 
      })
      loadScrapedArticles()
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to reject article' 
      })
    } finally {
      setLoading(false)
    }
  }

  const handleBulkApprove = async () => {
    if (selectedArticles.length === 0) {
      setMessage({ type: 'error', text: 'Please select at least one article' })
      return
    }
    
    setLoading(true)
    try {
      await bulkApproveArticles(selectedArticles)
      setMessage({ 
        type: 'success', 
        text: `${selectedArticles.length} article(s) approved and sent to generation!` 
      })
      setSelectedArticles([])
      loadScrapedArticles()
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to bulk approve' 
      })
    } finally {
      setLoading(false)
    }
  }

  const toggleArticleSelection = (articleId) => {
    setSelectedArticles(prev => 
      prev.includes(articleId) 
        ? prev.filter(id => id !== articleId)
        : [...prev, articleId]
    )
  }

  return (
    <div className="keyword-scraper">
      {showFullUI && (
        <>
          <div className="scraper-tabs">
            <button 
              className={`tab ${activeTab === 'scrape' ? 'active' : ''}`}
              onClick={() => setActiveTab('scrape')}
            >
              🚀 Scrape News
            </button>
            <button 
              className={`tab ${activeTab === 'review' ? 'active' : ''}`}
              onClick={() => setActiveTab('review')}
            >
              📰 Review Articles ({scrapedArticles.length})
            </button>
          </div>

          {message.text && (
            <div className={`message ${message.type}`}>
              {message.text}
            </div>
          )}
        </>
      )}

      {/* Setup Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>⚙️ Setup News Scraping Source</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <div className="modal-body">
              <p className="help-text" style={{ marginBottom: '20px' }}>
                Define keywords and target news websites. The system will scrape articles matching your keywords from these sites.
              </p>
              
              <form onSubmit={handleSetupSubmit} className="scraper-form">
                <div className="form-group">
                  <label>Configuration Name *</label>
                  <input
                    type="text"
                    value={setupData.name}
                    onChange={(e) => setSetupData({ ...setupData, name: e.target.value })}
                    placeholder="e.g., Tech News Daily, AI Research Weekly"
                    required
                  />
                  <span className="help-text">A descriptive name for this scraping configuration</span>
                </div>

                <div className="form-group">
                  <label>Keywords *</label>
                  <textarea
                    value={setupData.keywords}
                    onChange={(e) => setSetupData({ ...setupData, keywords: e.target.value })}
                    placeholder="Enter keywords (comma-separated or one per line)&#10;Example: AI, Technology, Climate Change"
                    rows={4}
                    required
                  />
                  <span className="help-text">Separate with commas or new lines</span>
                </div>

                <div className="form-group">
                  <label>Target News Websites *</label>
                  <textarea
                    value={setupData.source_websites}
                    onChange={(e) => setSetupData({ ...setupData, source_websites: e.target.value })}
                    placeholder="Enter website URLs (comma-separated or one per line)&#10;Example: bbc.com, reuters.com, techcrunch.com"
                    rows={4}
                    required
                  />
                  <span className="help-text">Separate with commas or new lines. Protocol (https://) is optional</span>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Category *</label>
                    <select
                      value={setupData.category}
                      onChange={(e) => setSetupData({ ...setupData, category: e.target.value })}
                      required
                    >
                      <option value="">Select category</option>
                      <option value="technology">Technology</option>
                      <option value="business">Business</option>
                      <option value="politics">Politics</option>
                      <option value="sports">Sports</option>
                      <option value="entertainment">Entertainment</option>
                      <option value="science">Science</option>
                      <option value="health">Health</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Max Articles per Scrape</label>
                    <input
                      type="number"
                      value={setupData.max_articles_per_scrape}
                      onChange={(e) => setSetupData({ ...setupData, max_articles_per_scrape: parseInt(e.target.value) })}
                      min="1"
                      max="100"
                    />
                  </div>
                </div>

                <div className="form-actions">
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? '⏳ Creating...' : '✅ Create Configuration'}
                  </button>
                  <button 
                    type="button" 
                    className="btn btn-secondary"
                    onClick={() => setShowModal(false)}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {showFullUI && activeTab === 'scrape' && (
        <div className="scrape-page">
          {/* Main Content - Configurations List */}
          <div className="configurations-section">
            <div className="configs-header">
              <div>
                <h2>📋 News Source Configurations</h2>
                <p className="subtitle">Manage your scraping sources and trigger bulk scraping</p>
              </div>
              {newsSourceConfigs.filter(c => c.status === 'active').length > 0 && (
                <button
                  className="btn btn-primary btn-large scrape-all-btn"
                  onClick={handleScrapeAll}
                  disabled={Object.keys(scrapingProgress).length > 0}
                >
                  🚀 Scrape All ({newsSourceConfigs.filter(c => c.status === 'active').length} active)
                </button>
              )}
            </div>

            {newsSourceConfigs.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📋</div>
                <h3>No Configurations Yet</h3>
                <p>Click "⚙️ Setup Configuration" in the header to create your first news scraping source</p>
              </div>
            ) : (
              <div className="configs-list">
                {newsSourceConfigs.map(config => (
                  <div key={config.id} className="config-card">
                    <div className="config-header">
                      <h4>{config.name}</h4>
                      <span className={`status-badge ${config.status}`}>{config.status}</span>
                    </div>
                    <div className="config-details">
                      <p><strong>Category:</strong> {config.category}</p>
                      <p><strong>Keywords:</strong> {config.keywords.join(', ')}</p>
                      <p><strong>Websites:</strong> {config.source_websites.length} source(s)</p>
                      <p><strong>Last scraped:</strong> {config.last_scraped_at ? new Date(config.last_scraped_at).toLocaleString() : 'Never'}</p>
                    </div>
                    
                    {/* Progress Bar */}
                    {scrapingProgress[config.id] && (
                      <div className="scraping-progress">
                        <div className="progress-info">
                          <span className="progress-message">{scrapingProgress[config.id].message}</span>
                          <span className="progress-percent">{scrapingProgress[config.id].progress}%</span>
                        </div>
                        <div className="progress-bar-container">
                          <div 
                            className={`progress-bar ${scrapingProgress[config.id].status}`}
                            style={{ width: `${scrapingProgress[config.id].progress}%` }}
                          />
                        </div>
                      </div>
                    )}
                    
                    <button 
                      className="btn btn-secondary btn-small"
                      onClick={() => handleTriggerScrape(config.id, config.name)}
                      disabled={scrapingProgress[config.id]}
                      title="Scrape only this configuration"
                    >
                      {scrapingProgress[config.id] ? '⏳ Scraping...' : '🔄 Scrape'}
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {showFullUI && activeTab === 'review' && (
        <div className="review-section">
          <div className="review-header">
            <h3>📰 Review Scraped Articles</h3>
            <div className="review-actions">
              <select 
                value={articleFilter} 
                onChange={(e) => setArticleFilter(e.target.value)}
                className="filter-select"
              >
                <option value="all">All Articles</option>
                <option value="pending">Pending Review</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
                <option value="generated">Generated</option>
              </select>
              {selectedArticles.length > 0 && (
                <button 
                  className="btn btn-primary"
                  onClick={handleBulkApprove}
                  disabled={loading}
                >
                  ✓ Approve Selected ({selectedArticles.length})
                </button>
              )}
            </div>
          </div>

          {loading && <div className="loading">⏳ Loading articles...</div>}

          {!loading && scrapedArticles.length === 0 && (
            <div className="empty-state">
              <div className="empty-state-icon">📭</div>
              <h3>No Scraped Articles Found</h3>
              <p>Set up a news source configuration and trigger scraping to see articles here.</p>
            </div>
          )}

          {!loading && scrapedArticles.length > 0 && (
            <div className="articles-grid">
              {scrapedArticles.map(article => (
                <div key={article.id} className="article-card">
                  {article.status === 'pending' && (
                    <div className="card-checkbox">
                      <input
                        type="checkbox"
                        checked={selectedArticles.includes(article.id)}
                        onChange={() => toggleArticleSelection(article.id)}
                      />
                    </div>
                  )}
                  
                  <div className="article-content">
                    <div className="article-header">
                      <h4>{article.title}</h4>
                      <span className={`status-badge ${article.status}`}>{article.status}</span>
                    </div>
                    
                    <div className="article-meta">
                      <span className="meta-item">🌐 {article.source_website}</span>
                      <span className="meta-item">📁 {article.category}</span>
                      <span className="meta-item">📅 {new Date(article.scraped_at).toLocaleDateString()}</span>
                    </div>

                    {article.matched_keywords && article.matched_keywords.length > 0 && (
                      <div className="keywords-tags">
                        {article.matched_keywords.map((kw, idx) => (
                          <span key={idx} className="keyword-tag">{kw}</span>
                        ))}
                      </div>
                    )}

                    <p className="article-summary">
                      {article.summary || article.content?.substring(0, 200) + '...'}
                    </p>

                    <div className="article-footer">
                      <a 
                        href={article.source_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="source-link"
                      >
                        🔗 View Original
                      </a>
                      
                      {article.image_urls && article.image_urls.length > 0 && (
                        <span className="meta-item">🖼️ {article.image_urls.length} image(s)</span>
                      )}
                      
                      {article.reference_urls && article.reference_urls.length > 0 && (
                        <span className="meta-item">📎 {article.reference_urls.length} reference(s)</span>
                      )}
                    </div>

                    {article.status === 'pending' && (
                      <div className="article-actions">
                        <button 
                          className="action-btn approve"
                          onClick={() => handleApproveArticle(article.id)}
                          disabled={loading}
                        >
                          ✓ Approve & Generate
                        </button>
                        <button 
                          className="action-btn reject"
                          onClick={() => handleRejectArticle(article.id)}
                          disabled={loading}
                        >
                          ✗ Reject
                        </button>
                      </div>
                    )}

                    {article.status === 'approved' && article.ai_article_id && (
                      <div className="article-status-info">
                        ✅ Approved - AI Article ID: {article.ai_article_id.substring(0, 8)}...
                      </div>
                    )}

                    {article.status === 'rejected' && article.rejection_reason && (
                      <div className="article-status-info rejection">
                        ❌ Rejected: {article.rejection_reason}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
