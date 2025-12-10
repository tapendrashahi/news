import React, { useState, useEffect } from 'react'
import seoRefinementConfig from '../../../config/seo-refinement-config.json'
import './SEOSettings.css'

const SEOSettings = () => {
  const [config, setConfig] = useState(seoRefinementConfig.seoRefinement)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })

  const handleToggle = (path) => {
    const keys = path.split('.')
    setConfig(prev => {
      const newConfig = JSON.parse(JSON.stringify(prev))
      let current = newConfig
      
      for (let i = 0; i < keys.length - 1; i++) {
        current = current[keys[i]]
      }
      
      current[keys[keys.length - 1]] = !current[keys[keys.length - 1]]
      return newConfig
    })
  }

  const handleInputChange = (path, value) => {
    const keys = path.split('.')
    setConfig(prev => {
      const newConfig = JSON.parse(JSON.stringify(prev))
      let current = newConfig
      
      for (let i = 0; i < keys.length - 1; i++) {
        current = current[keys[i]]
      }
      
      const lastKey = keys[keys.length - 1]
      current[lastKey] = typeof current[lastKey] === 'number' ? parseFloat(value) || 0 : value
      return newConfig
    })
  }

  const handleSave = async () => {
    setSaving(true)
    setMessage({ type: '', text: '' })

    try {
      // Save to backend (you'll need to create this endpoint)
      const response = await fetch('/api/admin/seo-refinement-config/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ seo_refinement: config })
      })

      if (response.ok) {
        setMessage({ type: 'success', text: 'SEO Refinement settings saved successfully!' })
      } else {
        throw new Error('Failed to save settings')
      }
    } catch (error) {
      console.error('Error saving SEO settings:', error)
      setMessage({ type: 'error', text: 'Failed to save settings. Please try again.' })
    } finally {
      setSaving(false)
      setTimeout(() => setMessage({ type: '', text: '' }), 3000)
    }
  }

  return (
    <div className="seo-settings-container">
      <div className="settings-header">
        <h2>SEO Refinement Settings</h2>
        <p className="settings-description">
          Configure automatic SEO refinement for articles that don't meet the target score
        </p>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      {/* Main Configuration */}
      <div className="settings-section">
        <h3>General Settings</h3>
        
        <div className="setting-row">
          <label className="setting-label">
            <input
              type="checkbox"
              checked={config.enabled}
              onChange={() => handleToggle('enabled')}
            />
            <span>Enable SEO Refinement</span>
          </label>
          <p className="setting-help">
            Automatically refine articles that don't meet the SEO target score
          </p>
        </div>

        <div className="setting-row">
          <label className="setting-label">Target SEO Score</label>
          <div className="input-with-help">
            <input
              type="number"
              min="0"
              max="100"
              value={config.targetScore}
              onChange={(e) => handleInputChange('targetScore', e.target.value)}
              disabled={!config.enabled}
            />
            <span className="input-suffix">/ 100</span>
          </div>
          <p className="setting-help">
            Articles with SEO score below this will be refined (recommended: 80)
          </p>
        </div>

        <div className="setting-row">
          <label className="setting-label">Maximum Retries</label>
          <input
            type="number"
            min="1"
            max="10"
            value={config.maxRetries}
            onChange={(e) => handleInputChange('maxRetries', e.target.value)}
            disabled={!config.enabled}
          />
          <p className="setting-help">
            Maximum number of refinement attempts before accepting the article
          </p>
        </div>
      </div>

      {/* Refinement Options */}
      <div className="settings-section">
        <h3>Refinement Options</h3>

        {/* Keyword Density */}
        <div className="option-group">
          <div className="option-header">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.keywordDensity.enabled}
                onChange={() => handleToggle('refinementOptions.keywordDensity.enabled')}
                disabled={!config.enabled}
              />
              <span>Keyword Density Optimization</span>
            </label>
            <span className={`priority-badge ${config.refinementOptions.keywordDensity.priority}`}>
              {config.refinementOptions.keywordDensity.priority}
            </span>
          </div>
          
          <div className="option-details">
            <div className="inline-inputs">
              <div className="input-group">
                <label>Min %</label>
                <input
                  type="number"
                  step="0.1"
                  value={config.refinementOptions.keywordDensity.targetRange.min}
                  onChange={(e) => handleInputChange('refinementOptions.keywordDensity.targetRange.min', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.keywordDensity.enabled}
                />
              </div>
              <div className="input-group">
                <label>Max %</label>
                <input
                  type="number"
                  step="0.1"
                  value={config.refinementOptions.keywordDensity.targetRange.max}
                  onChange={(e) => handleInputChange('refinementOptions.keywordDensity.targetRange.max', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.keywordDensity.enabled}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Internal Linking */}
        <div className="option-group">
          <div className="option-header">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.internalLinking.enabled}
                onChange={() => handleToggle('refinementOptions.internalLinking.enabled')}
                disabled={!config.enabled}
              />
              <span>Internal Linking Suggestions</span>
            </label>
            <span className={`priority-badge ${config.refinementOptions.internalLinking.priority}`}>
              {config.refinementOptions.internalLinking.priority}
            </span>
          </div>
          
          <div className="option-details">
            <div className="inline-inputs">
              <div className="input-group">
                <label>Min Links</label>
                <input
                  type="number"
                  value={config.refinementOptions.internalLinking.minLinks}
                  onChange={(e) => handleInputChange('refinementOptions.internalLinking.minLinks', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.internalLinking.enabled}
                />
              </div>
              <div className="input-group">
                <label>Max Links</label>
                <input
                  type="number"
                  value={config.refinementOptions.internalLinking.maxLinks}
                  onChange={(e) => handleInputChange('refinementOptions.internalLinking.maxLinks', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.internalLinking.enabled}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Meta Description */}
        <div className="option-group">
          <div className="option-header">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.metaDescription.enabled}
                onChange={() => handleToggle('refinementOptions.metaDescription.enabled')}
                disabled={!config.enabled}
              />
              <span>Meta Description Optimization</span>
            </label>
            <span className={`priority-badge ${config.refinementOptions.metaDescription.priority}`}>
              {config.refinementOptions.metaDescription.priority}
            </span>
          </div>
          
          <div className="option-details">
            <div className="inline-inputs">
              <div className="input-group">
                <label>Min Length</label>
                <input
                  type="number"
                  value={config.refinementOptions.metaDescription.minLength}
                  onChange={(e) => handleInputChange('refinementOptions.metaDescription.minLength', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.metaDescription.enabled}
                />
              </div>
              <div className="input-group">
                <label>Max Length</label>
                <input
                  type="number"
                  value={config.refinementOptions.metaDescription.maxLength}
                  onChange={(e) => handleInputChange('refinementOptions.metaDescription.maxLength', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.metaDescription.enabled}
                />
              </div>
            </div>
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.metaDescription.includeKeyword}
                onChange={() => handleToggle('refinementOptions.metaDescription.includeKeyword')}
                disabled={!config.enabled || !config.refinementOptions.metaDescription.enabled}
              />
              <span>Include focus keyword</span>
            </label>
          </div>
        </div>

        {/* Readability */}
        <div className="option-group">
          <div className="option-header">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.readability.enabled}
                onChange={() => handleToggle('refinementOptions.readability.enabled')}
                disabled={!config.enabled}
              />
              <span>Readability Improvements</span>
            </label>
            <span className={`priority-badge ${config.refinementOptions.readability.priority}`}>
              {config.refinementOptions.readability.priority}
            </span>
          </div>
          
          <div className="option-details">
            <div className="input-group">
              <label>Target Score</label>
              <input
                type="number"
                value={config.refinementOptions.readability.targetScore}
                onChange={(e) => handleInputChange('refinementOptions.readability.targetScore', e.target.value)}
                disabled={!config.enabled || !config.refinementOptions.readability.enabled}
              />
            </div>
            <div className="inline-inputs">
              <div className="input-group">
                <label>Max Sentence Length</label>
                <input
                  type="number"
                  value={config.refinementOptions.readability.maxSentenceLength}
                  onChange={(e) => handleInputChange('refinementOptions.readability.maxSentenceLength', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.readability.enabled}
                />
              </div>
              <div className="input-group">
                <label>Max Paragraph Length</label>
                <input
                  type="number"
                  value={config.refinementOptions.readability.maxParagraphLength}
                  onChange={(e) => handleInputChange('refinementOptions.readability.maxParagraphLength', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.readability.enabled}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Title Optimization */}
        <div className="option-group">
          <div className="option-header">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.titleOptimization.enabled}
                onChange={() => handleToggle('refinementOptions.titleOptimization.enabled')}
                disabled={!config.enabled}
              />
              <span>Title Optimization</span>
            </label>
            <span className={`priority-badge ${config.refinementOptions.titleOptimization.priority}`}>
              {config.refinementOptions.titleOptimization.priority}
            </span>
          </div>
          
          <div className="option-details">
            <div className="inline-inputs">
              <div className="input-group">
                <label>Min Length</label>
                <input
                  type="number"
                  value={config.refinementOptions.titleOptimization.minLength}
                  onChange={(e) => handleInputChange('refinementOptions.titleOptimization.minLength', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.titleOptimization.enabled}
                />
              </div>
              <div className="input-group">
                <label>Max Length</label>
                <input
                  type="number"
                  value={config.refinementOptions.titleOptimization.maxLength}
                  onChange={(e) => handleInputChange('refinementOptions.titleOptimization.maxLength', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.titleOptimization.enabled}
                />
              </div>
            </div>
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.titleOptimization.includeKeyword}
                onChange={() => handleToggle('refinementOptions.titleOptimization.includeKeyword')}
                disabled={!config.enabled || !config.refinementOptions.titleOptimization.enabled}
              />
              <span>Include focus keyword</span>
            </label>
          </div>
        </div>

        {/* Content Structure */}
        <div className="option-group">
          <div className="option-header">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.contentStructure.enabled}
                onChange={() => handleToggle('refinementOptions.contentStructure.enabled')}
                disabled={!config.enabled}
              />
              <span>Content Structure</span>
            </label>
            <span className={`priority-badge ${config.refinementOptions.contentStructure.priority}`}>
              {config.refinementOptions.contentStructure.priority}
            </span>
          </div>
          
          <div className="option-details">
            <div className="inline-inputs">
              <div className="input-group">
                <label>Min Word Count</label>
                <input
                  type="number"
                  value={config.refinementOptions.contentStructure.minWordCount}
                  onChange={(e) => handleInputChange('refinementOptions.contentStructure.minWordCount', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.contentStructure.enabled}
                />
              </div>
              <div className="input-group">
                <label>Max Word Count</label>
                <input
                  type="number"
                  value={config.refinementOptions.contentStructure.maxWordCount}
                  onChange={(e) => handleInputChange('refinementOptions.contentStructure.maxWordCount', e.target.value)}
                  disabled={!config.enabled || !config.refinementOptions.contentStructure.enabled}
                />
              </div>
            </div>
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.refinementOptions.contentStructure.headingDistribution}
                onChange={() => handleToggle('refinementOptions.contentStructure.headingDistribution')}
                disabled={!config.enabled || !config.refinementOptions.contentStructure.enabled}
              />
              <span>Optimize heading distribution</span>
            </label>
          </div>
        </div>
      </div>

      {/* Rewrite Stages */}
      <div className="settings-section">
        <h3>Rewrite Strategy</h3>
        <p className="section-description">
          Select which stages should be rewritten when SEO refinement is triggered
        </p>

        <div className="rewrite-stages">
          <div className="stage-option">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.rewriteStages.contentGeneration.rewrite}
                onChange={() => handleToggle('rewriteStages.contentGeneration.rewrite')}
                disabled={!config.enabled}
              />
              <span>Content Generation Stage</span>
            </label>
            <label className="setting-label sub-option">
              <input
                type="checkbox"
                checked={config.rewriteStages.contentGeneration.includeSuggestions}
                onChange={() => handleToggle('rewriteStages.contentGeneration.includeSuggestions')}
                disabled={!config.enabled || !config.rewriteStages.contentGeneration.rewrite}
              />
              <span>Include SEO suggestions in prompt</span>
            </label>
          </div>

          <div className="stage-option">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.rewriteStages.humanization.rewrite}
                onChange={() => handleToggle('rewriteStages.humanization.rewrite')}
                disabled={!config.enabled}
              />
              <span>Humanization Stage</span>
            </label>
            <label className="setting-label sub-option">
              <input
                type="checkbox"
                checked={config.rewriteStages.humanization.includeSuggestions}
                onChange={() => handleToggle('rewriteStages.humanization.includeSuggestions')}
                disabled={!config.enabled || !config.rewriteStages.humanization.rewrite}
              />
              <span>Include SEO suggestions in prompt</span>
            </label>
          </div>

          <div className="stage-option">
            <label className="setting-label">
              <input
                type="checkbox"
                checked={config.rewriteStages.seoOptimization.rewrite}
                onChange={() => handleToggle('rewriteStages.seoOptimization.rewrite')}
                disabled={!config.enabled}
              />
              <span>SEO Optimization Stage</span>
            </label>
            <label className="setting-label sub-option">
              <input
                type="checkbox"
                checked={config.rewriteStages.seoOptimization.includeSuggestions}
                onChange={() => handleToggle('rewriteStages.seoOptimization.includeSuggestions')}
                disabled={!config.enabled}
              />
              <span>Include SEO suggestions in prompt</span>
            </label>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="settings-footer">
        <button
          className="save-button"
          onClick={handleSave}
          disabled={saving || !config.enabled}
        >
          {saving ? 'Saving...' : 'Save SEO Refinement Settings'}
        </button>
      </div>
    </div>
  )
}

export default SEOSettings
