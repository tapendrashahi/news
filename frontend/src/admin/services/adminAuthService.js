import api from '../../services/api';

const BASE_URL = '/admin/auth';

class AdminAuthService {
  /**
   * Get CSRF token
   */
  async getCsrfToken() {
    try {
      await api.get('/admin/auth/csrf/');
    } catch (error) {
      console.error('Failed to get CSRF token:', error);
    }
  }

  /**
   * Login to admin panel
   */
  async login(username, password) {
    try {
      // Get CSRF token first
      await this.getCsrfToken();
      
      const response = await api.post(`${BASE_URL}/login/`, {
        username,
        password
      });
      
      if (response.data.success) {
        // Store user data in localStorage
        localStorage.setItem('adminUser', JSON.stringify(response.data.user));
        return response.data;
      }
      
      throw new Error(response.data.error || 'Login failed');
    } catch (error) {
      throw error.response?.data?.error || error.message || 'Login failed';
    }
  }

  /**
   * Logout from admin panel
   */
  async logout() {
    try {
      await api.post(`${BASE_URL}/logout/`);
      localStorage.removeItem('adminUser');
      return true;
    } catch (error) {
      // Clear local storage even if API call fails
      localStorage.removeItem('adminUser');
      throw error;
    }
  }

  /**
   * Get current admin user
   */
  async getCurrentUser() {
    try {
      const response = await api.get(`${BASE_URL}/user/`);
      localStorage.setItem('adminUser', JSON.stringify(response.data));
      return response.data;
    } catch (error) {
      localStorage.removeItem('adminUser');
      throw error;
    }
  }

  /**
   * Get stored user from localStorage
   */
  getStoredUser() {
    try {
      const user = localStorage.getItem('adminUser');
      return user ? JSON.parse(user) : null;
    } catch {
      return null;
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!this.getStoredUser();
  }

  /**
   * Check if user is admin
   */
  isAdmin() {
    const user = this.getStoredUser();
    return user?.is_staff || false;
  }
}

export default new AdminAuthService();
