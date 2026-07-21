#!/usr/bin/env python
"""
Kurulum teşhisi — veritabanı ve Django ortamını kontrol eder.
Kullanım (backend klasöründen):
  venv\\Scripts\\python tools\\diagnose.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_ROOT / '.env'


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if not ENV_PATH.exists():
        return env
    for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def say(title: str, detail: str, ok: bool) -> None:
    mark = 'OK' if ok else 'HATA'
    print(f'[{mark}] {title}')
    if detail:
        print(f'      {detail}')
    print()


def explain_mysql_error(exc: Exception) -> str:
    text = str(exc)
    code = None
    if hasattr(exc, 'args') and exc.args:
        code = exc.args[0]

    if code == 2003 or '2003' in text or "Can't connect" in text:
        return (
            'MySQL/MariaDB çalışmıyor veya 3306 kapalı. '
            'XAMPP Control Panel → MySQL → Start.'
        )
    if code == 2002 or '2002' in text:
        return (
            'Bağlantı reddedildi. XAMPP MySQL açık mı? '
            'DB_HOST=127.0.0.1 ve DB_PORT=3306 kontrol edin.'
        )
    if code == 1045 or '1045' in text or 'Access denied' in text:
        return (
            'Kullanıcı adı veya şifre yanlış. '
            'backend/.env içinde DB_USER ve DB_PASSWORD düzeltin. '
            'XAMPP varsayılanı genelde root + boş şifre veya root + 1234.'
        )
    if code == 1049 or '1049' in text or 'Unknown database' in text:
        return (
            'personel_db veritabanı yok. phpMyAdmin → Yeni → personel_db oluşturun '
            've SQL dosyasını içe aktarın (KURULUM.md Adım 5).'
        )
    if 'No module named' in text and 'MySQLdb' in text:
        return 'PyMySQL eksik. backend klasöründe: pip install -r requirements.txt'
    return text


def main() -> int:
    print('')
    print('=== Gebze Personel Portali — Backend Teshisi ===')
    print('')

    errors = 0

    # Python sürümü
    v = sys.version_info
    py_ok = v.major == 3 and v.minor >= 10
    say(
        'Python surumu',
        f'{v.major}.{v.minor}.{v.micro}' + ('' if py_ok else ' — Python 3.10+ gerekli'),
        py_ok,
    )
    if not py_ok:
        errors += 1

    # .env
    env = load_env()
    env_ok = ENV_PATH.exists()
    say(
        'backend/.env dosyasi',
        str(ENV_PATH) if env_ok else 'Yok. Kopyalayin: copy .env.example .env',
        env_ok,
    )
    if not env_ok:
        errors += 1

    db_name = env.get('DB_NAME', 'personel_db')
    db_user = env.get('DB_USER', 'root')
    db_password = env.get('DB_PASSWORD', '')
    db_host = env.get('DB_HOST', '127.0.0.1')
    db_port = int(env.get('DB_PORT', '3306'))

    # PyMySQL
    try:
        import pymysql  # noqa: F401
        say('PyMySQL paketi', 'Yuklu', True)
    except ImportError:
        say('PyMySQL paketi', 'Eksik. pip install -r requirements.txt', False)
        errors += 1
        print('Ozet: once kurulum yapin: ..\\setup.ps1')
        return 1

    # MySQL baglantisi
    try:
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            charset='utf8mb4',
            connect_timeout=5,
        )
        say(
            'MySQL sunucusu',
            f'{db_host}:{db_port} uzerinden baglanti basarili',
            True,
        )
    except Exception as exc:  # noqa: BLE001
        say('MySQL sunucusu', explain_mysql_error(exc), False)
        errors += 1
        print('Ozet: MySQL/XAMPP adimlarini KURULUM.md dosyasindan uygulayin.')
        return 1

    # Veritabani var mi
    try:
        with conn.cursor() as cur:
            cur.execute('SHOW DATABASES LIKE %s', (db_name,))
            row = cur.fetchone()
        if row:
            say('Veritabani', f'"{db_name}" mevcut', True)
        else:
            say(
                'Veritabani',
                f'"{db_name}" bulunamadi. phpMyAdmin ile olusturun.',
                False,
            )
            errors += 1
    except Exception as exc:  # noqa: BLE001
        say('Veritabani', explain_mysql_error(exc), False)
        errors += 1

    # Tablolar
    if errors == 0:
        try:
            with conn.cursor() as cur:
                cur.execute(f'USE `{db_name}`')
                cur.execute('SHOW TABLES')
                tables = [r[0] for r in cur.fetchall()]
            count = len(tables)
            ok = count > 0
            detail = f'{count} tablo bulundu' if ok else 'Tablo yok — SQL dosyasini ice aktarin'
            say('Tablolar', detail, ok)
            if not ok:
                errors += 1
            elif 'duyurular' not in tables:
                say('duyurular tablosu', 'Eksik — SQL dump tam import edilmemis olabilir', False)
                errors += 1
            else:
                say('duyurular tablosu', 'Mevcut', True)
        except Exception as exc:  # noqa: BLE001
            say('Tablolar', explain_mysql_error(exc), False)
            errors += 1

    conn.close()

    # Django migrate (opsiyonel kontrol)
    sys.path.insert(0, str(BACKEND_ROOT))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        import django
        django.setup()
        from django.db import connection
        with connection.cursor() as cur:
            cur.execute('SELECT 1')
        say('Django veritabani baglantisi', 'Basarili', True)
    except Exception as exc:  # noqa: BLE001
        say('Django veritabani baglantisi', str(exc), False)
        errors += 1

    print('---')
    if errors == 0:
        print('Tum kontroller gecti. Calistirmak icin: ..\\run.ps1')
        return 0
    print(f'{errors} sorun bulundu. KURULUM.md ve kontrol.ps1 dosyalarina bakin.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
