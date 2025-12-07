import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useNewsByCategory } from '../hooks';
import { NewsList, Pagination, Newsletter } from '../components';
import './Category.css';

const Category = () => {
  const { category } = useParams();
  const [currentPage, setCurrentPage] = useState(1);

  const { data, isLoading, error } = useNewsByCategory(category, currentPage);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const news = data?.results || [];
  const totalCount = data?.count || 0;
  const itemsPerPage = 10;
  const totalPages = Math.ceil(totalCount / itemsPerPage);

  // Format category name for display
  const categoryDisplay = category
    ? category.charAt(0).toUpperCase() + category.slice(1)
    : '';

  return (
    <div className="category-page">
      <div className="category-page__header">
        <h1 className="category-page__title">{categoryDisplay} News</h1>
        <p className="category-page__subtitle">
          Latest updates and articles in {categoryDisplay.toLowerCase()}
        </p>
      </div>

      <div className="category-page__content">
        <NewsList
          news={news}
          loading={isLoading}
          error={error}
          emptyMessage={`No articles found in ${categoryDisplay} category.`}
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
  );
};

export default Category;
