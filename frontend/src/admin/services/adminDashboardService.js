import api from '../../services/api';

const BASE_URL = '/admin';

class AdminDashboardService {
  /**
   * Get dashboard statistics
   */
  async getDashboardStats() {
    const response = await api.get(`${BASE_URL}/dashboard/stats/`);
    return response.data;
  }
}

export default new AdminDashboardService();
