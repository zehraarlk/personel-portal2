import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import './Navbar.css';

const NAV_LINKS = [
  { label: 'Ana Sayfa', to: '/' },
  { label: 'Duyurular', to: '/#duyurular' },
  { label: 'Sistem Testi', to: '/test' },
];

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <>
      <nav className="navbar">
        <div className="nav-container">
          <Link className="nav-brand" to="/">
            <img
              className="nav-brand-logo"
              src="/images/gebze-logo.webp"
              alt=""
              onError={(e) => {
                e.currentTarget.style.display = 'none';
              }}
            />
            <span className="nav-brand-text">
              <strong>Gebze Belediyesi</strong>
              <small>Personel Portalı</small>
            </span>
          </Link>

          <button
            type="button"
            className="nav-toggle"
            aria-label="Menüyü aç"
            onClick={() => setMenuOpen(true)}
          >
            <span />
            <span />
            <span />
          </button>

          <ul className="nav-links">
            {NAV_LINKS.map((link) => (
              <li key={link.label}>
                <NavLink
                  to={link.to}
                  className={({ isActive }) =>
                    isActive && !link.to.includes('#') ? 'active' : undefined
                  }
                >
                  {link.label}
                </NavLink>
              </li>
            ))}
          </ul>

          <div className="nav-profile">
            <div className="nav-profile-avatar" aria-hidden="true">
              P
            </div>
            <span className="nav-profile-name">Personel</span>
          </div>
        </div>
      </nav>

      <div
        className={`menu-backdrop${menuOpen ? ' open' : ''}`}
        onClick={() => setMenuOpen(false)}
        aria-hidden={!menuOpen}
      />
      <aside className={`side-menu${menuOpen ? ' open' : ''}`}>
        <div className="side-menu-header">
          <strong>Menü</strong>
          <button type="button" onClick={() => setMenuOpen(false)} aria-label="Kapat">
            ×
          </button>
        </div>
        <ul>
          {NAV_LINKS.map((link) => (
            <li key={link.label}>
              <Link to={link.to} onClick={() => setMenuOpen(false)}>
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </aside>
    </>
  );
}
