import React, { useState } from 'react';
import { useNews, useCategories } from '../hooks';
import { NewsList, Pagination, Newsletter, SearchBar, SEO } from '../components';
import './Home.css';

const Home = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState('');

  const { data, isLoading, error } = useNews({ 
    page: currentPage, 
    category: selectedCategory 
  });
  
  const { data: categoriesData } = useCategories();

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCategoryChange = (category) => {
    setSelectedCategory(category === selectedCategory ? '' : category);
    setCurrentPage(1);
  };

  const news = data?.results || [];
  const totalCount = data?.count || 0;
  const itemsPerPage = 10;
  const totalPages = Math.ceil(totalCount / itemsPerPage);

  return (
    <>
      <SEO
        title="Latest News - News Portal"
        description="Stay informed with the latest breaking news, updates, and stories from around the world."
        keywords="news, breaking news, latest news, world news, updates"
      />
      
      <div className="home">
        <div className="home__hero">
          <h1 className="home__title">Latest News</h1>
          <p className="home__subtitle">Stay informed with breaking news and updates</p>
          <SearchBar />
        </div>

        {categoriesData?.categories && categoriesData.categories.length > 0 && (
          <div className="home__categories">
            <h2 className="home__categories-title">Categories</h2>
            <div className="home__categories-list">
              {categoriesData.categories.map((cat) => (
                <button
                  key={cat.name}
                  className={`category-chip ${selectedCategory === cat.name ? 'category-chip--active' : ''}`}
                  onClick={() => handleCategoryChange(cat.name)}
                  aria-pressed={selectedCategory === cat.name}
                  aria-label={`Filter by ${cat.display_name} category`}
                >
                  {cat.display_name} ({cat.count})
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="home__content">
          <NewsList 
            news={news} 
            loading={isLoading} 
            error={error}
            emptyMessage={selectedCategory ? `No news found in ${selectedCategory} category.` : 'No news articles found.'}
          />
          
          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          )}
        </div>

        <Newsletter />
      </div>
    </>
  );
};

export default Home;
