import os
import sys
import shutil

import mystic.util

# los idiomas
ENGLISH = 0
ENGLISH_UK = 1
FRENCH = 2
GERMAN = 3
JAPAN = 4

# los md5sum de las rom stock originales
stockRomsMd5 = ['24cd3bdf490ef2e1aa6a8af380eccd78',
                '5f41a4de9f480c72cbc6eaad6bcc3753',
                '2efe1569e3be81e7e19b13eafc60cd24',
                'b6a08c7e3af4ec8c9559cd268115d97c',
                '3b359e9fec183bff5f964e25b599b246']

# los idiomas de las rom stock originales
stockRomsLang = ['en', 'en_uk', 'fr', 'de', 'jp']
stockRomsLanguage = ['english', 'english_uk', 'french', 'deutsch', 'japan']


def detectRomLanguage(romPath):
  """ detecta el idioma de la rom """

  # si no existe la rom
  if not os.path.exists(romPath):
    print(romPath + ': file not found')
    # termino con mensaje de error
    sys.exit(1)

  # sino
  else:

    # abro la rom
    array = mystic.util.fileToArray(romPath)
    # agarro los dos últimos bytes del bank0
    subArray = array[0x4000-4 : 0x4000]
    val = subArray[0]*0x100**3 + subArray[1]*0x100**2 + subArray[2]*0x100 + subArray[3]
#    print('val {:04x}'.format(val))

    if(val == 0xE7000000):
      lang = ENGLISH
      print(romPath + ': ' + stockRomsLanguage[lang] + ' rom detected')
    elif(val == 0xE7774AA3):
      lang = ENGLISH_UK
      print(romPath + ': english_uk rom detected')
    elif(val == 0x7F574AA3):
      lang = FRENCH
      print(romPath + ': french rom detected')
    elif(val == 0xD4D8DAA3):
      lang = GERMAN
      print(romPath + ': german rom detected')
    elif(val == 0x8B4400CF):
      lang = JAPAN
      print(romPath + ': japan rom detected')
    else:
      lang = -1
      print(romPath + ': unable to detect language')
      # termino con mensaje de error
      sys.exit(1)

  return lang


def protectStockRoms():
  """ hace copia de seguridad de las roms stock """


  path = './stockRoms'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  mypath = './'
  # agarro la lista de archivos de la carpeta actual
  files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

#  print('files: ' + str(files))

#  romPath = './stockRoms/en.gb'
  romPath = None

  # para cada archivo
  for fil in files:
    # calculo su md5
    md5 = mystic.util.md5sum(fil)

    # si es un md5 de stock rom original
    if(md5 in stockRomsMd5):
      idx = stockRomsMd5.index(md5)
      # me fijo en que idioma está
      lang = stockRomsLang[idx]
      romPath = './stockRoms/' + lang + '.gb'
      # si no está entre las roms stock
      if not os.path.exists(romPath):
        # copio la rom
        shutil.copyfile(fil, romPath)

#      mystic.address.language = idx
      mystic.romSplitter.loadBanksFromFile(romPath)
      # exporto música gbs
      mystic.romSplitter.exportSongsRom('./stockRoms/gbs_' + lang + '.gb')

  return romPath




