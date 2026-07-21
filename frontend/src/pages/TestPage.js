import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import MainLayout from '../components/MainLayout';
import ContentCard from '../components/ContentCard';
import {
  fetchDuyurular,
  fetchEtkinlikler,
  fetchHealth,
  fetchPersoneller,
} from '../api';
import './TestPage.css';

const CHECKS = [
  { id: 'health', label: 'API Health', path: '/api/health/' },
  { id: 'duyurular', label: 'Duyurular', path: '/api/duyurular/' },
  { id: 'etkinlikler', label: 'Etkinlikler', path: '/api/etkinlikler/' },
  { id: 'personeller', label: 'Personeller', path: '/api/personeller/' },
  { id: 'images', label: 'Görseller (/images)', path: null },
];

function statusClass(status) {
  if (status === 'pass') return 'pass';
  if (status === 'fail') return 'fail';
  return 'pending';
}

export default function TestPage() {
  const [results, setResults] = useState({});
  const [running, setRunning] = useState(false);
  const [lastRun, setLastRun] = useState(null);
  const [healthPayload, setHealthPayload] = useState(null);
  const [previewDuyuru, setPreviewDuyuru] = useState([]);
  const [previewEtkinlik, setPreviewEtkinlik] = useState([]);
  const [counts, setCounts] = useState({});

  const runTests = useCallback(async () => {
    setRunning(true);
    const pending = Object.fromEntries(CHECKS.map((c) => [c.id, 'pending']));
    setResults(pending);
    const next = {};

    try {
      const health = await fetchHealth();
      setHealthPayload(health);
      next.health = health?.status === 'ok' ? 'pass' : 'fail';
      setCounts({
        duyuru: health.duyuru_count ?? health.tables?.duyurular,
        personel: health.personel_count ?? health.tables?.personeller,
        etkinlik: health.tables?.etkinlikler,
      });
    } catch {
      setHealthPayload(null);
      next.health = 'fail';
    }

    try {
      const list = await fetchDuyurular();
      setPreviewDuyuru(list.slice(0, 4));
      next.duyurular = 'pass';
    } catch {
      setPreviewDuyuru([]);
      next.duyurular = 'fail';
    }

    try {
      const list = await fetchEtkinlikler();
      setPreviewEtkinlik(list.slice(0, 4));
      next.etkinlikler = 'pass';
    } catch {
      setPreviewEtkinlik([]);
      next.etkinlikler = 'fail';
    }

    try {
      await fetchPersoneller();
      next.personeller = 'pass';
    } catch {
      next.personeller = 'fail';
    }

    try {
      const img = await fetch('/images/gebze-logo.webp', { method: 'HEAD' });
      next.images = img.ok ? 'pass' : 'fail';
    } catch {
      next.images = 'fail';
    }

    setResults(next);
    setLastRun(new Date());
    setRunning(false);
  }, []);

  useEffect(() => {
    runTests();
  }, [runTests]);

  const passCount = Object.values(results).filter((v) => v === 'pass').length;

  return (
    <MainLayout
      title="Sistem Testi"
      crumbs={[{ label: 'Ana Sayfa', to: '/' }, { label: 'Sistem Testi' }]}
    >
      <header className="page-header test-header">
        <div>
          <h1>Sistem Testi</h1>
          <p>API, veritabanı ve görsellerin doğrulama ekranı</p>
        </div>
        <button
          type="button"
          className="test-run-btn"
          onClick={runTests}
          disabled={running}
        >
          {running ? 'Çalışıyor…' : 'Testleri Yenile'}
        </button>
      </header>

      <section className="test-summary">
        <article className="test-stat">
          <span className="test-stat-label">Başarılı</span>
          <strong>
            {passCount}/{CHECKS.length}
          </strong>
        </article>
        <article className="test-stat">
          <span className="test-stat-label">Duyuru</span>
          <strong>{counts.duyuru ?? '—'}</strong>
        </article>
        <article className="test-stat">
          <span className="test-stat-label">Etkinlik</span>
          <strong>{counts.etkinlik ?? '—'}</strong>
        </article>
        <article className="test-stat">
          <span className="test-stat-label">Personel</span>
          <strong>{counts.personel ?? '—'}</strong>
        </article>
      </section>

      <section className="test-grid">
        <div className="test-panel">
          <div className="test-panel-header">
            <h2>Kontrol listesi</h2>
          </div>
          <ul className="test-checklist">
            {CHECKS.map((check) => (
              <li key={check.id}>
                <div>
                  <strong>{check.label}</strong>
                  {check.path && <code>{check.path}</code>}
                </div>
                <span className={`test-status ${statusClass(results[check.id])}`}>
                  {results[check.id] === 'pass' && 'Geçti'}
                  {results[check.id] === 'fail' && 'Başarısız'}
                  {(!results[check.id] || results[check.id] === 'pending') &&
                    'Bekliyor'}
                </span>
              </li>
            ))}
          </ul>
          <p className="test-meta-line">
            Son:{' '}
            {lastRun
              ? lastRun.toLocaleTimeString('tr-TR')
              : '—'}{' '}
            · DB: {healthPayload?.database || '—'}
          </p>
          <Link to="/" className="test-link-btn">
            Ana sayfaya dön
          </Link>
        </div>

        <div className="test-panel test-preview-panel">
          <div className="test-panel-header">
            <h2>Görsel önizleme</h2>
            <p>API verisi + /images klasörü</p>
          </div>
          <div className="test-thumb-row">
            {['/images/gebze-logo.webp', '/images/gebze.webp', '/images/gebze(2).webp'].map(
              (src) => (
                <img key={src} src={src} alt="" className="test-thumb" />
              )
            )}
          </div>
        </div>
      </section>

      <section className="home-section">
        <div className="home-section-head">
          <h2>Duyuru kartları (canlı veri)</h2>
        </div>
        <div className="news-grid">
          {previewDuyuru.map((item) => (
            <ContentCard
              key={item.id}
              title={item.baslik}
              summary={(item.aciklama || '').slice(0, 100)}
              image={item.resim}
              meta={`${item.view ?? 0} görüntülenme`}
              badge="Duyuru"
            />
          ))}
        </div>
      </section>

      <section className="home-section">
        <div className="home-section-head">
          <h2>Etkinlik kartları (canlı veri)</h2>
        </div>
        <div className="news-grid">
          {previewEtkinlik.map((item) => (
            <ContentCard
              key={item.id}
              title={item.baslik}
              summary={(item.aciklama || '').slice(0, 100)}
              image={item.resim}
              meta={item.tarih || ''}
              badge="Etkinlik"
            />
          ))}
        </div>
      </section>
    </MainLayout>
  );
}
