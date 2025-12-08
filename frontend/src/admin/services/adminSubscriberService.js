import api from '../../services/api';

const BASE_URL = '/admin/subscribers';

class AdminSubscriberService {
  /**
   * Get all subscribers with optional filters
   */
  async getSubscribersList(params = {}) {
    const response = await api.get(`${BASE_URL}/`, { params });
    return response.data;
  }

  /**
   * Toggle subscriber active status
   */
  async toggleSubscriber(id) {
    const response = await api.post(`${BASE_URL}/${id}/toggle/`);
    return response.data;
  }

  /**
   * Delete a subscriber
   */
  async deleteSubscriber(id) {
    const response = await api.delete(`${BASE_URL}/${id}/`);
    return response.data;
  }

  /**
   * Export subscribers to CSV
   */
  async exportSubscribers() {
    const response = await api.get(`${BASE_URL}/export/`, {
      responseType: 'blob', // Important for file download
    });
    return response.data;
  }

  /**
   * Download CSV file
   */
  downloadCSV(blob, filename = 'subscribers.csv') {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  }
}

export default new AdminSubscriberService();
