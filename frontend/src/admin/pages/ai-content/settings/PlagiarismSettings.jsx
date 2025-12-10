import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './PlagiarismSettings.css'

const PlagiarismSettings = () => {
  const [config, setConfig] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState(null)

  useEffect(() => {
    fetchConfig()
  }, [])

  const fetchConfig = async () => {
    try {
      const response = await axios.get('/api/admin/plagiarism-config/')
      setConfig(response.data)
    } catch (error) {
      console.error('Failed to fetch plagiarism config:', error)
      setMessage({ type: 'error', text: 'Failed to load configuration' })
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    setMessage(null)

    try {
      const response = await axios.post('/api/admin/plagiarism-config/', config)
      if (response.data.success) {
        setMessage({ type: 'success', text: 'Configuration saved successfully!' })
      }
    } catch (error) {
      console.error('Failed to save plagiarism config:', error)
      setMessage({ type: 'error', text: 'Failed to save configuration' })
    } finally {
      setSaving(false)
    }
  }

  const updateConfig = (path, value) => {
    setConfig(prevConfig => {
      const newConfig = { ...prevConfig }
      const keys = path.split('.')
      let current = newConfig
      
      for (let i = 0; i < keys.length - 1; i++) {
        current = current[keys[i]]
      }
      
      current[keys[keys.length - 1]] = value
      return newConfig
    })
  }

  if (loading) {
    return <div className="plagiarism-settings-loading">Loading plagiarism settings...</div>
  }

  if (!config) {
    return <div className="plagiarism-settings-error">Failed to load configuration</div>
  }

  const plagiarismCheck = config.plagiarism_check

  return (
    <div className="plagiarism-settings">
      <div className="settings-header">
        <h2>Plagiarism Check Configuration</h2>
        <p className="section-description">
          Configure plagiarism detection using Codequiry API. Content with plagiarism score above the threshold will be automatically rewritten.
        </p>
      </div>

      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      {/* Enable/Disable Plagiarism Check */}
      <div className="settings-section">
        <div className="section-header">
          <h3>Plagiarism Detection</h3>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={plagiarismCheck.enabled}
              onChange={(e) => updateConfig('plagiarism_check.enabled', e.target.checked)}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>
        <p className="section-info">
          {plagiarismCheck.enabled 
            ? '✅ Plagiarism checking is enabled. Articles will be checked before publication.' 
            : '⚠️ Plagiarism checking is disabled. Articles will not be checked for plagiarism.'}
        </p>
      </div>

      {/* Threshold Configuration */}
      <div className="settings-section">
        <div className="section-header">
          <h3>Plagiarism Threshold</h3>
        </div>
        <p className="section-info">
          Articles with plagiarism score above this threshold will be flagged and rewritten.
          Lower values mean stricter plagiarism detection.
        </p>
        
        <div className="threshold-control">
          <div className="threshold-slider">
            <label>Maximum Allowed Plagiarism: {plagiarismCheck.threshold}%</label>
            <input
              type="range"
              min="0"
              max="20"
              step="0.5"
              value={plagiarismCheck.threshold}
              onChange={(e) => updateConfig('plagiarism_check.threshold', parseFloat(e.target.value))}
              className="slider"
            />
            <div className="slider-labels">
              <span>0% (Strictest)</span>
              <span>5% (Recommended)</span>
              <span>10%</span>
              <span>20% (Lenient)</span>
            </div>
          </div>
          
          <div className="threshold-info">
            <div className={`threshold-indicator ${plagiarismCheck.threshold <= 5 ? 'strict' : plagiarismCheck.threshold <= 10 ? 'moderate' : 'lenient'}`}>
              {plagiarismCheck.threshold <= 5 && '🔒 Strict - High originality required'}
              {plagiarismCheck.threshold > 5 && plagiarismCheck.threshold <= 10 && '⚖️ Moderate - Balanced approach'}
              {plagiarismCheck.threshold > 10 && '🔓 Lenient - Some similarity allowed'}
            </div>
          </div>
        </div>

        <div className="form-group">
          <label>Maximum Retry Attempts</label>
          <input
            type="number"
            min="1"
            max="5"
            value={plagiarismCheck.maxRetries}
            onChange={(e) => updateConfig('plagiarism_check.maxRetries', parseInt(e.target.value))}
            className="small-input"
          />
          <span className="input-hint">Number of rewrite attempts if plagiarism is detected (1-5)</span>
        </div>
      </div>

      {/* Check Options */}
      <div className="settings-section">
        <div className="section-header">
          <h3>Check Options</h3>
        </div>
        
        <div className="options-grid">
          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.checkOptions.checkWeb.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.checkOptions.checkWeb.enabled', e.target.checked)}
                />
                <span>Check Web Sources</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.checkOptions.checkWeb.description}
            </p>
          </div>

          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.checkOptions.checkDatabase.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.checkOptions.checkDatabase.enabled', e.target.checked)}
                />
                <span>Check Database</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.checkOptions.checkDatabase.description}
            </p>
          </div>

          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.checkOptions.autoRewrite.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.checkOptions.autoRewrite.enabled', e.target.checked)}
                />
                <span>Auto Rewrite</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.checkOptions.autoRewrite.description}
            </p>
          </div>
        </div>
      </div>

      {/* Rewrite Strategy */}
      <div className="settings-section">
        <div className="section-header">
          <h3>Rewrite Strategy</h3>
        </div>
        <p className="section-info">
          Configure how plagiarized content should be rewritten to ensure originality while maintaining quality.
        </p>
        
        <div className="options-grid">
          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.rewriteStrategy.rewriteSections.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.rewriteStrategy.rewriteSections.enabled', e.target.checked)}
                />
                <span>Rewrite Plagiarized Sections</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.rewriteStrategy.rewriteSections.description}
            </p>
          </div>

          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.rewriteStrategy.rewriteEntireArticle.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.rewriteStrategy.rewriteEntireArticle.enabled', e.target.checked)}
                />
                <span>Rewrite Entire Article</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.rewriteStrategy.rewriteEntireArticle.description}
            </p>
          </div>

          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.rewriteStrategy.maintainSEO.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.rewriteStrategy.maintainSEO.enabled', e.target.checked)}
                />
                <span>Maintain SEO</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.rewriteStrategy.maintainSEO.description}
            </p>
          </div>

          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.rewriteStrategy.maintainNepalContext.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.rewriteStrategy.maintainNepalContext.enabled', e.target.checked)}
                />
                <span>Maintain Nepal Context</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.rewriteStrategy.maintainNepalContext.description}
            </p>
          </div>
        </div>
      </div>

      {/* Report Options */}
      <div className="settings-section">
        <div className="section-header">
          <h3>Report Options</h3>
        </div>
        
        <div className="options-grid">
          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.reportOptions.saveReports.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.reportOptions.saveReports.enabled', e.target.checked)}
                />
                <span>Save Reports</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.reportOptions.saveReports.description}
            </p>
          </div>

          <div className="option-card">
            <div className="option-header">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={plagiarismCheck.reportOptions.detailedMatches.enabled}
                  onChange={(e) => updateConfig('plagiarism_check.reportOptions.detailedMatches.enabled', e.target.checked)}
                />
                <span>Detailed Matches</span>
              </label>
            </div>
            <p className="option-description">
              {plagiarismCheck.reportOptions.detailedMatches.description}
            </p>
          </div>
        </div>
      </div>

      {/* API Status */}
      <div className="settings-section">
        <div className="section-header">
          <h3>API Status</h3>
        </div>
        
        <div className="api-status">
          <div className="status-item">
            <span className="status-label">Codequiry API Key:</span>
            <span className="status-badge configured">✅ Configured</span>
          </div>
          <div className="status-info">
            <p>API key is set in environment variables (.env file)</p>
            <code>CODEQUIRY_API_KEY=84c86ced...a3554</code>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="settings-actions">
        <button 
          className="save-button"
          onClick={handleSave}
          disabled={saving}
        >
          {saving ? 'Saving...' : 'Save Configuration'}
        </button>
      </div>
    </div>
  )
}

export default PlagiarismSettings
