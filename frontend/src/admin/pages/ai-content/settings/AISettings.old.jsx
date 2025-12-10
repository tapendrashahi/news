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
      console.log('Fetched configs response:', response.data)
      
      // Handle both array response and paginated response
      const configsData = Array.isArray(response.data) ? response.data : (response.data.results || [])
      
      setConfigs(configsData)
      
      // Load the default config settings
      if (configsData.length > 0) {
        const defaultConfig = configsData.find(c => c.is_default) || configsData[0]
        console.log('Loading config into form:', defaultConfig)
        
        setGeneralSettings({
          ai_provider: defaultConfig.ai_provider || 'google',
          model_name: defaultConfig.model_name || 'gemini-exp-1206',
          temperature: parseFloat(defaultConfig.temperature) || aiModelsConfig.defaultSettings.temperature.default,
          max_tokens: parseInt(defaultConfig.max_tokens) || aiModelsConfig.defaultSettings.maxTokens.default
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
      const response = await updateConfig(id, data)
      // Update configs state with the returned data
      setConfigs(prevConfigs => 
        prevConfigs.map(c => c.id === id ? response.data : c)
      )
      // Update general settings to reflect the saved values
      setGeneralSettings(prev => ({
        ...prev,
        ...data
      }))
      alert('Settings updated successfully')
      return response
    } catch (error) {
      console.error('Failed to update config:', error)
      alert('Failed to update settings')
      throw error
    }
  }

  const handleSaveGeneral = async () => {
    try {
      const dataToSave = {
        ai_provider: generalSettings.ai_provider,
        model_name: generalSettings.model_name,
        temperature: parseFloat(generalSettings.temperature),
        max_tokens: parseInt(generalSettings.max_tokens)
      }
      
      console.log('Saving data:', dataToSave)
      console.log('Configs available:', configs)
      console.log('Configs is array?', Array.isArray(configs))
      console.log('Configs length:', configs?.length)
      
      if (Array.isArray(configs) && configs.length > 0) {
        // Find the default config or use the first one
        const defaultConfig = configs.find(c => c.is_default) || configs[0]
        console.log('Updating config:', defaultConfig.id, defaultConfig.name)
        // Update existing config
        await handleUpdateConfig(defaultConfig.id, dataToSave)
      } else {
        console.log('No configs found, creating new one')
        // Create new config if none exists - include all required fields
        const timestamp = Date.now()
        const newConfig = {
          name: `Default Configuration ${timestamp}`,
          description: 'Default AI generation configuration',
          template_type: 'analysis',
          ...dataToSave,
          system_prompt: 'You are AI Analitica, an unbiased news AI assistant committed to delivering balanced, fact-based journalism.',
          user_prompt_template: 'Write a comprehensive, balanced news article about {keyword}. Target word count: {word_count} words. Ensure multiple perspectives and fact-based analysis.',
          enabled: true,
          is_default: true
        }
        const response = await updateConfig('', newConfig) // POST request when no ID
        console.log('Config created:', response.data)
        
        // Update state with the new config
        setConfigs([response.data])
        setGeneralSettings({
          ai_provider: response.data.ai_provider,
          model_name: response.data.model_name,
          temperature: parseFloat(response.data.temperature),
          max_tokens: parseInt(response.data.max_tokens)
        })
        alert('Settings saved successfully')
      }
    } catch (error) {
      console.error('Failed to save settings:', error)
      console.error('Error response:', error.response?.data)
      
      // Extract detailed error messages
      const errorData = error.response?.data || {}
      let errorMsg = ''
      
      if (typeof errorData === 'object') {
        // Check for field-specific errors
        const fieldErrors = Object.entries(errorData)
          .filter(([key]) => key !== 'detail')
          .map(([field, messages]) => {
            const msg = Array.isArray(messages) ? messages.join(', ') : messages
            return `${field}: ${msg}`
          })
        
        if (fieldErrors.length > 0) {
          errorMsg = fieldErrors.join('\n')
        } else {
          errorMsg = errorData.detail || JSON.stringify(errorData)
        }
      } else {
        errorMsg = String(errorData)
      }
      
      alert('Failed to save settings:\n' + (errorMsg || error.message))
    }
  }

  const handleProviderChange = (newProvider) => {
    // Get the first model of the new provider
    const providerModels = getModelOptions(newProvider)
    const defaultModel = providerModels.find(m => m.recommended) || providerModels[0]
    
    setGeneralSettings({
      ...generalSettings, 
      ai_provider: newProvider,
      model_name: defaultModel ? defaultModel.value : generalSettings.model_name
    })
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
                onChange={(e) => handleProviderChange(e.target.value)}
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
