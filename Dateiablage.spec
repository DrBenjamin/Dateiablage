import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all submodules from your src package
hiddenimports = collect_submodules('src')

# Collect data files (e.g., images) from the Images directory
datas = [
    (os.path.join('_internal/images', '*'), '_internal/images'),
]

block_cipher = None

a = Analysis(
    ['Dateiablage.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# Create a GUI executable without a console
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Dateiablage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI apps
    icon=os.path.join('_internal/images', 'icon.ico')
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Dateiablage'
)

app = BUNDLE(
    coll,
    name='Dateiablage.app',
    icon=os.path.join('_internal/images', 'icon.icns'),
    info_plist={
        'CFBundleName': 'Dateiablage',
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleVersion': '0.1.0',
        'CFBundleIdentifier': 'org.seriousbenentertainment.dateiablage'
    }
)