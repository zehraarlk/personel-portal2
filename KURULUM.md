# Kurulum Rehberi — Sıfırdan Başlayanlar İçin

Bu rehber, projeyi **hiç kurmamış**, bilgisayarında **MySQL olmayan** ve sürekli hata alan biri için yazıldı.

**Kısayollar:**

| Ne yapmak istiyorsun? | Komut / dosya |
|------------------------|---------------|
| Otomatik kurulum dene | `setup.bat` veya `.\setup.ps1` |
| Hata nedenini öğren | `kontrol.bat` veya `.\kontrol.ps1` |
| Projeyi çalıştır | `.\run.ps1` |
| Kod nereye yazılır? | [BASLANGIC.md](./BASLANGIC.md) |

---

## Bu proje ne istiyor?

Bilgisayarınızda şunlar olmalı:

| Program | Ne işe yarar? | İndirme |
|---------|---------------|---------|
| **XAMPP** | MySQL veritabanı + phpMyAdmin | https://www.apachefriends.org/ |
| **Python 3.10+** | Backend (Django) | https://www.python.org/downloads/ |
| **Node.js 18+ (LTS)** | Frontend (React) | https://nodejs.org/ |

Git zorunlu değil; projeyi ZIP olarak da indirebilirsiniz.

---

## Adım 0 — Projeyi bilgisayara alın

Git ile:

```powershell
git clone https://github.com/zehraarlk/personel-portal2.git
cd personel-portal2
```

ZIP indirdiyseniz klasörü açın, örneğin:

`C:\Users\KULLANICI\Downloads\personel-portal2-main\personel-portal2-main`

PowerShell’de proje klasörüne gidin:

```powershell
cd C:\Users\KULLANICI\Downloads\personel-portal2-main\personel-portal2-main
```

---

## Adım 1 — Python kurulumu

1. https://www.python.org/downloads/ adresinden **Python 3.12** (veya 3.10+) indirin.
2. Kurulumda **mutlaka** şunu işaretleyin:  
   ☑ **Add python.exe to PATH**
3. Kurulum bitince **yeni bir PowerShell** açın.
4. Test:

```powershell
python --version
```

`Python 3.10` veya üstü görmelisiniz.

**Hata:** `'python' is not recognized`  
→ Python PATH’e eklenmemiş. Kurulumu tekrarlayın veya “Repair” ile PATH ekleyin.

---

## Adım 2 — Node.js kurulumu

1. https://nodejs.org/ → **LTS** sürümünü indirin.
2. Kurulumu varsayılan ayarlarla tamamlayın.
3. Yeni PowerShell açın:

```powershell
node --version
npm --version
```

**Hata:** `node` tanınmıyor  
→ Bilgisayarı yeniden başlatın veya Node’u yeniden kurun.

---

## Adım 3 — XAMPP (MySQL) kurulumu

Bu proje **MySQL veritabanı** olmadan çalışmaz. En kolay yol XAMPP’tır.

1. https://www.apachefriends.org/ → Windows için XAMPP indirin.
2. Kurun (varsayılan: `C:\xampp`).
3. **XAMPP Control Panel** açın.
4. **MySQL** satırında **Start** düğmesine basın.  
   Yeşil olunca MySQL çalışıyor demektir.

Test:

```powershell
.\kontrol.ps1
```

`[OK] MySQL/MariaDB (port 3306)` görmelisiniz.

**Hata:** MySQL Start olmuyor, port meşgul  
→ Başka bir program 3306 kullanıyor olabilir. XAMPP’te **Config → my.ini** veya çakışan MySQL servisini kapatın.

---

## Adım 4 — Veritabanı şifresini öğrenin

XAMPP’te varsayılan kullanıcı: **`root`**

Şifre genelde:
- **boş** (hiç şifre yok), veya
- **`1234`** (bazı kurulumlarda)

phpMyAdmin’e girin: http://localhost/phpmyadmin

Giriş yapamazsanız XAMPP dokümantasyonuna bakın veya ekibinizden şifreyi isteyin.

---

## Adım 5 — `personel_db` veritabanını oluşturun

1. Tarayıcıda: http://localhost/phpmyadmin
2. Sol menüden **Yeni** (New).
3. Veritabanı adı: **`personel_db`**
4. Karakter seti: **utf8mb4_general_ci** (veya utf8mb4_unicode_ci)
5. **Oluştur** deyin.

### Tabloları içe aktarma (SQL)

Projede tablolar ve örnek veriler bir **SQL dosyası** ile gelir. Ekibinizden `personel_db.sql` dosyasını isteyin veya phpMyAdmin’den dışa aktarılmış dosyayı kullanın.

1. phpMyAdmin → **personel_db** seçin
2. Üst menü → **İçe aktar** (Import)
3. SQL dosyasını seçin → **Git**

İçe aktarma bitince sol tarafta `duyurular`, `personeller` gibi tablolar görünmeli.

**Hata:** Tablo yok, site boş  
→ SQL import edilmemiş. Bu adımı tekrarlayın.

---

## Adım 6 — `backend/.env` dosyasını ayarlayın

Proje kökünde otomatik kurulum bunu sizin için yapabilir. Manuel yapmak için:

```powershell
copy backend\.env.example backend\.env
```

`backend\.env` dosyasını Not Defteri ile açın ve **şifreyi** kendi XAMPP ayarınıza göre düzeltin:

