import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="footer__container">
        <div className="footer__top">
          {/* Brand Section */}
          <div className="footer__brand">
            <div className="footer__logo">
              <div className="footer__logo-icon">🤖</div>
              <h2 className="footer__logo-text">AI Analitica</h2>
            </div>
            <p className="footer__description">
              AI-powered news analysis free from human bias. We deliver objective, 
              data-driven perspectives on global events using advanced artificial intelligence.
            </p>
            <div className="footer__social">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                <i className="fab fa-instagram"></i>
              </a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                <i className="fab fa-linkedin-in"></i>
              </a>
              <a href="https://youtube.com" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
                <i className="fab fa-youtube"></i>
              </a>
            </div>
          </div>

          {/* Company Section */}
          <div className="footer__section">
            <h3 className="footer__section-title">Company</h3>
            <ul className="footer__links">
              <li><Link to="/about" className="footer__link">About Us</Link></li>
              <li><Link to="/team" className="footer__link">Our Team</Link></li>
              <li><Link to="/careers" className="footer__link">Careers</Link></li>
              <li><Link to="/advertise" className="footer__link">Advertise</Link></li>
              <li><Link to="/contact" className="footer__link">Contact Us</Link></li>
            </ul>
          </div>

          {/* Topics Section */}
          <div className="footer__section">
            <h3 className="footer__section-title">Topics</h3>
            <ul className="footer__links">
              <li><Link to="/category/business" className="footer__link">Business</Link></li>
              <li><Link to="/category/politics" className="footer__link">Political</Link></li>
              <li><Link to="/category/tech" className="footer__link">Technology</Link></li>
              <li><Link to="/category/education" className="footer__link">Education</Link></li>
              <li><Link to="/category/sports" className="footer__link">Sports</Link></li>
            </ul>
          </div>

          {/* Legal Section */}
          <div className="footer__section">
            <h3 className="footer__section-title">Legal</h3>
            <ul className="footer__links">
              <li><Link to="/privacy-policy" className="footer__link">Privacy Policy</Link></li>
              <li><Link to="/terms-of-service" className="footer__link">Terms of Service</Link></li>
              <li><Link to="/cookie-policy" className="footer__link">Cookie Policy</Link></li>
              <li><Link to="/editorial-guidelines" className="footer__link">Editorial Guidelines</Link></li>
              <li><Link to="/ethics-policy" className="footer__link">Ethics Policy</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="footer__bottom">
          <p>&copy; {currentYear} AI Analitica. All rights reserved. Powered by AI, driven by data.</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
