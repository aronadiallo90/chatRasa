<#
.SYNOPSIS
    Lance le serveur d'actions Rasa en local avec la configuration de l'API PGDE.

.DESCRIPTION
    - lit CHATBOT_API_TOKEN dans le .env du projet Laravel emplois (aucun secret dans ce dépôt) ;
    - charge .env.local s'il existe (identifiants E-Carrière legacy, non suivi par git) ;
    - vérifie que Laravel répond et que le port des actions est libre ;
    - lance rasa run actions.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\start_actions_local.ps1
    powershell -ExecutionPolicy Bypass -File .\start_actions_local.ps1 -LaravelUrl http://127.0.0.1:8098
#>
param(
    [string]$LaravelUrl = 'http://127.0.0.1:8000',
    [string]$EmploisPath = 'C:\Users\Arona\Desktop\fp\emplois',
    [int]$Port = 5055,
    [ValidateSet('legacy', 'api')]
    [string]$ECarriereMode = 'legacy'
)

$ErrorActionPreference = 'Stop'
$projectPath = $PSScriptRoot

function Read-DotEnvValue([string]$filePath, [string]$key) {
    $line = Select-String -Path $filePath -Pattern "^\s*$key\s*=" | Select-Object -First 1
    if (-not $line) { return $null }
    return ($line.Line -split '=', 2)[1].Trim().Trim('"').Trim("'")
}

# 1. Jeton partagé avec Laravel
$emploisEnvFile = Join-Path $EmploisPath '.env'
if (-not (Test-Path $emploisEnvFile)) {
    Write-Host "ERREUR : fichier introuvable : $emploisEnvFile" -ForegroundColor Red
    exit 1
}
$chatbotToken = Read-DotEnvValue $emploisEnvFile 'CHATBOT_API_TOKEN'
if (-not $chatbotToken) {
    Write-Host "ERREUR : CHATBOT_API_TOKEN est absent ou vide dans $emploisEnvFile" -ForegroundColor Red
    exit 1
}

# 2. Variables locales facultatives (ex. LEGACY_ECARRIERE_DB_*)
$localEnvFile = Join-Path $projectPath '.env.local'
$localKeys = @()
if (Test-Path $localEnvFile) {
    foreach ($envLine in Get-Content $localEnvFile -Encoding UTF8) {
        if ($envLine -match '^\s*#' -or $envLine -notmatch '=') { continue }
        $parts = $envLine -split '=', 2
        $envKey = $parts[0].Trim()
        if (-not $envKey) { continue }
        Set-Item -Path "Env:$envKey" -Value $parts[1].Trim().Trim('"').Trim("'")
        $localKeys += $envKey
    }
}

$env:PYTHONIOENCODING = 'utf-8'
$env:CHATBOT_PGDE_BASE_URL = "$($LaravelUrl.TrimEnd('/'))/api/v1/chatbot"
$env:CHATBOT_PGDE_TOKEN = $chatbotToken
$env:CHATBOT_ECARRIERE_MODE = $ECarriereMode

# 3. Laravel doit répondre 401 sans jeton (preuve que la route chatbot existe)
try {
    Invoke-WebRequest -Method Post -Uri "$($env:CHATBOT_PGDE_BASE_URL)/pgde/accounts/verify" `
        -Headers @{ Accept = 'application/json' } -UseBasicParsing -TimeoutSec 10 | Out-Null
    Write-Host "ATTENTION : l'API PGDE a répondu sans jeton (attendu : 401)." -ForegroundColor Yellow
} catch {
    $statusCode = $null
    if ($_.Exception.Response) { $statusCode = [int]$_.Exception.Response.StatusCode }
    if ($statusCode -eq 401) {
        Write-Host "OK  Laravel répond sur $LaravelUrl" -ForegroundColor Green
    } elseif ($statusCode) {
        Write-Host "ATTENTION : l'API PGDE répond HTTP $statusCode (attendu : 401). Vérifie le .env de emplois et laravel.log." -ForegroundColor Yellow
    } else {
        Write-Host "ATTENTION : Laravel injoignable sur $LaravelUrl. Lance d'abord : php artisan serve" -ForegroundColor Yellow
    }
}

# 4. Un ancien serveur d'actions sur le port garderait l'ancienne configuration
$busyPort = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -First 1
if ($busyPort) {
    $oldProcess = Get-Process -Id $busyPort.OwningProcess -ErrorAction SilentlyContinue
    Write-Host "ERREUR : le port $Port est déjà utilisé (pid $($busyPort.OwningProcess), démarré à $($oldProcess.StartTime))." -ForegroundColor Red
    Write-Host "        Arrête l'ancien serveur d'actions (Ctrl+C dans son terminal) ou :" -ForegroundColor Red
    Write-Host "        Stop-Process -Id $($busyPort.OwningProcess)" -ForegroundColor Red
    exit 1
}

# 5. Lancement
Write-Host ''
Write-Host "PGDE         -> $($env:CHATBOT_PGDE_BASE_URL) (jeton : $($chatbotToken.Length) caractères)"
Write-Host "E-Carrière   -> mode $ECarriereMode"
if ($ECarriereMode -eq 'legacy' -and -not $env:LEGACY_ECARRIERE_DB_HOST) {
    Write-Host "               LEGACY_ECARRIERE_DB_* non définies : E-Carrière répondra 'Problème temporaire'." -ForegroundColor Yellow
    Write-Host "               (à renseigner dans .env.local, voir .env.example)" -ForegroundColor Yellow
}
if ($localKeys.Count -gt 0) { Write-Host ".env.local   -> $($localKeys -join ', ')" }
Write-Host "Actions      -> http://127.0.0.1:$Port"
Write-Host ''

& (Join-Path $projectPath '.venv\Scripts\rasa.exe') run actions --port $Port
