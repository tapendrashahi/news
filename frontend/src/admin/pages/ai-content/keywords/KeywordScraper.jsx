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

export default function KeywordScraper({ onKeywordsAdded, showModal, setShowModal, showFullUI = true, hideConfigurations = false, showConfigsOnly = false }) {
  const [activeTab, setActiveTab] = useState('review')
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
  const [configFilter, setConfigFilter] = useState('all')
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [totalCount, setTotalCount] = useState(0)
  
  // Scraping progress state
  const [scrapingProgress, setScrapingProgress] = useState({})
  
  // Configurations panel visibility
  const [showConfigsPanel, setShowConfigsPanel] = useState(false)

  const categories = [
    'Politics', 'Business', 'Technology', 'Health', 'Education',
    'Entertainment', 'Sports', 'Science', 'Environment', 'Culture'
  ]

  useEffect(() => {
    loadScrapedArticles()
    loadNewsSourceConfigs()
    
    // Listen for scrape all trigger from header
    const handleScrapeAllEvent = () => {
      handleScrapeAll()
    }
    
    window.addEventListener('triggerScrapeAll', handleScrapeAllEvent)
    return () => window.removeEventListener('triggerScrapeAll', handleScrapeAllEvent)
  }, [articleFilter, configFilter, currentPage])

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
      const params = { page: currentPage }
      
      // Add status filter
      if (articleFilter !== 'all') {
        params.status = articleFilter
      }
      
      // Add configuration filter
      if (configFilter !== 'all') {
        params.source_config = configFilter
      }
      
      const response = await getScrapedArticles(params)
      
      // Handle paginated response
      if (response.data.results) {
        setScrapedArticles(response.data.results)
        setTotalCount(response.data.count || 0)
        setTotalPages(Math.ceil((response.data.count || 0) / 50)) // 50 per page
      } else {
        setScrapedArticles(response.data)
        setTotalCount(response.data.length)
        setTotalPages(1)
      }
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
      console.error('Configuration creation error:', error)
      console.error('Error response:', error.response)
      
      let errorMessage = 'Failed to create configuration'
      
      if (error.response?.data) {
        // Handle validation errors
        if (typeof error.response.data === 'object') {
          const errors = Object.entries(error.response.data)
            .map(([field, messages]) => {
              const msgs = Array.isArray(messages) ? messages : [messages]
              return `${field}: ${msgs.join(', ')}`
            })
            .join('; ')
          errorMessage = errors || errorMessage
        } else if (error.response.data.detail) {
          errorMessage = error.response.data.detail
        } else if (typeof error.response.data === 'string') {
          errorMessage = error.response.data
        }
      }
      
      setMessage({ 
        type: 'error', 
        text: errorMessage
      })
    } finally {
      setLoading(false)
    }
  }

  const handleScrapeAll = async () => {
    // Reload and get latest configs
    let activeConfigs = newsSourceConfigs.filter(c => c.status === 'active')
    
    // If no configs loaded yet, fetch them
    if (newsSourceConfigs.length === 0) {
      try {
        const response = await getNewsSources()
        const configs = response.data.results || response.data
        setNewsSourceConfigs(configs)
        activeConfigs = configs.filter(c => c.status === 'active')
      } catch (error) {
        setMessage({ type: 'error', text: 'Failed to load configurations' })
        return
      }
    }
    
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
      [configId]: { 
        status: 'starting', 
        progress: 0, 
        message: 'Initializing scraper...',
        articlesFound: 0,
        articlesCreated: 0
      }
    }))
    
    try {
      // Update progress to scraping
      setScrapingProgress(prev => ({
        ...prev,
        [configId]: { 
          status: 'scraping', 
          progress: 30, 
          message: 'Searching for articles on websites...',
          articlesFound: 0,
          articlesCreated: 0
        }
      }))
      
      const response = await triggerScrape(configId)
      
      // Update progress with actual results
      setScrapingProgress(prev => ({
        ...prev,
        [configId]: { 
          status: 'complete', 
          progress: 100, 
          message: 'Scraping completed!',
          articlesFound: response.data.total_found || 0,
          articlesCreated: response.data.articles_created || 0
        }
      }))
      
      setMessage({ 
        type: 'success', 
        text: `✅ Found ${response.data.total_found || 0} articles, saved ${response.data.articles_created || 0} new articles for "${configName}"` 
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
      
    } catch (error) {
      console.error('Scraping error:', error)
      console.error('Error response:', error.response)
      
      let errorMessage = 'Failed to trigger scraping'
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      } else if (error.message) {
        errorMessage = error.message
      } else if (error.code === 'ECONNABORTED') {
        errorMessage = 'Scraping timeout - the operation took too long'
      } else if (!error.response) {
        errorMessage = 'Network error - cannot connect to server'
      }
      
      setScrapingProgress(prev => ({
        ...prev,
        [configId]: { 
          status: 'error', 
          progress: 0, 
          message: `Failed: ${errorMessage}`,
          articlesFound: 0,
          articlesCreated: 0
        }
      }))
      
      setMessage({ 
        type: 'error', 
        text: `❌ Scraping failed for "${configName}": ${errorMessage}` 
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
      {showFullUI && !showConfigsOnly && (
        <>
          <div className="scraper-tabs">
            <button 
              className={`tab active`}
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
                      <option value="Politics">Politics</option>
                      <option value="Business">Business</option>
                      <option value="Technology">Technology</option>
                      <option value="Health">Health</option>
                      <option value="Education">Education</option>
                      <option value="Entertainment">Entertainment</option>
                      <option value="Sports">Sports</option>
                      <option value="Science">Science</option>
                      <option value="Environment">Environment</option>
                      <option value="Culture">Culture</option>
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

      {showConfigsOnly && (
        <div className="scrape-page">
          <div className="configurations-section">
            <div className="configs-management-page">
                <div className="configs-page-header">
                  <div>
                    <h2>⚙️ Manage Configurations</h2>
                    <p className="subtitle">View, edit, and manage all your news scraping configurations</p>
                  </div>
                  {newsSourceConfigs.filter(c => c.status === 'active').length > 0 && (
                    <button
                      className="btn btn-primary btn-large"
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
                    <p>Click "➕ Setup Configuration" in the header to create your first news scraping source</p>
                  </div>
                ) : (
                  <div className="configs-full-list">
                    {newsSourceConfigs.map(config => (
                      <div key={config.id} className="config-card-full">
                        <div className="config-card-header">
                          <div>
                            <h3>{config.name}</h3>
                            <span className={`status-badge ${config.status}`}>{config.status}</span>
                          </div>
                          <div className="config-actions">
                            <button 
                              className="btn btn-primary"
                              onClick={() => handleTriggerScrape(config.id, config.name)}
                              disabled={scrapingProgress[config.id]}
                            >
                              {scrapingProgress[config.id] ? '⏳ Scraping...' : '🔄 Scrape Now'}
                            </button>
                            <button className="btn btn-secondary">
                              ✏️ Edit
                            </button>
                            <button className="btn btn-danger">
                              🗑️ Delete
                            </button>
                          </div>
                        </div>
                        
                        <div className="config-details-grid">
                          <div className="detail-item">
                            <span className="detail-label">Category:</span>
                            <span className="detail-value">{config.category}</span>
                          </div>
                          <div className="detail-item">
                            <span className="detail-label">Keywords:</span>
                            <span className="detail-value">{config.keywords.join(', ')}</span>
                          </div>
                          <div className="detail-item">
                            <span className="detail-label">Websites:</span>
                            <div className="detail-value">
                              {config.source_websites.map((site, idx) => (
                                <div key={idx} className="website-tag">{site}</div>
                              ))}
                            </div>
                          </div>
                          <div className="detail-item">
                            <span className="detail-label">Max Articles:</span>
                            <span className="detail-value">{config.max_articles_per_scrape}</span>
                          </div>
                          <div className="detail-item">
                            <span className="detail-label">Last Scraped:</span>
                            <span className="detail-value">
                              {config.last_scraped_at ? new Date(config.last_scraped_at).toLocaleString() : 'Never'}
                            </span>
                          </div>
                          <div className="detail-item">
                            <span className="detail-label">Created:</span>
                            <span className="detail-value">
                              {new Date(config.created_at).toLocaleString()}
                            </span>
                          </div>
                        </div>

                        {/* Progress Bar */}
                        {scrapingProgress[config.id] && (
                          <div className="scraping-progress" style={{ marginTop: '16px' }}>
                            <div className="progress-info">
                              <span className="progress-message">
                                {scrapingProgress[config.id].message}
                                {scrapingProgress[config.id].status === 'complete' && (
                                  <span className="article-count">
                                    {' '}📰 Found: {scrapingProgress[config.id].articlesFound} | ✅ New: {scrapingProgress[config.id].articlesCreated}
                                  </span>
                                )}
                              </span>
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
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
      )}

      {showFullUI && activeTab === 'review' && (
        <div className="review-section">
          <div className="review-header">
            <h3>📰 Review Scraped Articles</h3>
            <div className="review-actions">
              <select 
                value={configFilter} 
                onChange={(e) => {
                  setConfigFilter(e.target.value)
                  setCurrentPage(1) // Reset to page 1 when filter changes
                }}
                className="filter-select"
              >
                <option value="all">All Configurations</option>
                {newsSourceConfigs.map(config => (
                  <option key={config.id} value={config.id}>{config.name}</option>
                ))}
              </select>
              <select 
                value={articleFilter} 
                onChange={(e) => {
                  setArticleFilter(e.target.value)
                  setCurrentPage(1) // Reset to page 1 when filter changes
                }}
                className="filter-select"
              >
                <option value="all">All Status</option>
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

          {/* Scraping Progress Display */}
          {Object.keys(scrapingProgress).length > 0 && (
            <div className="active-scraping-container">
              {Object.entries(scrapingProgress).map(([configId, progress]) => {
                const config = newsSourceConfigs.find(c => c.id === configId)
                return (
                  <div key={configId} className="scraping-progress-card">
                    <div className="scraping-header">
                      <span className="scraping-config-name">🔄 {config?.name || 'Unknown Source'}</span>
                      <span className="progress-percent">{progress.progress}%</span>
                    </div>
                    <div className="progress-bar-container">
                      <div 
                        className={`progress-bar ${progress.status}`}
                        style={{ width: `${progress.progress}%` }}
                      />
                    </div>
                    <div className="scraping-status">
                      <span className="progress-message">
                        {progress.message}
                        {progress.status === 'complete' && (
                          <span className="article-count">
                            {' '}📰 Found: {progress.articlesFound} | ✅ New: {progress.articlesCreated}
                          </span>
                        )}
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>
          )}

          {loading && <div className="loading">⏳ Loading articles...</div>}

          {!loading && scrapedArticles.length === 0 && (
            <div className="empty-state">
              <div className="empty-state-icon">📭</div>
              <h3>No Scraped Articles Found</h3>
              <p>Set up a news source configuration and trigger scraping to see articles here.</p>
            </div>
          )}

          {!loading && scrapedArticles.length > 0 && (
            <div className="articles-list-view">
              {scrapedArticles.map(article => (
                <div key={article.id} className={`article-row ${
                  selectedArticles.includes(article.id) ? 'selected' : ''
                }`}>
                  <div className="article-checkbox">
                    {article.status === 'pending' && (
                      <input
                        type="checkbox"
                        checked={selectedArticles.includes(article.id)}
                        onChange={() => toggleArticleSelection(article.id)}
                      />
                    )}
                  </div>
                  <div className="article-main">
                    <h3 className="article-title">{article.title}</h3>
                    <p className="article-summary">{article.summary || article.content?.substring(0, 200) + '...'}</p>
                    <div className="scraped-article-meta">
                      <span className="meta-item">
                        <strong>Source:</strong> {article.source_website}
                      </span>
                      <span className="meta-item">
                        <strong>Category:</strong> {article.category}
                      </span>
                      <span className="meta-item">
                        <strong>Author:</strong> {article.author || 'Unknown'}
                      </span>
                      <span className="meta-item">
                        <strong>Date:</strong> {article.published_date ? new Date(article.published_date).toLocaleDateString() : 'N/A'}
                      </span>
                      <span className="meta-item">
                        <strong>Status:</strong> <span className={`status-badge ${article.status}`}>{article.status}</span>
                      </span>
                    </div>
                    <div className="article-tags">
                      {article.matched_keywords?.map((keyword, idx) => (
                        <span key={idx} className="keyword-tag">{keyword}</span>
                      ))}
                    </div>
                    {article.image_urls && article.image_urls.length > 0 && (
                      <div className="article-images-count">
                        🖼️ {article.image_urls.length} image(s)
                      </div>
                    )}
                  </div>
                  <div className="article-actions-col">
                    {article.status === 'pending' && (
                      <>
                        <button 
                          className="btn btn-primary btn-small"
                          onClick={() => handleApproveArticle(article.id)}
                          disabled={loading}
                        >
                          ✓ Approve
                        </button>
                        <button 
                          className="btn btn-danger btn-small"
                          onClick={() => handleRejectArticle(article.id)}
                          disabled={loading}
                        >
                          ✗ Reject
                        </button>
                      </>
                    )}
                    <a 
                      href={article.source_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="btn btn-secondary btn-small"
                    >
                      🔗 View Source
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
          
          {/* Pagination Controls */}
          {!loading && scrapedArticles.length > 0 && totalPages > 1 && (
            <div className="pagination-controls">
              <div className="pagination-info">
                Showing {((currentPage - 1) * 50) + 1} - {Math.min(currentPage * 50, totalCount)} of {totalCount} articles
              </div>
              <div className="pagination-buttons">
                <button
                  className="btn btn-small"
                  onClick={() => setCurrentPage(1)}
                  disabled={currentPage === 1}
                >
                  « First
                </button>
                <button
                  className="btn btn-small"
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                >
                  ‹ Previous
                </button>
                <span className="page-indicator">
                  Page {currentPage} of {totalPages}
                </span>
                <button
                  className="btn btn-small"
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                  disabled={currentPage === totalPages}
                >
                  Next ›
                </button>
                <button
                  className="btn btn-small"
                  onClick={() => setCurrentPage(totalPages)}
                  disabled={currentPage === totalPages}
                >
                  Last »
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
