# MIGRACIÓN DE BASE DE DATOS POSTGRESQL LOCAL A RAILWAY
# ====================================================

Write-Host "🚀 MIGRACIÓN DE BASE DE DATOS POSTGRESQL LOCAL A RAILWAY" -ForegroundColor Green
Write-Host "========================================================"
Write-Host "⚠️  IMPORTANTE: Este script se ejecuta UNA SOLA VEZ desde tu máquina local" -ForegroundColor Yellow
Write-Host ""

# Verificar que tenemos las herramientas necesarias
try {
    $null = Get-Command pg_dump -ErrorAction Stop
    $null = Get-Command psql -ErrorAction Stop
    Write-Host "✅ Herramientas PostgreSQL encontradas" -ForegroundColor Green
}
catch {
    Write-Host "❌ PostgreSQL tools no encontrados. Instala PostgreSQL desde:" -ForegroundColor Red
    Write-Host "https://www.postgresql.org/download/windows/"
    exit 1
}

Write-Host ""

# Configuración de la base de datos local
$LOCAL_HOST = "localhost"
$LOCAL_PORT = "5432"
$LOCAL_USER = "yagami"
$LOCAL_PASSWORD = "Ipsos2012*"
$LOCAL_DB = "raiz_digital"

Write-Host "📋 CONFIGURACIÓN LOCAL:" -ForegroundColor Cyan
Write-Host "Host: $LOCAL_HOST"
Write-Host "Puerto: $LOCAL_PORT"
Write-Host "Usuario: $LOCAL_USER"
Write-Host "Base de datos: $LOCAL_DB"
Write-Host ""

# Obtener credenciales de Railway
Write-Host "🔑 OBTENER CREDENCIALES DE RAILWAY:" -ForegroundColor Yellow
Write-Host "1. Ve a tu proyecto en Railway"
Write-Host "2. Click en 'Database' (PostgreSQL)"
Write-Host "3. Pestaña 'Connect'"
Write-Host "4. Copia las variables que aparecen ahí"
Write-Host ""

$RAILWAY_HOST = Read-Host "PGHOST de Railway"
$RAILWAY_PORT = Read-Host "PGPORT de Railway (presiona Enter para 5432)"
if ([string]::IsNullOrEmpty($RAILWAY_PORT)) { 
    $RAILWAY_PORT = "5432" 
}
$RAILWAY_USER = Read-Host "PGUSER de Railway"
$RAILWAY_PASSWORD = Read-Host "PGPASSWORD de Railway"
$RAILWAY_DB = Read-Host "PGDATABASE de Railway"

Write-Host ""
Write-Host "📋 CONFIGURACIÓN RAILWAY:" -ForegroundColor Cyan
Write-Host "Host: $RAILWAY_HOST"
Write-Host "Puerto: $RAILWAY_PORT"
Write-Host "Usuario: $RAILWAY_USER"
Write-Host "Base de datos: $RAILWAY_DB"
Write-Host ""

# Confirmar antes de proceder
Write-Host "⚠️  ATENCIÓN:" -ForegroundColor Yellow
Write-Host "- Se creará un backup de tu BD local"
Write-Host "- Se restaurará en Railway PostgreSQL"
Write-Host "- Esto puede sobrescribir datos existentes en Railway"
Write-Host ""
$CONFIRM = Read-Host "¿Continuar con la migración? (s/N)"

if ($CONFIRM -ne "s" -and $CONFIRM -ne "S") {
    Write-Host "❌ Migración cancelada" -ForegroundColor Red
    exit 0
}

# Crear directorio para backups
Write-Host ""
Write-Host "📁 Creando directorio de backup..." -ForegroundColor Cyan
$backupDir = ".\database_migration"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}
Set-Location $backupDir

# Paso 1: Crear backup de la base de datos local
Write-Host ""
Write-Host "📤 PASO 1: Creando backup de la base de datos local..." -ForegroundColor Green
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "raiz_digital_backup_$timestamp.sql"

Write-Host "Ejecutando pg_dump..."

# Configurar variable de entorno para la contraseña local
$env:PGPASSWORD = $LOCAL_PASSWORD

