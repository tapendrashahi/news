import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import './Category.css';

const Category = () => {
  const { category } = useParams();
  const [news, setNews] = useState([]);
  const [popularNews, setPopularNews] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('newest');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 9;

  useEffect(() => {
    fetchNews();
    fetchPopularNews();
    fetchCategories();
  }, [category, sortBy]);

  const fetchNews = () => {
    setLoading(true);
    fetch(`http://localhost:8000/api/news/?category=${category}`)
      .then(response => response.json())
      .then(data => {
        let newsItems = data.results || data;
        
        // Ensure newsItems is an array
        if (!Array.isArray(newsItems)) {
          newsItems = [];
        }
        
        // Sort news based on selection
        if (sortBy === 'oldest') {
          newsItems = [...newsItems].reverse();
        } else if (sortBy === 'popular') {
          newsItems = [...newsItems].sort((a, b) => 
            (b.comment_count + b.share_count) - (a.comment_count + a.share_count)
          );
        }
        
        setNews(newsItems);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading news:', error);
        setNews([]);
        setLoading(false);
      });
  };

  const fetchPopularNews = () => {
    fetch(`http://localhost:8000/api/news/?category=${category}&page_size=5`)
      .then(response => response.json())
      .then(data => {
        const newsItems = data.results || data;
        const newsArray = Array.isArray(newsItems) ? newsItems : [];
        setPopularNews(newsArray.slice(0, 5));
      })
      .catch(error => {
        console.error('Error loading popular news:', error);
        setPopularNews([]);
      });
  };

  const fetchCategories = () => {
    fetch('http://localhost:8000/api/categories/')
      .then(response => response.json())
      .then(data => {
        const cats = data.categories || [];
        setCategories(cats.filter(cat => cat.name.toLowerCase() !== category));
      })
      .catch(error => console.error('Error loading categories:', error));
  };

  const getCategoryIcon = (catName) => {
    const icons = {
      business: 'fa-briefcase',
      political: 'fa-landmark',
      tech: 'fa-microchip',
      technology: 'fa-microchip',
      education: 'fa-graduation-cap',
      sports: 'fa-futbol',
      health: 'fa-heartbeat'
    };
    return icons[catName.toLowerCase()] || 'fa-newspaper';
  };

  const getCategoryColor = () => {
    const colors = {
      business: '#10b981',
      political: '#3b82f6',
      tech: '#8b5cf6',
      technology: '#8b5cf6',
      education: '#f59e0b',
      sports: '#ef4444',
      health: '#ec4899'
    };
    return colors[category?.toLowerCase()] || '#6366f1';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    return `${Math.floor(seconds / 86400)} days ago`;
  };

  // Pagination
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentNews = Array.isArray(news) ? news.slice(indexOfFirstItem, indexOfLastItem) : [];
  const totalPages = Math.ceil((Array.isArray(news) ? news.length : 0) / itemsPerPage);

  const categoryDisplay = category?.charAt(0).toUpperCase() + category?.slice(1);

  if (loading) {
    return <div className="category-loading">Loading {categoryDisplay} news...</div>;
  }

  return (
    <div className="category-page">
      {/* Breadcrumbs */}
      <div className="breadcrumbs">
        <div className="breadcrumbs-list">
          <Link to="/"><i className="fas fa-home"></i> Home</Link>
          <span className="breadcrumbs-separator">/</span>
          <span className="breadcrumbs-current">{categoryDisplay}</span>
        </div>
      </div>

      {/* Category Header */}
      <div className="category-header" style={{ background: `linear-gradient(135deg, ${getCategoryColor()}, ${getCategoryColor()}dd)` }}>
        <div className="category-header-content">
          <div className="category-icon">
            <i className={`fas ${getCategoryIcon(category)}`}></i>
          </div>
          <h1 className="category-title">{categoryDisplay}</h1>
          <p className="category-description">
            Latest updates and in-depth analysis on {categoryDisplay.toLowerCase()} news
          </p>
          <div className="category-stats">
            <div className="stat-item">
              <i className="fas fa-newspaper"></i>
              <span>{news.length} Articles</span>
            </div>
            <div className="stat-item">
              <i className="fas fa-clock"></i>
              <span>Updated Daily</span>
            </div>
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="filter-bar">
        <div className="filter-content">
          <div className="filter-left">
            <span className="results-count">
              Showing {indexOfFirstItem + 1}-{Math.min(indexOfLastItem, news.length)} of {news.length} articles
            </span>
          </div>
          <div className="sort-dropdown">
            <label htmlFor="sortBy">Sort by:</label>
            <select id="sortBy" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="popular">Most Popular</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-layout">
          
          {/* News List */}
          <main>
            {currentNews.length > 0 ? (
              <>
                <div className="news-grid">
                  {currentNews.map((item) => (
                    <article key={item.id} className="news-card">
                      <Link to={`/news/${item.slug || item.id}`} className="news-card-image">
                        <img 
                          src={item.image || 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400'}
                          alt={item.title}
                          onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400'}
                        />
                        <span className="category-badge" style={{ backgroundColor: getCategoryColor() }}>
                          {categoryDisplay.toUpperCase()}
                        </span>
                      </Link>
                      <div className="news-card-content">
                        <div className="news-meta">
                          <span>
                            <i className="far fa-calendar"></i>
                            {formatDate(item.created_at)}
                          </span>
                          <span>
                            <i className="far fa-clock"></i>
                            {formatTimeAgo(item.created_at)}
                          </span>
                        </div>
                        <h2 className="news-card-title">
                          <Link to={`/news/${item.slug || item.id}`}>
                            {item.title}
                          </Link>
                        </h2>
                        <p className="news-card-excerpt">
                          {item.excerpt || item.content?.substring(0, 150)}...
                        </p>
                        <div className="news-card-footer">
                          <div className="news-author">
                            <i className="fas fa-user-circle"></i>
                            <span>{item.author?.name || 'Editorial'}</span>
                          </div>
                          <Link to={`/news/${item.slug || item.id}`} className="read-more">
                            Read More <i className="fas fa-arrow-right"></i>
                          </Link>
                        </div>
                      </div>
                    </article>
                  ))}
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="pagination">
                    <button
                      className={`page-link ${currentPage === 1 ? 'disabled' : ''}`}
                      onClick={() => currentPage > 1 && setCurrentPage(currentPage - 1)}
                      disabled={currentPage === 1}
                    >
                      <i className="fas fa-chevron-left"></i>
                    </button>
                    
                    {[...Array(totalPages)].map((_, idx) => {
                      const pageNum = idx + 1;
                      if (
                        pageNum === 1 ||
                        pageNum === totalPages ||
                        (pageNum >= currentPage - 2 && pageNum <= currentPage + 2)
                      ) {
                        return (
                          <button
                            key={pageNum}
                            className={`page-link ${currentPage === pageNum ? 'active' : ''}`}
                            onClick={() => setCurrentPage(pageNum)}
                          >
                            {pageNum}
                          </button>
                        );
                      } else if (pageNum === currentPage - 3 || pageNum === currentPage + 3) {
                        return <span key={pageNum} className="page-ellipsis">...</span>;
                      }
                      return null;
                    })}
                    
                    <button
                      className={`page-link ${currentPage === totalPages ? 'disabled' : ''}`}
                      onClick={() => currentPage < totalPages && setCurrentPage(currentPage + 1)}
                      disabled={currentPage === totalPages}
                    >
                      <i className="fas fa-chevron-right"></i>
                    </button>
                  </div>
                )}
              </>
            ) : (
              <div className="empty-state">
                <div className="empty-icon">
                  <i className="fas fa-inbox"></i>
                </div>
                <h3>No Articles Found</h3>
                <p>We couldn't find any articles in this category yet. Check back soon for updates!</p>
                <Link to="/" className="empty-btn">
                  <i className="fas fa-home"></i> Back to Home
                </Link>
              </div>
            )}
          </main>

          {/* Sidebar */}
          <aside className="sidebar">
            
            {/* Popular in Category */}
            <div className="widget">
              <h3 className="widget-title">Most Popular</h3>
              <div className="popular-list">
                {popularNews.map((item, index) => (
                  <div key={item.id} className="popular-post">
                    <div className="popular-rank">{String(index + 1).padStart(2, '0')}</div>
                    <div className="popular-info">
                      <h4>
                        <Link to={`/news/${item.slug || item.id}`}>
                          {item.title}
                        </Link>
                      </h4>
                      <div className="popular-meta">
                        <i className="far fa-clock"></i> {formatTimeAgo(item.created_at)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Other Categories */}
            <div className="widget">
              <h3 className="widget-title">Other Categories</h3>
              {categories.map((cat) => (
                <Link
                  key={cat.name}
                  to={`/category/${cat.name.toLowerCase()}`}
                  className="category-item"
                >
                  <div className="category-name">
                    <i className={`fas ${getCategoryIcon(cat.name)}`}></i>
                    <span>{cat.display_name || cat.name}</span>
                  </div>
                  <span className="category-count">{cat.count || 0}</span>
                </Link>
              ))}
            </div>

            {/* Newsletter Signup */}
            <div className="widget widget-newsletter">
              <h3 className="widget-title">Stay Updated</h3>
              <p className="newsletter-text">
                Get the latest {categoryDisplay} news delivered to your inbox
              </p>
              <form className="newsletter-form" onSubmit={(e) => {
                e.preventDefault();
                // Handle newsletter signup
              }}>
                <input
                  type="email"
                  placeholder="Your email address"
                  className="newsletter-input"
                  required
                />
                <button type="submit" className="newsletter-button">
                  Subscribe <i className="fas fa-paper-plane"></i>
                </button>
              </form>
            </div>

            {/* Tags */}
            <div className="widget">
              <h3 className="widget-title">Popular Tags</h3>
              <div className="tags-cloud">
                <Link to={`/search?q=AI`} className="tag-item">AI</Link>
                <Link to={`/search?q=Technology`} className="tag-item">Technology</Link>
                <Link to={`/search?q=Innovation`} className="tag-item">Innovation</Link>
                <Link to={`/search?q=Analysis`} className="tag-item">Analysis</Link>
                <Link to={`/search?q=Market`} className="tag-item">Market</Link>
                <Link to={`/search?q=Trends`} className="tag-item">Trends</Link>
                <Link to={`/search?q=Research`} className="tag-item">Research</Link>
                <Link to={`/search?q=Global`} className="tag-item">Global</Link>
              </div>
            </div>
          </aside>
        </div>
    </div>
  );
};

export default Category;

