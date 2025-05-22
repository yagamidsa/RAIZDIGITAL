#!/bin/bash

echo "🚀 Iniciando aplicación Django en Railway..."

echo "=== Variables de entorno ==="
echo "PGHOST: $PGHOST"
echo "PGDATABASE: $PGDATABASE" 
echo "PGUSER: $PGUSER"
echo "DATABASE_URL present: $([ -n "$DATABASE_URL" ] && echo "YES" || echo "NO")"
echo "SECRET_KEY present: $([ -n "$SECRET_KEY" ] && echo "YES" || echo "NO")"
echo "PORT: $PORT"

echo "📁 Verificando estructura de archivos estáticos..."
echo "Contenido de /app/core/static/core/css:"
ls -la /app/core/static/core/css/ 2>/dev/null || echo "Directorio core/static/core/css no existe"

echo "Verificando variables.css:"
if [ -f "/app/core/static/core/css/variables.css" ]; then
    echo "✅ variables.css encontrado en fuente"
    echo "Tamaño: $(wc -c < /app/core/static/core/css/variables.css) bytes"
else
    echo "❌ variables.css NO encontrado en fuente"
fi

echo "⏳ Esperando 10 segundos para asegurar que la BD esté lista..."
sleep 10

echo "🔧 Verificando conexión a la base de datos..."
python manage.py check --database default

echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📁 === RECOPILANDO ARCHIVOS ESTÁTICOS ==="
echo "Limpiando staticfiles anteriores..."
rm -rf /app/staticfiles/*

echo "Ejecutando collectstatic..."
python manage.py collectstatic --noinput --clear --verbosity=2 | head -50

echo "📁 Verificando archivos recopilados..."
echo "Contenido de staticfiles/:"
ls -la /app/staticfiles/ | head -20

echo "Buscando archivos CSS específicos:"
find /app/staticfiles -name "*.css" -path "*/core/*" | head -10

echo "Verificando variables.css en staticfiles:"
if [ -f "/app/staticfiles/core/css/variables.css" ]; then
    echo "✅ variables.css COPIADO correctamente a staticfiles"
    ls -la /app/staticfiles/core/css/variables.css
else
    echo "❌ variables.css NO encontrado en staticfiles"
    echo "Buscando en toda la estructura:"
    find /app/staticfiles -name "variables.css" -type f
fi

echo "🌐 Iniciando servidor Gunicorn..."
exec gunicorn raizdigital.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -