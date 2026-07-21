from django.http import HttpResponse


def home(request):
    return HttpResponse(
        '''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <title>Personel Portalı API</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 40rem; margin: 3rem auto; padding: 0 1rem; color: #022842; }
    a { color: #1e4a6b; }
    code { background: #f1f3f5; padding: 0.1rem 0.35rem; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>Gebze Personel Portalı — API</h1>
  <p>Bu adres sadece backend. Arayüz için:</p>
  <p><a href="http://localhost:3000/"><strong>http://localhost:3000/</strong></a></p>
  <ul>
    <li><a href="/api/health/">/api/health/</a></li>
    <li><a href="/api/duyurular/">/api/duyurular/</a></li>
    <li><a href="/admin/">/admin/</a></li>
  </ul>
</body>
</html>''',
        content_type='text/html; charset=utf-8',
    )
