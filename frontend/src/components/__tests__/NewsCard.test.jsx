import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import NewsCard from '../NewsCard';

const mockNews = {
  slug: 'test-news-slug',
  title: 'Test News Title',
  excerpt: 'This is a test excerpt for the news article',
  image: 'news_images/test.jpg',
  category_display: 'Technology',
  author: 'John Doe',
  created_at: '2024-01-15T10:00:00Z',
  comment_count: 5,
  share_count: 10,
};

describe('NewsCard Component', () => {
  test('renders news title', () => {
    render(
      <BrowserRouter>
        <NewsCard news={mockNews} />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Test News Title')).toBeInTheDocument();
  });

  test('renders news excerpt', () => {
    render(
      <BrowserRouter>
        <NewsCard news={mockNews} />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/This is a test excerpt/i)).toBeInTheDocument();
  });

  test('renders category badge', () => {
    render(
      <BrowserRouter>
        <NewsCard news={mockNews} />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Technology')).toBeInTheDocument();
  });

  test('renders author name', () => {
    render(
      <BrowserRouter>
        <NewsCard news={mockNews} />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/John Doe/i)).toBeInTheDocument();
  });

  test('renders comment and share counts', () => {
    render(
      <BrowserRouter>
        <NewsCard news={mockNews} />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/5/)).toBeInTheDocument();
    expect(screen.getByText(/10/)).toBeInTheDocument();
  });

  test('link points to correct news detail page', () => {
    const { container } = render(
      <BrowserRouter>
        <NewsCard news={mockNews} />
      </BrowserRouter>
    );
    
    const links = container.querySelectorAll('a[href="/news/test-news-slug"]');
    expect(links.length).toBeGreaterThan(0);
  });

  test('applies featured class when featured prop is true', () => {
    const { container } = render(
      <BrowserRouter>
        <NewsCard news={mockNews} featured={true} />
      </BrowserRouter>
    );
    
    expect(container.querySelector('.news-card--featured')).toBeInTheDocument();
  });
});
