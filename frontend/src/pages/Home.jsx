import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useNews, useCategories } from '../hooks';
import { SEO } from '../components';
import './Home.css';

const Home = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  
  // Fetch actual data from backend API
  const { data: newsData, isLoading: newsLoading } = useNews({ 
    page: currentPage,
    category: selectedCategory === 'all' ? '' : selectedCategory 
  });
  const { data: categoriesData, isLoading: categoriesLoading } = useCategories();
  
  const loading = newsLoading || categoriesLoading;
  const featuredNews = newsData?.results || [];

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
  
  // Build categories from backend data
  const backendCategories = categoriesData?.categories?.map(cat => ({
    id: cat.slug || cat.name.toLowerCase(),
    name: cat.name,
    icon: categoryIcons[cat.slug || cat.name.toLowerCase()] || '📄'
  })) || [];
  
  const categories = [
    { id: 'all', name: 'All News', icon: '📰' },
    ...backendCategories
  ];
  
  const API_BASE = process.env.REACT_APP_MEDIA_URL || 'http://localhost:8000';

  // Helper function to format date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    
    if (diffHours < 1) return 'Just now';
    if (diffHours < 24) return `${diffHours} hours ago`;
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };
  
  // Calculate read time based on content length
  const calculateReadTime = (content) => {
    const wordsPerMinute = 200;
    const words = content ? content.split(' ').length : 0;
    const minutes = Math.ceil(words / wordsPerMinute);
    return `${minutes} min read`;
  };
  
  // Generate AI confidence score (mock for now)
  const getAiConfidence = () => {
    return Math.floor(Math.random() * (98 - 85 + 1)) + 85;
  };

  // Category filtering is handled by the API, no need to filter locally
  const displayNews = featuredNews;

  return (
    <>
      <SEO
        title="AI Analitica - Unbiased News Analysis Powered by AI"
        description="Stay informed with AI-powered news analysis. Zero bias, data-driven insights, and multi-perspective coverage from around the world."
        keywords="AI news, unbiased news, artificial intelligence, news analysis, breaking news"
      />
      
      <div className="home">
        {/* Hero Section */}
      <section className="home__hero">
        <div className="hero__content">
          <div className="hero__badge">
            <span className="badge__icon">🤖</span>
            <span className="badge__text">AI-Powered News Analysis</span>
          </div>
          <h1 className="home__title">AI Analitica</h1>
          <p className="home__subtitle">
            Unbiased News. Data-Driven Insights. Powered by Artificial Intelligence.
          </p>
          <p className="home__mission">
            Every story analyzed through the lens of AI to deliver objective, 
            multi-perspective coverage free from human bias.
          </p>
        </div>
        <div className="hero__stats">
          <div className="stat">
            <div className="stat__number">10K+</div>
            <div className="stat__label">Articles Analyzed</div>
          </div>
          <div className="stat">
            <div className="stat__number">95%</div>
            <div className="stat__label">AI Accuracy</div>
          </div>
          <div className="stat">
            <div className="stat__number">24/7</div>
            <div className="stat__label">Real-time Updates</div>
          </div>
        </div>
      </section>

      {/* Category Navigation */}
      <section className="home__categories">
        <div className="categories__container">
          {categories.map(category => (
            <button
              key={category.id}
              className={`category-chip ${selectedCategory === category.id ? 'category-chip--active' : ''}`}
              onClick={() => setSelectedCategory(category.id)}
            >
              <span className="category-chip__icon">{category.icon}</span>
              <span className="category-chip__name">{category.name}</span>
            </button>
          ))}
        </div>
      </section>

      {/* Main Content */}
      <main className="home__content">
        {loading ? (
          <div className="loading">
            <div className="loading__spinner"></div>
            <p>AI analyzing latest news...</p>
          </div>
        ) : (
          <>
            {/* Featured Story */}
            {displayNews.length > 0 && (
              <article className="featured-story">
                <div className="featured-story__image">
                  <img 
                    src={displayNews[0].image ? `${API_BASE}${displayNews[0].image}` : 'https://images.unsplash.com/photo-1569163139394-de4798aa62b5?w=800'} 
                    alt={displayNews[0].title}
                    onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1569163139394-de4798aa62b5?w=800'}
                  />
                  <div className="featured-story__badge">Featured</div>
                  <div className="featured-story__ai-badge">
                    <span className="ai-icon">🤖</span>
                    <span>AI Confidence: {getAiConfidence()}%</span>
                  </div>
                </div>
                <div className="featured-story__content">
                  <div className="story__meta">
                    <span className="meta__category">{displayNews[0].category || 'News'}</span>
                    <span className="meta__separator">•</span>
                    <span className="meta__date">{formatDate(displayNews[0].created_at)}</span>
                    <span className="meta__separator">•</span>
                    <span className="meta__read-time">{calculateReadTime(displayNews[0].content)}</span>
                  </div>
                  <h2 className="featured-story__title">{displayNews[0].title}</h2>
                  <p className="featured-story__excerpt">{displayNews[0].excerpt || displayNews[0].content?.substring(0, 150) + '...'}</p>
                  <Link to={`/news/${displayNews[0].slug || displayNews[0].id}`} className="featured-story__link">
                    Read Full Analysis
                    <span className="link__arrow">→</span>
                  </Link>
                </div>
              </article>
            )}

            {/* News Grid */}
            <div className="news-grid">
              <div className="news-grid__header">
                <h2 className="news-grid__title">Latest Analysis</h2>
                <div className="news-grid__filter">
                  <span className="filter__label">Sorted by:</span>
                  <select className="filter__select">
                    <option>Most Recent</option>
                    <option>AI Confidence</option>
                    <option>Most Read</option>
                  </select>
                </div>
              </div>

              <div className="news-grid__items">
                {displayNews.slice(1).map(news => (
                  <article key={news.id} className="news-card">
                    <Link to={`/news/${news.slug || news.id}`} className="news-card__link">
                      <div className="news-card__image">
                        <img 
                          src={news.image ? `${API_BASE}${news.image}` : 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=800'} 
                          alt={news.title}
                          onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=800'}
                        />
                        <div className="news-card__ai-badge">
                          AI: {getAiConfidence()}%
                        </div>
                      </div>
                      <div className="news-card__content">
                        <div className="news-card__meta">
                          <span className="meta__category">{news.category || 'News'}</span>
                          <span className="meta__separator">•</span>
                          <span className="meta__date">{formatDate(news.created_at)}</span>
                        </div>
                        <h3 className="news-card__title">{news.title}</h3>
                        <p className="news-card__excerpt">{news.excerpt || news.content?.substring(0, 100) + '...'}</p>
                        <div className="news-card__footer">
                          <span className="footer__read-time">{calculateReadTime(news.content)}</span>
                          <span className="footer__arrow">→</span>
                        </div>
                      </div>
                    </Link>
                  </article>
                ))}
              </div>
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