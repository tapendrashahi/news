import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import adminAdvertisementService from '../../services/adminAdvertisementService';
import './AdvertisementsList.css';

const AdvertisementsList = () => {
  const [advertisements, setAdvertisements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [positionFilter, setPositionFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchAdvertisements();
    fetchStats();
  }, [searchQuery, positionFilter, statusFilter]);

  const fetchAdvertisements = async () => {
    try {
      setLoading(true);
      const params = {};
      
      if (searchQuery) {
        params.search = searchQuery;
      }
      
      if (positionFilter !== 'all') {
        params.position = positionFilter;
      }
      
      if (statusFilter !== 'all') {
        params.is_active = statusFilter === 'active';
      }

      const data = await adminAdvertisementService.getAdvertisements(params);
      setAdvertisements(Array.isArray(data) ? data : data.results || []);
    } catch (error) {
      console.error('Failed to fetch advertisements:', error);
      toast.error('Failed to load advertisements');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const data = await adminAdvertisementService.getStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handleToggle = async (id) => {
    try {
      await adminAdvertisementService.toggleAdvertisement(id);
      toast.success('Advertisement status updated');
      fetchAdvertisements();
      fetchStats();
    } catch (error) {
      console.error('Failed to toggle advertisement:', error);
      toast.error('Failed to update advertisement');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this advertisement?')) {
      return;
    }

    try {
      await adminAdvertisementService.deleteAdvertisement(id);
      toast.success('Advertisement deleted');
      fetchAdvertisements();
      fetchStats();
    } catch (error) {
      console.error('Failed to delete advertisement:', error);
      toast.error('Failed to delete advertisement');
    }
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  return (
    <div className="advertisements-list-page">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Advertisements</h1>
          <p className="page-subtitle">Manage website advertisements</p>
        </div>
        <Link to="/admin/advertisements/create" className="btn-primary">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"/>
          </svg>
          Add Advertisement
        </Link>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon total">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.total_ads}</div>
              <div className="stat-label">Total Ads</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon active">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.active_ads}</div>
              <div className="stat-label">Active</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon impressions">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.total_impressions.toLocaleString()}</div>
              <div className="stat-label">Total Impressions</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon clicks">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{stats.total_clicks.toLocaleString()}</div>
              <div className="stat-label">Total Clicks</div>
              <div className="stat-subtitle">{stats.average_ctr}% CTR</div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="filters-section">
        <div className="search-box">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            type="text"
            placeholder="Search by title..."
            value={searchQuery}
            onChange={handleSearch}
            className="search-input"
          />
        </div>

        <select
          value={positionFilter}
          onChange={(e) => setPositionFilter(e.target.value)}
          className="filter-select"
        >
          <option value="all">All Positions</option>
          <option value="sidebar">Sidebar</option>
          <option value="header">Header</option>
          <option value="footer">Footer</option>
          <option value="inline">Inline Content</option>
        </select>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="filter-select"
        >
          <option value="all">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>

      {/* Advertisements Table */}
      {loading ? (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading advertisements...</p>
        </div>
      ) : advertisements.length === 0 ? (
        <div className="empty-state">
          <svg width="64" height="64" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <h3>No advertisements found</h3>
          <p>Create your first advertisement to get started</p>
          <Link to="/admin/advertisements/create" className="btn-primary">
            Add Advertisement
          </Link>
        </div>
      ) : (
        <div className="advertisements-table-container">
          <table className="advertisements-table">
            <thead>
              <tr>
                <th>Advertisement</th>
                <th>Position</th>
                <th>Size</th>
                <th>Stats</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {advertisements.map((ad) => (
                <tr key={ad.id}>
                  <td>
                    <div className="ad-info">
                      {ad.image && (
                        <img src={ad.image} alt={ad.alt_text} className="ad-thumbnail" />
                      )}
                      <div>
                        <div className="ad-title">{ad.title}</div>
                        <div className="ad-url">{ad.link_url}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className="position-badge">{ad.position_display}</span>
                  </td>
                  <td>
                    <span className="size-badge">{ad.size_display}</span>
                  </td>
                  <td>
                    <div className="stats-cell">
                      <div className="stat-item">
                        <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                        </svg>
                        {ad.impressions.toLocaleString()}
                      </div>
                      <div className="stat-item">
                        <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"/>
                        </svg>
                        {ad.clicks.toLocaleString()}
                      </div>
                      <div className="ctr-badge">{ad.click_through_rate.toFixed(2)}%</div>
                    </div>
                  </td>
                  <td>
                    <span className={`status-badge ${ad.is_active ? 'active' : 'inactive'}`}>
                      {ad.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <Link
                        to={`/admin/advertisements/${ad.id}/edit`}
                        className="btn-action edit"
                        title="Edit"
                      >
                        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </Link>
                      <button
                        onClick={() => handleToggle(ad.id)}
                        className="btn-action toggle"
                        title={ad.is_active ? 'Deactivate' : 'Activate'}
                      >
                        {ad.is_active ? (
                          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                          </svg>
                        ) : (
                          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                          </svg>
                        )}
                      </button>
                      <button
                        onClick={() => handleDelete(ad.id)}
                        className="btn-action delete"
                        title="Delete"
                      >
                        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdvertisementsList;
