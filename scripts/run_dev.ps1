# Start the API server (backend/app, port 8000) in a new window, then the frontend dev server (port 5173).
# Needs: pip install -r requirements.txt (a .venv at the repo root is used when present) and cd frontend && npm ci.
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$frontendDir = Join-Path $repoRoot "frontend"

$condaEnvPython = "C:\Users\User\miniconda3\envs\ai4brain-clustering\python.exe"
if (Test-Path $condaEnvPython) {
    $python = $condaEnvPython
} elseif ($env:CONDA_PREFIX -and (Test-Path (Join-Path $env:CONDA_PREFIX "python.exe"))) {
    $python = Join-Path $env:CONDA_PREFIX "python.exe"
} else {
    $python = Join-Path $repoRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $python)) { $python = "python" }
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
