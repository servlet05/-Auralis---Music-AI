#!/bin/bash
# Auralis - Quick start script

echo "🎵 Iniciando Auralis - AI Music Platform"

# Verificar Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Variables de entorno
export FLASK_APP=run.py
export FLASK_ENV=development

# Inicializar base de datos si no existe
if [ ! -f "instance/auralis.db" ]; then
    echo "🗄️ Inicializando base de datos..."
    flask init-db
    
    echo "🎨 Creando datos de ejemplo..."
    flask create-sample-data
fi

# Iniciar servidor
echo "🚀 Servidor iniciado en http://localhost:5000"
echo "📝 Presiona Ctrl+C para detener"
echo ""

python run.py
