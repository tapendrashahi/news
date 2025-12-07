import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="footer__container">
        <div className="footer__content">
          <div className="footer__section">
            <h3 className="footer__title">About Us</h3>
            <p>Your trusted source for latest news and updates from around the world.</p>
          </div>
          
          <div className="footer__section">
            <h3 className="footer__title">Quick Links</h3>
            <ul className="footer__links">
              <li><Link to="/" className="footer__link">Home</Link></li>
              <li><Link to="/about" className="footer__link">About</Link></li>
              <li><Link to="/category/tech" className="footer__link">Technology</Link></li>
              <li><Link to="/category/business" className="footer__link">Business</Link></li>
            </ul>
          </div>
          
          <div className="footer__section">
            <h3 className="footer__title">Legal</h3>
            <ul className="footer__links">
              <li><Link to="/privacy" className="footer__link">Privacy Policy</Link></li>
              <li><Link to="/terms" className="footer__link">Terms of Service</Link></li>
              <li><Link to="/contact" className="footer__link">Contact</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="footer__bottom">
          <p>&copy; {currentYear} News Portal. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
