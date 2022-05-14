import sys
import os

# import language and stock-roms realted stuff
import mystic.language


# el idioma de la rom
language = mystic.language.ENGLISH

# el romPath
romPath = './stockRoms/en.gb'
romName = 'en'
# el path a la carpeta de base
basePath = './en'



# cosas del diccionario
addrDictionary = (0x00, 0x3f1d)
cantDictionary = 112

# listado de ventanas en el bank02
addrWindows = (0x02, 0x1baa)

# listado de magia en el bank02
addrMagic = (0x02, 0x1dda)

addrInitialWeapons = (0x02, 0x2f10)

addrLoadStateStrangeBytes = (0x02, 0x3aed)

# la intro en el bank02
addrIntro = (0x02, 0x3e8a)

addrMaps = (0x05, 0x0000)

# los offsets de 'world map', 'village', 'interior casa', 'interior cueva' y 'intro' respectivamente en el bank08
spriteSheetsAddr = [(0x08,0x00b0), (0x08,0x03b0), (0x08,0x06b0), (0x08,0x0938), (0x08,0x0c1a)]
# cantidad de sprites de cada spriteSheet
cantSpritesInSheet = [0x80, 0x80, 0x6c, 0x7b, 0x4c]

expTable = (0x08, 0x0dd6)

# cosas de scripts
addrScriptAddrDic = (0x08, 0x0f05)
cantScripts = 0x054a

# the songs
addrMusic = (0x0f, 0x0a12)

def setRomPath(romPath):

  # el romPath (ej: './roms/de.gb')
  mystic.address.romPath = romPath
  idx0 = romPath.rindex('/')+1
  idx1 = romPath.rindex('.')
  romName = romPath[idx0:idx1]
  # el romName (ej: 'de')
  mystic.address.romName = romName
  # el path a la carpeta de base
  mystic.address.basePath = './' + mystic.address.romName

  # configuro el romSplitter
  mystic.romSplitter.loadBanksFromFile(romPath)

  # detecto el idioma de la rom
  lang = mystic.language.detectRomLanguage(romPath)
  # y lo seteo
  mystic.address.language = lang


def decodeTxt(lines):
  for line in lines:
#    print('line: ' + line)

#    if(line.startswith('language')):
#      idx = line.index('=')
#      strLang = line[idx+1:].strip().strip('\"').strip('\'')
#      lang = mystic.language.stockRomsLang.index(strLang)
#      mystic.address.language = lang
#    elif(line.startswith('romPath')):
#      idx = line.index('=')
#      romPath = line[idx+1:].strip().strip('\"').strip('\'')
#      mystic.address.romPath = romPath
#    elif(line.startswith('romName')):
#      idx = line.index('=')
#      romName = line[idx+1:].strip().strip('\"').strip('\'')
#      mystic.address.romName = romName
#    elif(line.startswith('basePath')):
#      idx = line.index('=')
#      basePath = line[idx+1:].strip().strip('\"').strip('\'')
#      mystic.address.basePath = basePath

    if(line.startswith('addrDictionary')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrDictionary = (bank, offset)
    elif(line.startswith('cantDictionary')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      cantDictionary = int(string, 10)
#      print('cantDictionary: ' + str(cantDictionary))
      mystic.address.cantDictionary = cantDictionary

    elif(line.startswith('addrWindows')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrWindows = (bank, offset)

    elif(line.startswith('addrMagic')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrMagic = (bank, offset)

    elif(line.startswith('addrInitialWeapons')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrInitialWeapons = (bank, offset)

    elif(line.startswith('addrLoadStateStrangeBytes')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrLoadStateStrangeBytes = (bank, offset)

    elif(line.startswith('addrIntro')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrIntro = (bank, offset)

    elif(line.startswith('addrMaps')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrMaps = (bank, offset)

    elif(line.startswith('spriteSheetsAddr')):
      idx = line.index('=')
      strLista = line[idx+1:].strip().strip('\"').strip('\'').strip('[]').split(',')

      listado = []
      for string in strLista:
        idx = string.index(':')
        bank = int(string[idx-2:idx],16)
        offset = int(string[idx+1:idx+5], 16)
#        print('bank {:02x} offset {:04x}'.format(bank, offset))
        listado.append( (bank, offset) )

      mystic.address.spriteSheetsAddr = listado
    elif(line.startswith('cantSpritesInSheet')):
      idx = line.index('=')
      strLista = line[idx+1:].strip().strip('\"').strip('\'').strip('[]').split(',')
      mystic.address.cantSpritesInSheet = [int(addr,16) for addr in strLista]

    elif(line.startswith('expTable')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.expTable = (bank, offset)


    elif(line.startswith('addrScriptAddrDic')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrScriptAddrDic = (bank, offset)
    elif(line.startswith('cantScripts')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      cantScripts = int(string, 16)
#      print('cantScripts: {:04x}'.format(cantScripts))
      mystic.address.cantScripts = cantScripts

    elif(line.startswith('addrMusic')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrMusic = (bank, offset)


