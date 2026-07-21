# Gebze Personel Portalı — backend + frontend birlikte
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host ""
Write-Host " Gebze Personel Portali baslatiliyor..." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path (Join-Path $Root "backend\venv\Scripts\python.exe"))) {
    Write-Host "[!] Backend venv bulunamadi." -ForegroundColor Red
    Write-Host "    Kurulum icin: .\setup.ps1" -ForegroundColor Yellow
    Write-Host "    Teshis icin:  .\kontrol.ps1" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path (Join-Path $Root "frontend\node_modules"))) {
    Write-Host "[!] Frontend bagimliliklari yok." -ForegroundColor Red
    Write-Host "    Kurulum icin: .\setup.ps1" -ForegroundColor Yellow
    Write-Host "    veya: cd frontend; npm install" -ForegroundColor Yellow
    exit 1
}

Write-Host " Port 3000 ve 8000 temizleniyor..." -ForegroundColor DarkGray
foreach ($port in 3000, 8000) {
    Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
        ForEach-Object {
            Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
        }
}
Start-Sleep -Seconds 1

Start-Process cmd -ArgumentList '/k', 'call venv\Scripts\activate.bat && python manage.py runserver' -WorkingDirectory (Join-Path $Root 'backend')
Start-Process cmd -ArgumentList '/k', 'set HOST=localhost&& set BROWSER=none&& set PORT=3000&& npm run dev' -WorkingDirectory (Join-Path $Root 'frontend')

Write-Host " Backend  : http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host " Frontend : http://localhost:3000/" -ForegroundColor Green
Write-Host " Test     : http://localhost:3000/test" -ForegroundColor Green
Write-Host ""
Write-Host " Iki pencere acildi. Kapatmak icin o pencereleri kapatin." -ForegroundColor Yellow
Write-Host ""
