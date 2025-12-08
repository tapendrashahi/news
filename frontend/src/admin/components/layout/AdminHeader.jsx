import { useAdminAuth } from '../../context/AdminAuthContext';
import './AdminHeader.css';

const AdminHeader = ({ onMenuClick }) => {
  const { user, logout } = useAdminAuth();

  return (
    <header className="admin-header">
      <div className="admin-header__left">
        <button 
          className="admin-header__menu-btn"
          onClick={onMenuClick}
          aria-label="Toggle menu"
        >
          <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <div className="admin-header__breadcrumb">
          {/* Breadcrumb can be added here */}
        </div>
      </div>

      <div className="admin-header__actions">
        <div className="admin-header__user">
          <div className="admin-header__user-info">
            <span className="admin-header__user-name">
              {user?.first_name || user?.username || 'Admin'}
            </span>
            <span className="admin-header__user-role">
              {user?.is_superuser ? 'Super Admin' : 'Admin'}
            </span>
          </div>
          <div className="admin-header__user-avatar">
            {(user?.first_name?.[0] || user?.username?.[0] || 'A').toUpperCase()}
          </div>
        </div>

        <button
          className="admin-header__logout"
          onClick={logout}
          title="Logout"
        >
          🚪 Logout
        </button>
      </div>
    </header>
  );
};

export default AdminHeader;
