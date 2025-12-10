import React, { useState, useEffect } from 'react'
import { getConfigs, updateConfig } from '../../../services/aiContentService'
import aiModelsConfig from '../../../config/ai-models-config.json'
import SEOSettings from './SEOSettings'
import PlagiarismSettings from './PlagiarismSettings'
import './AISettings.css'

const AISettings = () => {
  const [configs, setConfigs] = useState([])
  const [loading, setLoading] = useState(true)
  const [savingStages, setSavingStages] = useState(false)
  const [activeTab, setActiveTab] = useState('general')
  
  // Pipeline stages configuration
  const pipelineStages = [
    { id: 'keyword_analysis', label: 'Keyword Analysis', description: 'Analyze keyword and plan article approach' },
    { id: 'research', label: 'Research', description: 'Gather sources and data (non-LLM stage)' },
    { id: 'outline', label: 'Outline', description: 'Create structured article outline' },
    { id: 'content_generation', label: 'Content Generation', description: 'Write full article content' },
    { id: 'humanization', label: 'Humanization', description: 'Make content natural and readable' },
    { id: 'ai_detection', label: 'AI Detection', description: 'Check AI detection scores' },
    { id: 'plagiarism_check', label: 'Plagiarism Check', description: 'Verify content originality (non-LLM stage)' },
    { id: 'bias_detection', label: 'Bias Detection', description: 'Analyze political and emotional bias' },
    { id: 'fact_verification', label: 'Fact Verification', description: 'Verify factual claims' },
    { id: 'perspective_analysis', label: 'Perspective Analysis', description: 'Analyze viewpoint coverage' },
    { id: 'seo_optimization', label: 'SEO Optimization', description: 'Optimize for search engines' },
    { id: 'meta_generation', label: 'Meta Generation', description: 'Generate meta tags and descriptions' },
    { id: 'image_generation', label: 'Image Generation', description: 'Generate featured image (non-LLM stage)' },
    { id: 'finalization', label: 'Finalization', description: 'Final quality checks and save' }
  ]
  
  const [generalSettings, setGeneralSettings] = useState({
    ai_provider: 'google',
    model_name: 'gemini-exp-1206',
    temperature: aiModelsConfig.defaultSettings.temperature.default,
    max_tokens: aiModelsConfig.defaultSettings.maxTokens.default
  })
  
  const [stageConfigs, setStageConfigs] = useState({})

  useEffect(() => {
    fetchConfigs()
  }, [])

  const fetchConfigs = async () => {
    try {
      const response = await getConfigs()
      const configsData = Array.isArray(response.data) ? response.data : (response.data.results || [])
      
      setConfigs(configsData)
      
      if (configsData.length > 0) {
        const defaultConfig = configsData.find(c => c.is_default) || configsData[0]
        
        setGeneralSettings({
          ai_provider: defaultConfig.ai_provider || 'google',
          model_name: defaultConfig.model_name || 'gemini-exp-1206',
          temperature: parseFloat(defaultConfig.temperature) || aiModelsConfig.defaultSettings.temperature.default,
          max_tokens: parseInt(defaultConfig.max_tokens) || aiModelsConfig.defaultSettings.maxTokens.default
        })
        
        // Load stage configs
        setStageConfigs(defaultConfig.stage_configs || {})
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
      setConfigs(prevConfigs => 
        prevConfigs.map(c => c.id === id ? response.data : c)
      )
      setGeneralSettings(prev => ({
        ...prev,
        ...data
      }))
      if (data.stage_configs) {
        setStageConfigs(data.stage_configs)
      }
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
      
      if (Array.isArray(configs) && configs.length > 0) {
        const defaultConfig = configs.find(c => c.is_default) || configs[0]
        await handleUpdateConfig(defaultConfig.id, dataToSave)
      } else {
        const timestamp = Date.now()
        const newConfig = {
          name: `Default Configuration ${timestamp}`,
          description: 'Default AI generation configuration',
          template_type: 'analysis',
          ...dataToSave,
          system_prompt: 'You are AI Analitica, an unbiased news AI assistant committed to delivering balanced, fact-based journalism.',
          user_prompt_template: 'Write an objective news analysis article about {keyword} with approximately {word_count} words.',
          enabled: true,
          is_default: true
        }
        const response = await updateConfig('', newConfig)
        setConfigs([response.data])
      }
    } catch (error) {
      console.error('Error saving general settings:', error)
    }
  }

  const handleSaveStageConfigs = async () => {
    if (savingStages) return // Prevent multiple simultaneous saves
    
    setSavingStages(true)
    try {
      if (Array.isArray(configs) && configs.length > 0) {
        const defaultConfig = configs.find(c => c.is_default) || configs[0]
        await handleUpdateConfig(defaultConfig.id, { stage_configs: stageConfigs })
        console.log('Stage configs saved successfully:', stageConfigs)
      } else {
        alert('No configuration found. Please save general settings first.')
      }
    } catch (error) {
      console.error('Error saving stage configs:', error)
      alert('Failed to save stage settings. Please try again.')
    } finally {
      setSavingStages(false)
    }
  }

  const handleStageConfigChange = (stageId, field, value) => {
    setStageConfigs(prev => ({
      ...prev,
      [stageId]: {
        ...(prev[stageId] || {}),
        [field]: value
      }
    }))
  }

  const handleProviderChange = (newProvider) => {
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

  const getImageModelOptions = (provider) => {
    const providerData = aiModelsConfig.providers.find(p => p.id === provider)
    return providerData ? providerData.imageModels : []
  }

  const getProviderOptions = () => {
    return aiModelsConfig.providers.map(provider => ({
      value: provider.id,
      label: provider.name
    }))
  }

  const getImageProviderOptions = () => {
    return aiModelsConfig.providers
      .filter(p => p.imageModels && p.imageModels.length > 0)
      .map(provider => ({
        value: provider.id,
        label: provider.name
      }))
  }

  const clearStageConfig = (stageId) => {
    const newStageConfigs = { ...stageConfigs }
    delete newStageConfigs[stageId]
    setStageConfigs(newStageConfigs)
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="ai-settings-container">
      <div className="page-header">
        <h1>AI Settings</h1>
        <p className="subtitle">Configure AI providers and models for each pipeline stage</p>
      </div>

      <div className="settings-tabs">
        {['general', 'stages', 'seo', 'plagiarism', 'api_keys', 'prompts', 'quality'].map(tab => (
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
            <h2>Default Settings</h2>
            <p className="section-description">
              These settings will be used for all stages unless overridden in the "Stages" tab.
            </p>
            
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
              Save Default Settings
            </button>
          </div>
        )}

        {activeTab === 'stages' && (
          <div className="settings-section">
            <div className="section-header">
              <div>
                <h2>Per-Stage Configuration</h2>
                <p className="section-description">
                  Customize AI provider and model for each pipeline stage. Leave empty to use default settings.
                </p>
              </div>
              <button 
                className="btn btn-primary" 
                onClick={handleSaveStageConfigs}
                disabled={savingStages}
              >
                {savingStages ? 'Saving...' : 'Save Stage Settings'}
              </button>
            </div>
            
            <div className="stages-grid">
              {pipelineStages.map((stage) => {
                const stageConfig = stageConfigs[stage.id] || {}
                const hasConfig = stageConfig.provider && stageConfig.model
                
                return (
                  <div key={stage.id} className={`stage-card ${hasConfig ? 'configured' : ''}`}>
                    <div className="stage-header">
                      <div>
                        <h3>{stage.label}</h3>
                        <p className="stage-description">{stage.description}</p>
                      </div>
                      {hasConfig && (
                        <button 
                          className="btn-clear"
                          onClick={() => clearStageConfig(stage.id)}
                          title="Use default settings"
                        >
                          ✕
                        </button>
                      )}
                    </div>
                    
                    {/* Only show config for LLM-based stages */}
                    {!['research', 'plagiarism_check'].includes(stage.id) && stage.id !== 'image_generation' && (
                      <div className="stage-config">
                        <div className="form-row">
                          <div className="form-group">
                            <label>Provider</label>
                            <select 
                              value={stageConfig.provider || ''}
                              onChange={(e) => {
                                const newProvider = e.target.value
                                if (newProvider) {
                                  const models = getModelOptions(newProvider)
                                  const defaultModel = models.find(m => m.recommended) || models[0]
                                  handleStageConfigChange(stage.id, 'provider', newProvider)
                                  handleStageConfigChange(stage.id, 'model', defaultModel?.value || '')
                                } else {
                                  clearStageConfig(stage.id)
                                }
                              }}
                            >
                              <option value="">Use Default</option>
                              {getProviderOptions().map(provider => (
                                <option key={provider.value} value={provider.value}>
                                  {provider.label}
                                </option>
                              ))}
                            </select>
                          </div>
                          
                          {stageConfig.provider && (
                            <div className="form-group">
                              <label>Model</label>
                              <select 
                                value={stageConfig.model || ''}
                                onChange={(e) => handleStageConfigChange(stage.id, 'model', e.target.value)}
                              >
                                {getModelOptions(stageConfig.provider).map(model => (
                                  <option key={model.value} value={model.value}>
                                    {model.label}
                                    {model.recommended && ' ⭐'}
                                  </option>
                                ))}
                              </select>
                            </div>
                          )}
                        </div>
                        
                        {!hasConfig && (
                          <div className="default-indicator">
                            Using default: <strong>{generalSettings.ai_provider}</strong> / <strong>{generalSettings.model_name}</strong>
                          </div>
                        )}
                      </div>
                    )}
                    
                    {/* Image generation stage with special image model selection */}
                    {stage.id === 'image_generation' && (
                      <div className="stage-config">
                        <div className="form-row">
                          <div className="form-group">
                            <label>Image Provider</label>
                            <select 
                              value={stageConfig.provider || ''}
                              onChange={(e) => {
                                const newProvider = e.target.value
                                if (newProvider) {
                                  const models = getImageModelOptions(newProvider)
                                  const defaultModel = models.find(m => m.recommended) || models[0]
                                  handleStageConfigChange(stage.id, 'provider', newProvider)
                                  handleStageConfigChange(stage.id, 'model', defaultModel?.value || '')
                                } else {
                                  clearStageConfig(stage.id)
                                }
                              }}
                            >
                              <option value="">Use Default (Google Imagen)</option>
                              {getImageProviderOptions().map(provider => (
                                <option key={provider.value} value={provider.value}>
                                  {provider.label}
                                </option>
                              ))}
                            </select>
                          </div>
                          
                          {stageConfig.provider && (
                            <div className="form-group">
                              <label>Image Model</label>
                              <select 
                                value={stageConfig.model || ''}
                                onChange={(e) => handleStageConfigChange(stage.id, 'model', e.target.value)}
                              >
                                {getImageModelOptions(stageConfig.provider).map(model => (
                                  <option key={model.value} value={model.value}>
                                    {model.label}
                                    {model.recommended && ' ⭐'}
                                  </option>
                                ))}
                              </select>
                            </div>
                          )}
                        </div>
                        
                        {!hasConfig && (
                          <div className="default-indicator">
                            Using default: <strong>Google</strong> / <strong>imagen-3.0-generate-001</strong>
                          </div>
                        )}
                      </div>
                    )}
                    
                    {['research', 'plagiarism_check'].includes(stage.id) && (
                      <div className="non-llm-stage">
                        <em>This stage does not use an LLM</em>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {activeTab === 'api_keys' && (
          <div className="settings-section">
            <h2>API Keys</h2>
            <p className="section-description">
              Configure API keys in your <code>.env</code> file. Current configuration:
            </p>
            
            <div className="api-keys-info">
              <div className="api-key-item">
                <strong>GEMINI_API_KEY</strong>
                <span className="status configured">Configured</span>
              </div>
              <div className="api-key-item">
                <strong>GROQ_API_KEY</strong>
                <span className="status configured">Configured</span>
              </div>
              <div className="api-key-item">
                <strong>NATURALWRITE_API_KEY</strong>
                <span className="status configured">Configured</span>
              </div>
              <div className="api-key-item">
                <strong>CODEQUIRY_API_KEY</strong>
                <span className="status configured">Configured</span>
              </div>
              <div className="api-key-item">
                <strong>YOAST_SEO_URL</strong>
                <span className="status configured">Configured</span>
              </div>
              <div className="api-key-item">
                <strong>OPENAI_API_KEY</strong>
                <span className="status not-configured">Not Configured</span>
              </div>
              <div className="api-key-item">
                <strong>ANTHROPIC_API_KEY</strong>
                <span className="status not-configured">Not Configured</span>
              </div>
            </div>
            
            <div className="info-box">
              <h4>⚠️ Security Notice</h4>
              <p>API keys should never be stored in the database or frontend code. Always use environment variables.</p>
              <p>Update keys in: <code>/home/tapendra/Downloads/projects/news/.env</code></p>
            </div>
          </div>
        )}

        {activeTab === 'seo' && (
          <SEOSettings />
        )}

        {activeTab === 'plagiarism' && (
          <PlagiarismSettings />
        )}

        {/* Other tabs remain the same */}
      </div>
    </div>
  )
}

export default AISettings
