#!/bin/bash
set -e

VERSION="$1"

echo "Building HobbySpark Debian package..."

rm -rf deb

mkdir -p deb/DEBIAN
mkdir -p deb/usr/bin
mkdir -p deb/usr/share/applications
mkdir -p deb/usr/share/icons/hicolor/256x256/apps
mkdir -p deb/usr/share/hobbyspark

##############################################################################
# control
##############################################################################

cat > deb/DEBIAN/control <<EOF
Package: hobbyspark
Version: $VERSION
Section: devel
Priority: optional
Architecture: amd64
Maintainer: HobbySpark Industries
Description: HobbySpark Programming Language and IDE
EOF

##############################################################################
# launcher
##############################################################################

cat > deb/usr/bin/hobbyspark <<'EOF'
#!/bin/bash
exec /usr/share/hobbyspark/HobbySpark "$@"
EOF

chmod +x deb/usr/bin/hobbyspark

##############################################################################
# desktop
##############################################################################

cat > deb/usr/share/applications/hobbyspark.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=HobbySpark
Comment=HobbySpark IDE
Exec=hobbyspark
Icon=hobbyspark
Terminal=false
Categories=Development;
EOF

##############################################################################
# icon
##############################################################################

cp assets/icon.png \
deb/usr/share/icons/hicolor/256x256/apps/hobbyspark.png

##############################################################################
# program
##############################################################################

cp -r dist/HobbySpark/* \
deb/usr/share/hobbyspark/

##############################################################################
# build
##############################################################################

dpkg-deb --build deb \
"HobbySpark-${VERSION}-Linux-amd64.deb"

echo
echo "Finished!"