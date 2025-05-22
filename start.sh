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
echo "Contenido de /app:"
ls -la /app/

echo "Contenido de /app/core/static:"
ls -la /app/core/static/ 2>/dev/null || echo "Directorio core/static no existe"

echo "Contenido de /app/core/static/core/css:"
ls -la /app/core/static/core/css/ 2>/dev/null || echo "Directorio core/static/core/css no existe"

echo "Verificando variables.css:"
if [ -f "/app/core/static/core/css/variables.css" ]; then
    echo "✅ variables.css encontrado"
    echo "Tamaño: $(wc -c < /app/core/static/core/css/variables.css) bytes"
else
    echo "❌ variables.css NO encontrado"
fi

echo "⏳ Esperando 10 segundos para asegurar que la BD esté lista..."
sleep 10

echo "🔧 Verificando conexión a la base de datos..."
python manage.py check --database default

echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📁 Recopilando archivos estáticos con verbose..."
python manage.py collectstatic --noinput --clear --verbosity=2

echo "📁 Verificando archivos recopilados..."
echo "Contenido de staticfiles:"
ls -la /app/staticfiles/ 2>/dev/null || echo "staticfiles no existe"

echo "Buscando variables.css en staticfiles:"
find /app/staticfiles -name "variables.css" -type f 2>/dev/null || echo "variables.css no encontrado en staticfiles"

echo "🌐 Iniciando servidor Gunicorn..."
exec gunicorn raizdigital.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -