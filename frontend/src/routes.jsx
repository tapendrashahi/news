import { Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import NewsDetail from './pages/NewsDetail';
import Category from './pages/Category';
import Search from './pages/Search';
import About from './pages/About';
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
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
