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

addrWindowsLabels = (0x02, 0x3cf6)
#addrWindowsLabels2 = (0x02, 0x1dc5)

# la intro en el bank02
addrIntro = (0x02, 0x3e8a)

# los bosses del bank04
addrBosses = (0x04, 0x0739)
cantBosses = 21

addrMaps = (0x05, 0x0000)

# los offsets de 'world map', 'village', 'interior casa', 'interior cueva' y 'intro' respectivamente en el bank08
spriteSheetsAddr = [(0x08,0x00b0), (0x08,0x03b0), (0x08,0x06b0), (0x08,0x0938), (0x08,0x0c1a)]
# cantidad de sprites de cada spriteSheet
cantSpritesInSheet = [0x80, 0x80, 0x6c, 0x7b, 0x4c]

tilesetsOffsetsBank8 = [0x10000, 0x11000, 0x12000, 0x13000, 0xC000]
# the base tile of each tileset is the offsetBank8/16
baseSubtile = [off//0x10 for off in tilesetsOffsetsBank8]


addrExpTable = (0x08, 0x0dd6)

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


def _addrToInt(strAddr):
  """ converts a string 'bb:aaaa' into the tuple (bb,aaaa) """

  strBb = strAddr[0:2]
  strAaaa = strAddr[3:7]
  bb = int(strBb,16)
  aaaa = int(strAaaa,16)
  addr = (bb,aaaa)

  return addr

def _intToAddr(addr):
  """ converts the tuple (bb,aaaa) into the string 'bb:aaaa' """

  strAddr = '{:02x}:{:04x}'.format(addr[0], addr[1])
  return strAddr


def decodeJs(filepath):

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

  import json
  address = json.loads(data)
#  print('address: ' + str(address))

  mystic.address.addrDictionary = _addrToInt(address['addr_dictionary'])
  mystic.address.cantDictionary = int(address['cant_dictionary'])

  mystic.address.addrWindows = _addrToInt(address['addr_windows'])

  mystic.address.addrMagic = _addrToInt(address['addr_magic'])

  mystic.address.addrInitialWeapons = _addrToInt(address['addr_initial_weapons'])

  mystic.address.addrLoadStateStrangeBytes = _addrToInt(address['addr_loadstate_strangebytes'])

  mystic.address.addrWindowsLabels = _addrToInt(address['addr_windows_labels'])
#  mystic.address.addrWindowsLabels2 = _addrToInt(address['addr_windows_labels2'])

  mystic.address.addrIntro = _addrToInt(address['addr_intro'])

  mystic.address.addrBosses = _addrToInt(address['addr_bosses'])

  mystic.address.addrMaps = _addrToInt(address['addr_maps'])

  mystic.address.spriteSheetsAddr = []
  for strAddr in address['addr_sheet']:
    addrSheet = _addrToInt(strAddr)
    mystic.address.spriteSheetsAddr.append(addrSheet)

  mystic.address.cantSpritesInSheet = address['cant_sprites_in_sheet']
   
  mystic.address.addrExpTable = _addrToInt(address['addr_exp_table'])

  mystic.address.addrScriptAddrDic = _addrToInt(address['addr_script_addr_dic'])
  mystic.address.cantScripts = address['cant_scripts']

  mystic.address.addrMusic = _addrToInt(address['addr_music'])


def encodeJs(filepath):

  address = {}

  address['addr_dictionary'] = _intToAddr(addrDictionary)
  address['cant_dictionary'] = cantDictionary

  address['addr_windows'] = _intToAddr(addrWindows)

  address['addr_magic'] = _intToAddr(addrMagic)
  address['addr_initial_weapons'] = _intToAddr(addrInitialWeapons)

  address['addr_loadstate_strangebytes'] = _intToAddr(addrLoadStateStrangeBytes)

  address['addr_windows_labels'] = _intToAddr(addrWindowsLabels)
#  address['addr_windows_labels2'] = _intToAddr(addrWindowsLabels2)
  address['addr_intro'] = _intToAddr(addrIntro)
  address['addr_bosses'] = _intToAddr(addrBosses)

  address['addr_maps'] = _intToAddr(addrMaps)

  address['addr_sheet'] = []
  for addrSheet in spriteSheetsAddr:
    strAddr = _intToAddr(addrSheet)
    address['addr_sheet'].append(strAddr)

  address['cant_sprites_in_sheet'] = cantSpritesInSheet

  address['addr_exp_table'] = _intToAddr(addrExpTable)

  address['addr_script_addr_dic'] = _intToAddr(addrScriptAddrDic)
  address['cant_scripts'] = cantScripts

  address['addr_music'] = _intToAddr(addrMusic)


  import json
  strJson = json.dumps(address, indent=2)
#  strJson = json.dumps(data)
  f = open(filepath, 'w', encoding="utf-8")
  f.write('addrs = \n' + strJson)
  f.close()



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

    elif(line.startswith('addrExpTable')):
      idx = line.index('=')
      string = line[idx+1:].strip().strip('\"').strip('\'')
      idx = string.index(':')
      bank = int(string[idx-2:idx],16)
      offset = int(string[idx+1:idx+5], 16)
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrExpTable = (bank, offset)


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


