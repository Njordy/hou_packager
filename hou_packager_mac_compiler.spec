# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/Users/njordy/Yandex.Disk.localized/Soup Manager/hou_packager/hou_packager.json'],
             pathex=['/Users/njordy'],
             binaries=[],
             datas=[],
             hiddenimports=['sip', "PySide2.QtCore", "PySide2.QtWidgets", 'json', "pathlib_mate"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.binaries +=[('shiboken2.so', '/Users/njordy/Prism/PythonLibs/Python27/PySide/PySide2/shiboken2.so', 'BINARY')]


exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='hou_packager',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='hou_packager')

app = BUNDLE(coll,
             name='hou_packager.app',
             icon=None,
             bundle_identifier=None)