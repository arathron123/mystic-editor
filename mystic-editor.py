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

VERSION = '0.95.14'

#
# dictionary of the mystic spanglish nomenclature
# -----------------------------------------------
#
# * tile = 8x8 pixel picture.
# * sprite = 16x16 pixel picture.  Can be both for background (maps) or foreground (personajes).  Even bosses have many sprites.
#
# in the code, if a variable name starts with:
# * cant = quantity (from the spanish "cantidad")
# * nro = id (from the spanish "número")
# * nose = IDK (I don't know) (from the spanish "no se")
#

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
  lines.append('Optional Arguments:')
  lines.append('--rom [filePath] specifies the rom file to decode, example:')
  lines.append('**python3 mystic-editor.py --rom stockRoms/en.gb -e**')
  lines.append('')
  lines.append('--addr [filePath] specifies the address-configuration file to encode, example:')
  lines.append('**python3 mystic-editor.py --addr addr_en.js -e**')
  lines.append('')
  lines.append('-x (or --romexpand) encodes an expanded rom with more banks, example:')
  lines.append('**python3 mystic-editor.py --rom stockRoms/en.gb --addr addr/addr_en_romexpand.js --romexpand -e**')
  lines.append('')
  lines.append('-m (or --mscripts) decodes/encodes the scripts into mscripts.txt instead of jscripts.js, example:')
  lines.append('**python3 mystic-editor.py -dm**')
  lines.append('')
  lines.append('-t (or --tilesetsLevel2) decodes/encodes the tilesetsLevel2 folder, overwriting the big tilesets.png file, example:')
  lines.append('**python3 mystic-editor.py -dt**')
  lines.append('')
  lines.append('-c (or --color) encodes a gameboy color rom (work in progress), example:')
  lines.append('**python3 mystic-editor.py -ec**')
  lines.append('')
  lines.append('-f (or --fix-checksum) fixes the header and global checksums of the rom, example:')
  lines.append('**python3 mystic-editor.py -ef**')
  lines.append('')
  lines.append('-i (or --ips) creates an .ips patch of the newRom.gb, example:')
  lines.append('**python3 mystic-editor.py -ei**')
  lines.append('')
  lines.append('--ffl2 path/to/ffl2.gb  (it decodes music from english version of FFL 2 rom with md5sum **2bb0df1b672253aaa5f9caf9aab78224**)')
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


def testPlayground(romPath, basePath):

#  print('ejecutando test playground...')

  # limpio el banks/
#  mystic.romSplitter.clean()
  # creo el banks/
#  mystic.romSplitter.split()


#  mystic.romSplitter.exportDictionary()
#  mystic.romSplitter.burnDictionary('./en/dictionary/dictionary.js')
#  sys.exit(0)

  # decodifico el diccionario (compress)
#  mystic.dictionary.decodeRom()

#  for i in range(0,0x100):
#    chary = mystic.dictionary.decodeByte(i)
#    print('{:02x} '.format(i) + chary)
#  sys.exit(0)

#  string = 'ちからつきたジェマ'
#  values = mystic.dictionary.tryJpCompress(string)
#  strHex = mystic.util.strHexa(values)
#  print('comprimido strHex: ' + strHex)


#  mystic.romSplitter.exportTilesets()

  tilesetsLevel2 = False
#  tilesetsLevel2 = True
#  if(tilesetsLevel2):
    # exporto los multi-tilesets
#    mystic.romSplitter.exportFont()
#    mystic.romSplitter.exportMultiTilesets()
#    mystic.romSplitter.exportSpriteSheetPersonajes()

  # exporto los cuatro spriteSheets 
#  mystic.romSplitter.exportSpriteSheets(tilesetsLevel2)

#  mystic.romSplitter.burnFont()
#  mystic.romSplitter.burnMultiTilesets()
#  mystic.romSplitter.burnSpriteSheetPersonajes()


  # exporto lo gráficos (cada .bin en cuatro .png)
#  mystic.romSplitter.exportGfx()
#  mystic.romSplitter.exportFont()
#  mystic.romSplitter.burnFont()
#  mystic.romSplitter.burnTilesets()

