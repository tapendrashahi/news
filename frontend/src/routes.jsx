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

function AppRoutes() {
  return (
    <Routes>
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
    </Routes>
  );
}

export default AppRoutes;
