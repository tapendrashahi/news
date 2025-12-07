import React from 'react';
import { Link } from 'react-router-dom';
import './CategoryBadge.css';

const CategoryBadge = ({ category, count, size = 'medium' }) => {
  if (!category) return null;

  const categoryColors = {
    business: '#28a745',
    tech: '#007bff',
    sports: '#fd7e14',
    entertainment: '#e83e8c',
    health: '#20c997',
    science: '#6f42c1',
    politics: '#dc3545',
    world: '#17a2b8',
  };

  const color = categoryColors[category.toLowerCase()] || '#6c757d';

  return (
    <Link
      to={`/category/${category.toLowerCase()}`}
      className={`category-badge category-badge--${size}`}
      style={{ backgroundColor: color }}
    >
      {category}
      {count !== undefined && <span className="category-badge__count">({count})</span>}
    </Link>
  );
};

export default CategoryBadge;
