#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

# command line arguments
import sys

# pip3 install pypng
import png


import mystic.language
import mystic.romSplitter
import mystic.dictionary
import mystic.romStats
import mystic.address
import mystic.battery
import mystic.romexpand

VERSION = '0.95.5'

def printHelp():
  print('------------------------------------------------------------')
  print('mystic-editor v' + VERSION)
  print('Usage:')
  print('  mystic-editor.py <command>')
  print('    where <command> should be one of "-d", "--decode", "-e", "--encode" ')
  print('Examples:')
  print('  mystic-editor.py -d         (decodes a rom)')
  print('  mystic-editor.py -e         (encodes a rom)')
  print('The rom should be placed in this folder')
  print('------------------------------------------------------------')

def exportREADME():
  print('exporting README.md')

  lines = []
  lines.append('# mystic-editor')
  lines.append('')
  lines.append('Hi! This is a Mystic Quest (also known as Final Fantasy Adventure) gameboy game editor version ' + VERSION)
  lines.append('')
  lines.append('Tutorial video here: ')
  lines.append('https://www.youtube.com/watch?v=XKPYtgKAiQw')
  lines.append('')
  lines.append('Place the mystic quest gameboy rom in the same folder of this script.  The md5sum of the english version should be **24cd3bdf490ef2e1aa6a8af380eccd78**')
  lines.append('')
  lines.append('To run this script you need the following python libraries: pypng, Pillow.')
  lines.append('You can install them with the following commands')
  lines.append('')
  lines.append('pip install pypng')
  lines.append('pip install Pillow')
  lines.append('')
  lines.append('To decode the rom run')
  lines.append('**python3 mystic-editor.py -d**')
  lines.append('')
  lines.append('A folder named **en** (for english) will be created with all the maps, scripts, sprites, and audio files decoded from the rom.  This files can be edited and re-encoded again into the rom.')
  lines.append('')
  lines.append('To encode the rom run')
  lines.append('**python3 mystic-editor.py -e**')
  lines.append('')
  lines.append('If you want more control, you can specify the rom-file and address-configuration file like this example')
  lines.append('**python3 mystic-editor.py --rom stockRoms/en.gb --addr addr_en.txt -d**')
  lines.append('')
  lines.append('If you want to expand the rom to 32 banks add the --romexpand argument before encoding like this example')
  lines.append('**python3 mystic-editor.py --rom stockRoms/en.gb --addr addr_en_romexpand.txt --romexpand -e**')
  lines.append('')
  lines.append('Feel free to join our discord server')
  lines.append('https://discord.gg/mdTDMKh5FR')
  lines.append('')
  lines.append('Github repository:')
  lines.append('https://github.com/arathron123/mystic-editor')

  strReadme = '\n'.join(lines)

  f = open('README.md', 'w', encoding="utf-8")
  f.write(strReadme)
  f.close()


def testPlayground():

#  print('ejecutando test playground...')

  # limpio el banks/
#  mystic.romSplitter.clean()
  # creo el banks/
#  mystic.romSplitter.split()

  # decodifico el diccionario (compress)
#  Dictionary.instance().decodeRom()



  # exporto los tilesets
#  mystic.romSplitter.exportTilesets()

  # exporto los cuatro spriteSheets 
#  mystic.romSplitter.exportSpriteSheets()


  # exporto lo gráficos (cada .bin en cuatro .png)
#  mystic.romSplitter.exportGfx()
#  mystic.romSplitter.exportFont()
#  mystic.romSplitter.burnFont()
#  mystic.romSplitter.burnTilesets()

#  print('exportando sprite sheet del heroe')
  # exporto los spriteSheet de personajes
#  mystic.romSplitter.exportSpriteSheetPersonajes()
#  mystic.romSplitter.exportSpriteSheetHero()
#  mystic.romSplitter.exportSpriteSheetMonster()
#  mystic.romSplitter.burnSpriteSheetPersonajes()





  # exporto el texto
#  mystic.romSplitter.exportTexto()

  # para buscar patterns en la rom
#  mystic.romSplitter.pattern()
#  mystic.romSplitter.pattern2()

  # exporto la magia, items y weapons
#  print('exportando items...')
#  mystic.romSplitter.exportItems()

