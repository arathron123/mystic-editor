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


# snowman spriteGroup
addrSnowmanSpriteGroup = (0x00, 0x2c93)

# cosas del diccionario
addrDictionary = (0x00, 0x3f1d)
cantDictionary = 112

# the hero
addrHero = (0x01, 0x0752)
# the hero projectiles
addrHeroProjs = (0x01, 0x1dcd)

# listado de ventanas en el bank02
addrWindows = (0x02, 0x1baa)

addrLevelUp = (0x02, 0x1cfe)
addrWindowsAddr = (0x02, 0x1d0e)

# listado de magia en el bank02
addrMagic = (0x02, 0x1dda)

addrInitialWeapons = (0x02, 0x2f10)

addrDoorTileLocations = (0x02, 0x3aed)

addrWindowsLabels = (0x02, 0x3cf6)
addrWindowsLabels2 = (0x02, 0x3df9)
#addrWindowsLabels2 = (0x02, 0x1dc5)

# la intro en el bank02
addrIntro = (0x02, 0x3e8a)

# the npcs
#addrNpc = (0x03, 0x1f5a)
addrNpc = (0x03, 0x19fe)
numberNpcStats = 98
numberNpc = 191 
numberNpcGroup = 109

# los bosses del bank04
addrBoss = (0x04, 0x0739)
numberBoss = 21

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

# the projectiles
addrProjectiles = (0x09, 0x0479)
numberProjectiles = 40


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



  mystic.address.addrSnowmanSpriteGroup = _addrToInt(address['addr_snowman'])

  mystic.address.addrDictionary = _addrToInt(address['addr_dictionary'])
  mystic.address.cantDictionary = int(address['cant_dictionary'])

  mystic.address.addrHero = _addrToInt(address['addr_hero'])
  mystic.address.addrHeroProjs = _addrToInt(address['addr_hero_projs'])

  mystic.address.addrWindows = _addrToInt(address['addr_windows'])

  mystic.address.addrLevelUp = _addrToInt(address['addr_level_up'])
  mystic.address.addrWindowsAddr = _addrToInt(address['addr_windows_addr'])

  mystic.address.addrMagic = _addrToInt(address['addr_magic'])

  mystic.address.addrInitialWeapons = _addrToInt(address['addr_initial_weapons'])

  mystic.address.addrDoorTileLocations = _addrToInt(address['addr_door_tile_locations'])

  mystic.address.addrWindowsLabels = _addrToInt(address['addr_windows_labels'])
  mystic.address.addrWindowsLabels2 = _addrToInt(address['addr_windows_labels2'])

  mystic.address.addrIntro = _addrToInt(address['addr_intro'])

  mystic.address.addrNpc = _addrToInt(address['addr_npc'])
  mystic.address.numberNpcStats = int(address['number_npc_stats'])
  mystic.address.numberNpc = int(address['number_npc'])
  mystic.address.numberNpcGroup = int(address['number_npc_group'])

  mystic.address.addrBoss = _addrToInt(address['addr_boss'])
  mystic.address.numberBoss = int(address['number_boss'])

  mystic.address.addrMaps = _addrToInt(address['addr_maps'])

  mystic.address.spriteSheetsAddr = []
  for strAddr in address['addr_sheet']:
    addrSheet = _addrToInt(strAddr)
    mystic.address.spriteSheetsAddr.append(addrSheet)

  mystic.address.cantSpritesInSheet = address['cant_sprites_in_sheet']
   
  mystic.address.addrExpTable = _addrToInt(address['addr_exp_table'])

  mystic.address.addrScriptAddrDic = _addrToInt(address['addr_script_addr_dic'])
  mystic.address.cantScripts = address['cant_scripts']

  mystic.address.addrProjectiles = _addrToInt(address['addr_projectiles'])
  mystic.address.numberProjectiles = address['number_projectiles']

  mystic.address.addrMusic = _addrToInt(address['addr_music'])


def encodeJs(filepath):

  address = {}



  address['addr_snowman'] = _intToAddr(addrSnowmanSpriteGroup)

  address['addr_dictionary'] = _intToAddr(addrDictionary)
  address['cant_dictionary'] = cantDictionary

  address['addr_hero'] = _intToAddr(addrHero)
  address['addr_hero_projs'] = _intToAddr(addrHeroProjs)

  address['addr_windows'] = _intToAddr(addrWindows)

  address['addr_level_up'] = _intToAddr(addrLevelUp)
  address['addr_windows_addr'] = _intToAddr(addrWindowsAddr)

  address['addr_magic'] = _intToAddr(addrMagic)
  address['addr_initial_weapons'] = _intToAddr(addrInitialWeapons)

  address['addr_door_tile_locations'] = _intToAddr(addrDoorTileLocations)

  address['addr_windows_labels'] = _intToAddr(addrWindowsLabels)
  address['addr_windows_labels2'] = _intToAddr(addrWindowsLabels2)
  address['addr_intro'] = _intToAddr(addrIntro)

  address['addr_npc'] = _intToAddr(addrNpc)
  address['number_npc_stats'] = numberNpcStats
  address['number_npc'] = numberNpc
  address['number_npc_group'] = numberNpcGroup
  address['addr_boss'] = _intToAddr(addrBoss)
  address['number_boss'] = numberBoss

  address['addr_maps'] = _intToAddr(addrMaps)

  address['addr_sheet'] = []
  for addrSheet in spriteSheetsAddr:
    strAddr = _intToAddr(addrSheet)
    address['addr_sheet'].append(strAddr)

  address['cant_sprites_in_sheet'] = cantSpritesInSheet

  address['addr_exp_table'] = _intToAddr(addrExpTable)

  address['addr_script_addr_dic'] = _intToAddr(addrScriptAddrDic)
  address['cant_scripts'] = cantScripts

  address['addr_projectiles'] = _intToAddr(addrProjectiles)
  address['number_projectiles'] = numberProjectiles

  address['addr_music'] = _intToAddr(addrMusic)


  import json
  strJson = json.dumps(address, indent=2)
#  strJson = json.dumps(data)
  f = open(filepath, 'w', encoding="utf-8")
  f.write('addrs = \n' + strJson)
  f.close()




