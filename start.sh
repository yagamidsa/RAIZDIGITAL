#!/bin/bash

echo " Iniciando aplicación Django en Railway..."

echo "=== Variables de entorno ==="
echo "PGHOST: $PGHOST"
echo "PGDATABASE: $PGDATABASE" 
echo "PGUSER: $PGUSER"
echo "DATABASE_URL present: $([ -n "$DATABASE_URL" ] && echo "YES" || echo "NO")"

echo "Esperando 10 segundos para asegurar que la BD esté lista..."
sleep 10

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor Gunicorn..."
gunicorn raizdigital.wsgi:application --bind 0.0.0.0:$PORT
