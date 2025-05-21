#!/bin/bash

# Exit on any error
set -e

echo "🧹 Removing existing database..."
rm -f ngss.db

echo "📦 Recreating database from schema..."
sqlite3 ngss.db < schema.sql

echo "🌱 Seeding data from JSON..."
python seed.py

echo "✅ Done! Your database is reset and seeded."