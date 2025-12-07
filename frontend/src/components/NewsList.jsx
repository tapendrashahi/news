import React from 'react';
import NewsCard from './NewsCard';
import Loading from './Loading';
import './NewsList.css';

const NewsList = ({ news, loading, error, emptyMessage = 'No news articles found.' }) => {
  if (loading) {
    return <Loading size="large" text="Loading news articles..." />;
  }

  if (error) {
    return (
      <div className="news-list__error">
        <p>Error loading news: {error.message}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  if (!news || news.length === 0) {
    return (
      <div className="news-list__empty">
        <p>{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="news-list">
      {news.map((article, index) => (
        <NewsCard 
          key={article.id} 
          news={article} 
          featured={index === 0}
        />
      ))}
    </div>
  );
};

export default NewsList;
