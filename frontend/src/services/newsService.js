import api from './api';

export const newsService = {
  // Get all news with pagination
  getNews: async (params = {}) => {
    console.log('🌐 [API CALL] newsService.getNews', {
      function: 'getNews',
      file: '/home/tapendra/Downloads/projects/news/frontend/src/services/newsService.js',
      params,
      endpoint: '/api/news/',
      method: 'GET',
      timestamp: new Date().toISOString()
    });

    try {
      const response = await api.get('/news/', { params });
      console.log('✅ [API SUCCESS] newsService.getNews', {
        status: response.status,
        dataKeys: Object.keys(response.data),
        resultsCount: response.data.results?.length,
        totalCount: response.data.count,
        data: response.data
      });
      return response.data;
    } catch (error) {
      console.error('❌ [API ERROR] newsService.getNews', {
        error: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      throw error;
    }
  },

  // Get single news by slug
  getNewsDetail: async (slug) => {
    const response = await api.get(`/news/${slug}/`);
    return response.data;
  },

  // Get news by category
  getNewsByCategory: async (category, page = 1) => {
    const response = await api.get('/news/by_category/', {
      params: { category, page }
    });
    return response.data;
  },

  // Search news
  searchNews: async (query, page = 1) => {
    const response = await api.get('/news/search/', {
      params: { q: query, page },
    });
    return response.data;
  },

  // Get categories
  getCategories: async () => {
    console.log('🌐 [API CALL] newsService.getCategories', {
      function: 'getCategories',
      file: '/home/tapendra/Downloads/projects/news/frontend/src/services/newsService.js',
      endpoint: '/api/categories/',
      method: 'GET',
      timestamp: new Date().toISOString()
    });

    try {
      const response = await api.get('/categories/');
      console.log('✅ [API SUCCESS] newsService.getCategories', {
        status: response.status,
        dataKeys: Object.keys(response.data),
        categoriesCount: response.data.categories?.length,
        data: response.data
      });
      return response.data;
    } catch (error) {
      console.error('❌ [API ERROR] newsService.getCategories', {
        error: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      throw error;
    }
  },

  // Get comments for a news article
  getComments: async (newsId) => {
    const response = await api.get(`/news/${newsId}/comments/`);
    return response.data;
  },

  // Add comment to news article
  addComment: async (newsId, commentData) => {
    const response = await api.post(`/news/${newsId}/add_comment/`, commentData);
    return response.data;
  },

  // Increment share count
  shareNews: async (newsId, platform) => {
    const response = await api.post(`/news/${newsId}/share/`, { platform });
    return response.data;
  },

  // Subscribe to newsletter
  subscribe: async (email) => {
    const response = await api.post('/subscribers/', { email });
    return response.data;
  },

  // Unsubscribe from newsletter
  unsubscribe: async (email) => {
    const response = await api.post('/subscribers/unsubscribe/', { email });
    return response.data;
  },

  // Get team members
  getTeam: async () => {
    const response = await api.get('/team/');
    return response.data;
  },

  // Get team member details
  getTeamMember: async (memberId) => {
    const response = await api.get(`/team/${memberId}/`);
    return response.data;
  },

  // Get articles by team member
  getTeamMemberArticles: async (memberId) => {
    const response = await api.get(`/team/${memberId}/articles/`);
    return response.data;
  },
};

export default newsService;
