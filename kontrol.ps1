# Gebze Personel Portali — kurulum on kontrolu ve hata teshisi
# Kullanim: .\kontrol.ps1

$ErrorActionPreference = 'Continue'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$issues = 0

function Write-Check {
    param(
        [string]$Name,
        [bool]$Ok,
        [string]$Detail = '',
        [string]$Fix = ''
    )
    if ($Ok) {
        Write-Host "[OK]   $Name" -ForegroundColor Green
        if ($Detail) { Write-Host "       $Detail" -ForegroundColor DarkGray }
    } else {
        $script:issues++
        Write-Host "[HATA] $Name" -ForegroundColor Red
        if ($Detail) { Write-Host "       $Detail" -ForegroundColor Yellow }
        if ($Fix) { Write-Host "       Cozum: $Fix" -ForegroundColor Cyan }
    }
}

function Test-PortOpen {
    param([int]$Port)
    try {
        $c = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction Stop
        return $null -ne $c
    } catch {
        return $false
    }
}

function Get-CommandVersion {
    param([string]$Command, [string[]]$VersionArgs = @('--version'))
    try {
        $out = & $Command @VersionArgs 2>&1 | Select-Object -First 1
        return @{ Ok = $true; Text = "$out".Trim() }
    } catch {
        return @{ Ok = $false; Text = 'Yuklu degil' }
    }
}

Write-Host ''
Write-Host '=== Gebze Personel Portali — Kurulum Kontrolu ===' -ForegroundColor Cyan
Write-Host ''

# 1. Proje klasoru
Write-Check -Name 'Proje klasoru' -Ok (Test-Path $Root) -Detail $Root

# 2. Python
$py = Get-CommandVersion -Command 'python'
if ($py.Ok) {
    $ver = [version]($py.Text -replace '[^\d\.]', '' -split '\s+' | Select-Object -First 1)
    $pyOk = $ver.Major -ge 3 -and $ver.Minor -ge 10
    Write-Check -Name 'Python 3.10+' -Ok $pyOk -Detail $py.Text `
        -Fix 'https://www.python.org/downloads/ — kurulumda "Add python.exe to PATH" isaretleyin'
} else {
    Write-Check -Name 'Python 3.10+' -Ok $false -Detail 'python komutu bulunamadi' `
        -Fix 'Python indirin ve PATH ekleyin, sonra terminali yeniden acin'
}

# 3. Node.js
$node = Get-CommandVersion -Command 'node'
if ($node.Ok) {
    $nver = [version]($node.Text -replace '^v', '')
    $nodeOk = $nver.Major -ge 18
    Write-Check -Name 'Node.js 18+' -Ok $nodeOk -Detail $node.Text `
        -Fix 'https://nodejs.org/ LTS surumunu kurun'
} else {
    Write-Check -Name 'Node.js 18+' -Ok $false -Fix 'Node.js LTS kurun'
}

# 4. npm
$npm = Get-CommandVersion -Command 'npm'
Write-Check -Name 'npm' -Ok $npm.Ok -Detail $npm.Text -Fix 'Node.js ile birlikte gelir'

# 5. Git (opsiyonel)
$git = Get-CommandVersion -Command 'git'
Write-Check -Name 'Git (opsiyonel)' -Ok $git.Ok -Detail $(if ($git.Ok) { $git.Text } else { 'Yok ama proje calismasi icin sart degil' })

# 6. MySQL portu
$mysqlPort = Test-PortOpen -Port 3306
Write-Check -Name 'MySQL/MariaDB (port 3306)' -Ok $mysqlPort `
    -Detail $(if ($mysqlPort) { 'Dinleniyor' } else { 'Kapali veya kurulu degil' }) `
    -Fix 'XAMPP kurun → Control Panel → MySQL Start. KURULUM.md Adim 3'

# 7. XAMPP yolu (bilgi — hata sayilmaz)
$xampp = 'C:\xampp\mysql\bin\mysql.exe'
if (Test-Path $xampp) {
    Write-Host "[OK]   XAMPP MySQL dosyasi" -ForegroundColor Green
    Write-Host "       $xampp" -ForegroundColor DarkGray
} elseif ($mysqlPort) {
    Write-Host "[BILGI] XAMPP varsayilan yolda yok; MySQL baska kurulumdan calisiyor olabilir" -ForegroundColor DarkYellow
} else {
    Write-Check -Name 'XAMPP / MySQL kurulumu' -Ok $false `
        -Fix 'XAMPP: https://www.apachefriends.org/ — MySQL Start'
}

# 8. backend/.env
$envFile = Join-Path $Root 'backend\.env'
$envExample = Join-Path $Root 'backend\.env.example'
$hasEnv = Test-Path $envFile
Write-Check -Name 'backend/.env' -Ok $hasEnv `
    -Detail $(if ($hasEnv) { $envFile } else { 'Dosya yok' }) `
    -Fix 'setup.ps1 calistirin veya: copy backend\.env.example backend\.env'

