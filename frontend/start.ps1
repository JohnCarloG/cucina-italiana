# Script di avvio per il Frontend (senza Python) usando HttpListener
param(
	[int]$Port = 3000
)

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Cucina Italiana - Avvio Frontend" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

$prefix = "http://localhost:$Port/"
$localUrl = "http://localhost:$Port/index.html"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($prefix)
$started = $false

try {
	try {
		$listener.Start()
		$started = $true
	} catch {
		Write-Host "Errore: la porta $Port è occupata o richiede permessi. Chiudi eventuali server già attivi su $Port e riprova." -ForegroundColor Red
		Write-Host "Suggerimento: netstat -ano ^| findstr :$Port  (per vedere il PID)" -ForegroundColor Yellow
		Write-Host "            taskkill /PID <pid> /F      (per chiudere il processo)" -ForegroundColor Yellow
		throw
	}
	Write-Host "Avvio server HTTP sulla porta $Port..." -ForegroundColor Yellow
	Write-Host ""
	Start-Sleep -Seconds 1

	Write-Host "====================================" -ForegroundColor Green
	Write-Host "Server avviato!" -ForegroundColor Green
	Write-Host ""
	Write-Host "Apertura browser..." -ForegroundColor Yellow
	Write-Host ""
	Write-Host "URL: $localUrl" -ForegroundColor Cyan
	Write-Host ""
	Write-Host "Premi CTRL+C per fermare il server" -ForegroundColor Yellow
	Write-Host "====================================" -ForegroundColor Green
	Write-Host ""

	Start-Process $localUrl

	$mimeMap = @{
		".html" = "text/html";
		".htm"  = "text/html";
		".js"   = "application/javascript";
		".css"  = "text/css";
		".png"  = "image/png";
		".jpg"  = "image/jpeg";
		".jpeg" = "image/jpeg";
		".svg"  = "image/svg+xml";
		".ico"  = "image/x-icon";
		".json" = "application/json";
	}

	while ($listener.IsListening) {
		$context = $listener.GetContext()
		$request = $context.Request
		$response = $context.Response

		$path = $request.Url.AbsolutePath.TrimStart('/')
		if ([string]::IsNullOrWhiteSpace($path)) { $path = "index.html" }

		$filePath = Join-Path $scriptPath $path
		if (-not (Test-Path $filePath)) {
			$response.StatusCode = 404
			$body = [System.Text.Encoding]::UTF8.GetBytes("404 - File not found")
			$response.OutputStream.Write($body, 0, $body.Length)
			$response.Close()
			continue
		}

		try {
			$bytes = [System.IO.File]::ReadAllBytes($filePath)
			$ext = [System.IO.Path]::GetExtension($filePath).ToLowerInvariant()
			if ($mimeMap.ContainsKey($ext)) {
				$response.ContentType = $mimeMap[$ext]
			}
			$response.StatusCode = 200
			$response.OutputStream.Write($bytes, 0, $bytes.Length)
		} catch {
			$response.StatusCode = 500
			$err = [System.Text.Encoding]::UTF8.GetBytes("500 - Server error")
			$response.OutputStream.Write($err, 0, $err.Length)
		}
		$response.Close()
	}
} catch {
	Write-Host "Errore: $_" -ForegroundColor Red
} finally {
	if ($started -and $listener -and $listener.IsListening) { $listener.Stop() }
	if ($listener) { $listener.Close() }
}