#  print('importando items...')
#  mystic.romSplitter.burnItems('magic','./en/items/magic.txt')
#  mystic.romSplitter.burnItems('item','./en/items/items.txt')
#  mystic.romSplitter.burnItems('weapon','./en/items/weapons.txt')
#  mystic.romSplitter.burnApdp('./en/items/03_apdp.txt', 0x24ca)
#  mystic.romSplitter.burnVendor('./en/items/04_vendor.txt', 0x24ea)
#  vaPorAddr = mystic.address.addrLoadStateStrangeBytes
#  mystic.romSplitter.burnSpecialItems('./en/items/10_specialItems.txt', vaPorAddr)


#  item = Cosas.instance().getItem(0x0e)
#  print('item: ' + str(item))
#  weap = Cosas.instance().getWeapon(0x0e)
#  print('weap: ' + str(weap))
#  magic = Cosas.instance().getMagic(0x03)
#  print('magic: ' + str(magic))




#  nroScript = 0x00e6
#  nroScript = 0x00fb # entra village
#  nroScript = 0x0525 # entra viejito village

#  nroScript = 0x010f # aparece cibba script largo
#  nroScript = 0x019d # aparece julius batalla final.
#  nroScript = 0x01a6 # abre puerta kett's sola si ya no está
  nroScript = 0x01e0 # habla kett's
#  nroScript = 0x01ec # habla señora cibba

#  nroScript = 0x0250 # habla rey Lorim
#  nroScript = 0x0257 # habla bogard (todas las veces, se ve que cambia por algún estado)
#  nroScript = 0x0258 # habla con jofy hasim está herido
#  nroScript = 0x0261 # habla amanda inicio
#  nroScript = 0x0265 # habla gladiador inicio
#  nroScript = 0x0267 # habla nene village
#  nroScript = 0x0268 # habla nene casita village
#  nroScript = 0x0269 # habla nena casita village
#  nroScript = 0x026a # habla viejo village
#  nroScript = 0x0275 # trata abrir cueva antes de ketts
#  nroScript = 0x029a # aparece bogard salida gaia

#  nroScript = 0x03d0 # cueva mtrocks caminó arriba
#  nroScript = 0x03ee # cueva mtrocks caminó derecha
#  nroScript = 0x03ef # cueva mtrocks camina derecha

#  bank, addr = 0x0d, 0x084c # cibba
#  bank, addr = 0x0e, 0x2967
#  bank, addr = 0x0e, 0x2a9b
#  bank, addr = 0x0e, 0x2bba
#  bank, addr = 0x0e, 0x11d7

#  script = mystic.romSplitter.scriptDecode(1)
#  script = mystic.romSplitter.scriptDecode(addr)
#  string, calls = script.iterarRecursivoRom(depth=0)
#  print('string: ' + string)


#  print('exportando scripts...')
#  mystic.romSplitter.exportScripts()
#  print('importando scripts...')
#  mystic.romSplitter.burnScripts('./en/scripts/scripts.txt')

  # exporto intro.txt
#  mystic.romSplitter.exportIntro()
#  mystic.romSplitter.burnIntro()
  # quemo el nroScript inicial (default 0x0003)
#  entraTopple = 0x0271
#  mystic.romSplitter.burnInitialScript(entraTopple)



#  bank06 = mystic.romSplitter.banks[0x06]
#  bloque = BloqueExterior()
#  array = bank06[0x2200:]
#  array = bank06[0x223e:]
#  array = bank06[0x2608:]
#  array = bank06[0x129d:]
#  bloque.decodeRomEvents(array)
#  array = bank06[0x2206:]
#  array = bank06[0x2247:]
#  array = bank06[0x260b:0x260b + 16]
#  bloque.decodeRomSprites(array, compress=3)
#  bloque.decodeRom(array,compress=3)

#  lines = bloque.encodeTxt()
#  strLines = '\n'.join(lines)

#  sheet = mystic.romSplitter.spriteSheets[1]
#  bloque.exportPngFile('./game/bloqu.png', sheet)

#  f = open('./game/bloquy.txt', 'w', encoding="utf-8")
#  f.write(strLines + '\n')
#  f.close()

#  f = open('./game/bloquy.txt', 'r', encoding="utf-8")
#  lines = f.readlines()
#  f.close()

  
#  bloque2 = BloqueExterior()
#  bloque2.decodeTxt(lines)
#  bloque2.decodeTxtEvents(lines)


