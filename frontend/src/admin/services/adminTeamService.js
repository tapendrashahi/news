import api from '../../services/api';

const BASE_URL = '/admin/team';

class AdminTeamService {
  /**
   * Get all team members with optional filters
   */
  async getTeamList(params = {}) {
    const response = await api.get(`${BASE_URL}/`, { params });
    return response.data;
  }

  /**
   * Get single team member by ID
   */
  async getTeamMemberById(id) {
    const response = await api.get(`${BASE_URL}/${id}/`);
    return response.data;
  }

  /**
   * Get articles by team member
   */
  async getMemberArticles(id) {
    const response = await api.get(`${BASE_URL}/${id}/articles/`);
    return response.data;
  }

  /**
   * Create new team member
   */
  async createTeamMember(formData) {
    const response = await api.post(`${BASE_URL}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  /**
   * Update team member
   */
  async updateTeamMember(id, formData) {
    const response = await api.put(`${BASE_URL}/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  /**
   * Delete team member
   */
  async deleteTeamMember(id) {
    const response = await api.delete(`${BASE_URL}/${id}/`);
    return response.data;
  }

  /**
   * Get role choices
   */
  getRoleChoices() {
    return [
      { value: 'editor', label: 'Editor' },
      { value: 'reporter', label: 'Reporter' },
      { value: 'columnist', label: 'Columnist' },
      { value: 'contributor', label: 'Contributor' },
      { value: 'photographer', label: 'Photographer' },
    ];
  }
}

export default new AdminTeamService();
