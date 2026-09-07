# IntelliDoc - Instalación Backend Windows (PowerShell)
# Ejecutar: .\install.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  IntelliDoc - Instalación Backend Windows" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# ChromaDB 0.4.22 no tiene wheel de chroma-hnswlib para Python 3.12.
$pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
if (-not $pythonLauncher) {
    Write-Host "ERROR: Instala Python 3.11 (https://www.python.org/downloads/release/python-3119/)" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}
py -3.11 -c "import sys; print(sys.version)" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Este proyecto requiere Python 3.11 para instalar ChromaDB en Windows." -ForegroundColor Red
    Write-Host "Instala Python 3.11 desde https://www.python.org/downloads/release/python-3119/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar directorio
if (-not (Test-Path "requirements.txt")) {
    Write-Host "ERROR: Ejecuta este script desde 09-Codigo-Fuente\backend" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "[1/6] Eliminando entorno virtual anterior..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
}

Write-Host "[2/6] Creando entorno virtual nuevo..." -ForegroundColor Yellow
py -3.11 -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: No se pudo crear venv. ¿Python en PATH?" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "[3/6] Activando entorno virtual..." -ForegroundColor Yellow
& venv\Scripts\Activate.ps1

Write-Host "[4/6] Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host "[5/6] Instalando dependencias BASE (numpy, scipy)..." -ForegroundColor Yellow
pip install --only-binary=:all: "numpy==1.26.4" "scipy==1.13.1"

Write-Host "[6/6] Instalando TODAS las dependencias del proyecto..." -ForegroundColor Yellow
pip install --only-binary=:all: -r requirements.txt

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para activar el entorno en futuras sesiones:" -ForegroundColor Gray
Write-Host "  cd 09-Codigo-Fuente\backend" -ForegroundColor Gray
Write-Host "  venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Para ejecutar el backend:" -ForegroundColor Gray
Write-Host "  uvicorn app.main:app --reload --port 8000" -ForegroundColor Gray
Write-Host ""
Read-Host "Presiona Enter para salir"