# Ejecutar pg_dump
$pgDumpCmd = "pg_dump -h $LOCAL_HOST -p $LOCAL_PORT -U $LOCAL_USER -d $LOCAL_DB --clean --no-owner --no-privileges --file=`"$BACKUP_FILE`""

try {
    Invoke-Expression $pgDumpCmd
    
    if (Test-Path $BACKUP_FILE) {
        $backupSize = (Get-Item $BACKUP_FILE).Length / 1KB
        Write-Host "✅ Backup creado: $BACKUP_FILE" -ForegroundColor Green
        Write-Host "📊 Tamaño del backup: $([math]::Round($backupSize, 2)) KB"
    }
    else {
        Write-Host "❌ Error creando backup" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error ejecutando pg_dump: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Paso 2: Verificar conexión a Railway
Write-Host ""
Write-Host "🔗 PASO 2: Verificando conexión a Railway..." -ForegroundColor Green

# Cambiar a contraseña de Railway
$env:PGPASSWORD = $RAILWAY_PASSWORD

$testCmd = "psql -h $RAILWAY_HOST -p $RAILWAY_PORT -U $RAILWAY_USER -d $RAILWAY_DB -c `"SELECT 1;`" --quiet"

try {
    Invoke-Expression $testCmd | Out-Null
    Write-Host "✅ Conexión a Railway exitosa" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error conectando a Railway. Verifica las credenciales" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)"
    exit 1
}

# Paso 3: Restaurar en Railway
Write-Host ""
Write-Host "📥 PASO 3: Restaurando backup en Railway PostgreSQL..." -ForegroundColor Green
Write-Host "⚠️  Esto puede tomar varios minutos dependiendo del tamaño de tu BD" -ForegroundColor Yellow

$restoreCmd = "psql -h $RAILWAY_HOST -p $RAILWAY_PORT -U $RAILWAY_USER -d $RAILWAY_DB -f `"$BACKUP_FILE`""

try {
    Invoke-Expression $restoreCmd
    Write-Host "✅ Restauración completada exitosamente" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error en la restauración: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Paso 4: Verificar la migración
Write-Host ""
Write-Host "🔍 PASO 4: Verificando la migración..." -ForegroundColor Green

Write-Host "Contando tablas en Railway..."
$countTablesCmd = "psql -h $RAILWAY_HOST -p $RAILWAY_PORT -U $RAILWAY_USER -d $RAILWAY_DB -t -c `"SELECT count(*) FROM information_schema.tables WHERE table_schema IN ('public', 'raiz');`""

try {
    $tableCount = Invoke-Expression $countTablesCmd
    Write-Host "📊 Tablas encontradas en Railway: $($tableCount.Trim())"
}
catch {
    Write-Host "⚠️  No se pudo contar las tablas"
}

# Verificar tabla de usuarios si existe
Write-Host "Verificando usuarios..."
$countUsersCmd = "psql -h $RAILWAY_HOST -p $RAILWAY_PORT -U $RAILWAY_USER -d $RAILWAY_DB -t -c `"SELECT count(*) FROM raiz.usuarios;`""

try {
    $userCount = Invoke-Expression $countUsersCmd 2>$null
    if ($userCount) {
        Write-Host "👥 Usuarios migrados: $($userCount.Trim())"
    }
}
catch {
    Write-Host "⚠️  No se pudo verificar la tabla de usuarios (puede ser normal si la estructura es diferente)"
}

# Limpiar variables de entorno
Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "✅ ¡MIGRACIÓN COMPLETADA!" -ForegroundColor Green
Write-Host "================================================"
Write-Host "📋 RESUMEN:" -ForegroundColor Cyan
Write-Host "- Backup local creado: $BACKUP_FILE"
Write-Host "- Datos restaurados en Railway PostgreSQL"
Write-Host "- Tu aplicación ya debería usar Railway PostgreSQL automáticamente"
Write-Host ""
Write-Host "🔧 PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "1. Tu aplicación en Railway ya está configurada para usar Railway PostgreSQL"
Write-Host "2. No necesitas cambiar nada en tu código"
Write-Host "3. Puedes probar tu aplicación en Railway"
Write-Host "4. ¡Guarda el archivo de backup en un lugar seguro!"
Write-Host ""
$currentLocation = Get-Location
Write-Host "📁 Archivo de backup guardado en: $currentLocation\$BACKUP_FILE" -ForegroundColor Cyan

# Volver al directorio original
Set-Location ..