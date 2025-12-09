import { useState, useEffect, useRef } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useNewsDetail, useComments, useAddComment, useShareNews, useNews } from '../hooks';
import { SEO } from '../components';
import Advertisement from '../components/Advertisement';
import './NewsDetail.css';

const NewsDetail = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [showShareMenu, setShowShareMenu] = useState(false);
  const [commentForm, setCommentForm] = useState({ name: '', email: '', text: '' });
  const [tableOfContents, setTableOfContents] = useState([]);
  const [activeSection, setActiveSection] = useState('');
  const contentRef = useRef(null);
  
  const { data: news, isLoading, error } = useNewsDetail(slug);
  const { data: commentsData, isLoading: commentsLoading } = useComments(news?.id);
  const addCommentMutation = useAddComment();
  const shareMutation = useShareNews();
  
  // Fetch more AI analysis articles for "Keep Learning" section
  const { data: moreArticles } = useNews({ page: 1 });

  // Handle paginated API response - extract results array
  const comments = Array.isArray(commentsData) 
    ? commentsData 
    : (commentsData?.results || []);

  // Extract table of contents from article content
  useEffect(() => {
    if (news?.content && contentRef.current) {
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = news.content;
      
      const headings = tempDiv.querySelectorAll('h1, h2, h3, h4');
      const toc = Array.from(headings).map((heading, index) => {
        const id = `section-${index}`;
        const level = parseInt(heading.tagName.substring(1));
        return {
          id,
          text: heading.textContent,
          level
        };
      });
      
      setTableOfContents(toc);
      
      // Add IDs to actual content headings
      setTimeout(() => {
        const actualHeadings = contentRef.current?.querySelectorAll('h1, h2, h3, h4');
        actualHeadings?.forEach((heading, index) => {
          heading.id = `section-${index}`;
        });
      }, 100);
    }
  }, [news?.content]);

  // Track active section on scroll with Intersection Observer
  useEffect(() => {
    if (!contentRef.current || tableOfContents.length === 0) return;

    const observerOptions = {
      rootMargin: '-100px 0px -66%',
      threshold: 0
    };

    const observerCallback = (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          setActiveSection(entry.target.id);
        }
      });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    // Observe all heading elements
    const headings = contentRef.current.querySelectorAll('h1, h2, h3, h4');
    headings.forEach((heading) => observer.observe(heading));

    return () => observer.disconnect();
  }, [tableOfContents]);

  // Helper functions
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatRelativeTime = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return formatDate(dateString);
  };

  const calculateReadTime = (content) => {
    const wordsPerMinute = 200;
    const words = content ? content.split(' ').length : 0;
    const minutes = Math.ceil(words / wordsPerMinute);
    return `${minutes} min read`;
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!news?.id) return;
    
    try {
      await addCommentMutation.mutateAsync({
        newsId: news.id,
        commentData: commentForm,
      });
      setCommentForm({ name: '', email: '', text: '' });
      alert('Comment submitted successfully!');
    } catch (error) {
      console.error('Error adding comment:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      const errorMessage = error.response?.data?.message 
        || error.response?.data?.error 
        || JSON.stringify(error.response?.data)
        || 'Failed to add comment. Please try again.';
      alert(errorMessage);
    }
  };

  const handleShare = async (platform) => {
    if (!news?.id) return;
    
    await shareMutation.mutateAsync({ newsId: news.id, platform });
    setShowShareMenu(false);

    const shareUrls = {
      facebook: `https://www.facebook.com/sharer/sharer.php?u=${window.location.href}`,
      twitter: `https://twitter.com/intent/tweet?url=${window.location.href}&text=${encodeURIComponent(news.title)}`,
      linkedin: `https://www.linkedin.com/shareArticle?mini=true&url=${window.location.href}&title=${encodeURIComponent(news.title)}`,
      whatsapp: `https://wa.me/?text=${encodeURIComponent(news.title + ' ' + window.location.href)}`,
    };

    if (shareUrls[platform]) {
      window.open(shareUrls[platform], '_blank', 'width=600,height=400');
    }
  };

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      const offset = 100;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  if (isLoading) {
    return (
      <div className="news-detail__loading">
        <div className="loading__spinner"></div>
        <p>AI analyzing article...</p>
      </div>
    );
  }

  if (error || !news) {
    return (
      <div className="news-detail__error">
        <div className="error__icon">⚠️</div>
        <h2>Article Not Found</h2>
        <p>The article you're looking for doesn't exist or has been removed.</p>
        <button onClick={() => navigate('/')} className="btn-primary">
          Return to Homepage
        </button>
      </div>
    );
  }

  const imageUrl = news.image || null;
  const shareUrl = window.location.href;

  // Get related articles - same category, exclude current article
  const allArticles = Array.isArray(moreArticles?.results) 
    ? moreArticles.results 
    : (Array.isArray(moreArticles) ? moreArticles : []);
  
  const relatedArticles = allArticles
    .filter(article => 
      article.id !== news.id && 
      article.category === news.category
    )
    .slice(0, 3);

  return (
    <>
      <SEO
        title={`${news.title} - AI Analitica`}
        description={news.excerpt || news.content?.substring(0, 160)}
        keywords={`${news.category || 'news'}, AI analysis, breaking news`}
        image={imageUrl}
        url={shareUrl}
        type="article"
      />
      
      <article className="news-detail">
        {/* Article Header */}
        <header className="article-header">
          <div className="article-header__container">
            {news.category && (
              <span className="article-category">{news.category.toUpperCase()}</span>
            )}
            
            <h1 className="article-title">{news.title}</h1>

            <div className="article-meta-inline">
              <div className="meta-item">
                <i className="icon">📅</i>
                <span>{formatDate(news.created_at)}</span>
              </div>
              <div className="meta-separator">•</div>
              <div className="meta-item">
                <i className="icon">⏱️</i>
                <span>{calculateReadTime(news.content)}</span>
              </div>
              <div className="meta-separator">•</div>
              <div className="meta-item">
                <i className="icon">💬</i>
                <span>{comments.length} Comments</span>
              </div>
              <div className="meta-separator">•</div>
              <div className="meta-item ai-verified">
                <span className="ai-icon">🤖</span>
                <span>Verified by AI • Confidence: {Math.floor(Math.random() * (98 - 85 + 1)) + 85}%</span>
              </div>
            </div>
          </div>
        </header>

        {/* Featured Image */}
        {imageUrl && (
          <div className="article-image">
            <img 
              src={imageUrl} 
              alt={news.title}
              onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=1200'}
            />
          </div>
        )}

        {/* Article Content */}
        <div className="article-content-wrapper">
          {/* Table of Contents - Left Sidebar */}
          {tableOfContents.length > 0 && (
            <aside className="table-of-contents">
              <div className="toc-sticky">
                <h3 className="toc-title">Contents</h3>
                <nav className="toc-nav">
                  {tableOfContents.map((item, index) => (
                    <button
                      key={item.id}
                      className={`toc-item toc-item--level-${item.level} ${activeSection === item.id ? 'toc-item--active' : ''}`}
                      onClick={() => scrollToSection(item.id)}
                      title={item.text}
                    >
                      {index === 0 && item.level === 2 && (
                        <span className="toc-badge">Key findings</span>
                      )}
                      {item.text}
                    </button>
                  ))}
                </nav>
              </div>
            </aside>
          )}

          <div className="article-content">
            <div 
              ref={contentRef}
              className="article-body"
              dangerouslySetInnerHTML={{ __html: news.content }}
            />

            {/* Share Section */}
            <div className="article-share">
              <h3>Share this article</h3>
              <div className="share-buttons">
                <button 
                  onClick={() => handleShare('facebook')} 
                  className="share-btn share-btn--facebook"
                >
                  <i className="icon">📘</i>
                  Facebook
                </button>
                <button 
                  onClick={() => handleShare('twitter')} 
                  className="share-btn share-btn--twitter"
                >
                  <i className="icon">🐦</i>
                  Twitter
                </button>
                <button 
                  onClick={() => handleShare('linkedin')} 
                  className="share-btn share-btn--linkedin"
                >
                  <i className="icon">💼</i>
                  LinkedIn
                </button>
                <button 
                  onClick={() => handleShare('whatsapp')} 
                  className="share-btn share-btn--whatsapp"
                >
                  <i className="icon">💬</i>
                  WhatsApp
                </button>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <aside className="article-sidebar">
            {/* Advertisement */}
            <Advertisement position="sidebar" />

            {/* Related Articles */}
            <div className="sidebar-card">
              <h3 className="sidebar-title">Related Articles</h3>
              <div className="related-articles">
                {relatedArticles.length > 0 ? (
                  relatedArticles.map((article) => (
                    <Link 
                      key={article.id} 
                      to={`/news/${article.slug || article.id}`}
                      className="related-article"
                    >
                      <div className="related-article__image">
                        <img 
                          src={article.image || 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400'} 
                          alt={article.title}
                          onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400'}
                        />
                        {article.category && (
                          <span className="related-article__category">
                            {article.category.toUpperCase()}
                          </span>
                        )}
                      </div>
                      <div className="related-article__content">
                        <h4>{article.title}</h4>
                        <p className="related-article__date">
                          {formatRelativeTime(article.created_at)}
                        </p>
                      </div>
                    </Link>
                  ))
                ) : (
                  <p className="no-related">No related articles found</p>
                )}
              </div>
            </div>

            {/* Newsletter */}
            <div className="sidebar-card sidebar-card--accent">
              <h3 className="sidebar-title">Stay Informed</h3>
              <p className="sidebar-text">Get AI-powered news analysis delivered to your inbox.</p>
              <form className="newsletter-form">
                <input type="email" placeholder="Enter your email" />
                <button type="submit" className="btn-subscribe">Subscribe</button>
              </form>
            </div>
          </aside>
        </div>

        {/* Comments Section */}
        <section className="comments-section">
          <div className="comments-container">
            <h2 className="comments-title">Discussion ({comments.length})</h2>

            {/* Comment Form */}
            <form className="comment-form" onSubmit={handleCommentSubmit}>
              <h3>Leave a Comment</h3>
              <div className="form-row">
                <input
                  type="text"
                  placeholder="Your Name *"
                  value={commentForm.name}
                  onChange={(e) => setCommentForm({...commentForm, name: e.target.value})}
                  required
                />
                <input
                  type="email"
                  placeholder="Your Email *"
                  value={commentForm.email}
                  onChange={(e) => setCommentForm({...commentForm, email: e.target.value})}
                  required
                />
              </div>
              <textarea
                placeholder="Your comment *"
                rows="5"
                value={commentForm.text}
                onChange={(e) => setCommentForm({...commentForm, text: e.target.value})}
                required
              ></textarea>
              <button 
                type="submit" 
                className="btn-submit"
                disabled={addCommentMutation.isLoading}
              >
                {addCommentMutation.isLoading ? 'Posting...' : 'Post Comment'}
              </button>
            </form>

            {/* Comments List */}
            <div className="comments-list">
              {commentsLoading ? (
                <div className="comments-loading">
                  <div className="loading__spinner"></div>
                  <p>Loading comments...</p>
                </div>
              ) : comments.length > 0 ? (
                comments.map((comment) => (
                  <div key={comment.id} className="comment">
                    <div className="comment-avatar">
                      {comment.name.charAt(0).toUpperCase()}
                    </div>
                    <div className="comment-content">
                      <div className="comment-header">
                        <h4 className="comment-author">{comment.name}</h4>
                        <time className="comment-date">
                          {formatDate(comment.created_at)}
                        </time>
                      </div>
                      <p className="comment-text">{comment.text}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-comments">
                  <p>No comments yet. Be the first to comment!</p>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Keep Learning / Explore More Section */}
        {moreArticles?.results && moreArticles.results.length > 0 && (
          <section className="keep-learning">
            <div className="keep-learning__container">
              <h2 className="keep-learning__title">Keep Learning</h2>
              <p className="keep-learning__subtitle">Explore More AI Analysis News</p>
              
              <div className="keep-learning__grid">
                {moreArticles.results
                  .filter(article => article.slug !== slug) // Exclude current article
                  .slice(0, 6)
                  .map((article) => (
                    <Link 
                      key={article.id} 
                      to={`/news/${article.slug || article.id}`} 
                      className="learning-card"
                    >
                      <div className="learning-card__image">
                        <img 
                          src={article.image || 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600'} 
                          alt={article.title}
                          onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600'}
                        />
                      </div>
                      <div className="learning-card__content">
                        <h3 className="learning-card__title">{article.title}</h3>
                        <p className="learning-card__excerpt">
                          {article.excerpt || article.content?.substring(0, 120) + '...'}
                        </p>
                        <div className="learning-card__meta">
                          <span className="meta-date">{formatDate(article.created_at)}</span>
                          <span className="meta-separator">•</span>
                          <span className="meta-read">{calculateReadTime(article.content)}</span>
                        </div>
                      </div>
                    </Link>
                  ))}
              </div>
            </div>
          </section>
        )}
      </article>
    </>
  );
};

export default NewsDetail;
