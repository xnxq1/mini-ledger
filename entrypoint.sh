#!/bin/bash
set -e

echo "🔄 Waiting for PostgreSQL..."

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "⏳ PostgreSQL is unavailable - sleeping..."
  sleep 2
done

echo "✅ PostgreSQL is up!"

echo "🔄 Running Alembic migrations..."
alembic upgrade head

echo "✅ Migrations applied successfully!"

echo "🚀 Starting application..."
exec "$@"

