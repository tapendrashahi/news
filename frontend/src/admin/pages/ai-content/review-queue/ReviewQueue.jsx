/**
 * Review Queue Component
 * 
 * Task 5.4: Review Queue
 * Articles ready for human review
 */
import React from 'react';

function ReviewQueue() {
  return (
    <div className="admin-page">
      <div className="admin-page__header">
        <h1>Review Queue</h1>
      </div>
      <div className="admin-page__content">
        <div className="placeholder-message">
          <h2>📝 Article Review Queue</h2>
          <p>This page will display AI-generated articles ready for review.</p>
          <p><strong>API Endpoint:</strong> /api/admin/ai/articles/?stage=REVIEW</p>
        </div>
      </div>
    </div>
  );
}

export default ReviewQueue;
