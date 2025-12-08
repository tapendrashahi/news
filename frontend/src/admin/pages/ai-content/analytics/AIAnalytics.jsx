import React, { useState, useEffect } from 'react'
import { getArticles } from '../../../services/aiContentService'
import './AIAnalytics.css'

const AIAnalytics = () => {
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    failed: 0,
    avgBiasScore: 0,
    avgFactScore: 0,
    avgSeoScore: 0,
    totalCost: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await getArticles({})
      const articles = response.data.results || response.data
      
      const completed = articles.filter(a => a.status === 'completed')
      const failed = articles.filter(a => a.status === 'failed')
      
      const avgBias = completed.reduce((sum, a) => sum + (parseFloat(a.bias_score) || 0), 0) / (completed.length || 1)
      const avgFact = completed.reduce((sum, a) => sum + (parseFloat(a.fact_check_score) || 0), 0) / (completed.length || 1)
      const avgSeo = completed.reduce((sum, a) => sum + (parseFloat(a.seo_score) || 0), 0) / (completed.length || 1)
      const totalCost = articles.reduce((sum, a) => sum + (parseFloat(a.cost_estimate) || 0), 0)
      
      setStats({
        total: articles.length,
        completed: completed.length,
        failed: failed.length,
        avgBiasScore: avgBias.toFixed(1),
        avgFactScore: avgFact.toFixed(1),
        avgSeoScore: avgSeo.toFixed(1),
        totalCost: totalCost.toFixed(2)
      })
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Loading analytics...</div>

  return (
    <div className="ai-analytics-container">
      <div className="page-header">
        <h1>AI Analytics Dashboard</h1>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Articles</h3>
          <div className="stat-value">{stats.total}</div>
        </div>
        <div className="stat-card success">
          <h3>Completed</h3>
          <div className="stat-value">{stats.completed}</div>
        </div>
        <div className="stat-card danger">
          <h3>Failed</h3>
          <div className="stat-value">{stats.failed}</div>
        </div>
        <div className="stat-card">
          <h3>Success Rate</h3>
          <div className="stat-value">
            {stats.total > 0 ? ((stats.completed / stats.total) * 100).toFixed(1) : 0}%
          </div>
        </div>
      </div>

      <div className="quality-metrics">
        <h2>Average Quality Scores</h2>
        <div className="metrics-grid">
          <div className="metric-card">
            <h4>Bias Score</h4>
            <div className="metric-value" style={{ color: stats.avgBiasScore < 20 ? '#28a745' : '#dc3545' }}>
              {stats.avgBiasScore}%
            </div>
            <small>Target: &lt; 20%</small>
          </div>
          <div className="metric-card">
            <h4>Fact Check Score</h4>
            <div className="metric-value" style={{ color: stats.avgFactScore > 80 ? '#28a745' : '#dc3545' }}>
              {stats.avgFactScore}%
            </div>
            <small>Target: &gt; 80%</small>
          </div>
          <div className="metric-card">
            <h4>SEO Score</h4>
            <div className="metric-value" style={{ color: stats.avgSeoScore > 75 ? '#28a745' : '#dc3545' }}>
              {stats.avgSeoScore}%
            </div>
            <small>Target: &gt; 75%</small>
          </div>
        </div>
      </div>

      <div className="cost-section">
        <h2>Cost Analysis</h2>
        <div className="cost-card">
          <div className="cost-item">
            <span>Total API Cost:</span>
            <strong>${stats.totalCost}</strong>
          </div>
          <div className="cost-item">
            <span>Average Cost per Article:</span>
            <strong>${stats.completed > 0 ? (stats.totalCost / stats.completed).toFixed(2) : '0.00'}</strong>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AIAnalytics
