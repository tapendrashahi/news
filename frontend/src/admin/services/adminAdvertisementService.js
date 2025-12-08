import api from '../../services/api';

const BASE_URL = '/admin/advertisements';

class AdminAdvertisementService {
  /**
   * Get all advertisements with optional filters
   */
  async getAdvertisements(params = {}) {
    const response = await api.get(`${BASE_URL}/`, { params });
    return response.data;
  }

  /**
   * Get a single advertisement by ID
   */
  async getAdvertisement(id) {
    const response = await api.get(`${BASE_URL}/${id}/`);
    return response.data;
  }

  /**
   * Create a new advertisement
   */
  async createAdvertisement(formData) {
    const response = await api.post(`${BASE_URL}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  /**
   * Update an advertisement
   */
  async updateAdvertisement(id, formData) {
    const response = await api.put(`${BASE_URL}/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  /**
   * Delete an advertisement
   */
  async deleteAdvertisement(id) {
    const response = await api.delete(`${BASE_URL}/${id}/`);
    return response.data;
  }

  /**
   * Toggle advertisement active status
   */
  async toggleAdvertisement(id) {
    const response = await api.post(`${BASE_URL}/${id}/toggle/`);
    return response.data;
  }

  /**
   * Get advertisement statistics
   */
  async getStats() {
    const response = await api.get(`${BASE_URL}/stats/`);
    return response.data;
  }
}

export default new AdminAdvertisementService();
