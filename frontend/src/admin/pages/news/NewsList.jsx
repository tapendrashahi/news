import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import adminNewsService from '../../services/adminNewsService';
import './NewsList.css';

const NewsList = () => {
  const navigate = useNavigate();
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');

  const categories = adminNewsService.getCategoryChoices();

  useEffect(() => {
    loadNews();
  }, [searchQuery, categoryFilter]);

  const loadNews = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchQuery) params.search = searchQuery;
      if (categoryFilter) params.category = categoryFilter;
      
      const data = await adminNewsService.getNewsList(params);
      setNews(data.results || data);
    } catch (error) {
      console.error('Error loading news:', error);
      toast.error('Failed to load news articles');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this article?')) {
      return;
    }

    try {
      await adminNewsService.deleteNews(id);
      toast.success('Article deleted successfully');
      loadNews();
    } catch (error) {
      console.error('Error deleting article:', error);
      toast.error('Failed to delete article');
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getCategoryBadge = (category) => {
    const colors = {
      business: '#10b981',
      political: '#3b82f6',
      tech: '#8b5cf6',
      education: '#f59e0b'
    };
    return colors[category] || '#6b7280';
  };

  return (
    <div className="news-list-page">
      <div className="page-header">
        <div>
          <h1>News Articles</h1>
          <p className="page-subtitle">Manage all news articles</p>
        </div>
        <Link to="/admin/news/create" className="btn-create">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"/>
          </svg>
          Create Article
        </Link>
      </div>

      <div className="filters-bar">
        <div className="search-box">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input 
            type="text" 
            placeholder="Search articles..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        <select 
          className="filter-select"
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat.value} value={cat.value}>{cat.label}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading articles...</p>
        </div>
      ) : news.length === 0 ? (
        <div className="empty-state">
          <svg width="64" height="64" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <h3>No articles found</h3>
          <p>Get started by creating your first article</p>
          <Link to="/admin/news/create" className="btn-create">Create Article</Link>
        </div>
      ) : (
        <div className="news-table-container">
          <table className="news-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Category</th>
                <th>Visibility</th>
                <th>Published</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {news.map((article) => (
                <tr key={article.id}>
                  <td className="title-cell">
                    {article.image && (
                      <img src={article.image} alt={article.title} className="article-thumb" />
                    )}
                    <div>
                      <div className="article-title">{article.title}</div>
                      {article.excerpt && (
                        <div className="article-excerpt">{article.excerpt.substring(0, 80)}...</div>
                      )}
                    </div>
                  </td>
                  <td>
                    {article.author ? article.author.name : 'N/A'}
                  </td>
                  <td>
                    <span 
                      className="category-badge" 
                      style={{ backgroundColor: getCategoryBadge(article.category) }}
                    >
                      {categories.find(c => c.value === article.category)?.label || article.category}
                    </span>
                  </td>
                  <td>
                    <span className={`visibility-badge visibility-${article.visibility}`}>
                      {article.visibility}
                    </span>
                  </td>
                  <td>{formatDate(article.publish_date)}</td>
                  <td>{formatDate(article.created_at)}</td>
                  <td className="actions-cell">
                    <a 
                      href={`/news/${article.slug}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-icon btn-preview" 
                      title="Preview"
                    >
                      <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                      </svg>
                    </a>
                    <button 
                      className="btn-icon btn-edit" 
                      onClick={() => navigate(`/admin/news/edit/${article.id}`)}
                      title="Edit"
                    >
                      <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button 
                      className="btn-icon btn-delete" 
                      onClick={() => handleDelete(article.id)}
                      title="Delete"
                    >
                      <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                    </button>
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

export default NewsList;
