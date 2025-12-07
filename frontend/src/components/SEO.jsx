import { useEffect } from 'react';

const SEO = ({
  title = 'News Portal',
  description = 'Stay informed with the latest news and updates',
  keywords = 'news, breaking news, latest news, updates',
  author = 'News Portal',
  image = '/og-image.jpg',
  url = window.location.href,
  type = 'website',
}) => {
  useEffect(() => {
    // Set document title
    document.title = title;

    // Set or update meta tags
    const setMetaTag = (name, content, property = false) => {
      const attribute = property ? 'property' : 'name';
      let element = document.querySelector(`meta[${attribute}="${name}"]`);
      
      if (!element) {
        element = document.createElement('meta');
        element.setAttribute(attribute, name);
        document.head.appendChild(element);
      }
      
      element.setAttribute('content', content);
    };

    // Standard meta tags
    setMetaTag('description', description);
    setMetaTag('keywords', keywords);
    setMetaTag('author', author);

    // Open Graph meta tags
    setMetaTag('og:title', title, true);
    setMetaTag('og:description', description, true);
    setMetaTag('og:image', image, true);
    setMetaTag('og:url', url, true);
    setMetaTag('og:type', type, true);

    // Twitter Card meta tags
    setMetaTag('twitter:card', 'summary_large_image');
    setMetaTag('twitter:title', title);
    setMetaTag('twitter:description', description);
    setMetaTag('twitter:image', image);

    // Cleanup function
    return () => {
      document.title = 'News Portal';
    };
  }, [title, description, keywords, author, image, url, type]);

  return null; // This component doesn't render anything
};

export default SEO;
