# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'assets/fonts/*.*', 'assets/fonts' ),
         ( 'assets/images/cars/flame_decorated_F1_cars_small/*.*', 'assets/images/cars/flame_decorated_F1_cars_small' ),
         ( 'assets/music/background/*.ogg', 'assets/music/background' ),
         ( 'assets/music/start/*.ogg', 'assets/music/start' ),
         ( 'assets/music/end/*.ogg', 'assets/music/end' ),
         ( 'assets/*.txt', 'assets' ),
         ( 'assets/music/background/*.*', 'assets/music/background' )
         ]

a = Analysis(['main.py'],
             pathex=['/home/shan/Documents/Work/Programming/PythonProjects/dodge-car'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
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
               name='main')
