# -*- mode: python -*-
a = Analysis(['client.py'],
             pathex=['/Users/conor/umass/lol_analysis/ItemBuilds'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='client',
          debug=False,
          strip=None,
          upx=True,
          console=True )
