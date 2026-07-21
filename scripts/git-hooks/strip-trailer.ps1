$text = [Console]::In.ReadToEnd()
$text = $text -replace '(?m)^Co-authored-by:\s*Cursor\s*<cursoragent@cursor\.com>\s*\r?\n', ''
[Console]::Out.Write($text.TrimEnd())
