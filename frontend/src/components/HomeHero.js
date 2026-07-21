import { resolveImage } from '../utils/resolveImage';
import './HomeHero.css';

export default function HomeHero() {
  return (
    <section className="home-hero">
      <img
        className="home-hero-bg"
        src="/images/gebze.webp"
        alt=""
        onError={(e) => {
          e.currentTarget.src = '/images/gebze(2).webp';
        }}
      />
      <div className="home-hero-overlay" />
      <div className="home-hero-content">
        <img
          className="home-hero-logo"
          src={resolveImage('images/gebze-logo.webp')}
          alt="Gebze Belediyesi"
        />
        <h1>Gebze Belediyesi</h1>
        <p>Personel Portalı — duyurular, etkinlikler ve kurum içi bilgilendirme</p>
        <a className="home-hero-cta" href="#duyurular">
          Duyuruları incele
        </a>
      </div>
    </section>
  );
}
