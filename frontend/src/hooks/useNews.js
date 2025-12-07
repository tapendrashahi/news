import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { newsService } from '../services/newsService';

/**
 * Hook for fetching paginated news list
 * @param {Object} params - Query parameters
 * @param {number} params.page - Page number
 * @param {string} params.category - Category filter
 * @param {string} params.search - Search query
 * @returns {Object} Query result with news data, loading state, and error
 */
export const useNews = ({ page = 1, category = '', search = '' } = {}) => {
  return useQuery({
    queryKey: ['news', { page, category, search }],
    queryFn: () => newsService.getNews({ page, category, search }),
    keepPreviousData: true,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook for fetching single news article by slug
 * @param {string} slug - News article slug
 * @returns {Object} Query result with news detail, loading state, and error
 */
export const useNewsDetail = (slug) => {
  return useQuery({
    queryKey: ['news', slug],
    queryFn: () => newsService.getNewsDetail(slug),
    enabled: !!slug,
    staleTime: 5 * 60 * 1000,
  });
};

/**
 * Hook for fetching news by category
 * @param {string} category - Category name
 * @param {number} page - Page number
 * @returns {Object} Query result with news data
 */
export const useNewsByCategory = (category, page = 1) => {
  return useQuery({
    queryKey: ['news', 'category', category, page],
    queryFn: () => newsService.getNewsByCategory(category, page),
    enabled: !!category,
    keepPreviousData: true,
    staleTime: 5 * 60 * 1000,
  });
};

/**
 * Hook for searching news
 * @param {string} query - Search query
 * @param {number} page - Page number
 * @returns {Object} Query result with search results
 */
export const useSearchNews = (query, page = 1) => {
  return useQuery({
    queryKey: ['news', 'search', query, page],
    queryFn: () => newsService.searchNews(query, page),
    enabled: !!query && query.length >= 2,
    keepPreviousData: true,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

/**
 * Hook for fetching all categories
 * @returns {Object} Query result with categories data
 */
export const useCategories = () => {
  return useQuery({
    queryKey: ['categories'],
    queryFn: () => newsService.getCategories(),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

/**
 * Hook for fetching comments for a news article
 * @param {number} newsId - News article ID
 * @returns {Object} Query result with comments data
 */
export const useComments = (newsId) => {
  return useQuery({
    queryKey: ['comments', newsId],
    queryFn: () => newsService.getComments(newsId),
    enabled: !!newsId,
    staleTime: 1 * 60 * 1000, // 1 minute
  });
};

/**
 * Hook for adding a comment
 * @returns {Object} Mutation object with mutate function
 */
export const useAddComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ newsId, commentData }) => 
      newsService.addComment(newsId, commentData),
    onSuccess: (data, { newsId }) => {
      // Invalidate and refetch comments
      queryClient.invalidateQueries(['comments', newsId]);
      // Invalidate news detail to update comment count
      queryClient.invalidateQueries(['news']);
    },
  });
};

/**
 * Hook for incrementing share count
 * @returns {Object} Mutation object with mutate function
 */
export const useShareNews = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ newsId, platform }) => 
      newsService.shareNews(newsId, platform),
    onSuccess: (data, { newsId }) => {
      // Invalidate news queries to update share count
      queryClient.invalidateQueries(['news']);
    },
  });
};

/**
 * Hook for newsletter subscription
 * @returns {Object} Mutation object with mutate function
 */
export const useSubscribe = () => {
  return useMutation({
    mutationFn: (email) => newsService.subscribe(email),
  });
};

/**
 * Hook for newsletter unsubscription
 * @returns {Object} Mutation object with mutate function
 */
export const useUnsubscribe = () => {
  return useMutation({
    mutationFn: (email) => newsService.unsubscribe(email),
  });
};

/**
 * Hook for fetching team members
 * @returns {Object} Query result with team data
 */
export const useTeam = () => {
  return useQuery({
    queryKey: ['team'],
    queryFn: () => newsService.getTeam(),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

/**
 * Hook for fetching team member details
 * @param {number} memberId - Team member ID
 * @returns {Object} Query result with team member data
 */
export const useTeamMember = (memberId) => {
  return useQuery({
    queryKey: ['team', memberId],
    queryFn: () => newsService.getTeamMember(memberId),
    enabled: !!memberId,
    staleTime: 30 * 60 * 1000,
  });
};
