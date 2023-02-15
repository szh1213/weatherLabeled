# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['weatherLabeled.py'],
             pathex=[r'C:\Users\99930\Desktop\标注'],
             binaries=[],
             datas=[(r'C:\Users\99930\Desktop\标注\qss','qss'),
                (r'C:\Users\99930\Desktop\标注\img','png')],
             hiddenimports=['PySide6'],
             hookspath=[],
             hooksconfig={},
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='天气现象标注',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='img/logo.ico')