# 9. Python venv
$venvPy = Join-Path $Root 'backend\venv\Scripts\python.exe'
Write-Check -Name 'Python sanal ortam (venv)' -Ok (Test-Path $venvPy) `
    -Fix 'setup.ps1 calistirin veya KURULUM.md Adim 7'

# 10. pip paketleri
if (Test-Path $venvPy) {
    $djangoCheck = & $venvPy -c "import django; print(django.get_version())" 2>&1
    $djangoOk = $LASTEXITCODE -eq 0
    Write-Check -Name 'Django paketi' -Ok $djangoOk -Detail $(if ($djangoOk) { "Django $djangoCheck" } else { "$djangoCheck" }) `
        -Fix 'cd backend; .\venv\Scripts\activate; pip install -r requirements.txt'
} else {
    Write-Check -Name 'Django paketi' -Ok $false -Fix 'Once venv olusturun (setup.ps1)'
}

# 11. frontend node_modules
$nodeModules = Join-Path $Root 'frontend\node_modules'
Write-Check -Name 'Frontend bagimliliklari' -Ok (Test-Path $nodeModules) `
    -Fix 'cd frontend; npm install'

# 12. frontend/.env
$feEnv = Join-Path $Root 'frontend\.env'
$feEnvEx = Join-Path $Root 'frontend\.env.example'
if (-not (Test-Path $feEnv) -and (Test-Path $feEnvEx)) {
    Write-Check -Name 'frontend/.env' -Ok $false -Fix 'copy frontend\.env.example frontend\.env'
} else {
    Write-Check -Name 'frontend/.env' -Ok (Test-Path $feEnv) -Detail $(if (Test-Path $feEnv) { 'Mevcut' } else { 'Eksik' })
}

# 13. Gorseller
$imagesRoot = Join-Path $Root 'images\gebze-logo.webp'
$imagesPublic = Join-Path $Root 'frontend\public\images\gebze-logo.webp'
$imgOk = (Test-Path $imagesRoot) -or (Test-Path $imagesPublic)
Write-Check -Name 'Gorsel dosyalari' -Ok $imgOk `
    -Fix 'Git clone tam mi kontrol edin; images/ klasoru olmali'

# 14. Portlar (bilgi)
$p3000 = Test-PortOpen -Port 3000
$p8000 = Test-PortOpen -Port 8000
if ($p3000 -or $p8000) {
    Write-Host "[BILGI] Port kullanimi:" -ForegroundColor DarkYellow
    if ($p3000) { Write-Host "       3000 mesgul — frontend zaten calisiyor olabilir" -ForegroundColor DarkYellow }
    if ($p8000) { Write-Host "       8000 mesgul — backend zaten calisiyor olabilir" -ForegroundColor DarkYellow }
} else {
    Write-Check -Name 'Port 3000 ve 8000' -Ok $true -Detail 'Bos — run.ps1 ile baslatabilirsiniz'
}

# 15. Backend DB teshisi (venv varsa)
Write-Host ''
Write-Host '--- Veritabani detay teshisi ---' -ForegroundColor Cyan
if (Test-Path $venvPy) {
    Push-Location (Join-Path $Root 'backend')
    & $venvPy tools\diagnose.py
    $dbExit = $LASTEXITCODE
    Pop-Location
    if ($dbExit -ne 0) { $issues++ }
} else {
    Write-Host '[ATLA] venv olmadigi icin veritabani testi yapilmadi.' -ForegroundColor DarkYellow
    $issues++
}

# 16. API health (backend calisiyorsa)
if ($p8000) {
    Write-Host ''
    Write-Host '--- API kontrolu ---' -ForegroundColor Cyan
    try {
        $resp = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health/' -TimeoutSec 5
        if ($resp.status -eq 'ok') {
            Write-Check -Name 'API /api/health/' -Ok $true -Detail "DB: $($resp.database)"
        } else {
            Write-Check -Name 'API /api/health/' -Ok $false -Detail $resp.message
        }
    } catch {
        Write-Check -Name 'API /api/health/' -Ok $false -Detail $_.Exception.Message `
            -Fix 'Backend penceresindeki kirmizi hata satirlarini okuyun'
    }
}

Write-Host ''
Write-Host '=== Ozet ===' -ForegroundColor Cyan
if ($issues -eq 0) {
    Write-Host 'Hazirsiniz! Calistirmak icin: .\run.ps1' -ForegroundColor Green
} else {
    Write-Host "$issues sorun bulundu. Adim adim cozum: KURULUM.md" -ForegroundColor Red
    Write-Host 'Otomatik kurulum denemek icin: .\setup.ps1' -ForegroundColor Yellow
}
Write-Host ''
exit $(if ($issues -eq 0) { 0 } else { 1 })
