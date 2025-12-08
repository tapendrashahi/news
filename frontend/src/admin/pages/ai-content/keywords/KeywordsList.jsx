/**
 * Keywords List Component
 * 
 * Task 5.2: Keywords Management
 * Main list view for keyword management
 */
import React from 'react';

function KeywordsList() {
  return (
    <div className="admin-page">
      <div className="admin-page__header">
        <h1>Keywords Management</h1>
      </div>
      <div className="admin-page__content">
        <div className="placeholder-message">
          <h2>🔑 Keywords List</h2>
          <p>This page will display keyword sources for AI content generation.</p>
          <p><strong>API Endpoint:</strong> /api/admin/ai/keywords/</p>
        </div>
      </div>
    </div>
  );
}

export default KeywordsList;
