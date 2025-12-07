import React from 'react';
import './CommentList.css';

const CommentList = ({ comments, loading = false }) => {
  if (loading) {
    return (
      <div className="comment-list__loading">
        <div className="spinner"></div>
        <p>Loading comments...</p>
      </div>
    );
  }

  if (!comments || comments.length === 0) {
    return (
      <div className="comment-list__empty">
        <p>No comments yet. Be the first to comment!</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const options = { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="comment-list">
      <h3 className="comment-list__title">Comments ({comments.length})</h3>
      {comments.map((comment) => (
        <div key={comment.id} className="comment">
          <div className="comment__header">
            <div className="comment__avatar">
              {comment.name.charAt(0).toUpperCase()}
            </div>
            <div className="comment__meta">
              <span className="comment__author">{comment.name}</span>
              <span className="comment__date">{formatDate(comment.created_at)}</span>
            </div>
          </div>
          <div className="comment__body">
            <p className="comment__text">{comment.text}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CommentList;
