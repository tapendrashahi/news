import { Link, NavLink } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header__container">
        <Link to="/" className="header__logo">
          News Portal
        </Link>
        <nav className="header__nav">
          <ul className="header__nav-list">
            <li>
              <NavLink 
                to="/" 
                className={({ isActive }) => 
                  isActive ? 'header__nav-link header__nav-link--active' : 'header__nav-link'
                }
              >
                Home
              </NavLink>
            </li>
            <li>
              <NavLink 
                to="/category/tech" 
                className={({ isActive }) => 
                  isActive ? 'header__nav-link header__nav-link--active' : 'header__nav-link'
                }
              >
                Tech
              </NavLink>
            </li>
            <li>
              <NavLink 
                to="/category/business" 
                className={({ isActive }) => 
                  isActive ? 'header__nav-link header__nav-link--active' : 'header__nav-link'
                }
              >
                Business
              </NavLink>
            </li>
            <li>
              <NavLink 
                to="/category/political" 
                className={({ isActive }) => 
                  isActive ? 'header__nav-link header__nav-link--active' : 'header__nav-link'
                }
              >
                Political
              </NavLink>
            </li>
            <li>
              <NavLink 
                to="/about" 
                className={({ isActive }) => 
                  isActive ? 'header__nav-link header__nav-link--active' : 'header__nav-link'
                }
              >
                About
              </NavLink>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;
