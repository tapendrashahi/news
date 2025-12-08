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
    { path: '/admin/reports', icon: '📈', label: 'Reports' },
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
      </nav>
    </aside>
  );
};

export default AdminSidebar;
