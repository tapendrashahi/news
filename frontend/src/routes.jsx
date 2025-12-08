import { Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import NewsDetail from './pages/NewsDetail';
import Category from './pages/Category';
import Search from './pages/Search';
import About from './pages/About';
import Team from './pages/Team';
import Careers from './pages/Careers';
import PrivacyPolicy from './pages/PrivacyPolicy';
import TermsOfService from './pages/TermsOfService';
import CookiePolicy from './pages/CookiePolicy';
import EditorialGuidelines from './pages/EditorialGuidelines';
import EthicsPolicy from './pages/EthicsPolicy';
import NotFound from './pages/NotFound';

// Admin imports
import { AdminAuthProvider } from './admin/context/AdminAuthContext';
import AdminAuthGuard from './admin/components/common/AdminAuthGuard';
import AdminLogin from './admin/pages/AdminLogin';
import AdminLayout from './admin/components/layout/AdminLayout';
import Dashboard from './admin/pages/Dashboard';
import NewsList from './admin/pages/news/NewsList';
import NewsCreate from './admin/pages/news/NewsCreate';
import NewsEdit from './admin/pages/news/NewsEdit';
import TeamList from './admin/pages/team/TeamList';
import TeamCreate from './admin/pages/team/TeamCreate';
import TeamEdit from './admin/pages/team/TeamEdit';
import TeamDetail from './admin/pages/team/TeamDetail';
import CommentsList from './admin/pages/comments/CommentsList';
import SubscribersList from './admin/pages/subscribers/SubscribersList';
import Reports from './admin/pages/reports/Reports';

function AppRoutes() {
  return (
    <AdminAuthProvider>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="news/:slug" element={<NewsDetail />} />
          <Route path="category/:category" element={<Category />} />
          <Route path="search" element={<Search />} />
          <Route path="about" element={<About />} />
          <Route path="team" element={<Team />} />
          <Route path="careers" element={<Careers />} />
          <Route path="privacy-policy" element={<PrivacyPolicy />} />
          <Route path="terms-of-service" element={<TermsOfService />} />
          <Route path="cookie-policy" element={<CookiePolicy />} />
          <Route path="editorial-guidelines" element={<EditorialGuidelines />} />
          <Route path="ethics-policy" element={<EthicsPolicy />} />
          <Route path="*" element={<NotFound />} />
        </Route>

        {/* Admin routes */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route
          path="/admin/*"
          element={
            <AdminAuthGuard>
              <AdminLayout />
            </AdminAuthGuard>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="news" element={<NewsList />} />
          <Route path="news/create" element={<NewsCreate />} />
          <Route path="news/:id/edit" element={<NewsEdit />} />
          <Route path="team" element={<TeamList />} />
          <Route path="team/create" element={<TeamCreate />} />
          <Route path="team/:id" element={<TeamDetail />} />
          <Route path="team/:id/edit" element={<TeamEdit />} />
          <Route path="comments" element={<CommentsList />} />
          <Route path="subscribers" element={<SubscribersList />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
    </AdminAuthProvider>
  );
}

export default AppRoutes;
