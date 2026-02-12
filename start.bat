@echo off
REM Auralis - Quick start script for Windows

echo 🎵 Iniciando Auralis - AI Music Platform

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt

REM Variables de entorno
set FLASK_APP=run.py
set FLASK_ENV=development

REM Inicializar base de datos si no existe
if not exist "instance\auralis.db" (
    echo 🗄️ Inicializando base de datos...
    flask init-db
    
    echo 🎨 Creando datos de ejemplo...
    flask create-sample-data
)

REM Iniciar servidor
echo 🚀 Servidor iniciado en http://localhost:5000
echo 📝 Presiona Ctrl+C para detener
echo.

python run.py
