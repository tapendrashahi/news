import api from './api';

class AdvertisementService {
  /**
   * Get active advertisements by position
   */
  async getAdvertisements(position = null) {
    const params = position ? { position } : {};
    const response = await api.get('/advertisements/', { params });
    return response.data;
  }

  /**
   * Track advertisement impression
   */
  async trackImpression(id) {
    try {
      await api.post(`/advertisements/${id}/track_impression/`);
    } catch (error) {
      console.error('Error tracking impression:', error);
    }
  }

  /**
   * Track advertisement click
   */
  async trackClick(id) {
    try {
      const response = await api.post(`/advertisements/${id}/track_click/`);
      return response.data;
    } catch (error) {
      console.error('Error tracking click:', error);
      return null;
    }
  }
}

export default new AdvertisementService();
