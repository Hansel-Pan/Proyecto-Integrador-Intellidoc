@echo off
echo ==========================================
echo  IntelliDoc - Instalacion Backend Windows
echo ==========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "requirements.txt" (
    echo ERROR: Ejecuta este script desde 09-Codigo-Fuente/backend
    pause
    exit /b 1
)

REM ChromaDB 0.4.22 requiere un wheel disponible para Python 3.11.
py -3.11 -c "import sys; print(sys.version)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Este proyecto requiere Python 3.11 para instalar ChromaDB en Windows.
    echo Instala Python 3.11 desde https://www.python.org/downloads/release/python-3119/
    pause
    exit /b 1
)

echo [1/6] Eliminando entorno virtual anterior...
if exist venv rmdir /s /q venv

echo [2/6] Creando entorno virtual nuevo...
py -3.11 -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear venv. ¿Python en PATH?
    pause
    exit /b 1
)

echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [4/6] Actualizando pip...
python -m pip install --upgrade pip

echo [5/6] Instalando dependencias BASE (numpy, scipy)...
pip install --only-binary=:all: "numpy==1.26.4" "scipy==1.13.1"

echo [6/6] Instalando TODAS las dependencias del proyecto...
pip install --only-binary=:all: -r requirements.txt

echo.
echo ==========================================
echo  INSTALACION COMPLETADA
echo ==========================================
echo.
echo Para activar el entorno en futuras sesiones:
echo   cd 09-Codigo-Fuente\backend
echo   venv\Scripts\activate
echo.
echo Para ejecutar el backend:
echo   uvicorn app.main:app --reload --port 8000
echo.
pause