Write-Host "Setting up PatentScout Development Environment..." -ForegroundColor Green

# 1. Create directories
Write-Host "Creating directory structure..." -ForegroundColor Cyan
$dirs = @("agents", "workflows", "tools", "scripts", "skills", "reports", "faiss_index", "tests")
foreach ($d in $dirs) {
    if (-Not (Test-Path $d)) {
        New-Item -ItemType Directory -Force -Path $d | Out-Null
    }
}
$initDirs = @("agents", "workflows", "tools", "scripts", "tests")
foreach ($d in $initDirs) {
    if (-Not (Test-Path "$d/__init__.py")) {
        New-Item -ItemType File -Force -Path "$d/__init__.py" | Out-Null
    }
}
$keepDirs = @("skills", "reports", "faiss_index", "db")
foreach ($d in $keepDirs) {
    if (-Not (Test-Path "$d/.gitkeep")) {
        New-Item -ItemType File -Force -Path "$d/.gitkeep" | Out-Null
    }
}

# 2. Python Setup
Write-Host "Setting up Python environment with uv..." -ForegroundColor Cyan
# Ensure uv is installed
if (-Not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Please install 'uv' first: https://github.com/astral-sh/uv" -ForegroundColor Red
    exit 1
}

uv venv
uv pip install -e ".[dev]"

# 3. Pre-commit
Write-Host "Setting up pre-commit hooks..." -ForegroundColor Cyan
uv run pre-commit install

# 4. Frontend Setup
Write-Host "Setting up Frontend environment..." -ForegroundColor Cyan
Push-Location frontend
npm install
npm install -D prettier eslint-config-prettier eslint-plugin-prettier
Pop-Location

# 5. Run Pre-commit
Write-Host "Running Pre-commit checks..." -ForegroundColor Cyan
uv run pre-commit run --all-files

Write-Host "Setup Complete! You can now start developing." -ForegroundColor Green
Write-Host "To start the backend: uv run uvicorn app:app --reload" -ForegroundColor Yellow
Write-Host "To start the frontend: cd frontend; npm run dev" -ForegroundColor Yellow
