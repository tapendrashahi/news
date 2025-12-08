import { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import toast from 'react-hot-toast';
import adminReportsService from '../../services/adminReportsService';
import './Reports.css';

// Register ChartJS components
ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Reports = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState(30);

  useEffect(() => {
    fetchAnalytics();
  }, [dateRange]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const params = adminReportsService.getDateRange(dateRange);
      const data = await adminReportsService.getAnalytics(params);
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
      toast.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="reports-page">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return null;
  }

  // Category distribution chart data
  const categoryData = {
    labels: analytics.category_breakdown?.map(cat => cat.category) || [],
    datasets: [
      {
        data: analytics.category_breakdown?.map(cat => cat.count) || [],
        backgroundColor: [
          '#3b82f6',
          '#10b981',
          '#f59e0b',
          '#ef4444',
          '#8b5cf6',
          '#ec4899',
        ],
        borderWidth: 0,
      },
    ],
  };

  // Top authors chart data
  const authorsData = {
    labels: analytics.top_authors?.map(author => author.author__name) || [],
    datasets: [
      {
        label: 'Articles',
        data: analytics.top_authors?.map(author => author.count) || [],
        backgroundColor: '#3b82f6',
        borderRadius: 6,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
      },
    },
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          precision: 0,
        },
      },
    },
  };

  return (
    <div className="reports-page">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Reports & Analytics</h1>
          <p className="page-subtitle">Track your content performance</p>
        </div>
        
        <div className="date-range-selector">
          <button
            className={`range-btn ${dateRange === 30 ? 'active' : ''}`}
            onClick={() => setDateRange(30)}
          >
            30 Days
          </button>
          <button
            className={`range-btn ${dateRange === 60 ? 'active' : ''}`}
            onClick={() => setDateRange(60)}
          >
            60 Days
          </button>
          <button
            className={`range-btn ${dateRange === 90 ? 'active' : ''}`}
            onClick={() => setDateRange(90)}
          >
            90 Days
          </button>
        </div>
      </div>

      {/* News Statistics */}
      <div className="section">
        <h2 className="section-title">News Statistics</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon news">
              <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{adminReportsService.formatNumber(analytics.news_stats?.total || 0)}</div>
              <div className="stat-label">Total Published</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon views">
              <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{adminReportsService.formatNumber(analytics.news_stats?.total_views || 0)}</div>
              <div className="stat-label">Total Views</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon shares">
              <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{adminReportsService.formatNumber(analytics.news_stats?.total_shares || 0)}</div>
              <div className="stat-label">Total Shares</div>
            </div>
          </div>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="section">
        <h2 className="section-title">Category Distribution</h2>
        <div className="charts-grid">
          <div className="chart-card">
            <div className="chart-container">
              {analytics.category_breakdown && analytics.category_breakdown.length > 0 ? (
                <Pie data={categoryData} options={chartOptions} />
              ) : (
                <div className="no-data">No category data available</div>
              )}
            </div>
          </div>

          <div className="category-list">
            {analytics.category_breakdown?.map((cat, index) => {
              const total = analytics.news_stats?.total || 1;
              const percentage = adminReportsService.calculatePercentage(cat.count, total);
              return (
                <div key={index} className="category-item">
                  <div className="category-info">
                    <div className="category-name">{cat.category}</div>
                    <div className="category-count">{cat.count} articles</div>
                  </div>
                  <div className="category-bar">
                    <div className="category-fill" style={{ width: `${percentage}%` }}></div>
                  </div>
                  <div className="category-percent">{percentage}%</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Comment Statistics */}
      <div className="section">
        <h2 className="section-title">Comment Statistics</h2>
        <div className="stats-grid small">
          <div className="stat-card">
            <div className="stat-icon comments">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{analytics.comment_stats?.total || 0}</div>
              <div className="stat-label">Total Comments</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon approved">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{analytics.comment_stats?.approved || 0}</div>
              <div className="stat-label">Approved</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon pending">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{analytics.comment_stats?.pending || 0}</div>
              <div className="stat-label">Pending</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon rate">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <div className="stat-content">
              <div className="stat-value">{analytics.comment_stats?.approval_rate || 0}%</div>
              <div className="stat-label">Approval Rate</div>
            </div>
          </div>
        </div>
      </div>

      {/* Top Authors */}
      <div className="section">
        <h2 className="section-title">Top 5 Authors</h2>
        <div className="chart-card full">
          <div className="chart-container-bar">
            {analytics.top_authors && analytics.top_authors.length > 0 ? (
              <Bar data={authorsData} options={barChartOptions} />
            ) : (
              <div className="no-data">No author data available</div>
            )}
          </div>
        </div>
      </div>

      {/* Share Statistics */}
      <div className="section">
        <h2 className="section-title">Share Statistics by Platform</h2>
        <div className="share-stats">
          {analytics.share_stats && Object.entries(analytics.share_stats).map(([platform, count]) => (
            <div key={platform} className="share-item">
              <div className="share-platform">
                {platform === 'facebook' && (
                  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                )}
                {platform === 'twitter' && (
                  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"/>
                  </svg>
                )}
                {platform === 'linkedin' && (
                  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/>
                    <circle cx="4" cy="4" r="2"/>
                  </svg>
                )}
                {platform === 'whatsapp' && (
                  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                )}
                <span>{platform.charAt(0).toUpperCase() + platform.slice(1)}</span>
              </div>
              <div className="share-count">{adminReportsService.formatNumber(count)}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Most Commented Articles */}
      {analytics.most_commented && analytics.most_commented.length > 0 && (
        <div className="section">
          <h2 className="section-title">Most Commented Articles</h2>
          <div className="articles-list">
            {analytics.most_commented.map((article, index) => (
              <div key={article.id} className="article-row">
                <div className="article-rank">#{index + 1}</div>
                <div className="article-info">
                  <div className="article-title">{article.title}</div>
                  <div className="article-meta">
                    <span className="category-badge">{article.category}</span>
                    <span className="comment-count">
                      <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                      </svg>
                      {article.comment_count} comments
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;
