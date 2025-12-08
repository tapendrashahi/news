import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import adminDashboardService from '../services/adminDashboardService';
import StatsCard from '../components/common/StatsCard';
import './Dashboard.css';
import '../styles/shared.css';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await adminDashboardService.getDashboardStats();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard statistics');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="dashboard__header">
          <div className="skeleton skeleton-title"></div>
          <div className="skeleton skeleton-text" style={{ width: '40%' }}></div>
        </div>
        
        <div className="dashboard__stats">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton skeleton-card"></div>
          ))}
        </div>

        <div className="dashboard__content">
          <div className="skeleton skeleton-card" style={{ height: '300px' }}></div>
          <div className="skeleton skeleton-card" style={{ height: '300px' }}></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>{error}</p>
        <button onClick={loadDashboardStats}>Retry</button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard__header">
        <h1>Dashboard</h1>
        <p>Welcome back! Here's what's happening with your news platform.</p>
      </div>

      {/* Stats Cards */}
      <div className="dashboard__stats">
        <StatsCard
          title="Total News"
          value={stats?.total_news || 0}
          icon="📰"
          color="#3b82f6"
          subtitle={`${stats?.news_last_month || 0} this month`}
        />
        <StatsCard
          title="Team Members"
          value={stats?.total_team || 0}
          icon="👥"
          color="#10b981"
          subtitle="Active members"
        />
        <StatsCard
          title="Comments"
          value={stats?.total_comments || 0}
          icon="💬"
          color="#f59e0b"
          subtitle={`${stats?.pending_comments || 0} pending`}
        />
        <StatsCard
          title="Subscribers"
          value={stats?.active_subscribers || 0}
          icon="📧"
          color="#8b5cf6"
          subtitle={`${stats?.total_subscribers || 0} total`}
        />
      </div>

      <div className="dashboard__content">
        {/* Recent News */}
        <div className="dashboard__section">
          <div className="dashboard__section-header">
            <h2>Recent News</h2>
            <Link to="/admin/news" className="dashboard__link">View All →</Link>
          </div>
          <div className="dashboard__list">
            {stats?.recent_news?.map((news) => (
              <div key={news.id} className="dashboard__list-item">
                <div className="dashboard__list-icon">📰</div>
                <div className="dashboard__list-content">
                  <h4>{news.title}</h4>
                  <p>{new Date(news.created_at).toLocaleDateString()}</p>
                </div>
                <span className="dashboard__list-badge">{news.category_display}</span>
              </div>
            ))}
            {(!stats?.recent_news || stats.recent_news.length === 0) && (
              <p className="dashboard__empty">No recent news articles</p>
            )}
          </div>
        </div>

        {/* Recent Comments */}
        <div className="dashboard__section">
          <div className="dashboard__section-header">
            <h2>Recent Comments</h2>
            <Link to="/admin/comments" className="dashboard__link">View All →</Link>
          </div>
          <div className="dashboard__list">
            {stats?.recent_comments?.map((comment) => (
              <div key={comment.id} className="dashboard__list-item">
                <div className="dashboard__list-icon">💬</div>
                <div className="dashboard__list-content">
                  <h4>{comment.name}</h4>
                  <p>{comment.text.substring(0, 60)}...</p>
                </div>
                <span className={`dashboard__list-badge ${comment.is_approved ? 'success' : 'warning'}`}>
                  {comment.is_approved ? 'Approved' : 'Pending'}
                </span>
              </div>
            ))}
            {(!stats?.recent_comments || stats.recent_comments.length === 0) && (
              <p className="dashboard__empty">No recent comments</p>
            )}
          </div>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="dashboard__categories">
        <h2>Category Breakdown</h2>
        <div className="dashboard__categories-grid">
          {stats?.categories?.map((category) => (
            <div key={category.code} className="dashboard__category-card">
              <div className="dashboard__category-name">{category.name}</div>
              <div className="dashboard__category-count">{category.count}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
