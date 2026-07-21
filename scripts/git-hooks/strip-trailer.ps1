$text = [Console]::In.ReadToEnd()
$text = $text -replace '(?m)^Co-authored-by:\s*.+<cursoragent@cursor\.com>\s*\r?\n', ''
[Console]::Out.Write($text.TrimEnd())
