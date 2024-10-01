# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ["gotify_gnome_desktop.py"],
    pathex=[],
    binaries=[
        ("/usr/lib/x86_64-linux-gnu/girepository-1.0/Notify-0.7.typelib", "."),
        ("/usr/lib/x86_64-linux-gnu/libnotify.so.4.0.0", "."),
        ("/usr/lib/x86_64-linux-gnu/libnotify.so.4", "."),
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="gotify_gnome_desktop",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
