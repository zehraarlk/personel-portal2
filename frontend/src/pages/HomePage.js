import { useEffect, useState } from 'react';
import MainLayout from '../components/MainLayout';
import HomeHero from '../components/HomeHero';
import ContentCard from '../components/ContentCard';
import AnnouncementDetail from '../components/AnnouncementDetail';
import {
  fetchAnasayfaDuyurular,
  fetchAnasayfaLinkler,
  fetchDuyurular,
  fetchEtkinlikler,
  fetchHealth,
} from '../api';
import { resolveImage } from '../utils/resolveImage';
import './HomePage.css';

function shorten(text, max = 110) {
  const t = (text || '').trim();
  if (t.length <= max) return t;
  return `${t.slice(0, max)}…`;
}

export default function HomePage() {
  const [duyurular, setDuyurular] = useState([]);
  const [etkinlikler, setEtkinlikler] = useState([]);
  const [linkler, setLinkler] = useState([]);
  const [apiStatus, setApiStatus] = useState('bağlanıyor…');
  const [error, setError] = useState('');
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const [health, duyuruList, anasayfaList, etkinlikList, linkList] =
          await Promise.all([
            fetchHealth(),
            fetchDuyurular(),
            fetchAnasayfaDuyurular().catch(() => []),
            fetchEtkinlikler().catch(() => []),
            fetchAnasayfaLinkler().catch(() => []),
          ]);

        if (cancelled) return;

        const fromAnasayfa = anasayfaList.length ? anasayfaList : duyuruList;
        setDuyurular(fromAnasayfa.slice(0, 8));
        setEtkinlikler(etkinlikList.slice(0, 4));
        setLinkler(linkList.slice(0, 6));
        setApiStatus(
          health.database
            ? `Bağlı: ${health.database}`
            : health.message || 'API hazır'
        );
      } catch (err) {
        if (cancelled) return;
        setError(err.message || 'Veriler yüklenemedi');
        setApiStatus('API bağlantısı yok');
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <MainLayout title="Ana Sayfa">
      <HomeHero />

      <div className="home-status-row">
        <span className={`api-chip${error ? ' error' : ''}`}>{apiStatus}</span>
      </div>

      {error && (
        <div className="alert-error">
          {error}. Backend’in çalıştığından emin olun.
        </div>
      )}

      <section id="duyurular" className="home-section">
        <div className="home-section-head">
          <h2>Güncel Duyurular</h2>
          <p>personel_db üzerinden gelen kurum içi duyurular</p>
        </div>
        <div className="news-grid">
          {duyurular.map((item) => (
            <ContentCard
              key={`d-${item.id}`}
              title={item.baslik}
              summary={shorten(item.ozet || item.aciklama)}
              image={item.resim}
              meta={`${item.view ?? 0} görüntülenme`}
              badge="Duyuru"
              onClick={() => setSelected(item)}
            />
          ))}
        </div>
        {!error && duyurular.length === 0 && (
          <div className="empty-state">Henüz duyuru yok.</div>
        )}
      </section>

      <section className="home-section">
        <div className="home-section-head">
          <h2>Etkinlikler</h2>
          <p>Yaklaşan ve güncel personel etkinlikleri</p>
        </div>
        <div className="news-grid home-grid-4">
          {etkinlikler.map((item) => (
            <ContentCard
              key={`e-${item.id}`}
              title={item.baslik}
              summary={shorten(item.aciklama)}
              image={item.resim}
              meta={item.tarih || item.durum_kodu || ''}
              badge="Etkinlik"
            />
          ))}
        </div>
        {!error && etkinlikler.length === 0 && (
          <div className="empty-state">Etkinlik kaydı bulunamadı.</div>
        )}
      </section>

      {linkler.length > 0 && (
        <section className="home-section">
          <div className="home-section-head">
            <h2>Hızlı Erişim</h2>
            <p>Anasayfa yardımcı bağlantıları</p>
          </div>
          <div className="home-links">
            {linkler.map((link) => (
              <a
                key={link.id}
                className="home-link-card"
                href={link.hedef_url || '#'}
                target="_blank"
                rel="noreferrer"
              >
                <img
                  src={resolveImage(link.logo_url)}
                  alt=""
                  onError={(e) => {
                    e.currentTarget.src = '/images/gebze-logo.webp';
                  }}
                />
                <span>{link.baslik}</span>
              </a>
            ))}
          </div>
        </section>
      )}

      {selected && (
        <AnnouncementDetail item={selected} onClose={() => setSelected(null)} />
      )}
    </MainLayout>
  );
}
