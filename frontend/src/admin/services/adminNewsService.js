import api from '../../services/api';

const BASE_URL = '/admin/news';

class AdminNewsService {
  /**
   * Get all news articles with optional filters
   */
  async getNewsList(params = {}) {
    const response = await api.get(`${BASE_URL}/`, { params });
    return response.data;
  }

  /**
   * Get single news article by ID
   */
  async getNewsById(id) {
    const response = await api.get(`${BASE_URL}/${id}/`);
    return response.data;
  }

  /**
   * Create new news article
   */
  async createNews(formData) {
    const response = await api.post(`${BASE_URL}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  /**
   * Update news article
   */
  async updateNews(id, formData) {
    const response = await api.put(`${BASE_URL}/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  /**
   * Partially update news article
   */
  async patchNews(id, data) {
    const response = await api.patch(`${BASE_URL}/${id}/`, data);
    return response.data;
  }

  /**
   * Delete news article
   */
  async deleteNews(id) {
    const response = await api.delete(`${BASE_URL}/${id}/`);
    return response.data;
  }

  /**
   * Get category choices
   */
  getCategoryChoices() {
    return [
      { value: 'business', label: 'Business' },
      { value: 'political', label: 'Political' },
      { value: 'tech', label: 'Tech' },
      { value: 'education', label: 'Education' },
    ];
  }

  /**
   * Get visibility choices
   */
  getVisibilityChoices() {
    return [
      { value: 'public', label: 'Public' },
      { value: 'private', label: 'Private' },
      { value: 'password', label: 'Password Protected' },
    ];
  }

  /**
   * Generate slug from title
   */
  generateSlug(title) {
    return title
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();
  }
}

export default new AdminNewsService();
