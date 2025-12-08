import { NavLink } from 'react-router-dom';
import './AdminSidebar.css';

const AdminSidebar = ({ isOpen, onClose }) => {
  const menuItems = [
    { path: '/admin/dashboard', icon: '📊', label: 'Dashboard' },
    { path: '/admin/news', icon: '📰', label: 'News' },
    { path: '/admin/team', icon: '👥', label: 'Team' },
    { path: '/admin/comments', icon: '💬', label: 'Comments' },
    { path: '/admin/subscribers', icon: '📧', label: 'Subscribers' },
    { path: '/admin/advertisements', icon: '📢', label: 'Advertisements' },
    { path: '/admin/legal', icon: '⚖️', label: 'Legal Pages' },
    { path: '/admin/reports', icon: '📈', label: 'Reports' },
  ];

  const aiContentItems = [
    { path: '/admin/ai-content/keywords', icon: '🔑', label: 'Keywords' },
    { path: '/admin/ai-content/generation-queue', icon: '⚙️', label: 'Generation Queue' },
    { path: '/admin/ai-content/review-queue', icon: '✓', label: 'Review Queue' },
    { path: '/admin/ai-content/settings', icon: '⚙️', label: 'AI Settings' },
    { path: '/admin/ai-content/analytics', icon: '📊', label: 'Analytics' },
  ];

  return (
    <aside 
      className={`admin-sidebar ${isOpen ? 'admin-sidebar--open' : ''}`}
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="admin-sidebar__header">
        <div>
          <h2>AI Analitica</h2>
          <p>Admin Panel</p>
        </div>
        <button 
          className="admin-sidebar__close"
          onClick={onClose}
          aria-label="Close menu"
        >
          ✕
        </button>
      </div>

      <nav className="admin-sidebar__nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            onClick={onClose}
            className={({ isActive }) =>
              `admin-sidebar__link ${isActive ? 'admin-sidebar__link--active' : ''}`
            }
            aria-label={`Navigate to ${item.label}`}
          >
            <span className="admin-sidebar__icon" aria-hidden="true">{item.icon}</span>
            <span className="admin-sidebar__label">{item.label}</span>
          </NavLink>
        ))}

        <div className="admin-sidebar__section">
          <h3 className="admin-sidebar__section-title">🤖 AI Content Generation</h3>
          {aiContentItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={onClose}
              className={({ isActive }) =>
                `admin-sidebar__link ${isActive ? 'admin-sidebar__link--active' : ''}`
              }
              aria-label={`Navigate to ${item.label}`}
            >
              <span className="admin-sidebar__icon" aria-hidden="true">{item.icon}</span>
              <span className="admin-sidebar__label">{item.label}</span>
            </NavLink>
          ))}
        </div>
      </nav>
    </aside>
  );
};

export default AdminSidebar;
