import api from '../../services/api'

// Keywords
export const getKeywords = (params) => api.get('/admin/ai/keywords/', { params })
export const getKeyword = (id) => api.get(`/admin/ai/keywords/${id}/`)
export const createKeyword = (data) => api.post('/admin/ai/keywords/', data)
export const updateKeyword = (id, data) => api.patch(`/admin/ai/keywords/${id}/`, data)
export const approveKeyword = (id) => api.post(`/admin/ai/keywords/${id}/approve/`)
export const rejectKeyword = (id, reason) => api.post(`/admin/ai/keywords/${id}/reject/`, { reason })

// Articles / Generation
export const getArticles = (params) => api.get('/admin/ai/articles/', { params })
export const getArticle = (id) => api.get(`/admin/ai/articles/${id}/`)
export const startGeneration = (id) => api.post(`/admin/ai/articles/${id}/start_generation/`)
export const retryStage = (id, stage) => api.post(`/admin/ai/articles/${id}/retry_stage/`, { stage })
export const cancelGeneration = (id) => api.post(`/admin/ai/articles/${id}/cancel/`)
export const deleteArticle = (id) => api.delete(`/admin/ai/articles/${id}/`)
export const approveArticle = (id, notes) => api.post(`/admin/ai/articles/${id}/approve/`, { notes })
export const rejectArticle = (id, notes, regenerate = false) => api.post(`/admin/ai/articles/${id}/reject/`, { notes, regenerate })
export const publishArticle = (id, visibility = 'public') => api.post(`/admin/ai/articles/${id}/publish/`, { visibility })

// Queue
export const getGenerationQueue = (params) => api.get('/admin/ai/articles/', { params })

// Configs
export const getConfigs = () => api.get('/admin/ai/configs/')
export const updateConfig = (id, data) => api.patch(`/admin/ai/configs/${id}/`, data)

// News Source Configurations
export const getNewsSources = (params) => api.get('/admin/ai/news-sources/', { params })
export const getNewsSource = (id) => api.get(`/admin/ai/news-sources/${id}/`)
export const createNewsSource = (data) => api.post('/admin/ai/news-sources/', data)
export const updateNewsSource = (id, data) => api.patch(`/admin/ai/news-sources/${id}/`, data)
export const deleteNewsSource = (id) => api.delete(`/admin/ai/news-sources/${id}/`)
// Scraping can take a long time, so use extended timeout (2 minutes)
export const triggerScrape = (id) => api.post(`/admin/ai/news-sources/${id}/trigger_scrape/`, {}, { timeout: 120000 })

// Scraped Articles
export const getScrapedArticles = (params) => api.get('/admin/ai/scraped-articles/', { params })
export const getScrapedArticle = (id) => api.get(`/admin/ai/scraped-articles/${id}/`)
export const approveScrapedArticle = (id, data) => api.post(`/admin/ai/scraped-articles/${id}/approve/`, data)
export const rejectScrapedArticle = (id, reason) => api.post(`/admin/ai/scraped-articles/${id}/reject/`, { reason })
export const bulkApproveArticles = (articleIds) => api.post('/admin/ai/scraped-articles/bulk_approve/', { 
  article_ids: articleIds, 
  auto_generate: true 
})

export default {
	getKeywords,
	getKeyword,
	createKeyword,
	updateKeyword,
	approveKeyword,
	rejectKeyword,
	getArticles,
	getArticle,
	startGeneration,
	retryStage,
	cancelGeneration,
	deleteArticle,
	approveArticle,
	rejectArticle,
	publishArticle,
	getGenerationQueue,
	getConfigs,
	updateConfig,
	getNewsSources,
	getNewsSource,
	createNewsSource,
	updateNewsSource,
	deleteNewsSource,
	triggerScrape,
	getScrapedArticles,
	getScrapedArticle,
	approveScrapedArticle,
	rejectScrapedArticle,
	bulkApproveArticles
}
