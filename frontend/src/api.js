const API_BASE = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

async function fetchList(endpoint) {
  const res = await fetch(`${API_BASE}/${endpoint}/`);
  if (!res.ok) throw new Error(`${endpoint} yüklenemedi`);
  const data = await res.json();
  return Array.isArray(data) ? data : data.results || [];
}

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health/`);
  if (!res.ok) throw new Error('API yanıt vermedi');
  return res.json();
}

export async function fetchDuyurular() {
  return fetchList('duyurular');
}

export async function fetchAnasayfaDuyurular() {
  return fetchList('anasayfa_duyurular');
}

export async function fetchEtkinlikler() {
  return fetchList('etkinlikler');
}

export async function fetchHaberler() {
  return fetchList('haberler');
}

export async function fetchAnasayfaLinkler() {
  return fetchList('anasayfa_linkler');
}

export async function fetchPersoneller() {
  return fetchList('personeller');
}

export { API_BASE };