#  print('exportando sprite sheet del heroe')
  # exporto los spriteSheet de personajes
#  mystic.romSplitter.exportSpriteSheetPersonajes()
#  mystic.romSplitter.exportSpriteSheetMonster()
#  mystic.romSplitter.burnSpriteSheetPersonajes()


  # exporto el texto
#  mystic.romSplitter.exportTexto()

  # para buscar patterns en la rom
#  mystic.romSplitter.pattern()
#  mystic.romSplitter.pattern2()



  # exports the game windows (Equip, Stats, Magic, etc)
#  mystic.romSplitter.exportWindows()
#  mystic.romSplitter.burnWindows(basePath + '/windows/windows.js')

#  mystic.romSplitter.exportWindowsTextLabels()
#  mystic.romSplitter.burnWindowsTextLabels('./en/items/windowsTextLabels.js')


#  print('exportando jscripts...')
#  mystic.romSplitter.exportJScripts()
#  print('importando jscripts...')
#  mystic.romSplitter.burnJScripts('./en/scripts/jscripts.js')

  # quemo el nroScript inicial (default 0x0003)
#  entraTopple = 0x0271
#  mystic.romSplitter.burnInitialScript(entraTopple)


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


  # export npcs
#  npcs = mystic.romSplitter.exportNpc()
#  mystic.romSplitter.burnNpc('./en/npc/npcs.js')

  # export bosses
#  bosses = mystic.romSplitter.exportBosses()
#  mystic.romSplitter.burnBosses('./en/bosses/bosses.js')

  # export projectiles
#  mystic.romSplitter.exportProjectiles()
#  mystic.romSplitter.burnProjectiles('./en/projectiles/projectiles.js')

  # export hero
#  mystic.romSplitter.exportHero()
#  mystic.romSplitter.burnHero('./en/npc/hero.js')



#  mystic.romSplitter.burnInitialScript(0x0208)

#  mystic.romSplitter.exportHeroProjectilesOld()
#  mystic.romSplitter.burnHeroProjectilesOld('./en/projectiles/heroProjsOld.js')

#  mystic.romSplitter.exportHeroProjectiles()
#  mystic.romSplitter.burnHeroProjectiles('./en/projectiles/heroProjs.js')

  # exporto golpes
#  mystic.romSplitter.exportGolpes()

  # exporto monstruo grande dobleTiles
#  mystic.romSplitter.exportMonstruoGrandeDosTiles()



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


  # -----------

  # exporto la música
#  mystic.romSplitter.exportSongs(exportLilypond=False)
#  mystic.romSplitter.exportSongs(exportLilypond=True)
#  mystic.romSplitter.exportSongsXml()
#  mystic.romSplitter.exportAudioJson()

#  nroBank, vaPorAddr = mystic.address.addrMusic
#  vaPorAddr = mystic.romSplitter.burnSongs('./en/audio/01_songs.txt', nroBank, vaPorAddr)

#  mystic.romSplitter.exportAudio()
#  mystic.romSplitter.burnAudio('./en/audio/02_vibrato.txt')
#  mystic.romSplitter.burnAudio('./en/audio/02_vibrato.txt', './en/audio/03_volume.txt', './en/audio/04_waves.txt')

  # exporto efectos de sonido
#  mystic.romSplitter.exportSounds()

#  mystic.romSplitter.burnSounds('./en/audio/05_sounds.txt')

  # cargo el banco 16 con las canciones
#  bank = mystic.romSplitter.banks[0x0F]

#  melody2 = mystic.music.Melody(29)
#  melody2 = mystic.music.Melody(nroChannel=2, addr=0x4d05, repeatTermina=False)
#  melody2.decodeRom(bank)

#  print('melody2: ' + str(melody2))
#  string = melody2.encodeTxt()
#  print('string: ' + '\n'.join(string))

#  array = melody2.encodeRom()
#  print('array: ' + mystic.util.strHexa(array))


  # exporto las estadísticas del rom
#  mystic.romStats.exportPng()

