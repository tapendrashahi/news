import React from 'react'

const QualityMetrics = ({ article }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745'
    if (score >= 60) return '#ffc107'
    return '#dc3545'
  }

  return (
    <div className="quality-metrics-panel">
      <h3>Quality Scores</h3>
      <div className="scores-grid">
        <div className="score-item">
          <span>Bias Score:</span>
          <div className="score-bar">
            <div 
              className="score-fill" 
              style={{ width: `${article.bias_score || 0}%`, background: getScoreColor(100 - (article.bias_score || 0)) }}
            />
          </div>
          <strong style={{ color: getScoreColor(100 - (article.bias_score || 0)) }}>
            {article.bias_score || 0}%
          </strong>
        </div>
        
        <div className="score-item">
          <span>Fact Check Score:</span>
          <div className="score-bar">
            <div 
              className="score-fill" 
              style={{ width: `${article.fact_check_score || 0}%`, background: getScoreColor(article.fact_check_score || 0) }}
            />
          </div>
          <strong style={{ color: getScoreColor(article.fact_check_score || 0) }}>
            {article.fact_check_score || 0}%
          </strong>
        </div>
        
        <div className="score-item">
          <span>SEO Score:</span>
          <div className="score-bar">
            <div 
              className="score-fill" 
              style={{ width: `${article.seo_score || 0}%`, background: getScoreColor(article.seo_score || 0) }}
            />
          </div>
          <strong style={{ color: getScoreColor(article.seo_score || 0) }}>
            {article.seo_score || 0}%
          </strong>
        </div>
        
        <div className="score-item">
          <span>Overall Quality:</span>
          <div className="score-bar">
            <div 
              className="score-fill" 
              style={{ width: `${article.overall_quality_score || 0}%`, background: getScoreColor(article.overall_quality_score || 0) }}
            />
          </div>
          <strong style={{ color: getScoreColor(article.overall_quality_score || 0) }}>
            {article.overall_quality_score || 0}%
          </strong>
        </div>
      </div>
      
      {article.perspective_balance_score && (
        <div className="additional-metrics">
          <p>Perspective Balance: {article.perspective_balance_score}%</p>
          <p>Perspectives Covered: {article.perspectives_covered || 'N/A'}</p>
        </div>
      )}
    </div>
  )
}

export default QualityMetrics
