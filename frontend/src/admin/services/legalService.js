import api from '../../services/api';

const legalService = {
  // Get all legal pages
  getAll: async (params = {}) => {
    const response = await api.get('/admin/legal/', { params });
    return response.data;
  },

  // Get a specific legal page
  get: async (id) => {
    const response = await api.get(`/admin/legal/${id}/`);
    return response.data;
  },

  // Get legal page by slug
  getBySlug: async (slug) => {
    const response = await api.get(`/admin/legal/slug/${slug}/`);
    return response.data;
  },

  // Get legal page by type
  getByType: async (pageType) => {
    const response = await api.get(`/admin/legal/type/${pageType}/`);
    return response.data;
  },

  // Create a new legal page
  create: async (data) => {
    const response = await api.post('/admin/legal/', data);
    return response.data;
  },

  // Update a legal page
  update: async (id, data) => {
    const response = await api.put(`/admin/legal/${id}/`, data);
    return response.data;
  },

  // Partially update a legal page
  partialUpdate: async (id, data) => {
    const response = await api.patch(`/admin/legal/${id}/`, data);
    return response.data;
  },

  // Delete a legal page
  delete: async (id) => {
    const response = await api.delete(`/admin/legal/${id}/`);
    return response.data;
  },

  // Publish a legal page
  publish: async (id) => {
    const response = await api.post(`/admin/legal/${id}/publish/`);
    return response.data;
  },

  // Unpublish a legal page
  unpublish: async (id) => {
    const response = await api.post(`/admin/legal/${id}/unpublish/`);
    return response.data;
  },

  // Archive a legal page
  archive: async (id) => {
    const response = await api.post(`/admin/legal/${id}/archive/`);
    return response.data;
  },

  // Get available page types
  getPageTypes: async () => {
    const response = await api.get('/admin/legal/page_types/');
    return response.data;
  },
};

export default legalService;
