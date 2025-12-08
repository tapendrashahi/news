import { Outlet } from 'react-router-dom';
import AdminSidebar from './AdminSidebar';
import AdminHeader from './AdminHeader';
import './AdminLayout.css';

const AdminLayout = () => {
  return (
    <div className="admin-layout">
      <AdminSidebar />
      <div className="admin-layout__main">
        <AdminHeader />
        <div className="admin-layout__content">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AdminLayout;
