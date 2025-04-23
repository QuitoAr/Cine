# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=['C:/Cine'],  # Ruta completa donde está tu proyecto
    binaries=[],
    datas=[
            ('gui/*.ui', 'gui'),  # Todos los archivos .ui
            ('*.ico', '.'),       # Todos los archivos .ico en el directorio raíz
            ('*.png', '.'),       # Todos los archivos .png en el directorio raíz
            ('*.jpg', '.'),       # Todos los archivos .jpg en el directorio raíz
        ],    
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
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
