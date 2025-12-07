import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useSearchNews } from '../hooks';
import { NewsList, Pagination, SearchBar } from '../components';
import './Search.css';

const Search = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const [currentPage, setCurrentPage] = useState(1);

  const { data, isLoading, error } = useSearchNews(query, currentPage);

  // Reset page when search query changes
  useEffect(() => {
    setCurrentPage(1);
  }, [query]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const news = data?.results || [];
  const totalCount = data?.count || 0;
  const itemsPerPage = 10;
  const totalPages = Math.ceil(totalCount / itemsPerPage);

  return (
    <div className="search">
      <div className="search__header">
        <h1 className="search__title">Search Results</h1>
        <div className="search__bar-container">
          <SearchBar initialValue={query} />
        </div>
      </div>

      {query && (
        <div className="search__query-info">
          <p>
            {isLoading ? (
              'Searching...'
            ) : (
              <>
                Found <strong>{totalCount}</strong> result{totalCount !== 1 ? 's' : ''} for{' '}
                <strong>"{query}"</strong>
              </>
            )}
          </p>
        </div>
      )}

      {!query ? (
        <div className="search__empty">
          <h2>Enter a search term</h2>
          <p>Type keywords in the search box above to find news articles.</p>
        </div>
      ) : (
        <>
          <NewsList
            news={news}
            loading={isLoading}
            error={error}
            emptyMessage={`No results found for "${query}". Try different keywords.`}
          />

          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          )}
        </>
      )}
    </div>
  );
};

export default Search;
