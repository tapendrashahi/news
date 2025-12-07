import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for debounced search
 * @param {string} initialValue - Initial search value
 * @param {number} delay - Debounce delay in milliseconds
 * @returns {Object} Search state and controls
 */
export const useSearch = (initialValue = '', delay = 500) => {
  const [searchTerm, setSearchTerm] = useState(initialValue);
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState(initialValue);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    setIsSearching(true);
    const handler = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
      setIsSearching(false);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [searchTerm, delay]);

  const clearSearch = useCallback(() => {
    setSearchTerm('');
    setDebouncedSearchTerm('');
  }, []);

  const handleSearchChange = useCallback((value) => {
    setSearchTerm(value);
  }, []);

  return {
    searchTerm,
    debouncedSearchTerm,
    isSearching,
    setSearchTerm: handleSearchChange,
    clearSearch,
  };
};
