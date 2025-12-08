import api from '../../services/api';

const BASE_URL = '/admin/reports';

class AdminReportsService {
  /**
   * Get analytics data with optional date range
   */
  async getAnalytics(params = {}) {
    const response = await api.get(`${BASE_URL}/analytics/`, { params });
    return response.data;
  }

  /**
   * Get predefined date range
   */
  getDateRange(days) {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);
    
    return {
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
    };
  }

  /**
   * Format number with commas
   */
  formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  /**
   * Calculate percentage
   */
  calculatePercentage(value, total) {
    if (total === 0) return 0;
    return ((value / total) * 100).toFixed(1);
  }
}

export default new AdminReportsService();
