import React from 'react';
import { Link } from 'react-router-dom';
import { OptimizedImage } from './';
import './NewsCard.css';

const NewsCard = ({ news, featured = false }) => {
  const {
    slug,
    title,
    excerpt,
    image,
    category_display,
    author,
    created_at,
    comment_count,
    share_count,
  } = news;

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const imageUrl = image ? `${process.env.REACT_APP_MEDIA_URL}${image}` : '/placeholder.jpg';

  return (
    <article className={`news-card ${featured ? 'news-card--featured' : ''}`}>
      <Link to={`/news/${slug}`} className="news-card__image-link">
        <OptimizedImage
          src={imageUrl} 
          alt={title}
          className="news-card__image"
        />
        {category_display && (
          <span className="news-card__category">{category_display}</span>
        )}
      </Link>
      
      <div className="news-card__content">
        <Link to={`/news/${slug}`} className="news-card__title-link">
          <h3 className="news-card__title">{title}</h3>
        </Link>
        
        {excerpt && (
          <p className="news-card__excerpt">{excerpt}</p>
        )}
        
        <div className="news-card__meta">
          {author && (
            <span className="news-card__author">
              By {author.name}
            </span>
          )}
          <span className="news-card__date">
            {formatDate(created_at)}
          </span>
        </div>
        
        <div className="news-card__stats">
          <span className="news-card__stat">
            <i className="icon-comment"></i> {comment_count || 0} Comments
          </span>
          <span className="news-card__stat">
            <i className="icon-share"></i> {share_count || 0} Shares
          </span>
        </div>
      </div>
    </article>
  );
};

export default NewsCard;
