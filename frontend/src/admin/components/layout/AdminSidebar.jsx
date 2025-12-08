import { NavLink } from 'react-router-dom';
import './AdminSidebar.css';

const AdminSidebar = () => {
  const menuItems = [
    { path: '/admin/dashboard', icon: '📊', label: 'Dashboard' },
    { path: '/admin/news', icon: '📰', label: 'News' },
    { path: '/admin/team', icon: '👥', label: 'Team' },
    { path: '/admin/comments', icon: '💬', label: 'Comments' },
    { path: '/admin/subscribers', icon: '📧', label: 'Subscribers' },
    { path: '/admin/reports', icon: '📈', label: 'Reports' },
  ];

  return (
    <aside className="admin-sidebar">
      <div className="admin-sidebar__header">
        <h2>AI Analitica</h2>
        <p>Admin Panel</p>
      </div>

      <nav className="admin-sidebar__nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `admin-sidebar__link ${isActive ? 'admin-sidebar__link--active' : ''}`
            }
          >
            <span className="admin-sidebar__icon">{item.icon}</span>
            <span className="admin-sidebar__label">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default AdminSidebar;
