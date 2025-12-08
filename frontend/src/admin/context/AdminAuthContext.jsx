import { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import adminAuthService from '../services/adminAuthService';

const AdminAuthContext = createContext(null);

export const AdminAuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user session is valid
    const checkAuth = async () => {
      try {
        // First get CSRF token
        await adminAuthService.getCsrfToken();
        
        // Then check if user is authenticated
        const userData = await adminAuthService.getCurrentUser();
        setUser(userData);
      } catch (error) {
        // Session invalid or expired
        console.log('No valid session found');
        setUser(null);
        localStorage.removeItem('adminUser');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (username, password) => {
    try {
      const data = await adminAuthService.login(username, password);
      setUser(data.user);
      navigate('/admin/dashboard');
      return { success: true };
    } catch (error) {
      return { success: false, error };
    }
  };

  const logout = async () => {
    try {
      await adminAuthService.logout();
      setUser(null);
      navigate('/admin/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear user state even if API fails
      setUser(null);
      navigate('/admin/login');
    }
  };

  const refreshUser = async () => {
    try {
      const userData = await adminAuthService.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to refresh user:', error);
      setUser(null);
    }
  };

  const value = {
    user,
    loading,
    login,
    logout,
    refreshUser,
    isAuthenticated: !!user,
    isAdmin: user?.is_staff || false
  };

  return (
    <AdminAuthContext.Provider value={value}>
      {children}
    </AdminAuthContext.Provider>
  );
};

export const useAdminAuth = () => {
  const context = useContext(AdminAuthContext);
  if (!context) {
    throw new Error('useAdminAuth must be used within AdminAuthProvider');
  }
  return context;
};

export default AdminAuthContext;
