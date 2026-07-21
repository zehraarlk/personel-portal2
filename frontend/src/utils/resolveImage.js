/**
 * DB yolları: ../images/foo.webp → /images/foo.webp (public/images)
 */
export function resolveImage(path, fallback = '/images/gebze-logo.webp') {
  if (!path || typeof path !== 'string') return fallback;

  let cleaned = path.trim().replace(/\\/g, '/');
  cleaned = cleaned.replace(/^\.\.\//, '');
  if (!cleaned.startsWith('images/') && !cleaned.startsWith('/images/')) {
    cleaned = cleaned.startsWith('/') ? cleaned.slice(1) : cleaned;
    if (!cleaned.startsWith('images/')) {
      cleaned = `images/${cleaned}`;
    }
  }
  if (cleaned.startsWith('/')) {
    return cleaned;
  }
  return `/${cleaned}`;
}
