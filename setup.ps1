# Gebze Personel Portali — otomatik kurulum
# Kullanim: .\setup.ps1
# Hata alirsaniz: .\kontrol.ps1

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Fail {
    param([string]$Message, [string]$Fix = '')
    Write-Host ''
    Write-Host "[KURULUM HATASI] $Message" -ForegroundColor Red
    if ($Fix) { Write-Host "Cozum: $Fix" -ForegroundColor Cyan }
    Write-Host ''
    Write-Host 'Detayli teshis icin: .\kontrol.ps1' -ForegroundColor Yellow
    Write-Host 'Adim adim rehber: KURULUM.md' -ForegroundColor Yellow
    exit 1
}

function Step {
    param([string]$Text)
    Write-Host ''
    Write-Host ">> $Text" -ForegroundColor Cyan
}

Write-Host ''
Write-Host '=== Gebze Personel Portali — Kurulum ===' -ForegroundColor Cyan
Write-Host ''

Step 'Git hook kuruluyor...'
& (Join-Path $Root 'scripts\install-git-hooks.ps1')

# Python
Step 'Python kontrol ediliyor...'
try {
    $pyVer = python --version 2>&1
    Write-Host "   $pyVer"
    $v = [version](($pyVer -replace 'Python\s+', '').Trim())
    if ($v.Major -lt 3 -or $v.Minor -lt 10) {
        Fail 'Python 3.10 veya ustu gerekli.' 'https://www.python.org/downloads/'
    }
} catch {
    Fail 'Python bulunamadi.' 'Python kurun ve "Add to PATH" secin, terminali yeniden acin.'
}

# Node
Step 'Node.js kontrol ediliyor...'
try {
    $nodeVer = node --version 2>&1
    Write-Host "   $nodeVer"
} catch {
    Fail 'Node.js bulunamadi.' 'https://nodejs.org/ LTS kurun.'
}

# MySQL uyarisi
Step 'MySQL/XAMPP kontrol ediliyor...'
$mysqlUp = $false
try {
    $conn = Get-NetTCPConnection -LocalPort 3306 -State Listen -ErrorAction SilentlyContinue
    $mysqlUp = $null -ne $conn
} catch { $mysqlUp = $false }

if (-not $mysqlUp) {
    Write-Host '   [!] MySQL port 3306 kapali.' -ForegroundColor Yellow
    Write-Host '   XAMPP kurup MySQL Start yapmaniz gerekecek (KURULUM.md Adim 3-5).' -ForegroundColor Yellow
    Write-Host '   Kuruluma devam ediliyor; veritabani adimini sonra tamamlayin.' -ForegroundColor Yellow
} else {
    Write-Host '   MySQL dinleniyor (port 3306).' -ForegroundColor Green
}

# backend .env
Step 'backend/.env hazirlaniyor...'
$envPath = Join-Path $Root 'backend\.env'
$envExample = Join-Path $Root 'backend\.env.example'
if (-not (Test-Path $envPath)) {
    if (-not (Test-Path $envExample)) { Fail 'backend/.env.example bulunamadi.' }
    Copy-Item $envExample $envPath
    Write-Host '   .env.example kopyalandi.'
    Write-Host '   ONEMLI: DB_PASSWORD degerini XAMPP sifrenize gore duzenleyin!' -ForegroundColor Yellow
} else {
    Write-Host '   .env zaten var, dokunulmadi.'
}

# frontend .env
Step 'frontend/.env hazirlaniyor...'
$feEnv = Join-Path $Root 'frontend\.env'
$feEx = Join-Path $Root 'frontend\.env.example'
if (-not (Test-Path $feEnv) -and (Test-Path $feEx)) {
    Copy-Item $feEx $feEnv
    Write-Host '   frontend/.env olusturuldu.'
}

# venv
Step 'Python sanal ortam (venv) olusturuluyor...'
$venvPy = Join-Path $Root 'backend\venv\Scripts\python.exe'
if (-not (Test-Path $venvPy)) {
    Push-Location (Join-Path $Root 'backend')
    python -m venv venv
    if ($LASTEXITCODE -ne 0) { Pop-Location; Fail 'venv olusturulamadi.' }
    Pop-Location
    Write-Host '   venv olusturuldu.'
} else {
    Write-Host '   venv zaten var.'
}

# pip install
Step 'Python paketleri yukleniyor (pip)...'
Push-Location (Join-Path $Root 'backend')
& .\venv\Scripts\python.exe -m pip install --upgrade pip 2>&1 | Out-Null
& .\venv\Scripts\pip.exe install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Pop-Location
    Fail 'pip install basarisiz.' 'Internet baglantisi ve pip surumunu kontrol edin.'
}
Pop-Location
Write-Host '   Paketler yuklendi.'

# migrate
Step 'Django migrate calistiriliyor...'
Push-Location (Join-Path $Root 'backend')
& .\venv\Scripts\python.exe manage.py migrate --noinput
if ($LASTEXITCODE -ne 0) {
    Pop-Location
    Fail 'migrate basarisiz.' 'MySQL acik mi? personel_db var mi? kontrol.ps1 calistirin.'
}
Pop-Location
Write-Host '   migrate tamam.'

# npm install
Step 'Frontend paketleri yukleniyor (npm install)...'
Push-Location (Join-Path $Root 'frontend')
npm install
if ($LASTEXITCODE -ne 0) {
    Pop-Location
    Fail 'npm install basarisiz.' 'Node.js LTS kurulu mu? Internet var mi?'
}
Pop-Location
Write-Host '   npm install tamam.'

# DB teshis
Step 'Veritabani baglantisi test ediliyor...'
Push-Location (Join-Path $Root 'backend')
& .\venv\Scripts\python.exe tools\diagnose.py
$dbOk = ($LASTEXITCODE -eq 0)
Pop-Location

Write-Host ''
Write-Host '=== Kurulum tamamlandi ===' -ForegroundColor Green
if (-not $dbOk) {
    Write-Host ''
    Write-Host '[!] Veritabani henuz hazir degil.' -ForegroundColor Yellow
    Write-Host '    1. XAMPP → MySQL Start' -ForegroundColor Yellow
    Write-Host '    2. http://localhost/phpmyadmin → personel_db olustur' -ForegroundColor Yellow
    Write-Host '    3. SQL dosyasini ice aktar (KURULUM.md Adim 5)' -ForegroundColor Yellow
    Write-Host '    4. backend/.env icinde DB_PASSWORD duzelt' -ForegroundColor Yellow
    Write-Host '    5. Tekrar: .\kontrol.ps1' -ForegroundColor Yellow
} else {
    Write-Host 'Her sey hazir. Calistirmak icin: .\run.ps1' -ForegroundColor Green
}
Write-Host ''
