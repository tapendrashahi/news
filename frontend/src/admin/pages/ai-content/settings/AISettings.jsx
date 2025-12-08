import React, { useState, useEffect } from 'react'
import { getConfigs, updateConfig } from '../../../services/aiContentService'
import './AISettings.css'

const AISettings = () => {
  const [configs, setConfigs] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('general')

  useEffect(() => {
    fetchConfigs()
  }, [])

  const fetchConfigs = async () => {
    try {
      const response = await getConfigs()
      setConfigs(response.data)
    } catch (error) {
      console.error('Failed to fetch configs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateConfig = async (id, data) => {
    try {
      await updateConfig(id, data)
      fetchConfigs()
      alert('Settings updated successfully')
    } catch (error) {
      console.error('Failed to update config:', error)
      alert('Failed to update settings')
    }
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="ai-settings-container">
      <div className="page-header">
        <h1>AI Settings</h1>
      </div>

      <div className="settings-tabs">
        {['general', 'api_keys', 'prompts', 'quality'].map(tab => (
          <button
            key={tab}
            className={activeTab === tab ? 'active' : ''}
            onClick={() => setActiveTab(tab)}
          >
            {tab.replace('_', ' ').toUpperCase()}
          </button>
        ))}
      </div>

      <div className="settings-content">
        {activeTab === 'general' && (
          <div className="settings-section">
            <h2>General Settings</h2>
            <div className="form-group">
              <label>Default AI Provider</label>
              <select defaultValue="openai">
                <option value="openai">OpenAI (GPT-4)</option>
                <option value="anthropic">Anthropic (Claude)</option>
              </select>
            </div>
            <div className="form-group">
              <label>Default Model</label>
              <select defaultValue="gpt-4">
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                <option value="claude-3-opus">Claude 3 Opus</option>
              </select>
            </div>
            <div className="form-group">
              <label>Temperature</label>
              <input type="number" step="0.1" min="0" max="2" defaultValue="0.7" />
            </div>
            <button className="btn btn-primary">Save General Settings</button>
          </div>
        )}

        {activeTab === 'api_keys' && (
          <div className="settings-section">
            <h2>API Credentials</h2>
            <p className="warning">⚠️ API keys are stored securely. Only admins can view/edit.</p>
            <div className="form-group">
              <label>OpenAI API Key</label>
              <input type="password" placeholder="sk-..." />
            </div>
            <div className="form-group">
              <label>Anthropic API Key</label>
              <input type="password" placeholder="sk-ant-..." />
            </div>
            <div className="form-group">
              <label>NewsAPI Key</label>
              <input type="password" placeholder="..." />
            </div>
            <button className="btn btn-primary">Save API Keys</button>
          </div>
        )}

        {activeTab === 'prompts' && (
          <div className="settings-section">
            <h2>Prompt Templates</h2>
            <p>Customize AI prompts for different article types</p>
            <div className="form-group">
              <label>System Prompt</label>
              <textarea rows="5" defaultValue="You are AI Analitica, an unbiased news AI..." />
            </div>
            <div className="form-group">
              <label>Article Generation Prompt</label>
              <textarea rows="8" defaultValue="Write a balanced news article about..." />
            </div>
            <button className="btn btn-primary">Save Prompts</button>
          </div>
        )}

        {activeTab === 'quality' && (
          <div className="settings-section">
            <h2>Quality Thresholds</h2>
            <div className="form-group">
              <label>Maximum Bias Score (%)</label>
              <input type="number" min="0" max="100" defaultValue="20" />
            </div>
            <div className="form-group">
              <label>Minimum Fact Check Score (%)</label>
              <input type="number" min="0" max="100" defaultValue="80" />
            </div>
            <div className="form-group">
              <label>Minimum SEO Score (%)</label>
              <input type="number" min="0" max="100" defaultValue="75" />
            </div>
            <div className="form-group">
              <label>Minimum Perspectives Required</label>
              <input type="number" min="1" max="10" defaultValue="2" />
            </div>
            <button className="btn btn-primary">Save Quality Settings</button>
          </div>
        )}
      </div>
    </div>
  )
}

export default AISettings
