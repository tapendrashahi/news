import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import AdminSidebar from './AdminSidebar';
import AdminHeader from './AdminHeader';
import './AdminLayout.css';

const AdminLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <div className="admin-layout">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div 
          className="admin-layout__overlay" 
          onClick={closeSidebar}
          aria-hidden="true"
        />
      )}
      
      <AdminSidebar isOpen={sidebarOpen} onClose={closeSidebar} />
      
      <div className="admin-layout__main">
        <AdminHeader onMenuClick={toggleSidebar} />
        <div className="admin-layout__content">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AdminLayout;
