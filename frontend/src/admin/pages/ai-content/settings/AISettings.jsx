import React, { useState, useEffect } from 'react'
import { getConfigs, updateConfig } from '../../../services/aiContentService'
import aiModelsConfig from '../../../config/ai-models-config.json'
import './AISettings.css'

const AISettings = () => {
  const [configs, setConfigs] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('general')
  const [generalSettings, setGeneralSettings] = useState({
    ai_provider: 'google',
    model_name: 'gemini-exp-1206',
    temperature: aiModelsConfig.defaultSettings.temperature.default,
    max_tokens: aiModelsConfig.defaultSettings.maxTokens.default
  })

  useEffect(() => {
    fetchConfigs()
  }, [])

  const fetchConfigs = async () => {
    try {
      const response = await getConfigs()
      setConfigs(response.data)
      // Load the first config as general settings
      if (response.data.length > 0) {
        const config = response.data[0]
        setGeneralSettings({
          ai_provider: config.ai_provider || 'google',
          model_name: config.model_name || 'gemini-exp-1206',
          temperature: config.temperature || aiModelsConfig.defaultSettings.temperature.default,
          max_tokens: config.max_tokens || aiModelsConfig.defaultSettings.maxTokens.default
        })
      }
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

  const handleSaveGeneral = async () => {
    if (configs.length > 0) {
      await handleUpdateConfig(configs[0].id, generalSettings)
    }
  }

  const getModelOptions = (provider) => {
    const providerData = aiModelsConfig.providers.find(p => p.id === provider)
    return providerData ? providerData.models : []
  }

  const getProviderOptions = () => {
    return aiModelsConfig.providers.map(provider => ({
      value: provider.id,
      label: provider.name
    }))
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
              <select 
                value={generalSettings.ai_provider}
                onChange={(e) => setGeneralSettings({...generalSettings, ai_provider: e.target.value})}
              >
                {getProviderOptions().map(provider => (
                  <option key={provider.value} value={provider.value}>{provider.label}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Default Model</label>
              <select 
                value={generalSettings.model_name}
                onChange={(e) => setGeneralSettings({...generalSettings, model_name: e.target.value})}
              >
                {getModelOptions(generalSettings.ai_provider).map(model => (
                  <option key={model.value} value={model.value}>
                    {model.label}
                    {model.recommended && ' ⭐ Recommended'}
                  </option>
                ))}
              </select>
              {getModelOptions(generalSettings.ai_provider).find(m => m.value === generalSettings.model_name)?.description && (
                <small className="model-description">
                  {getModelOptions(generalSettings.ai_provider).find(m => m.value === generalSettings.model_name).description}
                </small>
              )}
            </div>
            <div className="form-group">
              <label>Temperature</label>
              <input 
                type="number" 
                step={aiModelsConfig.defaultSettings.temperature.step}
                min={aiModelsConfig.defaultSettings.temperature.min}
                max={aiModelsConfig.defaultSettings.temperature.max}
                value={generalSettings.temperature}
                onChange={(e) => setGeneralSettings({...generalSettings, temperature: parseFloat(e.target.value)})}
              />
              <small>{aiModelsConfig.defaultSettings.temperature.description} ({aiModelsConfig.defaultSettings.temperature.min}-{aiModelsConfig.defaultSettings.temperature.max})</small>
            </div>
            <div className="form-group">
              <label>Max Tokens</label>
              <input 
                type="number" 
                step={aiModelsConfig.defaultSettings.maxTokens.step}
                min={aiModelsConfig.defaultSettings.maxTokens.min}
                max={aiModelsConfig.defaultSettings.maxTokens.max}
                value={generalSettings.max_tokens}
                onChange={(e) => setGeneralSettings({...generalSettings, max_tokens: parseInt(e.target.value)})}
              />
              <small>{aiModelsConfig.defaultSettings.maxTokens.description} ({aiModelsConfig.defaultSettings.maxTokens.min}-{aiModelsConfig.defaultSettings.maxTokens.max})</small>
            </div>
            <button className="btn btn-primary" onClick={handleSaveGeneral}>
              Save General Settings
            </button>
          </div>
        )}

        {activeTab === 'api_keys' && (
          <div className="settings-section">
            <h2>API Credentials</h2>
            <p className="warning">⚠️ API keys are stored securely. Only admins can view/edit.</p>
            <div className="form-group">
              <label>Google API Key (Gemini)</label>
              <input type="password" placeholder="AIza..." />
              <small>Get from: https://aistudio.google.com/app/apikey</small>
            </div>
            <div className="form-group">
              <label>OpenAI API Key</label>
              <input type="password" placeholder="sk-..." />
              <small>Get from: https://platform.openai.com/api-keys</small>
            </div>
            <div className="form-group">
              <label>Anthropic API Key</label>
              <input type="password" placeholder="sk-ant-..." />
              <small>Get from: https://console.anthropic.com/</small>
            </div>
            <div className="form-group">
              <label>NewsAPI Key</label>
              <input type="password" placeholder="..." />
              <small>Get from: https://newsapi.org/</small>
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
