# Start the API server (backend/app, port 8000) in a new window, then the frontend dev server (port 5173).
# Needs: pip install -r requirements.txt (a .venv at the repo root is used when present) and cd frontend && npm ci.
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$frontendDir = Join-Path $repoRoot "frontend"

if ($env:CONDA_PREFIX -and (Test-Path (Join-Path $env:CONDA_PREFIX "python.exe"))) {
    $python = Join-Path $env:CONDA_PREFIX "python.exe"
} elseif (Test-Path (Join-Path $repoRoot ".venv\Scripts\python.exe")) {
    $python = Join-Path $repoRoot ".venv\Scripts\python.exe"
} elseif (Test-Path (Join-Path $repoRoot ".venv\bin\python")) {
    $python = Join-Path $repoRoot ".venv\bin\python"
} else {
    $resolvedConda = $null
    if (Get-Command conda -ErrorAction SilentlyContinue) {
        $found = (& conda info --envs | Where-Object { $_ -match "ai4brain-clustering\s+(.+)$" } | ForEach-Object { $matches[1].Trim() })
        if ($found -and (Test-Path (Join-Path $found "python.exe"))) {
            $resolvedConda = Join-Path $found "python.exe"
        }
    }
    if ($resolvedConda) {
        $python = $resolvedConda
    } else {
        $python = "python"
    }
}

if (-not (Test-Path (Join-Path $frontendDir "node_modules"))) {
    Write-Error "Usage: run 'cd frontend && npm ci' first, then scripts/run_dev.ps1"
    exit 1
}

# Fit the clustering model and train the twin if they are missing (about 3 minutes the first time,
# instant after). Without them the server still runs, with no archetype or forecast.
Push-Location $repoRoot
& $python -m brain_twin_jepa.bootstrap
Pop-Location

Start-Process -FilePath $python -WorkingDirectory $repoRoot -ArgumentList "-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--reload", "--host", "127.0.0.1", "--port", "8000"

Set-Location $frontendDir
npm.cmd run dev
