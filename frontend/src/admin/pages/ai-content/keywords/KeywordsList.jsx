import React, { useState, useEffect } from 'react'
import { getKeywords, approveKeyword, rejectKeyword } from '../../../services/aiContentService'
import KeywordScraper from './KeywordScraper'
import './Keywords.css'

const KeywordsList = () => {
  const [keywords, setKeywords] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [showScraper, setShowScraper] = useState(false)
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    fetchKeywords()
  }, [filter])

  const fetchKeywords = async () => {
    setLoading(true)
    try {
      const params = {}
      if (filter !== 'all') params.status = filter
      if (searchTerm) params.search = searchTerm
      
      const response = await getKeywords(params)
      setKeywords(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch keywords:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleKeywordsAdded = (newKeywords) => {
    setShowScraper(false)
    fetchKeywords()
  }

  const handleApprove = async (id) => {
    try {
      await approveKeyword(id)
      fetchKeywords()
    } catch (error) {
      console.error('Failed to approve keyword:', error)
    }
  }

  const handleReject = async (id) => {
    const reason = prompt('Rejection reason (optional):')
    try {
      await rejectKeyword(id, reason)
      fetchKeywords()
    } catch (error) {
      console.error('Failed to reject keyword:', error)
    }
  }

  const getPriorityBadge = (priority) => {
    return <span className={`priority-badge ${priority}`}>{priority}</span>
  }

  const getStatusBadge = (status) => {
    return <span className={`status-badge ${status}`}>{status}</span>
  }

  if (loading) return <div className="loading">⏳ Loading keywords...</div>

  return (
    <div className="keywords-page">
      <div className="keywords-header">
        <h1>📋 Topic Research & Keyword Management</h1>
        <div className="header-actions">
          <button 
            className="btn btn-secondary" 
            onClick={() => setShowModal(true)}
          >
            ⚙️ Setup Configuration
          </button>
          <button 
            className="btn btn-primary" 
            onClick={() => setShowScraper(!showScraper)}
          >
            {showScraper ? '📋 View Topics' : '➕ Add New Topics'}
          </button>
        </div>
      </div>

      {/* Always render KeywordScraper for modal functionality */}
      <KeywordScraper 
        onKeywordsAdded={handleKeywordsAdded} 
        showModal={showModal} 
        setShowModal={setShowModal}
        showFullUI={showScraper}
      />

      {!showScraper && (
        <div className="keywords-list">
        <div className="list-header">
          <div className="filters">
            <div className="filter-group">
              <label>Status</label>
              <select value={filter} onChange={(e) => setFilter(e.target.value)}>
                <option value="all">All Topics</option>
                <option value="pending">Pending Review</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
            <div className="filter-group">
              <label>Search</label>
              <input
                type="text"
                placeholder="Search topics..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && fetchKeywords()}
              />
            </div>
            <div className="filter-group" style={{ justifyContent: 'flex-end' }}>
              <button className="btn btn-secondary" onClick={fetchKeywords}>
                🔄 Refresh
              </button>
            </div>
          </div>
        </div>

        {keywords.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📝</div>
            <h3>No Topics Found</h3>
            <p>Add topics manually or scrape from news websites to get started</p>
          </div>
        ) : (
          <table className="keywords-table">
            <thead>
              <tr>
                <th>Topic / Keyword</th>
                <th>Source</th>
                <th>Category</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Volume</th>
                <th>Score</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {keywords.map(keyword => (
                <tr key={keyword.id}>
                  <td className="keyword-cell">
                    {keyword.keyword}
                    {keyword.source_url && (
                      <div style={{ fontSize: '12px', color: '#6b7280', marginTop: '4px' }}>
                        <a href={keyword.source_url} target="_blank" rel="noopener noreferrer">
                          🔗 Source
                        </a>
                      </div>
                    )}
                  </td>
                  <td>{keyword.source || 'manual'}</td>
                  <td>{keyword.category || 'N/A'}</td>
                  <td>{getPriorityBadge(keyword.priority || 'medium')}</td>
                  <td>{getStatusBadge(keyword.status || 'pending')}</td>
                  <td>{keyword.search_volume || '-'}</td>
                  <td>{keyword.viability_score ? `${keyword.viability_score}%` : '-'}</td>
                  <td className="actions-cell">
                    {keyword.status === 'pending' && (
                      <>
                        <button 
                          className="action-btn approve" 
                          onClick={() => handleApprove(keyword.id)}
                          title="Approve for article generation"
                        >
                          ✓ Approve
                        </button>
                        <button 
                          className="action-btn reject" 
                          onClick={() => handleReject(keyword.id)}
                          title="Reject this topic"
                        >
                          ✗ Reject
                        </button>
                      </>
                    )}
                    {keyword.status === 'approved' && (
                      <button className="action-btn view">
                        📄 View Articles
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        </div>
      )}
    </div>
  )
}

export default KeywordsList
