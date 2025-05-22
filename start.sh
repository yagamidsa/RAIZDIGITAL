#!/bin/bash

echo "🚀 Iniciando aplicación Django en Railway..."

echo "=== Variables de entorno ==="
echo "PGHOST: $PGHOST"
echo "PGDATABASE: $PGDATABASE" 
echo "PGUSER: $PGUSER"
echo "DATABASE_URL present: $([ -n "$DATABASE_URL" ] && echo "YES" || echo "NO")"
echo "SECRET_KEY present: $([ -n "$SECRET_KEY" ] && echo "YES" || echo "NO")"
echo "PORT: $PORT"

echo "⏳ Esperando 10 segundos para asegurar que la BD esté lista..."
sleep 10

echo "🔧 Verificando conexión a la base de datos..."
python manage.py check --database default

echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "🌐 Iniciando servidor Gunicorn..."
exec gunicorn raizdigital.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -