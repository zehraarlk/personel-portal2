import { resolveImage } from '../utils/resolveImage';

export default function AnnouncementDetail({ item, onClose }) {
  const body = item.icerik || item.aciklama || '';
  const imageSrc = resolveImage(item.resim);

  return (
    <div className="detail-backdrop" onClick={onClose}>
      <div
        className="detail-panel"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="detail-title"
      >
        <button
          type="button"
          className="detail-close"
          onClick={onClose}
          aria-label="Kapat"
        >
          ×
        </button>
        <p className="detail-meta">{item.view ?? 0} görüntülenme</p>
        <h2 id="detail-title">{item.baslik}</h2>
        <img
          src={imageSrc}
          alt=""
          className="detail-image"
          onError={(e) => {
            e.currentTarget.src = '/images/gebze-logo.webp';
          }}
        />
        <p className="detail-body">{body}</p>
      </div>
    </div>
  );
}
