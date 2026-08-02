#!/bin/bash
set -e

VERSION="$1"

if [ -z "$VERSION" ]; then
    VERSION="DEV"
fi

echo "Building Debian package..."

rm -rf deb

mkdir -p deb/DEBIAN
mkdir -p deb/usr/bin
mkdir -p deb/usr/share/applications
mkdir -p deb/usr/share/icons/hicolor/256x256/apps
mkdir -p deb/usr/share/hobbyspark

###############################################################################
# control
###############################################################################

cat > deb/DEBIAN/control <<EOF
Package: hobbyspark
Version: $VERSION
Section: development
Priority: optional
Architecture: amd64
Maintainer: HobbySpark Industries
Description: HobbySpark Programming Language and IDE
EOF

###############################################################################
# launcher
###############################################################################

cat > deb/usr/bin/hobbyspark <<'EOF'
#!/bin/bash
exec /usr/share/hobbyspark/HobbySpark "$@"
EOF

chmod +x deb/usr/bin/hobbyspark

###############################################################################
# desktop entry
###############################################################################

cat > deb/usr/share/applications/hobbyspark.desktop <<EOF
[Desktop Entry]
Name=HobbySpark
Comment=HobbySpark IDE
Exec=hobbyspark
Icon=hobbyspark
Terminal=false
Type=Application
Categories=Development;IDE;
EOF

###############################################################################
# icon
###############################################################################

cp assets/icon.png \
   deb/usr/share/icons/hicolor/256x256/apps/hobbyspark.png

###############################################################################
# application
###############################################################################

cp -r dist/HobbySpark/* deb/usr/share/hobbyspark/

###############################################################################
# build package
###############################################################################

dpkg-deb --build deb \
    "HobbySpark-${VERSION}-Linux-amd64.deb"

echo
echo "Successfully built:"
echo "HobbySpark-${VERSION}-Linux-amd64.deb"