```env
SECRET_KEY=gelistirme-icin-uzun-rastgele-bir-metin
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=personel_db
DB_USER=root
DB_PASSWORD=1234
DB_HOST=127.0.0.1
DB_PORT=3306
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

- Şifreniz boşsa: `DB_PASSWORD=` (eşittir işaretinden sonra boş bırakın)
- Şifreniz `1234` ise: `DB_PASSWORD=1234`

---

## Adım 7 — Otomatik kurulum (önerilen)

Proje klasöründe PowerShell:

```powershell
.\setup.ps1
```

veya çift tık: **`setup.bat`**

Bu script sırayla:
- Python venv oluşturur
- `pip install` yapar
- `npm install` yapar
- `migrate` çalıştırır
- Veritabanı bağlantısını test eder

**Hata alırsanız** script size ne yapmanız gerektiğini yazar. Sonra:

```powershell
.\kontrol.ps1
```

---

## Adım 8 — Manuel kurulum (otomatik çalışmazsa)

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# .env icinde DB_PASSWORD duzeltin
python manage.py migrate
cd ..
```

### Frontend

```powershell
cd frontend
copy .env.example .env
npm install
cd ..
```

### Veritabanı testi

```powershell
cd backend
.\venv\Scripts\python tools\diagnose.py
cd ..
```

Tüm satırlar `[OK]` ise hazırsınız.

---

## Adım 9 — Projeyi çalıştırın

```powershell
.\run.ps1
```

İki siyah pencere açılır (backend + frontend). Kapatmak için pencereleri kapatın.

| Adres | Ne? |
|-------|-----|
| http://localhost:3000/ | Ana sayfa (React) |
| http://localhost:3000/test | Sistem testi |
| http://127.0.0.1:8000/api/ | API |
| http://127.0.0.1:8000/admin/ | Django admin |

---

## Sık görülen hatalar ve çözümleri

### `Backend venv bulunamadi`

Kurulum yapılmamış. Çalıştırın: `.\setup.ps1`

### `Frontend bagimliliklari yok`

```powershell
cd frontend
npm install
```

### `Can't connect to MySQL server` / `2003`

- XAMPP Control Panel → **MySQL Start**
- `.\kontrol.ps1` ile port 3306 kontrolü

### `Access denied for user 'root'` / `1045`

`backend\.env` içinde `DB_PASSWORD` yanlış. phpMyAdmin’e hangi şifreyle giriyorsanız onu yazın.

### `Unknown database 'personel_db'` / `1049`

phpMyAdmin’de `personel_db` oluşturulmamış. [Adım 5](#adım-5--personel_db-veritabanını-oluşturun)

### Ana sayfa açılıyor ama duyuru yok / API hata veriyor

- http://127.0.0.1:8000/api/health/ açın
- `status: error` ise mesajı okuyun
- `.\kontrol.ps1` ve `backend\venv\Scripts\python tools\diagnose.py` çalıştırın

### Port 3000 veya 8000 meşgul

`run.ps1` portları temizlemeye çalışır. Olmazsa:

```powershell
# Hangi program kullaniyor (ornek 8000)
netstat -ano | findstr :8000
# Gorev Yoneticisi'nden ilgili process'i kapat
```

### `npm run dev` / `allowedHosts` hatası

`frontend\.env` dosyasında şunlar olmalı:

```env
HOST=localhost
BROWSER=none
```

### PowerShell script çalışmıyor

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Sonra tekrar `.\setup.ps1`

### Görseller görünmüyor

- `images\gebze-logo.webp` dosyası var mı kontrol edin
- Tarayıcıda: http://localhost:3000/images/gebze-logo.webp

---

## Teşhis araçları özeti

| Araç | Ne yapar? |
|------|-----------|
| `kontrol.ps1` | Python, Node, MySQL, venv, npm, port, API — hepsini kontrol eder |
| `setup.ps1` | İlk kurulumu otomatik yapar |
| `backend/tools/diagnose.py` | Sadece veritabanı bağlantısını detaylı test eder |
| http://localhost:3000/test | Tarayıcıdan API + görsel testi |
| http://127.0.0.1:8000/api/health/ | API ve DB durumu (JSON) |

**Önerilen sıra:** Hata aldınız → `kontrol.ps1` → çıktıdaki “Çözüm” satırlarını uygulayın → tekrar `run.ps1`

---

## Kurulum kontrol listesi

- [ ] Python 3.10+ (`python --version`)
- [ ] Node.js 18+ (`node --version`)
- [ ] XAMPP MySQL çalışıyor (yeşil)
- [ ] phpMyAdmin’de `personel_db` var
- [ ] SQL dosyası import edildi (tablolar görünüyor)
- [ ] `backend\.env` — `DB_PASSWORD` doğru
- [ ] `.\setup.ps1` hatasız bitti
- [ ] `.\kontrol.ps1` — tüm OK
- [ ] `.\run.ps1` — site açılıyor

Hepsi tamamsa kurulum bitti.

---

## Yardım istemeden önce

Şunları kopyalayıp gönderin:

1. `.\kontrol.ps1` çıktısının tamamı
2. Backend siyah penceresindeki kırmızı hata satırları
3. `backend\.env` dosyası (**şifreyi silerek** veya `****` yaparak)