#  array = bloque2.encodeRom(compress=4, disabledSpriteBytes=8)
#  strArray = mystic.util.strHexa(array)
#  print('strArray: ' + strArray)

#  lines = lines[3:]

#  bloque2.decodeTxtSprites(lines)

#  array = bloque2.encodeRomSprites(compress=3)
#  print('array = ' + str(array))
#  strArray = mystic.util.strHexa(array)
#  print('strArray: ' + strArray)


#  nroSpriteSheet=1
  # agarro el spriteSheet del nroSpriteSheet indicado
#  spriteSheet = SpriteSheet(16,8)
#  spriteSheet.readBank(nroSpriteSheet)



  # exporto el titulo
#  spriteSheet = SpriteSheet(16,8)
#  spriteSheet.readBank(4)
#  spriteSheet.exportPng('./de/coco.png')
#  bloque = BloqueExterior()
#  bank07 = mystic.romSplitter.banks[0x07]
#  array = bank07[0x3ee5:]
#  bloque._decodeRomSprites(array, 4)


#  bank07 = mystic.romSplitter.banks[0x07]
#  array = bank07[0x09f2:]
#  bloque3 = BloqueInterior()
#  bloque3.decodeRom(array)
  
#  lines = bloque3.encodeTxt()
#  strLines = '\n'.join(lines)

#  sheet = mystic.romSplitter.spriteSheets[2]
#  bloque3.exportPngFile('./game/inte.png',sheet)

#  f = open('./de/bloquyint2.txt', 'w', encoding="utf-8")
#  f.write(strLines + '\n')
#  f.close()

#  f = open('./de/bloquyint2.txt', 'r', encoding="utf-8")
#  lines = f.readlines()
#  f.close()

#  bloque4 = BloqueInterior()
#  bloque4.decodeTxt(lines)

#  array = bloque4.encodeRom()
#  strArray = mystic.util.strHexa(array)
#  print('strArray4: ' + strArray)



#  nroSpriteSheet=2
  # agarro el spriteSheet del nroSpriteSheet indicado
#  spriteSheet = SpriteSheet(16,8)
#  spriteSheet.readBank(nroSpriteSheet)


  # exporto todos los mapas
#  mystic.romSplitter.exportMapas(exportPngFile=False)
#  mystic.romSplitter.exportMapas(exportPngFile=True)



#  mapa = MapaExterior()

#  bank05 = mystic.romSplitter.banks[0x05]
#  array = bank05
#  disabledSpriteBytes = 8
#  mapa.decodeRom(array, disabledSpriteBytes)
#  sheet = mystic.romSplitter.spriteSheets[0]
#  mapa.exportPngFile('./game/mapy.png', sheet)

#  mapa = MapaInterior()
#  bank07 = mystic.romSplitter.banks[0x07]
#  array = bank07[0x0871:]
#  mapa.decodeRom(array)
#  sheet = mystic.romSplitter.spriteSheets[2]
#  mapa.exportPngFile('./game/mapu.png', sheet)




  # exporto los personajes
#  print('exportando personajes...')
#  mystic.romSplitter.exportPersonajes()
#  print('importando personajes...')
#  mystic.romSplitter.burnPersonajes('./en/personajes/personajes.txt')

#  mystic.romSplitter.exportPersonajeStats()
#  mystic.romSplitter.burnPersonajeStats('./en/personajes/personajeStats.txt')

  # exporto grupos de 3 personajes
#  mystic.romSplitter.exportGrupos3Personajes()
#  mystic.romSplitter.burnGrupos3Personajes('./game/personajes/grupos3Personajes.txt')
 
  # exporto cosas raras personajes tiles
#  mystic.romSplitter.exportCosasRarasPersonajes()


  # exporto las animaciones dosTiles de personajes
#  mystic.romSplitter.exportPersonajesAnimations()
#  mystic.romSplitter.burnPersonajesAnimations('./en/personajes/personajesAnimations.txt')


#  bosses = mystic.romSplitter.exportBosses()
#  mystic.romSplitter.burnBosses('./en/bosses/01_bosses.txt', './en/bosses/02_bossesDamage.txt', './en/bosses/03_bossesBehaviour.txt', './en/bosses/04_bossesAction.txt', './en/bosses/05_bossesMiniAction.txt', './en/bosses/06_bossesSpritesPos.txt', './en/bosses/07_bossesSortTiles.txt', './en/bosses/08_bossesAnimations.txt')
#  mystic.romSplitter.exportBossesBehaviour(bosses)



