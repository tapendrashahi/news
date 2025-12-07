import React from 'react';
import './Pagination.css';

const Pagination = ({ currentPage, totalPages, onPageChange, maxVisible = 5 }) => {
  if (totalPages <= 1) return null;

  const getPageNumbers = () => {
    const pages = [];
    let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);

    if (endPage - startPage + 1 < maxVisible) {
      startPage = Math.max(1, endPage - maxVisible + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return pages;
  };

  const pageNumbers = getPageNumbers();
  const showFirstPage = pageNumbers[0] > 1;
  const showLastPage = pageNumbers[pageNumbers.length - 1] < totalPages;

  return (
    <nav className="pagination" role="navigation" aria-label="Pagination navigation">
      <button
        className="pagination__button"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Go to previous page"
      >
        ‹ Previous
      </button>

      {showFirstPage && (
        <>
          <button
            className="pagination__page"
            onClick={() => onPageChange(1)}
            aria-label="Go to page 1"
          >
            1
          </button>
          {pageNumbers[0] > 2 && <span className="pagination__ellipsis" aria-hidden="true">...</span>}
        </>
      )}

      {pageNumbers.map((pageNum) => (
        <button
          key={pageNum}
          className={`pagination__page ${pageNum === currentPage ? 'pagination__page--active' : ''}`}
          onClick={() => onPageChange(pageNum)}
          aria-current={pageNum === currentPage ? 'page' : undefined}
          aria-label={`Go to page ${pageNum}`}
        >
          {pageNum}
        </button>
      ))}

      {showLastPage && (
        <>
          {pageNumbers[pageNumbers.length - 1] < totalPages - 1 && (
            <span className="pagination__ellipsis" aria-hidden="true">...</span>
          )}
          <button
            className="pagination__page"
            onClick={() => onPageChange(totalPages)}
            aria-label={`Go to page ${totalPages}`}
          >
            {totalPages}
          </button>
        </>
      )}

      <button
        className="pagination__button"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label="Go to next page"
      >
        Next ›
      </button>
    </nav>
  );
};

export default Pagination;
