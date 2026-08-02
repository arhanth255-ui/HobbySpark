#!/bin/bash
set -e

VERSION="$1"

cd "$(dirname "$0")/.."

echo "Building Debian package..."

rm -rf deb

mkdir -p deb/DEBIAN
mkdir -p deb/usr/bin
mkdir -p deb/usr/share/applications
mkdir -p deb/usr/share/icons/hicolor/256x256/apps
mkdir -p deb/usr/share/hobbyspark

cp control deb/DEBIAN/control
cp hobbyspark.desktop deb/usr/share/applications/
cp hobbyspark deb/usr/bin/
cp assets/icon.png deb/usr/share/icons/hicolor/256x256/apps/hobbyspark.png
chmod +x deb/usr/bin/hobbyspark

cp -r dist/HobbySpark/* deb/usr/share/hobbyspark/

sed -i "s/@VERSION@/$VERSION/g" deb/DEBIAN/control

dpkg-deb --build deb
mv deb.deb HobbySpark-${VERSION}-amd64.deb

echo "Done."