#  mystic.romSplitter.exportSongsRom('./en/songs.gb')
#  mystic.romSplitter.exportSongsRom('./de/songs.gb')
#  mystic.romSplitter.exportSongsRom('./game/songs.gb')


#  mystic.romSplitter.exportSoundsRom('./en/sounds.gb')



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
#  mystic.romSplitter.burnMapasTiledXml()
#  mystic.romSplitter.burnMapasJs()


#  mystic.romSplitter.gameGenieHacks()


  # exporto a solarus
#  mystic.romSplitter.exportSolarus()

#  mystic.romSplitter.burnSpriteSheets()


#  for i in range(0,0xbf):
#    pers = Variables.instance().personajes[i]
#    print('pers: ' + str(pers))


#  basePath = './en'
  # exporto nueva rom
  mystic.romSplitter.exportRom(basePath + '/newRom.gb')

#  pathStock = './stockRoms/en.gb'
#  pathNew = './en/newRom.gb'

#  print('comparing ' + pathStock + ' with ' + pathNew)
#  iguales = mystic.util.compareFiles(pathStock, pathNew, 0x0000, 0x40000)
#  print('roms coincide = ' + str(iguales))

  pathStock = romPath
  pathNew = basePath + '/newRom.gb'

  print('comparing ' + pathStock + ' with ' + pathNew)
  iguales = mystic.util.compareFiles(pathStock, pathNew, 0x0000, 0x40000)
  print('roms coincide = ' + str(iguales))





#  iguales = mystic.util.compareFiles('/home/arathron/newRomOrig.sav', '/home/arathron/newRom.sav', 0x0000, 0x40000)
#  print('save iguales = ' + str(iguales))





  # la juego
#  mystic.romSplitter.testRom(basePath + '/newRom.gb', 'vba')
#  shutil.copyfile(basePath + '/newRom.gb', '/home/arathron/RetroPie/roms/gb/newRom.gb')
#  mystic.romSplitter.testRom('/home/arathron/RetroPie/roms/gb/newRom.gb', 'vba-m')
#  mystic.romSplitter.testRom(basePath + '/newRom.gb', 'vba-m2')
#  mystic.romSplitter.testRom(basePath + '/newRom.gb', 'mgba')
#  mystic.romSplitter.testRom('/home/arathron/newRom.gb', 'vba-m')


#  iguales = mystic.util.compareFiles('./en/songs.gb', './stockRoms/gbs_en2.gb', 0x4000, 0x40000)
#  iguales = mystic.util.compareFiles('./en/songs.gb', './stockRoms/gbs_en.gb', 0x00, 0x8000)
#  iguales = mystic.util.compareFiles('./en/banks/bank_15/bank_15.bin','./fr/banks/bank_15/bank_15.bin', 0x0000, 0x4000)
#  print('los gbs iguales = ' + str(iguales))

  # la escucho
#  mystic.romSplitter.testRom('./de/gbs.gb', 'vba')



def _ffl2Extract(argv, argFlags):
    idx = argv.index('--ffl2')
    # agarro el romPath
    romPath = argv[idx+1]

    basePath = './ffl2_en'
    # si el directorio no existía
    if not os.path.exists(basePath):
      # lo creo
      os.makedirs(basePath)

    # read the rom
    romArray = mystic.util.fileToArray(romPath)

    # read the gbs bank 0
    gbsBank0 = mystic.util.fileToArray('gbsBank00.bin')

    # ffl2 gbs header
    gbsHeader = '47 42 53 01 13 01 df 3f df 3f 00 40 00 cf 00 00 46 69 6e 61 6c 20 46 61 6e 74 61 73 79 20 4c 65 67 65 6e 64 20 49 49 00 00 00 00 00 00 00 00 00 4e 6f 62 75 6f 20 55 65 6d 61 74 73 75 2c 20 4b 65 6e 6a 69 20 49 74 6f 00 00 00 00 00 00 00 00 31 39 39 31 20 53 71 75 61 72 65 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 21 ed 3f 85 6f 7e f5 cd 03 40 f1 e0 b1 c9 05 01 02 03 04 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13'

    header = mystic.util.hexaStr(gbsHeader)
    start = 0x3f64
    # replace the ffa gbs header with the ff2 gbs header
    for i in range(0,len(header)):
      gbsBank0[start+i] = header[i]    

    # load into banks
    banks = []
    subArray = romArray
    while(True):
      banco = subArray[:0x4000]
