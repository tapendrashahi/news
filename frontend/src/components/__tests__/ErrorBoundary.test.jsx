import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ErrorBoundary from '../ErrorBoundary';

const ThrowError = () => {
  throw new Error('Test error');
};

const GoodComponent = () => <div>Content loaded successfully</div>;

describe('ErrorBoundary Component', () => {
  beforeEach(() => {
    // Suppress console.error for cleaner test output
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    console.error.mockRestore();
  });

  test('renders children when there is no error', () => {
    render(
      <BrowserRouter>
        <ErrorBoundary>
          <GoodComponent />
        </ErrorBoundary>
      </BrowserRouter>
    );
    
    expect(screen.getByText('Content loaded successfully')).toBeInTheDocument();
  });

  test('renders error UI when child component throws', () => {
    render(
      <BrowserRouter>
        <ErrorBoundary>
          <ThrowError />
        </ErrorBoundary>
      </BrowserRouter>
    );
    
    expect(screen.getByText('Oops! Something went wrong')).toBeInTheDocument();
  });

  test('displays error message when available', () => {
    render(
      <BrowserRouter>
        <ErrorBoundary>
          <ThrowError />
        </ErrorBoundary>
      </BrowserRouter>
    );
    
    expect(screen.getByText(/Test error/i)).toBeInTheDocument();
  });

  test('renders Try Again button', () => {
    render(
      <BrowserRouter>
        <ErrorBoundary>
          <ThrowError />
        </ErrorBoundary>
      </BrowserRouter>
    );
    
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();
  });
});
