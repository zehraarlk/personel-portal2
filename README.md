# Gebze Personel Portalı

Django API + React arayüzü. Veritabanı: phpMyAdmin’deki mevcut **personel_db**.

**Yeni başlayanlar için:** [BASLANGIC.md](./BASLANGIC.md) — hangi kodu nereye yazacağınız burada.

## Klasör yapısı

```text
├── images/                 # Tüm görseller (tek kaynak)
├── run.ps1                 # Backend + frontend birlikte başlat
├── BASLANGIC.md            # Kod nereye yazılır rehberi
├── backend/
│   ├── config/             # Django ayarları ve URL’ler
│   └── apps/portal/        # Modeller, API, admin
└── frontend/
    ├── public/images/      # → images/ klasörüne bağlı
    └── src/
        ├── App.js          # Sayfa yolları
        ├── api.js          # API çağrıları
        ├── pages/          # HomePage, TestPage
        ├── components/     # Navbar, kartlar, layout
        ├── styles/         # global.css, layout.css
        └── utils/          # resolveImage.js
```

## Çalıştırma

```powershell
.\run.ps1
```

- Arayüz: http://localhost:3000/
- Test: http://localhost:3000/test
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

## Veritabanı

Django, mevcut **personel_db** MySQL veritabanına bağlanır. SQL dump: `backend/db/personel_db.sql`

31 tablo `managed=False` ile tanımlıdır; Django yeni tablo oluşturmaz.

API örnekleri: `/api/duyurular/`, `/api/personeller/`, `/api/etkinlikler/`

`backend/.env` örneği:

```env
SECRET_KEY=gebze-portal-dev-2026-xK9mP2qR7vL4nW8
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=personel_db
DB_USER=root
DB_PASSWORD=1234
DB_HOST=127.0.0.1
DB_PORT=3306
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

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