#  mystic.romSplitter.exportExplosions()

  # exporto golpes
#  mystic.romSplitter.exportGolpes()

  # exporto monstruo grande dobleTiles
#  mystic.romSplitter.exportMonstruoGrandeDosTiles()


  # exports the game windows (Equip, Stats, Magic, etc)
#  mystic.romSplitter.exportWindows()
#  mystic.romSplitter.burnWindows('./en/items/windows.txt')


#  mystic.romSplitter.exportExpTable()
#  mystic.romSplitter.burnExpTable('./en_uk/exp.txt')

  modificarBateria = False
#  modificarBateria = True
  if(modificarBateria):
#    saveFile = '/home/arathron/RetroPie/roms/gb/newRom.sav'
    saveFile = '/home/arathron/newRom.sav'
    save = mystic.battery.Save(saveFile)
#    save.printLindo()
    save.printBatt()


#    save.slot[0].setFlag(0x0b, True)
#    save.slot[0].setFlag(0x51, True)

#    save.slot[0].setFlag(0x0d, True)
#    save.slot[0].setFlag(0x27, True)
#    save.slot[0].setFlag(0x48, True)
#    save.slot[0].setFlag(0x52, False)

#    save.slot[0].setFlagByLabel('AMANDA_ACOMPANIA', False)
    save.slot[0].setFlagByLabel('FUJI_ACOMPANIA', True)
    save.slot[0].setFlagByLabel('CHOCOBO_ACOMPANIA', False)
    save.slot[0].setFlagByLabel('VENCIMOS_MEGAPEDE_CIENPIES', False)
    save.slot[0].setFlagByLabel('BOGARD_NOS_DIO_MATTOCK', False)
    save.slot[0].setFlagByLabel('BOGARD_DISCUTIO_SUMO', False)
    save.slot[0].setFlagByLabel('ENCONTRAMOS_MATTOCK', False)
    save.slot[0].setFlagByLabel('VENCIMOS_LOBITO', False)

#    val = save.slot[0].getFlagByLabel('CHOCOBO_ACOMPANIA')
#    print('val choco: ' + str(val))

#    mm,xy,uu,vv = save.slot[0].getCoords()
    # bogard
#    save.slot[0].setCoords(0x06,0x32,10,10)
    # lee
    save.slot[0].setCoords(0x03,0x41,10,10)
    # cibba
#    save.slot[0].setCoords(0x0e,0x17,10,10)

    save.slot[0].printFull()
    # grabo al archivo!
    save.saveFile()


#  scripts = Scripts()
#  scripts.decodeRom()

  # -----------

  # exporto la música
#  mystic.romSplitter.exportSongs(exportLilypond=False)
#  mystic.romSplitter.exportSongs(exportLilypond=True)


  # cargo el banco 16 con las canciones
#  bank = mystic.romSplitter.banks[0x0F]

#  melody2 = Melody(29)
#  melody2 = Melody(nroChannel=2, addr=0x4d05, repeatTermina=False)
#  melody2.decodeRom(bank)

#  print('melody2: ' + str(melody2))
#  string = melody2.encodeTxt()
#  print('string: ' + '\n'.join(string))



  # trata de mantener compatibilidad binaria con la rom original
#  mystic.romSplitter.burnSongs(filepath='./game/audio/songs.txt')
  # concatena todas las canciones, default para roms nuevas (no compatible con la original)
#  mystic.romSplitter.burnSongs(filepath='./de/audio/songs.txt', ignoreAddrs=True)
  # compatible con la original (agrega los headers misteriosos sin uso)
#  mystic.romSplitter.burnSongsHeaders(filepath='./de/audio/songs.txt')


  # exporto las estadísticas del rom
#  mystic.romStats.exportPng()

#  mystic.romSplitter.exportGbsRom('./de/gbs.gb')
#  mystic.romSplitter.exportGbsRom('./game/gbs.gb')


#  nroTileset = 0
#  banco12 = mystic.romSplitter.banks[12]
#  array = banco12[0x1000*nroTileset:0x1000*(nroTileset+1)]
#  tileset.decodeRom(array)
#  tile = Tile()
#  tile.decodeRom(array)
#  tile.exportPngFile('./game/tile.png')
#  tile.importPngFile('./game/tile.png')
#  lines = tile.encodeTxt()
#  string = '\n'.join(lines)
#  print(string)



