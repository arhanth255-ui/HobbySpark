#!/bin/bash
set -e

VERSION="$1"

echo "Building Debian package..."

# Clean previous build
rm -rf deb

# Create package structure
mkdir -p deb/DEBIAN
mkdir -p deb/usr/bin
mkdir -p deb/usr/share/applications
mkdir -p deb/usr/share/icons/hicolor/256x256/apps
mkdir -p deb/usr/share/hobbyspark

# Package metadata
cp control deb/DEBIAN/control

# Desktop launcher
cp hobbyspark.desktop deb/usr/share/applications/

# Launcher script
cp hobbyspark deb/usr/bin/
chmod +x deb/usr/bin/hobbyspark

# Icon
cp assets/icon.png \
   deb/usr/share/icons/hicolor/256x256/apps/hobbyspark.png

# Application files
cp -r dist/HobbySpark/* deb/usr/share/hobbyspark/

# Replace version placeholder
sed -i "s/@VERSION@/$VERSION/g" deb/DEBIAN/control

# Build package
dpkg-deb --build deb "HobbySpark-${VERSION}-Linux-amd64.deb"

echo "Done!"