#      print('len banco: ' + str(len(banco)))
      if(len(banco) == 0):
        break
      # lo agrego a la lista de bancos
      banks.append(banco)
      subArray = subArray[0x4000:]

    # aca comienza el addr de música  (0a12 en mystic)
    addrMusic = 0x09f5
    musicBank = 14

    bank = banks[musicBank]

    canciones = mystic.music.Canciones()
    canciones.decodeRom(bank,addrMusic)

    lines = canciones.encodeTxt()
    strCanciones = '\n'.join(lines)
    f = open(basePath + '/01_songs.txt', 'w', encoding="utf-8")
    f.write(strCanciones)
    f.close()

    for i in range(0,19):
      cancion = canciones.canciones[i]

      lines = cancion.encodeTxt()
      strCancion = '\n'.join(lines)
      f = open(basePath + '/song_{:02}.txt'.format(i), 'w', encoding="utf-8")
      f.write(strCancion)
      f.close()

      lines = cancion.encodeLilypond()
      strCancion = '\n'.join(lines)
      f = open(basePath + '/song_{:02}_lily.txt'.format(i), 'w', encoding="utf-8")
      f.write(strCancion)
      f.close()
      


def _decode(argv, argFlags):
    # limpio el banks/
    mystic.romSplitter.clean()
    # creo el banks/
    mystic.romSplitter.split()

    # exporto lo gráficos (cada .bin en cuatro .png)
#    mystic.romSplitter.exportGfx()

    print('exporting dictionary...')
    mystic.romSplitter.exportDictionary()


    # exports the game windows (Equip, Stats, Magic, etc) and items
    print('exporting windows...')
    mystic.romSplitter.exportWindows()

    print('exporting tilesets...')
    # exporto los tilesets
    mystic.romSplitter.exportTilesets()

    tilesetsLevel2 = False
    # if it want to export the tilesets as multiple images (overwriting the big tileset)
    if('t' in argFlags or '--tilesetsLevel2' in argv):
      print('exporting tilesets level 2...')
      tilesetsLevel2 = True
      mystic.romSplitter.exportFont()
      mystic.romSplitter.exportMultiTilesets()
      # exporto los spriteSheet de personajes
      mystic.romSplitter.exportSpriteSheetPersonajes()
      # TODO: Esto no está terminado
#      print('exportando spriteSheet de bosses')
#      mystic.romSplitter.exportSpriteSheetMonster()

    # exporto los cuatro spriteSheets 
    mystic.romSplitter.exportSpriteSheets(tilesetsLevel2)


    # exporto la tabla de experiencia
    mystic.romSplitter.exportExpTable()

    print('exporting NPCs...')
    mystic.romSplitter.exportNpc()
    mystic.romSplitter.exportHero()

    print('exporting projectiles...')
    # exporto los proyectiles
    mystic.romSplitter.exportProjectiles()
    mystic.romSplitter.exportHeroProjectiles()

    print('exporting bosses...')
    # exporto los monstruos grandes
    mystic.romSplitter.exportBosses()

    # exporto el texto
    mystic.romSplitter.exportTexto()

    print('exporting jscripts...')
    mystic.romSplitter.exportJScripts()
    if('m' in argFlags or '--mscripts' in argv):
      print('exporting mscripts...')
      mystic.romSplitter.exportMScripts()
#      mystic.romSplitter.exportJScripts()


    print('exporting maps...')
    # exporto todos los mapas
#    mystic.romSplitter.exportMapas(exportPngFile=True)
    mystic.romSplitter.exportMapas(exportPngFile=False)

    print('exporting songs...')
    # exporto la música
#    mystic.romSplitter.exportSongs(exportLilypond=False)
    mystic.romSplitter.exportSongs(exportLilypond=True)

    # exporto todo el audio en formato json
    mystic.romSplitter.exportAudioJson()

    print('exporting sounds...')
    # exporto los efectos de sonido sfx
    mystic.romSplitter.exportSounds()



