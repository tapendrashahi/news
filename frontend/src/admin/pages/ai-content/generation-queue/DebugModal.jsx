import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './DebugModal.css';

const DebugModal = ({ article, onClose }) => {
  const [debugInfo, setDebugInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (article) {
      fetchDebugInfo();
    }
  }, [article]);

  const fetchDebugInfo = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/admin/ai/articles/${article.id}/debug_info/`);
      setDebugInfo(response.data);
    } catch (error) {
      console.error('Failed to fetch debug info:', error);
      
      // Provide fallback data structure
      setDebugInfo({
        error: true,
        error_message: 'Failed to load debug information',
        article_id: article.id,
        keyword: article.keyword?.keyword || 'Unknown',
        status: article.status || 'Unknown',
        workflow_stage: article.workflow_stage || 'Unknown',
        failed_stage: article.failed_stage || null,
        last_updated: article.updated_at || null,
        created_at: article.created_at || null,
        has_error: true,
        last_error: error.response?.data?.detail || error.message || 'Unknown error occurred',
        error_log: [],
        progress: {
          has_title: false,
          has_research: false,
          has_outline: false,
          has_content: false,
          word_count: 0
        }
      });
    } finally {
      setLoading(false);
    }
  };

  if (!article) return null;

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'N/A';
    return new Date(timestamp).toLocaleString();
  };

  const formatDuration = (seconds) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}m ${secs}s`;
  };

  const exportDebugInfo = () => {
    if (!debugInfo) return;

    // Build text content
    let content = `DEBUG INFORMATION - Article ${debugInfo.article_id}\n`;
    content += `Generated: ${new Date().toLocaleString()}\n`;
    content += `${'='.repeat(80)}\n\n`;

    // Article Info
    content += `ARTICLE INFORMATION\n`;
    content += `${'-'.repeat(80)}\n`;
    content += `ID: ${debugInfo.article_id}\n`;
    content += `Keyword: ${debugInfo.keyword}\n`;
    content += `Status: ${debugInfo.status}\n`;
    content += `Current Stage: ${debugInfo.workflow_stage || 'N/A'}\n`;
    if (debugInfo.failed_stage) {
      content += `Failed Stage: ${debugInfo.failed_stage}\n`;
    }
    content += `Created: ${formatTimestamp(debugInfo.created_at)}\n`;
    content += `Last Updated: ${formatTimestamp(debugInfo.last_updated)}\n\n`;

    // Progress
    if (debugInfo.progress) {
      content += `PROGRESS\n`;
      content += `${'-'.repeat(80)}\n`;
      content += `Title Generated: ${debugInfo.progress.has_title ? 'YES' : 'NO'}\n`;
      content += `Research Completed: ${debugInfo.progress.has_research ? 'YES' : 'NO'}\n`;
      content += `Outline Created: ${debugInfo.progress.has_outline ? 'YES' : 'NO'}\n`;
      content += `Content Generated: ${debugInfo.progress.has_content ? 'YES' : 'NO'}\n`;
      content += `Word Count: ${debugInfo.progress.word_count || 0}\n\n`;
    }

    // Timing
    content += `TIMING\n`;
    content += `${'-'.repeat(80)}\n`;
    if (debugInfo.generation_started) {
      content += `Generation Started: ${formatTimestamp(debugInfo.generation_started)}\n`;
    }
    if (debugInfo.generation_completed) {
      content += `Generation Completed: ${formatTimestamp(debugInfo.generation_completed)}\n`;
    }
    if (debugInfo.generation_duration_seconds) {
      content += `Duration: ${formatDuration(debugInfo.generation_duration_seconds)}\n`;
    }
    if (debugInfo.elapsed_seconds) {
      content += `Elapsed Time: ${formatDuration(debugInfo.elapsed_seconds)}\n`;
    }
    content += `\n`;

    // Error Details
    if (debugInfo.has_error) {
      content += `ERROR DETAILS\n`;
      content += `${'-'.repeat(80)}\n`;
      if (debugInfo.last_error) {
        content += `Last Error:\n${debugInfo.last_error}\n\n`;
      }

      if (debugInfo.error_log && debugInfo.error_log.length > 0) {
        content += `ERROR LOG (${debugInfo.error_log.length} entries)\n`;
        content += `${'-'.repeat(80)}\n`;
        debugInfo.error_log.forEach((log, idx) => {
          content += `\nError #${idx + 1}\n`;
          content += `Timestamp: ${formatTimestamp(log.timestamp)}\n`;
          content += `Stage: ${log.stage}\n`;
          content += `Type: ${log.error_type}\n`;
          content += `Message: ${log.error_message}\n`;
          if (log.traceback) {
            content += `\nTraceback:\n${log.traceback}\n`;
          }
          content += `${'-'.repeat(40)}\n`;
        });
      }
    }

    // Quality Metrics
    if (debugInfo.quality_metrics) {
      content += `\nQUALITY METRICS\n`;
      content += `${'-'.repeat(80)}\n`;
      Object.entries(debugInfo.quality_metrics).forEach(([key, value]) => {
        const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        content += `${label}: ${value !== null ? value : 'N/A'}\n`;
      });
    }

    content += `\n${'='.repeat(80)}\n`;
    content += `End of Debug Report\n`;

    // Create and download file
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `debug-${debugInfo.article_id}-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="debug-modal-overlay" onClick={onClose}>
      <div className="debug-modal" onClick={(e) => e.stopPropagation()}>
        <div className="debug-modal-header">
          <h2>🐛 Debug Information</h2>
          <div className="debug-header-actions">
            <button className="btn-refresh" onClick={fetchDebugInfo} title="Refresh">
              🔄 Refresh
            </button>
            <button className="btn-export" onClick={exportDebugInfo} title="Export to TXT">
              📥 Export
            </button>
            <button className="close-btn" onClick={onClose}>×</button>
          </div>
        </div>

        {loading ? (
          <div className="debug-loading">
            <div className="spinner"></div>
            <p>Loading debug information...</p>
          </div>
        ) : debugInfo ? (
          <div className="debug-modal-content">
            {debugInfo.error && (
              <div className="debug-warning">
                <p>⚠️ {debugInfo.error_message}</p>
                <p style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
                  Showing available information from article object
                </p>
              </div>
            )}
            
            {/* Article Info */}
            <section className="debug-section">
              <h3>📄 Article Information</h3>
              <div className="debug-info-grid">
                <div className="debug-info-item">
                  <span className="label">ID:</span>
                  <span className="value mono">{debugInfo.article_id}</span>
                </div>
                <div className="debug-info-item">
                  <span className="label">Keyword:</span>
                  <span className="value">{debugInfo.keyword}</span>
                </div>
                <div className="debug-info-item">
                  <span className="label">Status:</span>
                  <span className={`value status-badge status-${debugInfo.status}`}>
                    {debugInfo.status}
                  </span>
                </div>
                <div className="debug-info-item">
                  <span className="label">Current Stage:</span>
                  <span className="value">{debugInfo.workflow_stage || 'N/A'}</span>
                </div>
                {debugInfo.failed_stage && (
                  <div className="debug-info-item">
                    <span className="label">Failed Stage:</span>
                    <span className="value error-text">{debugInfo.failed_stage}</span>
                  </div>
                )}
              </div>
            </section>

            {/* Progress Info */}
            {debugInfo.progress && (
              <section className="debug-section">
                <h3>📊 Progress</h3>
                <div className="debug-progress-grid">
                  <div className={`progress-item ${debugInfo.progress.has_title ? 'complete' : 'incomplete'}`}>
                    <span className="icon">{debugInfo.progress.has_title ? '✓' : '○'}</span>
                    <span>Title Generated</span>
                  </div>
                  <div className={`progress-item ${debugInfo.progress.has_research ? 'complete' : 'incomplete'}`}>
                    <span className="icon">{debugInfo.progress.has_research ? '✓' : '○'}</span>
                    <span>Research Completed</span>
                  </div>
                  <div className={`progress-item ${debugInfo.progress.has_outline ? 'complete' : 'incomplete'}`}>
                    <span className="icon">{debugInfo.progress.has_outline ? '✓' : '○'}</span>
                    <span>Outline Created</span>
                  </div>
                  <div className={`progress-item ${debugInfo.progress.has_content ? 'complete' : 'incomplete'}`}>
                    <span className="icon">{debugInfo.progress.has_content ? '✓' : '○'}</span>
                    <span>Content Generated ({debugInfo.progress.word_count || 0} words)</span>
                  </div>
                </div>
              </section>
            )}

            {/* Timing Info */}
            <section className="debug-section">
              <h3>⏱️ Timing</h3>
              <div className="debug-info-grid">
                <div className="debug-info-item">
                  <span className="label">Created:</span>
                  <span className="value">{formatTimestamp(debugInfo.created_at)}</span>
                </div>
                <div className="debug-info-item">
                  <span className="label">Last Updated:</span>
                  <span className="value">{formatTimestamp(debugInfo.last_updated)}</span>
                </div>
                {debugInfo.generation_started && (
                  <div className="debug-info-item">
                    <span className="label">Started:</span>
                    <span className="value">{formatTimestamp(debugInfo.generation_started)}</span>
                  </div>
                )}
                {debugInfo.generation_duration_seconds && (
                  <div className="debug-info-item">
                    <span className="label">Duration:</span>
                    <span className="value">{formatDuration(debugInfo.generation_duration_seconds)}</span>
                  </div>
                )}
                {debugInfo.elapsed_seconds && (
                  <div className="debug-info-item">
                    <span className="label">Elapsed Time:</span>
                    <span className="value warning-text">{formatDuration(debugInfo.elapsed_seconds)}</span>
                  </div>
                )}
              </div>
            </section>

            {/* Error Information */}
            {debugInfo.has_error && (
              <section className="debug-section error-section">
                <h3>❌ Error Details</h3>
                {debugInfo.last_error && (
                  <div className="error-box">
                    <pre className="error-content">{debugInfo.last_error}</pre>
                  </div>
                )}
                
                {debugInfo.error_log && debugInfo.error_log.length > 0 && (
                  <div className="error-log">
                    <h4>Error Log ({debugInfo.error_log.length} entries)</h4>
                    {debugInfo.error_log.slice(-3).reverse().map((log, idx) => (
                      <div key={idx} className="error-log-entry">
                        <div className="error-log-header">
                          <span className="error-type">{log.error_type}</span>
                          <span className="error-timestamp">{formatTimestamp(log.timestamp)}</span>
                        </div>
                        <div className="error-stage">Stage: {log.stage}</div>
                        <div className="error-message">{log.error_message}</div>
                        {log.traceback && (
                          <details>
                            <summary>Show Traceback</summary>
                            <pre className="traceback">{log.traceback}</pre>
                          </details>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </section>
            )}

            {/* Quality Metrics */}
            {debugInfo.quality_metrics && (
              <section className="debug-section">
                <h3>📈 Quality Metrics</h3>
                <div className="debug-info-grid">
                  {Object.entries(debugInfo.quality_metrics).map(([key, value]) => (
                    <div key={key} className="debug-info-item">
                      <span className="label">{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                      <span className="value">{value !== null ? value : 'N/A'}</span>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </div>
        ) : (
          <div className="debug-error">
            <p>Failed to load debug information</p>
          </div>
        )}

        <div className="debug-modal-footer">
          <button className="btn-refresh" onClick={fetchDebugInfo}>
            🔄 Refresh
          </button>
          <button className="btn-close" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default DebugModal;
