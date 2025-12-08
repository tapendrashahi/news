import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import adminSubscriberService from '../../services/adminSubscriberService';
import './SubscribersList.css';

const SubscribersList = () => {
  const [subscribers, setSubscribers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [selectedIds, setSelectedIds] = useState([]);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    fetchSubscribers();
  }, [searchQuery, statusFilter]);

  const fetchSubscribers = async () => {
    try {
      setLoading(true);
      const params = {};
      
      if (searchQuery) {
        params.search = searchQuery;
      }
      
      if (statusFilter === 'active') {
        params.is_active = true;
      } else if (statusFilter === 'inactive') {
        params.is_active = false;
      }

      const data = await adminSubscriberService.getSubscribersList(params);
      setSubscribers(data.results || data);
    } catch (error) {
      console.error('Failed to fetch subscribers:', error);
      toast.error('Failed to load subscribers');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (id) => {
    try {
      await adminSubscriberService.toggleSubscriber(id);
      toast.success('Subscriber status updated');
      fetchSubscribers();
    } catch (error) {
      console.error('Failed to toggle subscriber:', error);
      toast.error('Failed to update subscriber');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this subscriber?')) {
      return;
    }

    try {
      await adminSubscriberService.deleteSubscriber(id);
      toast.success('Subscriber deleted');
      fetchSubscribers();
      setSelectedIds(selectedIds.filter(sid => sid !== id));
    } catch (error) {
      console.error('Failed to delete subscriber:', error);
      toast.error('Failed to delete subscriber');
    }
  };

  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) {
      toast.error('Please select subscribers to delete');
      return;
    }

    if (!window.confirm(`Are you sure you want to delete ${selectedIds.length} subscriber(s)?`)) {
      return;
    }

    try {
      await Promise.all(selectedIds.map(id => adminSubscriberService.deleteSubscriber(id)));
      toast.success(`${selectedIds.length} subscriber(s) deleted`);
      setSelectedIds([]);
      fetchSubscribers();
    } catch (error) {
      console.error('Failed to delete subscribers:', error);
      toast.error('Failed to delete subscribers');
    }
  };

  const handleExport = async () => {
    try {
      setExporting(true);
      const blob = await adminSubscriberService.exportSubscribers();
      const timestamp = new Date().toISOString().split('T')[0];
      adminSubscriberService.downloadCSV(blob, `subscribers_${timestamp}.csv`);
      toast.success('Subscribers exported successfully');
    } catch (error) {
      console.error('Failed to export subscribers:', error);
      toast.error('Failed to export subscribers');
    } finally {
      setExporting(false);
    }
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterChange = (filter) => {
    setStatusFilter(filter);
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === subscribers.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(subscribers.map(s => s.id));
    }
  };

  const toggleSelect = (id) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter(sid => sid !== id));
    } else {
      setSelectedIds([...selectedIds, id]);
    }
  };

  // Calculate stats
  const stats = {
    total: subscribers.length,
    active: subscribers.filter(s => s.is_active).length,
    inactive: subscribers.filter(s => !s.is_active).length,
  };

  // Calculate new this month
  const thisMonth = new Date();
  thisMonth.setDate(1);
  const newThisMonth = subscribers.filter(s => 
    new Date(s.created_at) >= thisMonth
  ).length;

  return (
    <div className="subscribers-list-page">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Subscribers</h1>
          <p className="page-subtitle">Manage newsletter subscribers</p>
        </div>
        <button 
          onClick={handleExport} 
          className="btn-export"
          disabled={exporting || subscribers.length === 0}
        >
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          {exporting ? 'Exporting...' : 'Export CSV'}
        </button>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon total">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total Subscribers</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon active">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.active}</div>
            <div className="stat-label">Active</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon inactive">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
            </svg>
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats.inactive}</div>
            <div className="stat-label">Unsubscribed</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon new">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/>
            </svg>
          </div>
          <div className="stat-content">
            <div className="stat-value">{newThisMonth}</div>
            <div className="stat-label">New This Month</div>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="filter-tabs">
        <button
          className={`tab-btn ${statusFilter === 'all' ? 'active' : ''}`}
          onClick={() => handleFilterChange('all')}
        >
          All ({stats.total})
        </button>
        <button
          className={`tab-btn ${statusFilter === 'active' ? 'active' : ''}`}
          onClick={() => handleFilterChange('active')}
        >
          Active ({stats.active})
        </button>
        <button
          className={`tab-btn ${statusFilter === 'inactive' ? 'active' : ''}`}
          onClick={() => handleFilterChange('inactive')}
        >
          Unsubscribed ({stats.inactive})
        </button>
      </div>

      {/* Search & Bulk Actions */}
      <div className="toolbar">
        <div className="search-box">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            type="text"
            placeholder="Search by email..."
            value={searchQuery}
            onChange={handleSearch}
            className="search-input"
          />
        </div>

        {selectedIds.length > 0 && (
          <div className="bulk-actions">
            <span className="selected-count">{selectedIds.length} selected</span>
            <button onClick={handleBulkDelete} className="btn-bulk-delete">
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              Delete Selected
            </button>
          </div>
        )}
      </div>

      {/* Subscribers Table */}
      {loading ? (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading subscribers...</p>
        </div>
      ) : subscribers.length === 0 ? (
        <div className="empty-state">
          <svg width="64" height="64" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          <h3>No subscribers found</h3>
          <p>
            {statusFilter === 'active' ? 'No active subscribers' : 
             statusFilter === 'inactive' ? 'No unsubscribed users' :
             'No subscribers available'}
          </p>
        </div>
      ) : (
        <div className="subscribers-table-container">
          <table className="subscribers-table">
            <thead>
              <tr>
                <th style={{ width: '40px' }}>
                  <input
                    type="checkbox"
                    checked={selectedIds.length === subscribers.length && subscribers.length > 0}
                    onChange={toggleSelectAll}
                  />
                </th>
                <th>Email</th>
                <th>Subscribed Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {subscribers.map((subscriber) => (
                <tr key={subscriber.id}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedIds.includes(subscriber.id)}
                      onChange={() => toggleSelect(subscriber.id)}
                    />
                  </td>
                  <td>
                    <div className="email-cell">
                      <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                      </svg>
                      <span>{subscriber.email}</span>
                    </div>
                  </td>
                  <td>
                    <div className="date-cell">
                      {new Date(subscriber.created_at).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    </div>
                  </td>
                  <td>
                    <span className={`status-badge ${subscriber.is_active ? 'active' : 'inactive'}`}>
                      {subscriber.is_active ? 'Active' : 'Unsubscribed'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button
                        onClick={() => handleToggle(subscriber.id)}
                        className="btn-action toggle"
                        title={subscriber.is_active ? 'Deactivate' : 'Activate'}
                      >
                        {subscriber.is_active ? (
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
                        onClick={() => handleDelete(subscriber.id)}
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

export default SubscribersList;