def _encode(argv, argFlags, romPath):

    basePath = mystic.address.basePath

    # quemo el nroScript inicial (default 0x0003)
#    entraTopple = 0x0271
#    mystic.romSplitter.burnInitialScript(entraTopple)

    if('x' in argFlags or '--romexpand' in argv):
      # cambio el MBC y expando la rom a 32 banks
      mystic.romexpand.romExpand()

    if('c' in argFlags or '--color' in argv):
      # cambio el MBC y expando la rom a 32 banks, y coloreamos sprites
      mystic.romexpand.romExpandDX()



    print('burning dictionary...')
    # burn the dictionary
    mystic.romSplitter.burnDictionary(basePath+'/dictionary/dictionary.js')

    # burns the game windows (Equip, Stats, Magic, etc) and items
    print('burning windows...')
    mystic.romSplitter.burnWindows(basePath+'/windows/windows.js')


    print('burning tilesets...')
    mystic.romSplitter.burnTilesets()

    tilesetsLevel2 = False
    if('t' in argFlags or '--tilesetsLevel2' in argv):
      print('burning tilesets level 2...')
      tilesetsLevel2 = True
      # exporto los multi-tilesets
      mystic.romSplitter.burnFont()
      mystic.romSplitter.burnMultiTilesets()
      mystic.romSplitter.burnSpriteSheetPersonajes()

    # y tabla de experiencia
    mystic.romSplitter.burnExpTable(basePath+'/exp.txt')

    print('burning spriteSheets...')
    mystic.romSplitter.burnSpriteSheets()
#    mystic.romSplitter.burnSpriteSheetPersonajes()

    print('burning NPCs...')
    mystic.romSplitter.burnNpc(basePath + '/npc/npcs.js')
    mystic.romSplitter.burnHero(basePath + '/npc/hero.js')

    print('burning projectiles...')
    # exporto los proyectiles
    mystic.romSplitter.burnProjectiles(basePath + '/projectiles/projectiles.js')
    mystic.romSplitter.burnHeroProjectiles(basePath + '/projectiles/heroProjs.js')

    print('burning bosses...')
    # quemo los monstruos grandes
    mystic.romSplitter.burnBosses(basePath + '/bosses/bosses.js')

    print('burning maps...')
#    mystic.romSplitter.burnMapas(basePath + '/mapas/mapas.txt')
#    mystic.romSplitter.burnMapasTiled()
    mystic.romSplitter.burnMapasTiledXml()
#    mystic.romSplitter.burnMapasJs()


    if('m' in argFlags or '--mscripts' in argv):
      print('burning mscripts...')
      mystic.romSplitter.burnMScripts(basePath + '/scripts/mscripts.txt')
    else:
      print('burning jscripts...')
      mystic.romSplitter.burnJScripts(basePath + '/scripts/jscripts.js')


    print('burning songs...')
    nroBank, vaPorAddr = mystic.address.addrMusic
#    print('addrMusic {:04x}'.format(vaPorAddr))

    # trata de mantener compatibilidad binaria con la rom original
    vaPorAddr = mystic.romSplitter.burnSongs(basePath+'/audio/01_songs.txt', nroBank, vaPorAddr)
#    print('vaPorAddr {:04x}'.format(vaPorAddr))

    print('burning sounds...')
    # quemo los efectos de sonido sfx
    mystic.romSplitter.burnSounds(filepath=basePath+'/audio/05_sounds.txt')


    # exporto la gbs rom con música
    mystic.romSplitter.exportSongsRom(basePath+'/songs.gb')
    # exporto la gbs rom con efectos de sonido
    mystic.romSplitter.exportSoundsRom(basePath+'/sounds.gb')


    if('f' in argFlags or '--fix-checksums' in argv):
      mystic.romSplitter.fixChecksums()

    # exporto nueva rom
    mystic.romSplitter.exportRom(basePath + '/newRom.gb')