#  iguales = mystic.util.compareFiles('./stockRoms/gbs_de.gb', './de/gbs.gb', 0x0000, 0x8000)
#  print('gbs iguales = ' + str(iguales))


#  mapas = Mapas()
#  mapas.decodeRom()
#  mystic.romSplitter.exportMapas(exportPngFile=False)
#  mystic.romSplitter.exportMapas(exportPngFile=True)
#  mystic.romSplitter.burnMapas('./game/mapas/mapas.txt')
#  mystic.romSplitter.burnMapasTiled()


#  mystic.romSplitter.gameGenieHacks()


  # exporto a solarus
#  mystic.romSplitter.exportSolarus()

#  mystic.romSplitter.burnSpriteSheets()


#  for i in range(0,0xbf):
#    pers = Variables.instance().personajes[i]
#    print('pers: ' + str(pers))


#  basePath = './en'
  # exporto nueva rom
#  mystic.romSplitter.exportRom(basePath + '/newRom.gb')

#  pathStock = './stockRoms/en.gb'
#  pathNew = './en/newRom.gb'

#  print('comparando ' + pathStock + ' con ' + pathNew)
#  iguales = mystic.util.compareFiles(pathStock, pathNew, 0x0000, 0x40000)
#  print('roms iguales = ' + str(iguales))




#  iguales = mystic.util.compareFiles('/home/arathron/newRomOrig.sav', '/home/arathron/newRom.sav', 0x0000, 0x40000)
#  print('save iguales = ' + str(iguales))





  # la juego
#  mystic.romSplitter.testRom(basePath + '/newRom.gb', 'vba')
#  shutil.copyfile(basePath + '/newRom.gb', '/home/arathron/RetroPie/roms/gb/newRom.gb')
#  mystic.romSplitter.testRom('/home/arathron/RetroPie/roms/gb/newRom.gb', 'vba-m')
#  mystic.romSplitter.testRom(basePath + '/newRom.gb', 'vba-m2')
#  mystic.romSplitter.testRom(basePath + '/newRom.gb', 'mgba')
#  mystic.romSplitter.testRom('/home/arathron/newRom.gb', 'vba-m')


#  iguales = mystic.util.compareFiles('./roms/gbs.gb', './game/banks/bank_15/bank_15.bin', 0x4000, 0x40000)
#  iguales = mystic.util.compareFiles('./en/banks/bank_15/bank_15.bin','./fr/banks/bank_15/bank_15.bin', 0x0000, 0x4000)
#  print('los gbs iguales = ' + str(iguales))

  # la escucho
#  mystic.romSplitter.testRom('./de/gbs.gb', 'vba')

  # generates de README.md with the current version
#  exportREADME()


#################################
def main(argv):
  print('Welcome to mystic-editor')

  # hago copia de seguridad de las roms stock que encuentre en el directorio actual, y asumo que quiere la rom que encuentre
  romPath = mystic.language.protectStockRoms()

  # si especifica la rom
  if('--rom' in argv):
    idx = argv.index('--rom')
    # agarro el romPath
    romPath = argv[idx+1]
  else:
    if(romPath == None):
      print('rom not found')

      printHelp()
      # termino el script
      sys.exit(0)

    else:
      print('found romPath = ' + romPath)

#  romPath = './stockRoms/en.gb'
#  romPath = './stockRoms/en_uk.gb'
#  romPath = './stockRoms/fr.gb'
#  romPath = './stockRoms/de.gb'
#  romPath = './stockRoms/jp.gb'
#  romPath = './ember.gb'

  # seteo la rom y language
  mystic.address.setRomPath(romPath)

  # si especifica el archivo de configuración
  if('--addr' in argv):
    idx = argv.index('--addr')
    # agarro el romPath
    configAddrPath = argv[idx+1]
  else: 
    
#    lang = mystic.language.detectRomLanguage(romPath)
    lang = mystic.address.language
    strLang = mystic.language.stockRomsLang[lang]
    configAddrPath = './addr/addr_' + strLang + '.txt'

  idx0 = configAddrPath.index('addr_')
  configAddrFile = configAddrPath[idx0:]
