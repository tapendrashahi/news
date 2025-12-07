import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useNewsDetail, useComments, useAddComment, useShareNews } from '../hooks';
import { CommentList, CommentForm, CategoryBadge, SEO, OptimizedImage } from '../components';
import './NewsDetail.css';

const NewsDetail = () => {
  const { slug } = useParams();
  const [showShareMenu, setShowShareMenu] = useState(false);
  
  const { data: news, isLoading, error } = useNewsDetail(slug);
  const { data: comments, isLoading: commentsLoading } = useComments(news?.id);
  const addCommentMutation = useAddComment();
  const shareMutation = useShareNews();

  const handleCommentSubmit = async (commentData) => {
    if (!news?.id) return;
    
    try {
      await addCommentMutation.mutateAsync({
        newsId: news.id,
        commentData,
      });
    } catch (error) {
      console.error('Error adding comment:', error);
      alert('Failed to add comment. Please try again.');
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

  if (isLoading) {
    return (
      <div className="news-detail__loading">
        <div className="spinner"></div>
        <p>Loading article...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="news-detail__error">
        <h2>Error Loading Article</h2>
        <p>{error.message || 'Failed to load article. Please try again.'}</p>
        <Link to="/" className="btn btn--primary">Back to Home</Link>
      </div>
    );
  }

  if (!news) {
    return (
      <div className="news-detail__not-found">
        <h2>Article Not Found</h2>
        <p>The article you're looking for doesn't exist.</p>
        <Link to="/" className="btn btn--primary">Back to Home</Link>
      </div>
    );
  }

  const imageUrl = news.image ? `${process.env.REACT_APP_MEDIA_URL}${news.image}` : null;
  const shareUrl = window.location.href;

  return (
    <>
      <SEO
        title={`${news.title} - News Portal`}
        description={news.excerpt || news.content?.substring(0, 160)}
        keywords={`${news.category_display}, news, ${news.author || ''}`}
        image={imageUrl}
        url={shareUrl}
        type="article"
      />
      
      <article className="news-detail">
        <div className="news-detail__header">
          <div className="news-detail__meta">
            {news.category_display && <CategoryBadge category={news.category_display} />}
            <time className="news-detail__date">
              {new Date(news.created_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </time>
          </div>
          
          <h1 className="news-detail__title">{news.title}</h1>
          
          {news.excerpt && (
            <p className="news-detail__excerpt">{news.excerpt}</p>
          )}
          
          <div className="news-detail__author-info">
            {news.author && (
              <span className="news-detail__author">By {news.author}</span>
            )}
            <div className="news-detail__stats">
              <span className="news-detail__stat">
                <i className="icon-comment"></i>
                {news.comment_count || 0} Comments
              </span>
              <span className="news-detail__stat">
                <i className="icon-share"></i>
                {news.share_count || 0} Shares
              </span>
            </div>
          </div>
        </div>

        {imageUrl && (
          <div className="news-detail__image-wrapper">
            <OptimizedImage
              src={imageUrl}
              alt={news.title}
              className="news-detail__image"
            />
          </div>
        )}

        <div className="news-detail__content">
          <div 
            className="news-detail__body"
            dangerouslySetInnerHTML={{ __html: news.content }}
          />
        </div>

        <div className="news-detail__actions">
          <div className="news-detail__share">
            <button 
              className="btn btn--outline"
              onClick={() => setShowShareMenu(!showShareMenu)}
              aria-expanded={showShareMenu}
              aria-label="Share article"
            >
              <i className="icon-share"></i>
              Share Article
            </button>
            
            {showShareMenu && (
              <div className="share-menu" role="menu">
                <button 
                  onClick={() => handleShare('facebook')} 
                  className="share-menu__item"
                  role="menuitem"
                  aria-label="Share on Facebook"
                >
                  <i className="icon-facebook"></i>
                  Facebook
                </button>
                <button 
                  onClick={() => handleShare('twitter')} 
                  className="share-menu__item"
                  role="menuitem"
                  aria-label="Share on Twitter"
                >
                  <i className="icon-twitter"></i>
                  Twitter
                </button>
                <button 
                  onClick={() => handleShare('linkedin')} 
                  className="share-menu__item"
                  role="menuitem"
                  aria-label="Share on LinkedIn"
                >
                  <i className="icon-linkedin"></i>
                  LinkedIn
                </button>
                <button 
                  onClick={() => handleShare('whatsapp')} 
                  className="share-menu__item"
                  role="menuitem"
                  aria-label="Share on WhatsApp"
                >
                  <i className="icon-whatsapp"></i>
                  WhatsApp
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="news-detail__comments-section">
          <h2 className="news-detail__comments-title">
            Comments ({comments?.length || 0})
          </h2>
          
          <CommentForm onSubmit={handleCommentSubmit} />
          
          {commentsLoading ? (
            <div className="news-detail__comments-loading">
              <div className="spinner"></div>
              <p>Loading comments...</p>
            </div>
          ) : (
            <CommentList comments={comments || []} />
          )}
        </div>
      </article>
    </>
  );
};

export default NewsDetail;
