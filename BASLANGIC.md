# Başlangıç rehberi — Kodu nereye yazmalıyım?

React (ön yüz) ve Django (arka uç) ayrı klasörlerdedir. Aşağıdaki tablo günlük geliştirme için yeterlidir.

## Proje ağacı (sade)

```text
personel-portal2/
├── images/                 ← Tüm görseller (TEK yer)
├── run.ps1                 ← Projeyi başlat (backend + frontend)
├── backend/                ← Django (veri + API)
│   ├── .env                ← Veritabanı şifresi (gizli)
│   ├── manage.py
│   └── apps/portal/
│       ├── models/         ← MySQL tablolarının Python karşılığı
│       ├── api/            ← REST API (/api/duyurular/ vb.)
│       ├── admin.py        ← Admin panel kayıtları
│       └── views.py        ← http://127.0.0.1:8000/ HTML sayfası
└── frontend/               ← React (kullanıcı arayüzü)
    ├── public/images/      ← images/ klasörüne bağlı (dokunmayın)
    └── src/
        ├── App.js          ← Sayfa yolları (/, /test)
        ├── api.js          ← Backend’den veri çekme
        ├── pages/          ← Tam sayfalar
        ├── components/     ← Tekrar kullanılan parçalar
        ├── styles/         ← Genel CSS
        └── utils/          ← Yardımcı fonksiyonlar
```

## Ne yapmak istiyorsun? → Hangi dosya?

| İstek | Nereye yaz |
|--------|------------|
| Yeni sayfa (ör. `/haberler`) | `frontend/src/pages/HaberlerPage.js` + `App.js` içine route |
| Menüye link ekle | `frontend/src/components/Navbar.js` |
| Ana sayfa düzeni / bölümler | `frontend/src/pages/HomePage.js` |
| Kart, navbar, footer gibi parça | `frontend/src/components/` |
| API’den veri çekme | `frontend/src/api.js` |
| Görsel yolu düzeltme | `frontend/src/utils/resolveImage.js` |
| Renk, font, genel stil | `frontend/src/styles/` |
| Yeni API uç noktası | `backend/apps/portal/api/` |
| Veritabanı tablosu (okuma) | `backend/apps/portal/models/personel_db.py` |
| Admin’de tablo görünümü | `backend/apps/portal/admin.py` |
| Django kök sayfası (8000/) | `backend/apps/portal/views.py` |
| Veritabanı bağlantısı | `backend/.env` |

## Görseller (önemli)

1. Dosyayı **`images/`** klasörüne koyun (proje kökü).
2. `frontend/public/images/` bir **kopya değil**, kök `images/` klasörüne bağlıdır.
3. Sitede kullanım: `/images/dosya.webp`
4. `frontend/src/images` diye bir klasör **kullanmayın** (kaldırıldı).

## Çalıştırma

```powershell
.\run.ps1
```

- Arayüz: http://localhost:3000/
- Test: http://localhost:3000/test
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

## İlk kurulum

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate

cd ..\frontend
npm install
```

## React akışı (kısa)

1. `App.js` → hangi URL hangi sayfayı açar
2. `pages/HomePage.js` → sayfa açılınca `api.js` ile veri çeker
3. `components/ContentCard.js` → veriyi ekranda gösterir
4. Görseller `resolveImage()` ile `/images/...` olur

## Django akışı (kısa)

1. MySQL’deki `personel_db` tabloları → `models/personel_db.py`
2. `api/serializers.py` + `api/urls.py` → JSON API
3. React `api.js` içinde `fetch('http://127.0.0.1:8000/api/duyurular/')` çağırır

Modeller `managed=False` olduğu için Django tablo **oluşturmaz**; sadece mevcut veriyi okur/yazar.
