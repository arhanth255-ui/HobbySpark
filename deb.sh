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

cp linux/control deb/DEBIAN/control
cp linux/hobbyspark.desktop deb/usr/share/applications/
cp assets/icon.png deb/usr/share/icons/hicolor/256x256/apps/hobbyspark.png
cp linux/hobbyspark deb/usr/bin/
chmod +x deb/usr/bin/hobbyspark

cp -r dist/HobbySpark/* deb/usr/share/hobbyspark/

sed -i "s/@VERSION@/$VERSION/g" deb/DEBIAN/control

dpkg-deb --build deb
mv deb.deb HobbySpark-${VERSION}-amd64.deb

echo "Done."