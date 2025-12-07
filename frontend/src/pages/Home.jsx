import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useNews, useCategories } from '../hooks';
import { SEO } from '../components';
import './Home.css';

const Home = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [breakingNews, setBreakingNews] = useState([]);
  const [showAllCategories, setShowAllCategories] = useState(false);
  
  const { data: newsData, isLoading: newsLoading } = useNews({ 
    page: currentPage,
    category: selectedCategory === 'all' ? '' : selectedCategory 
  });
  const { data: categoriesData, isLoading: categoriesLoading } = useCategories();
  
  const loading = newsLoading || categoriesLoading;
  const news = newsData?.results || [];
  
  // Set breaking news
  useEffect(() => {
    if (news.length > 0) {
      setBreakingNews(news.slice(0, 5));
    }
  }, [news]);

  // Map icons to categories
  const categoryIcons = {
    'all': '📰',
    'politics': '🏛️',
    'political': '🏛️',
    'technology': '💻',
    'tech': '💻',
    'business': '💼',
    'science': '🔬',
    'health': '🏥',
    'environment': '🌍',
    'sports': '⚽',
    'education': '📚',
    'entertainment': '🎬'
  };
  
  // Build categories from backend data with counts
  const backendCategories = categoriesData?.categories?.map(cat => ({
    id: cat.slug || cat.name.toLowerCase(),
    name: cat.name,
    icon: categoryIcons[cat.slug || cat.name.toLowerCase()] || '📄',
    count: cat.article_count || 0
  })) || [];
  
  const categories = [
    { id: 'all', name: 'All News', icon: '📰', count: news.length },
    ...backendCategories
  ];
  
  // Determine which categories to show
  const INITIAL_CATEGORY_LIMIT = 8;
  const displayedCategories = showAllCategories 
    ? categories 
    : categories.slice(0, INITIAL_CATEGORY_LIMIT);
  const hasMoreCategories = categories.length > INITIAL_CATEGORY_LIMIT;
  
  const API_BASE = process.env.REACT_APP_MEDIA_URL || 'http://localhost:8000';

  // Helper function to format date - compact version
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    
    if (diffHours < 1) return 'Just now';
    if (diffHours < 24) return `${diffHours}h ago`;
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };
  
  // Calculate read time based on content length - compact version
  const calculateReadTime = (content) => {
    const wordsPerMinute = 200;
    const words = content ? content.split(' ').length : 0;
    const minutes = Math.ceil(words / wordsPerMinute);
    return `${minutes} min`;
  };
  
  // Generate AI confidence score (mock for now)
  const getAiConfidence = () => {
    return Math.floor(Math.random() * (98 - 85 + 1)) + 85;
  };
  
  // Get category color
  const getCategoryColor = (category) => {
    const colors = {
      'politics': '#ef4444',
      'political': '#ef4444',
      'technology': '#3b82f6',
      'tech': '#3b82f6',
      'business': '#10b981',
      'science': '#8b5cf6',
      'health': '#ec4899',
      'environment': '#14b8a6',
      'sports': '#f59e0b',
      'education': '#f97316',
      'entertainment': '#a855f7'
    };
    return colors[category?.toLowerCase()] || '#7e22ce';
  };

  // Category filtering is handled by the API, no need to filter locally
  const displayNews = news;

  return (
    <>
      <SEO
        title="AI Analitica - Unbiased News Analysis Powered by AI"
        description="Stay informed with AI-powered news analysis. Zero bias, data-driven insights, and multi-perspective coverage from around the world."
        keywords="AI news, unbiased news, artificial intelligence, news analysis, breaking news"
      />
      
      <div className="home">
        {/* Breaking News Ticker */}
        {breakingNews.length > 0 && (
          <div className="breaking-news">
            <div className="breaking-news__label">
              <span className="breaking-news__icon">⚡</span>
              <span className="breaking-news__text">BREAKING</span>
            </div>
            <div className="breaking-news__ticker">
              <div className="breaking-news__track">
                {breakingNews.map(item => (
                  <Link 
                    key={item.id} 
                    to={`/news/${item.slug || item.id}`} 
                    className="breaking-news__item"
                  >
                    {item.title}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        )}

      {/* Main Content */}
      <main className="home__content">
        {loading ? (
          <div className="loading">
            <div className="loading__spinner"></div>
            <p>AI analyzing latest news...</p>
          </div>
        ) : (
          <>
            {/* Split Hero Section - 1 Large + 2 Small */}
            {displayNews.length >= 3 && (
              <section className="split-hero">
                {/* Large Featured Story */}
                <article className="split-hero__main">
                  <Link to={`/news/${displayNews[0].slug || displayNews[0].id}`} className="split-hero__link">
                    <div className="split-hero__image">
                      <img 
                        src={displayNews[0].image ? `${API_BASE}${displayNews[0].image}` : 'https://images.unsplash.com/photo-1569163139394-de4798aa62b5?w=800'} 
                        alt={displayNews[0].title}
                        onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1569163139394-de4798aa62b5?w=800'}
                      />
                      <div className="split-hero__overlay"></div>
                      <div className="split-hero__badge">Featured</div>
                      <div className="split-hero__ai-badge">
                        <span className="ai-icon">🤖</span>
                        <span>{getAiConfidence()}%</span>
                      </div>
                    </div>
                    <div className="split-hero__content">
                      <span className="split-hero__category" style={{backgroundColor: getCategoryColor(displayNews[0].category)}}>
                        {displayNews[0].category || 'News'}
                      </span>
                      <h2 className="split-hero__title">{displayNews[0].title}</h2>
                      <p className="split-hero__excerpt">{displayNews[0].excerpt || displayNews[0].content?.substring(0, 120) + '...'}</p>
                      <div className="split-hero__meta">
                        <span>{formatDate(displayNews[0].created_at)}</span>
                        <span className="meta__separator">•</span>
                        <span>{calculateReadTime(displayNews[0].content)}</span>
                      </div>
                    </div>
                  </Link>
                </article>

                {/* Two Small Stories */}
                <div className="split-hero__side">
                  {displayNews.slice(1, 3).map((item) => (
                    <article key={item.id} className="split-hero__small">
                      <Link to={`/news/${item.slug || item.id}`} className="split-hero__small-link">
                        <div className="split-hero__small-image">
                          <img 
                            src={item.image ? `${API_BASE}${item.image}` : 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400'} 
                            alt={item.title}
                            onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400'}
                          />
                          <span className="split-hero__small-ai">🤖 {getAiConfidence()}%</span>
                        </div>
                        <div className="split-hero__small-content">
                          <span className="split-hero__small-category" style={{backgroundColor: getCategoryColor(item.category)}}>
                            {item.category || 'News'}
                          </span>
                          <h3 className="split-hero__small-title">{item.title}</h3>
                          <div className="split-hero__small-meta">
                            <span>{formatDate(item.created_at)}</span>
                            <span className="meta__separator">•</span>
                            <span>{calculateReadTime(item.content)}</span>
                          </div>
                        </div>
                      </Link>
                    </article>
                  ))}
                </div>
              </section>
            )}

            {/* Main Content Grid with Sidebar */}
            <div className="content-wrapper">
              {/* News Grid */}
              <div className="news-grid">
                <div className="news-grid__header">
                  <h2 className="news-grid__title">Latest Analysis</h2>
                  <div className="news-grid__filter">
                    <span className="filter__label">Sort:</span>
                    <select className="filter__select">
                      <option>Most Recent</option>
                      <option>AI Confidence</option>
                      <option>Most Read</option>
                    </select>
                  </div>
                </div>

                <div className="news-grid__items">
                  {displayNews.slice(3).map((item, index) => (
                    <article key={item.id} className={`news-card ${index === 0 || index === 5 ? 'news-card--large' : ''}`}>
                      <Link to={`/news/${item.slug || item.id}`} className="news-card__link">
                        <div className="news-card__image">
                          <img 
                            src={item.image ? `${API_BASE}${item.image}` : 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=800'} 
                            alt={item.title}
                            onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=800'}
                          />
                          <div className="news-card__ai-badge">
                            🤖 {getAiConfidence()}%
                          </div>
                        </div>
                        <div className="news-card__content">
                          <span className="news-card__category" style={{backgroundColor: getCategoryColor(item.category)}}>
                            {item.category || 'News'}
                          </span>
                          <h3 className="news-card__title">{item.title}</h3>
                          <p className="news-card__excerpt">{item.excerpt || item.content?.substring(0, 100) + '...'}</p>
                          <div className="news-card__footer">
                            <span className="footer__date">{formatDate(item.created_at)}</span>
                            <span className="meta__separator">•</span>
                            <span className="footer__read-time">{calculateReadTime(item.content)}</span>
                          </div>
                        </div>
                      </Link>
                    </article>
                  ))}
                </div>
              </div>

              {/* Sidebar */}
              <aside className="sidebar">
                {/* Trending Widget */}
                <div className="sidebar__widget">
                  <h3 className="sidebar__widget-title">
                    <span className="widget-icon">🔥</span>
                    Trending Now
                  </h3>
                  <div className="trending-list">
                    {displayNews.slice(0, 5).map((item, index) => (
                      <Link key={item.id} to={`/news/${item.slug || item.id}`} className="trending-item">
                        <span className="trending-item__number">#{index + 1}</span>
                        <div className="trending-item__content">
                          <h4 className="trending-item__title">{item.title}</h4>
                          <div className="trending-item__meta">
                            <span>{formatDate(item.created_at)}</span>
                            <span className="meta__separator">•</span>
                            <span className="trending-item__views">🤖 {getAiConfidence()}%</span>
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>

                {/* Browse Topics Widget */}
                <div className="sidebar__widget">
                  <h3 className="sidebar__widget-title">
                    <span className="widget-icon">📂</span>
                    Browse Topics
                  </h3>
                  <div className="browse-topics__list">
                    {categories.map(category => (
                      <button
                        key={category.id}
                        className={`topic-item ${selectedCategory === category.id ? 'topic-item--active' : ''}`}
                        onClick={() => setSelectedCategory(category.id)}
                      >
                        <span className="topic-item__icon">{category.icon}</span>
                        <span className="topic-item__name">{category.name}</span>
                        {category.count !== undefined && (
                          <span className="topic-item__count">{category.count}</span>
                        )}
                      </button>
                    ))}
                  </div>
                </div>

                {/* AI Insights Widget */}
                <div className="sidebar__widget">
                  <h3 className="sidebar__widget-title">
                    <span className="widget-icon">🤖</span>
                    AI Insights
                  </h3>
                  <div className="ai-insights">
                    <div className="insight-stat">
                      <div className="insight-stat__label">Highest Confidence</div>
                      <div className="insight-stat__value">98%</div>
                      <div className="insight-stat__description">Technology sector analysis</div>
                    </div>
                    <div className="insight-stat">
                      <div className="insight-stat__label">Most Analyzed</div>
                      <div className="insight-stat__value">Politics</div>
                      <div className="insight-stat__description">247 articles today</div>
                    </div>
                    <div className="insight-stat">
                      <div className="insight-stat__label">Bias Score</div>
                      <div className="insight-stat__value">0.02%</div>
                      <div className="insight-stat__description">Near-zero detection</div>
                    </div>
                  </div>
                </div>

                {/* Subscribe Widget */}
                <div className="sidebar__widget sidebar__widget--subscribe">
                  <h3 className="sidebar__widget-title">
                    <span className="widget-icon">📧</span>
                    Daily AI Briefing
                  </h3>
                  <p className="subscribe__description">
                    Get AI-analyzed news delivered to your inbox every morning.
                  </p>
                  <form className="subscribe__form">
                    <input 
                      type="email" 
                      className="subscribe__input" 
                      placeholder="your@email.com"
                      required
                    />
                    <button type="submit" className="subscribe__button">
                      Subscribe
                    </button>
                  </form>
                  <p className="subscribe__privacy">No spam. Unsubscribe anytime.</p>
                </div>
              </aside>
            </div>
          </>
        )}
      </main>

      {/* AI Mission Section */}
      <section className="home__mission-section">
        <div className="mission__content">
          <h2 className="mission__title">Our AI-Driven Mission</h2>
          <div className="mission__grid">
            <div className="mission__card">
              <div className="mission__icon">🎯</div>
              <h3>Zero Bias</h3>
              <p>AI algorithms analyze news from multiple sources, eliminating human bias and political leanings.</p>
            </div>
            <div className="mission__card">
              <div className="mission__icon">📊</div>
              <h3>Data-Driven</h3>
              <p>Every analysis backed by comprehensive data evaluation and fact-checking algorithms.</p>
            </div>
            <div className="mission__card">
              <div className="mission__icon">🔍</div>
              <h3>Multi-Perspective</h3>
              <p>AI synthesizes viewpoints from across the spectrum to present complete, balanced coverage.</p>
            </div>
            <div className="mission__card">
              <div className="mission__icon">⚡</div>
              <h3>Real-Time</h3>
              <p>Continuous AI monitoring and analysis ensures you're always informed with the latest insights.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
    </>
  );
};

export default Home;