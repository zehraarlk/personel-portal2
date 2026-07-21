import { resolveImage } from '../utils/resolveImage';
import './ContentCard.css';

export default function ContentCard({
  title,
  summary,
  image,
  meta,
  badge = 'İçerik',
  onClick,
}) {
  const src = resolveImage(image);

  return (
    <article
      className="news-card content-card"
      onClick={onClick}
      onKeyDown={(e) => e.key === 'Enter' && onClick?.()}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      <div className="news-card-media" aria-hidden="true">
        <img
          src={src}
          alt=""
          className="news-card-image"
          onError={(e) => {
            e.currentTarget.src = '/images/gebze-logo.webp';
          }}
        />
      </div>
      <div className="news-card-body">
        <span className="badge aktif">{badge}</span>
        <h2>{title}</h2>
        {summary ? <p>{summary}</p> : null}
        {meta ? <span className="news-card-views">{meta}</span> : null}
      </div>
    </article>
  );
}
