$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    $pythonPath = $env:SENTINELMEM_PYTHON
    if (-not $pythonPath) {
        $localPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
        $pythonPath = if (Test-Path -LiteralPath $localPython) { $localPython } else { "python" }
    }
    $pnpmPath = $env:SENTINELMEM_PNPM
    if (-not $pnpmPath) { $pnpmPath = "pnpm" }

    & $pythonPath -m pytest -p no:cacheprovider
    if ($LASTEXITCODE -ne 0) { throw "pytest failed with exit code $LASTEXITCODE" }
    & $pythonPath -m ruff check src tests scripts
    if ($LASTEXITCODE -ne 0) { throw "ruff failed with exit code $LASTEXITCODE" }
    & $pnpmPath --dir frontend run build
    if ($LASTEXITCODE -ne 0) { throw "frontend build failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}