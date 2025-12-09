import React from 'react'
import './QualityMetrics.css'

const QualityMetrics = ({ article }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745'
    if (score >= 60) return '#ffc107'
    return '#dc3545'
  }

  const metrics = [
    {
      label: 'Overall Quality',
      value: article.overall_quality_score,
      icon: '⭐'
    },
    {
      label: 'SEO Score',
      value: article.seo_score,
      icon: '🎯'
    },
    {
      label: 'Bias Score',
      value: article.bias_score,
      icon: '⚖️',
      invert: true
    },
    {
      label: 'AI Detection',
      value: article.ai_detection_score,
      icon: '🤖',
      invert: true
    },
    {
      label: 'Plagiarism',
      value: article.plagiarism_score,
      icon: '📋',
      invert: true
    }
  ]

  return (
    <div className="quality-metrics">
      <h3>Quality Metrics</h3>
      <div className="metrics-grid">
        {metrics.map((metric, idx) => {
          if (metric.value === null || metric.value === undefined) return null
          
          const displayValue = metric.invert ? 100 - metric.value : metric.value
          const color = getScoreColor(displayValue)
          
          return (
            <div key={idx} className="metric-card">
              <div className="metric-icon">{metric.icon}</div>
              <div className="metric-info">
                <div className="metric-label">{metric.label}</div>
                <div className="metric-value" style={{ color }}>
                  {Math.round(metric.value)}%
                </div>
              </div>
              <div className="metric-bar">
                <div 
                  className="metric-bar-fill" 
                  style={{ 
                    width: `${displayValue}%`,
                    background: color
                  }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default QualityMetrics
