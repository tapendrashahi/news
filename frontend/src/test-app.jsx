import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

const TestApp = () => {
  return <h1 style={{ color: 'red', fontSize: '48px' }}>REACT IS WORKING!</h1>;
};

const root = createRoot(document.getElementById('root'));
root.render(
  <StrictMode>
    <TestApp />
  </StrictMode>
);
