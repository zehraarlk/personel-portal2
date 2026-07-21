# Git hook kurulumu
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$HookSrc = Join-Path $Root 'scripts\git-hooks\commit-msg.ps1'
$HooksDir = Join-Path $Root '.git\hooks'
$HookDst = Join-Path $HooksDir 'commit-msg'

if (-not (Test-Path $HooksDir)) {
    Write-Host '[!] .git/hooks bulunamadi.' -ForegroundColor Red
    exit 1
}

$hookPath = $HookSrc -replace '\\', '/'
$wrapper = @"
#!/bin/sh
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$hookPath" "`$1"
"@

[System.IO.File]::WriteAllText($HookDst, $wrapper.Replace("`r`n", "`n"))
Write-Host 'Git hook kuruldu.' -ForegroundColor Green
