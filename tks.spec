# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.datastruct import Tree

block_cipher = None

# -----------------------------------------------------------------------------
# Resources
# -----------------------------------------------------------------------------

datas = [("assets", "assets"), ("installers", "installers"), ("package.h", ".")]



# -----------------------------------------------------------------------------
# Hidden imports
# -----------------------------------------------------------------------------

hiddenimports = []

hiddenimports += collect_submodules("nodes")
hiddenimports += collect_submodules("stub")

hiddenimports += [
    "jaraco",
    "jaraco.text",
    "jaraco.context",
    "jaraco.functools",
]

# -----------------------------------------------------------------------------
# Analysis
# -----------------------------------------------------------------------------

a = Analysis(
    ["tks.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pytest",
        "pip",
        "setuptools",
        "wheel",
        "tkinter.test",
        "unittest",
    ],
    noarchive=False,
    optimize=0,
)

# -----------------------------------------------------------------------------

pyz = PYZ(
    a.pure,
)

# -----------------------------------------------------------------------------

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,

    name="HobbySpark",

    debug=False,
    bootloader_ignore_signals=False,

    strip=False,
    upx=True,
    upx_exclude=[],

    console=False,

    disable_windowed_traceback=False,

    argv_emulation=False,
    target_arch=None,

    codesign_identity=None,
    entitlements_file=None,

    icon="installers/icon.ico",
)

# -----------------------------------------------------------------------------

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,

    strip=False,

    upx=True,
    upx_exclude=[],

    name="HobbySpark",
)

app = BUNDLE(
    coll,
    name="HobbySpark.app",
    icon="installers/icon.icns",
    bundle_identifier="com.hobbyspark.app",
)