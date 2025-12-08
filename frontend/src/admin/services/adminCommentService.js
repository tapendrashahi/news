import api from '../../services/api';

const BASE_URL = '/admin/comments';

class AdminCommentService {
  /**
   * Get all comments with optional filters
   */
  async getCommentsList(params = {}) {
    const response = await api.get(`${BASE_URL}/`, { params });
    return response.data;
  }

  /**
   * Approve a comment
   */
  async approveComment(id) {
    const response = await api.post(`${BASE_URL}/${id}/approve/`);
    return response.data;
  }

  /**
   * Delete a comment
   */
  async deleteComment(id) {
    const response = await api.delete(`${BASE_URL}/${id}/`);
    return response.data;
  }
}

export default new AdminCommentService();