#    lang = mystic.address.language
#    strLang = mystic.language.stockRomsLang[lang]
#    print('strLang: ' + strLang)
#    pathStock = './stockRoms/' + strLang + '.gb'
    pathStock = romPath
    pathNew = basePath + '/newRom.gb'

    if('i' in argFlags or '--ips' in argv):
      # exporto el .ips
      mystic.romSplitter.exportIps(pathStock, pathNew, basePath + '/newRom.ips')

    print('comparing ' + pathStock + ' with ' + pathNew)
    iguales = mystic.util.compareFiles(pathStock, pathNew, 0x0000, 0x40000)
    print('roms coincide = ' + str(iguales))

    # la juego
#    mystic.romSplitter.testRom(basePath + '/newRom.gb', 'vba')
#    mystic.romSplitter.testRom(basePath + '/newRom.gb', 'mgba')

#    shutil.copyfile(basePath + '/newRom.gb', '/home/arathron/RetroPie/roms/gb/newRom.gb')
#    mystic.romSplitter.testRom('/home/arathron/RetroPie/roms/gb/newRom.gb', 'vba-m')




#################################
def main(argv):
  print('Welcome to mystic-editor')

  # hago copia de seguridad de las roms stock que encuentre en el directorio actual, y asumo que quiere la rom que encuentre
  romPath = mystic.language.protectStockRoms()

  argFlags = []
  # we set up the short argument flags (like '-d' for decoding)
  for arg in argv:
    if(arg.startswith('-') and not arg.startswith('--')):
      for char in arg[1:]:
        argFlags.append(char)

  # if it want to extract FFL music data
  if('--ffl2' in argv):
    print('FFL2 extractor')
    _ffl2Extract(argv, argFlags)
    # termino el script
    sys.exit(0)


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
#    configAddrPath = './addr/addr_' + strLang + '.txt'
    configAddrPath = './addr/addr_' + strLang + '.js'

  idx0 = configAddrPath.index('addr_')
  configAddrFile = configAddrPath[idx0:]
#  print('configAddrFile: ' + configAddrFile)

  print('using configAddrPath: ' + configAddrPath)

#  f = open(configAddrPath, 'r', encoding="utf-8")
#  lines = f.readlines()
#  f.close()
#  mystic.address.decodeTxt(lines)
  mystic.address.decodeJs(configAddrPath)


  mystic.romSplitter.loadBanksFromFile(mystic.address.romPath)
  # decodifico el diccionario (compress)
  mystic.dictionary.decodeRom()

#  for i in range(0,0x100):
#    chary = mystic.dictionary.decodeByte(i)
#    print('{:02x} '.format(i) + chary)
#  sys.exit(0)


#  string = 'ちからつきたジェマ'
#  values = mystic.dictionary.tryJpCompress(string)
#  strHex = mystic.util.strHexa(values)
#  print('comprimido strHex: ' + strHex)

  basePath = mystic.address.basePath
  print('basePath: ' + basePath)

  # si tiene la cantidad correcta de parámetros
#  if('-d' in argv or '--decode' in argv):
  if('d' in argFlags or '--decode' in argv):

    print('decoding ' + mystic.address.romPath + '...')
    # decoding
    _decode(argv, argFlags)

    # encoding
    _encode(argv, argFlags, romPath)
    # copio el configAddrPath
    shutil.copyfile(configAddrPath, basePath+'/'+configAddrFile)

    # exporto las estadísticas del rom como decode (y primer encode)
    mystic.romStats.exportData('rom_info_decode')
    mystic.romStats.exportData('rom_info_encode')




    # termino el script
    sys.exit(0)

  elif('e' in argFlags or '--encode' in argv):
    print('encoding ' + romPath + '...')

    # encoding
    _encode(argv, argFlags, romPath)
    # copio el configAddrPath
    shutil.copyfile(configAddrPath, basePath+'/'+configAddrFile)

    # exporto las estadísticas del rom
    mystic.romStats.exportData('rom_info_encode')



    # termino el script
    sys.exit(0)


  else:
    printHelp()

  # si quiero testear algo
#  testPlayground(romPath, basePath)
  # generates de README.md with the current version
#  exportREADME()


if __name__ == "__main__":
  main(sys.argv[1:])