#  print('configAddrFile: ' + configAddrFile)

  print('using configAddrPath: ' + configAddrPath)
  f = open(configAddrPath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  mystic.address.decodeTxt(lines)


  mystic.romSplitter.loadBanksFromFile(mystic.address.romPath)
  # decodifico el diccionario (compress)
  mystic.dictionary.decodeRom()

#  for i in range(0,0x100):
#    chary = Dictionary.instance().decodeByte(i)
#    print('{:02x} '.format(i) + chary)
#  sys.exit(0)


#  string = 'ちからつきたジェマ'
#  values = Dictionary.instance().tryJpCompress(string)
#  strHex = mystic.util.strHexa(values)
#  print('comprimido strHex: ' + strHex)

  basePath = mystic.address.basePath
  print('basePath: ' + basePath)

  # si tiene la cantidad correcta de parámetros
  if('-d' in argv or '--decode' in argv):

    print('decoding ' + mystic.address.romPath + '...')

    # limpio el banks/
    mystic.romSplitter.clean()
    # creo el banks/
    mystic.romSplitter.split()

    # exporto lo gráficos (cada .bin en cuatro .png)
    mystic.romSplitter.exportGfx()
    # exporto los tilesets
    mystic.romSplitter.exportTilesets()
    # y la tabla de experiencia
    mystic.romSplitter.exportExpTable()

    mystic.romSplitter.exportFont()
    # exporto los cuatro spriteSheets 
    mystic.romSplitter.exportSpriteSheets()
    # exporto los spriteSheet de personajes
    mystic.romSplitter.exportSpriteSheetPersonajes()
    print('exportando sprite sheet del heroe')
    mystic.romSplitter.exportSpriteSheetHero()
    print('exportando spriteSheet de bosses')
    mystic.romSplitter.exportSpriteSheetMonster()

    print('exportando personajes')
    # exporto los personajes
    personajes = mystic.romSplitter.exportPersonajes()
    # exporto grupos de aparición de personajes
    mystic.romSplitter.exportGrupos3Personajes()
    # exporto las stats de enemigos
    mystic.romSplitter.exportPersonajeStats(personajes)
    # exporto las animaciones para los personajes
    mystic.romSplitter.exportPersonajesAnimations()

    print('exportando bosses')
    # exporto los monstruos grandes
    mystic.romSplitter.exportBosses()

    # exporto el texto
    mystic.romSplitter.exportTexto()

    # exporto las ventanas/paneles
    mystic.romSplitter.exportWindows()

    # exporto intro.txt
    mystic.romSplitter.exportIntro()
    # exporto la magia, items y weapons
    mystic.romSplitter.exportItems()

    print('exportando scripts...')
    mystic.romSplitter.exportScripts()

    # exporto todos los mapas
    mystic.romSplitter.exportMapas(exportPngFile=True)
#    mystic.romSplitter.exportMapas(exportPngFile=False)

    # exporto la música
#    mystic.romSplitter.exportSongs(exportLilypond=False)
    mystic.romSplitter.exportSongs(exportLilypond=True)

    # exporto las estadísticas del rom
    mystic.romStats.exportPng()

    # termino el script
    sys.exit(0)


  elif('-e' in argv or '--encode' in argv):
    print('encoding ' + romPath + '...')

    # copio el configAddrPath
    shutil.copyfile(configAddrPath, basePath+'/'+configAddrFile)

    # quemo el nroScript inicial (default 0x0003)
#    entraTopple = 0x0271
#    mystic.romSplitter.burnInitialScript(entraTopple)

    if('--romexpand' in argv):
      # cambio el MBC y expando la rom a 32 banks
      mystic.romexpand.romExpand()

    # quemo las ventanas/paneles
    mystic.romSplitter.burnWindows(basePath+'/items/windows.txt')

    # quemo la intro
    mystic.romSplitter.burnIntro()

    nroBank, vaPorAddr = mystic.address.addrMagic
    # quemando la magia
    vaPorAddr = mystic.romSplitter.burnItems('magic', basePath+'/items/00_magic.txt', nroBank, vaPorAddr)
    # items
    vaPorAddr = mystic.romSplitter.burnItems('item', basePath+'/items/01_items.txt', nroBank, vaPorAddr)
    # weapons
    vaPorAddr = mystic.romSplitter.burnItems('weapon', basePath+'/items/02_weapons.txt', nroBank, vaPorAddr)
    # el ap/dp
    vaPorAddr = mystic.romSplitter.burnApdp(basePath+'/items/03_apdp.txt', nroBank, vaPorAddr)
    # los vendedores
    vaPorAddr = mystic.romSplitter.burnVendor(basePath+'/items/04_vendor.txt', nroBank, vaPorAddr)

    nroBank, vaPorAddr = mystic.address.addrLoadStateStrangeBytes
    # el listado de items especiales
    vaPorAddr = mystic.romSplitter.burnSpecialItems(basePath+'/items/10_specialItems.txt', nroBank, vaPorAddr)

    mystic.romSplitter.burnFont()
    mystic.romSplitter.burnTilesets()

    # y tabla de experiencia
    mystic.romSplitter.burnExpTable(basePath+'/exp.txt')

    print('quemando spriteSheets...')
    mystic.romSplitter.burnSpriteSheets()

    mystic.romSplitter.burnSpriteSheetPersonajes()

    print('quemando personajes...')
    # quemo las animaciones para los personajes
    mystic.romSplitter.burnPersonajesAnimations(basePath + '/personajes/personajesAnimations.txt')
    # quemo los personajes en la rom
    mystic.romSplitter.burnPersonajes(basePath + '/personajes/personajes.txt')
    # quemo los grupos de aparición de personajes
    mystic.romSplitter.burnGrupos3Personajes(basePath + '/personajes/grupos3Personajes.txt')
    # quemo los stats de los personajes
    mystic.romSplitter.burnPersonajeStats(basePath + '/personajes/personajeStats.txt')

    print('quemando bosses...')
    # quemo los monstruos grandes
    mystic.romSplitter.burnBosses(basePath + '/bosses/01_bosses.txt', basePath + '/bosses/02_bossesDamage.txt', basePath + '/bosses/03_bossesBehaviour.txt', basePath + '/bosses/04_bossesAction.txt', basePath + '/bosses/05_bossesMiniAction.txt', basePath + '/bosses/06_bossesSpritesPos.txt', basePath + '/bosses/07_bossesSortTiles.txt', basePath + '/bosses/08_bossesAnimations.txt')


    print('quemando mapas...')
#    mystic.romSplitter.burnMapas(basePath + '/mapas/mapas.txt')
    mystic.romSplitter.burnMapasTiled()

    print('quemando scripts...')
    mystic.romSplitter.burnScripts(basePath + '/scripts/scripts.txt')

    print('quemando songs...')
    # trata de mantener compatibilidad binaria con la rom original
#    mystic.romSplitter.burnSongs(filepath=basePath+'/audio/songs.txt', ignoreAddrs=False)
    # concatena todas las canciones, default para roms nuevas (no compatible con la original)
#    mystic.romSplitter.burnSongs(filepath=basePath+'/audio/songs.txt', ignoreAddrs=True)
    # compatible con la original (agrega los headers misteriosos sin uso)
    mystic.romSplitter.burnSongsHeaders(filepath=basePath+'/audio/songs.txt')

    # exporto la gbs rom con música
    mystic.romSplitter.exportGbsRom(basePath+'/audio.gb')

    # exporto nueva rom
    mystic.romSplitter.exportRom(basePath + '/newRom.gb')

#    lang = mystic.address.language
#    strLang = mystic.language.stockRomsLang[lang]
#    print('strLang: ' + strLang)
#    pathStock = './stockRoms/' + strLang + '.gb'
    pathStock = romPath
    pathNew = basePath + '/newRom.gb'

    # exporto el .ips
    mystic.romSplitter.exportIps(pathStock, pathNew, basePath + '/newRom.ips')

    print('comparando ' + pathStock + ' con ' + pathNew)
    iguales = mystic.util.compareFiles(pathStock, pathNew, 0x0000, 0x40000)
    print('roms iguales = ' + str(iguales))

    # la juego
#    mystic.romSplitter.testRom(basePath + '/newRom.gb', 'vba')
#    mystic.romSplitter.testRom(basePath + '/newRom.gb', 'mgba')

#    shutil.copyfile(basePath + '/newRom.gb', '/home/arathron/RetroPie/roms/gb/newRom.gb')
#    mystic.romSplitter.testRom('/home/arathron/RetroPie/roms/gb/newRom.gb', 'vba-m')


    # termino el script
    sys.exit(0)

  else:
    printHelp()


  # si quiero testear algo
  testPlayground()


if __name__ == "__main__":
  main(sys.argv[1:])

