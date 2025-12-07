import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Loading from '../Loading';

const queryClient = new QueryClient();

const renderWithProviders = (component) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {component}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('Loading Component', () => {
  test('renders loading text', () => {
    renderWithProviders(<Loading text="Loading..." />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders with custom text', () => {
    renderWithProviders(<Loading text="Custom loading message" />);
    expect(screen.getByText('Custom loading message')).toBeInTheDocument();
  });

  test('renders spinner', () => {
    const { container } = renderWithProviders(<Loading />);
    expect(container.querySelector('.loading__spinner')).toBeInTheDocument();
  });

  test('applies correct size class', () => {
    const { container } = renderWithProviders(<Loading size="large" />);
    expect(container.querySelector('.loading__spinner--large')).toBeInTheDocument();
  });

  test('fullScreen prop adds correct class', () => {
    const { container } = renderWithProviders(<Loading fullScreen />);
    expect(container.querySelector('.loading--fullscreen')).toBeInTheDocument();
  });
});
