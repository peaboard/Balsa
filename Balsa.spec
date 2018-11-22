# -*- mode: python -*-

block_cipher = None


a = Analysis(['Balsa.py'],
             pathex=['G:\\data1\\BilateralAlternatingStimulation'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [ ('balsa.ico', 'G:\\data1\\BilateralAlternatingStimulation\\balsa.ico', 'Data')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Balsa',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='balsa.ico')
