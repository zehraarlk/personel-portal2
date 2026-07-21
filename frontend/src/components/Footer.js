import './Footer.css';

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div>
          <strong>Gebze Belediyesi</strong>
          <p>Personel Portalı — kurum içi duyuru ve kaynak merkezi</p>
        </div>
        <p className="footer-copy">© {new Date().getFullYear()} Gebze Belediyesi</p>
      </div>
    </footer>
  );
}
