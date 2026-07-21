# commit-msg — istenmeyen ortak yazar satirlarini siler
param([string]$CommitMsgFile)

if (-not (Test-Path $CommitMsgFile)) { exit 0 }

$lines = Get-Content $CommitMsgFile -Encoding UTF8
$filtered = $lines | Where-Object {
    $_ -notmatch '^\s*Co-authored-by:\s*.+<cursoragent@cursor\.com>\s*$'
}
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllLines($CommitMsgFile, $filtered, $utf8)
