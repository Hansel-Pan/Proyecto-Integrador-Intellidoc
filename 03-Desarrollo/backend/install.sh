#!/bin/bash
# IntelliDoc - Instalación Backend (Git Bash / WSL / Linux)
# Ejecutar: bash install.sh

set -e  # Salir si hay error

echo "=========================================="
echo "  IntelliDoc - Instalación Backend (Bash)"
echo "=========================================="
echo

# Verificar directorio
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: Ejecuta este script desde 09-Codigo-Fuente/backend"
    exit 1
fi

# ChromaDB 0.4.22 requiere el wheel de chroma-hnswlib disponible para Python 3.11.
if command -v py >/dev/null 2>&1 && py -3.11 -c "import sys" >/dev/null 2>&1; then
    PYTHON_CMD=(py -3.11)
elif command -v python3.11 >/dev/null 2>&1; then
    PYTHON_CMD=(python3.11)
else
    echo "ERROR: Este proyecto requiere Python 3.11 para instalar ChromaDB en Windows."
    echo "Instala Python 3.11 desde https://www.python.org/downloads/release/python-3119/"
    exit 1
fi
echo "Python seleccionado: $(${PYTHON_CMD[@]} --version)"

echo "[1/6] Eliminando entorno virtual anterior..."
rm -rf venv

echo "[2/6] Creando entorno virtual nuevo..."
"${PYTHON_CMD[@]}" -m venv venv

echo "[3/6] Activando entorno virtual..."
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "[4/6] Actualizando pip..."
python -m pip install --upgrade pip

echo "[5/6] Instalando dependencias BASE (numpy, scipy)..."
pip install --only-binary=:all: "numpy==1.26.4" "scipy==1.13.1"

echo "[6/6] Instalando TODAS las dependencias del proyecto..."
pip install --only-binary=:all: -r requirements.txt

echo
echo "=========================================="
echo "  INSTALACIÓN COMPLETADA"
echo "=========================================="
echo
echo "Para activar el entorno en futuras sesiones:"
echo "  cd 09-Codigo-Fuente/backend"
echo "  source venv/Scripts/activate"
echo
echo "Para ejecutar el backend:"
echo "  uvicorn app.main:app --reload --port 8000"
echo