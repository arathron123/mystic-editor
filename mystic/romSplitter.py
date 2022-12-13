import os
import shutil

import mystic.address
import mystic.tileset
import mystic.spriteSheet
import mystic.romStats
import mystic.spritePersonaje
import mystic.personaje
import mystic.bosses
import mystic.projectiles
import mystic.inventory
import mystic.mscripts
import mystic.jscripts
import mystic.maps
import mystic.music
import mystic.ippy

# la rom
#self.rom = []
# los bancos
banks = []
# los cinco tilesets
#tilesets = []
tilesets = None
# los cinco spriteSheets
spriteSheets = []
# los mapas
#mapas = None

tilesetsOffsetsBank8 = [0x10000, 0x11000, 0x12000, 0x13000, 0xC000]
# the base tile of each tileset is the offsetBank8/16
baseTiles = [off//0x10 for off in tilesetsOffsetsBank8]


def getVal(bank, offset):
  hexa = self.banks[bank][offset]
  return hexa

def setVal(bank, offset, hexa):
  self.banks[bank][offset] = hexa


#def configure():
def loadBanksFromFile(romPath):
  """ lo preparo para splitear la rom indicada """

#  romPath = mystic.address.romPath

  mystic.romSplitter.banks = []

  f = open(romPath, 'rb')
  while True:
    piece = f.read(0x4000)

    listPiece = list(piece)

    if(len(piece) == 0):
      break

    # lo agrego a la lista de bancos
    mystic.romSplitter.banks.append(listPiece)

  f.close()


def loadBanksFromArray(romArray):
  """ load the banks from the rom array """

  mystic.romSplitter.banks = []

  subArray = romArray
  while(True):

    banco = subArray[:0x4000]
#    print('len banco: ' + str(len(banco)))

    if(len(banco) == 0):
      break

    # lo agrego a la lista de bancos
    mystic.romSplitter.banks.append(banco)

    subArray = subArray[0x4000:]

def getRomArrayFromBanks():
  """ returns the rom array by joining the banks """

  hexs = []

  for bank in mystic.romSplitter.banks:
    hexs.extend(bank)

  return hexs

def clean():
  """ borro la carpeta de split de la rom indicada """

  romName = mystic.address.romName

  # si el directorio existía
  if os.path.exists(romName):
    # lo borro 
    shutil.rmtree(romName)

def cleanBank(banco):
  """ pone un banco en 0x00 """

  clean = [0x00] * 0x4000
  mystic.romSplitter.banks[banco] = clean


#def fixHeader(self, *, name=None):
#        if name is not None:
#            name = name.encode("utf-8")
#            name = (name + (b"\x00" * 15))[:15]
#            self.banks[0][0x134:0x143] = name

#        checksum = 0
#        for c in self.banks[0][0x134:0x14D]:
#            checksum -= c + 1
#        self.banks[0][0x14D] = checksum & 0xFF

        # zero out the checksum before calculating it.
#        self.banks[0][0x14E] = 0
#        self.banks[0][0x14F] = 0
#        checksum = 0
#        for bank in self.banks:
#            checksum = (checksum + sum(bank)) & 0xFFFF
#        self.banks[0][0x14E] = checksum >> 8
#        self.banks[0][0x14F] = checksum & 0xFF



def fixChecksums():
  """ fixes the checksums for allowing playing on original hardware """

  bank0 = mystic.romSplitter.banks[0]

  # first we fix the header checksum
  prevHeaderChecksum = bank0[0x014d]
  checksum = 0
  for i in range(0x0134,0x014d):
    c = bank0[i]
    checksum -= c + 1
  headerChecksum = checksum & 0xFF
  print('setting headerChecksum (before: {:02x}   now: {:02x})'.format(prevHeaderChecksum, headerChecksum))
  bank0[0x014d] = headerChecksum

  globalChecksum = 0
  # now we fix the global checksum
  prevGlobalChecksum = bank0[0x014E]*0x100 + bank0[0x014F]
  # zero out the checksum before calculating it.
  bank0[0x014E] = 0
  bank0[0x014F] = 0
  for bank in mystic.romSplitter.banks:
    globalChecksum = (globalChecksum + sum(bank)) & 0xFFFF

  print('setting globalChecksum (before: {:04x} now: {:04x})'.format(prevGlobalChecksum, globalChecksum))
#  bank0[0x014E] = globalChecksum >> 8
#  bank0[0x014F] = globalChecksum & 0xFF
  bank0[0x014E] = globalChecksum // 0x100
  bank0[0x014F] = globalChecksum % 0x100


def exportRom(filepath):
  """ vuelve a juntar los bancos en una rom """

  hexs = mystic.romSplitter.getRomArrayFromBanks()

  f = open(filepath, 'wb')
  f.write( bytes(hexs) )
  f.close()

def exportBank(nroBank, filepath):

  # creo el archivo binario del banco
  g = open(filepath, 'wb')
  bank = mystic.romSplitter.banks[nroBank]
  bytesbank = bytes(bank)
  g.write(bytesbank)
  g.close()

def exportIps(pathStock, pathNew, pathIps):
  """ exports the .ips file """

  patch = mystic.ippy.Patch()
  patch.buildIpsFromFiles(pathStock, pathNew, pathIps)

def gameGenieHacks():
  """ cambia un par de bytes para que no reste HP """

  # gamegenie hacks!
  bank0 = mystic.romSplitter.banks[0]
  val = bank0[0x3e3a]
#  print('val1: {:02x}'.format(val))
  # cambio la resta 'sub l' por un nop (no resta hp los golpes, si el veneno)
  bank0[0x3e3a] = 0x00

  bank2 = mystic.romSplitter.banks[2]
  val = bank2[0x396c]
#  print('val2: {:02x}'.format(val))
  # cambio la resta 'sub l' por 'sub h' para que reste 0x00 el daño por veneno
  bank2[0x396c] = 0x94


def exportGbsRom(filepath):
  """ exporta a una rom musical gbs """

  # cargo el gbs rom
#  gbsRom = mystic.util.fileToArray('./roms/audio.gb')
  # me quedo con el bank00
#  gbsRom = gbsRom[0:0x4000]
  gbsRom = mystic.util.fileToArray('./gbsBank00.bin')
  # agarro el bank0f
  bank0f = mystic.romSplitter.banks[0x0f]
  # los concateno
  gbsRom.extend(bank0f)
  # creo la rom gbs de salida
  mystic.util.arrayToFile(gbsRom, filepath)


def testRom(filepath, emulator):
  """ ejecuta la rom indicada con el emulador vba de linux """

  # si es vba (sudo apt install visualboyadvance)
  if(emulator == 'vba'):
    comando = 'vba ' + filepath
    os.system(comando)

  # si es el mgba (sudo apt install mgba-sdl)
  elif(emulator == 'mgba'):
    comando = 'mgba -3 ' + filepath
    os.system(comando)

  elif(emulator == 'vba-m'):
    # para instalar vba-m
    #sudo snap install visualboyadvance-m --beta

    # cambio dir para evitar bug de vba-m
    os.chdir('/home/arathron/')

    comando = 'visualboyadvance-m ' + filepath
    os.system(comando)

  # si es el vba-m compilado
  elif(emulator == 'vba-m2'):
#    comando = 'vba ' + filepath
    comando = '../visualboyadvance-m/build/visualboyadvance-m ' + filepath
    os.system(comando)


def split():
  """ parte una rom en banks """

  basePath = mystic.address.basePath
  romPath = mystic.address.romPath
  romName = mystic.address.romName

  # si el directorio no existía
  if not os.path.exists(romName):
    # lo creo
    os.makedirs(romName)

  # copio la rom
  shutil.copyfile(romPath, basePath + '/' + romName + '.gb')

#  for i in range(0, 0x10):
  i = 0x00
  for bank in mystic.romSplitter.banks:
    bank = mystic.romSplitter.banks[i]

#    banco = 'bank_' + hex(i)[2:].zfill(2)
    banco = 'bank_' + str(i).zfill(2)
    folderName = romName + '/banks/' + banco 

    # si el directorio no existía
    if not os.path.exists(folderName):
      # creo la carpeta del banco
      os.makedirs(folderName)

    # creo el archivo binario del banco
    filepath = romName + '/banks/' + banco + '/' + banco + '.bin'
    mystic.romSplitter.exportBank(i, filepath)
    i += 1



def pattern():

#  pattern = 'abbba'
  pattern = 'ababbbbaba'
  pattern = 'abccba'
  pattern = 'babaabab'
  pattern = 'bbbaabbb'
  pattern = 'abcdabcdcdcdcdabcdab'
  pattern = 'abcd1234abcd1234'
  pattern = 'abababcdcdababab'
  pattern = 'aaaaaaaaaaaaaa'
  pattern = 'ab**ba'
  pattern = 'b*****a*****b*****a*****a*****a*****a*****b*****a*****b'
  pattern = 'a*b*a*b*a'
  pattern = 'ab*cd*ab*cd*cd'
  pattern = 'b*a*b*a*a*a*a*b'

  pattern = 'ababababababab'

  iPat = 0
  dic = {}

  array = mystic.romSplitter.rom

  iArr = 0
  for byty in array:

#    print('byty: ' + hex(byty))

    # agarro la letra del pattern que toca
    patKey = pattern[iPat]
#    print('patKey: ' + patKey)

    if(patKey == '*'):
      iPat += 1
    else:

      # si la letra ya estaba en el dic
      if(patKey in dic.keys()):
        # agarro el byty pattern
        bytyPat = dic[patKey]
#        print('tenia bytyPat: ' + hex(bytyPat))
      # sino
      else:

        # si el byty no estaba en los values anteriores
        if(byty not in dic.values()):
          # creo el byty pattern
          bytyPat = byty
          # lo seteo a la letra
          dic[patKey] = bytyPat
#          print('creamos bytyPat: ' + hex(bytyPat))
        # sino, el key ya estaba
        else:
          bytyPat = None
#          print('poniendo noneee!')


      # si el byty pattern coincide con el byty
      if(bytyPat == byty):
        # incremento la cuenta
        iPat += 1
      else:
        iPat = 0
        dic = {}

    if(iPat == len(pattern)):
#      print(' --- byty: ' + hex(byty)[2:].zfill(2) + ' - key: ' + pattern[0:iPat+1])
      patron = array[iArr - iPat + 1: iArr+1]
#      print('patron: ' + str(patron))

      strhex = ''
      for num in patron:
        strhex += hex(num)[2:].zfill(2) + ' '
#      strhex = mystic.romSplitter.bytesDecode(patron)
      print('addr: ' + hex(iArr)[2:].zfill(6) + ' - strhex: ' + strhex)
      iPat = 0
      dic = {}

    iArr += 1
   

def pattern2():

#  pattern = 'ababababababab'

  array = mystic.romSplitter.rom

  iArr = 0
  for i in range(10,len(array)):
    a0 = array[i-10]
    a1 = array[i-9]
    a2 = array[i-8]
    a3 = array[i-7]
    a4 = array[i-6]
    a5 = array[i-5]
    a6 = array[i-4]
    a7 = array[i-3]
    a8 = array[i-2]
    a9 = array[i-1]
    a10 = array[i-0]

    strhex = ''
    if(a1 == 0x00 and a2 == 0x03 and a3 == 0x01):

      strhex += hex(a0)[2:].zfill(2) + ' '
      strhex += hex(a1)[2:].zfill(2) + ' '
      strhex += hex(a2)[2:].zfill(2) + ' '
      strhex += hex(a3)[2:].zfill(2) + ' '
      strhex += hex(a4)[2:].zfill(2) + ' '
      strhex += hex(a5)[2:].zfill(2) + ' '
      strhex += hex(a6)[2:].zfill(2) + ' '
      strhex += hex(a7)[2:].zfill(2) + ' '
      strhex += hex(a8)[2:].zfill(2) + ' '
      strhex += hex(a9)[2:].zfill(2) + ' '
      strhex += hex(a10)[2:].zfill(2) + ' '


#      strhex = mystic.romSplitter.bytesDecode(patron)
      print('addr: ' + hex(iArr)[2:].zfill(6) + ' - strhex: ' + strhex)
 
    iArr += 1

def exportGfx():
  """ convierte los banks .bin en .png """

  basePath = mystic.address.basePath

  i = 0x00
  for bank in mystic.romSplitter.banks:
    # para cada una de las 4 paletas del banko
    for nroTileset in range(0,4):
      # creo el tileset
      tileset = mystic.tileset.Tileset(16,16)

      array = bank[0x1000*nroTileset:0x1000*(nroTileset+1)]        

      tileset.decodeRom(array)

      filepath = basePath + '/banks/bank_{:02}/tileset_{:02}_{:02}.png'.format(i, i, nroTileset)
#      print(filepath)
      tileset.exportPngFile(filepath)
    i += 1


def exportFont():

  basePath = mystic.address.basePath
  bank = mystic.romSplitter.banks[8]
  # creo el tileset
  tileset = mystic.tileset.Tileset(16,9)

  array = bank[0x1000*2+7*0x100:0x1000*(2+1)]

  tileset.decodeRom(array)
  tileset.exportPngFile(basePath + '/font.png')

def burnFont():

  basePath = mystic.address.basePath

  tileset = mystic.tileset.Tileset(16,9)
  tileset.importPngFile(basePath + '/font.png')
  array = tileset.encodeRom()

  mystic.romSplitter.burnBank(8, 0x1000*2+7*0x100, array)

def exportTilesetsOld():
  """ exporta los cinco tilesets """

  basePath = mystic.address.basePath
  path = basePath + '/tilesets'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  mystic.romSplitter.tilesets = []
  # para cada uno de los cinco tilesets
  for nroTileset in range(0,5):

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)

    # para los primeros 4 tilesets
    if(nroTileset < 4):
      tileset = mystic.tileset.Tileset(16,16)
      banco12 = mystic.romSplitter.banks[12]
      array = banco12[0x1000*nroTileset:0x1000*(nroTileset+1)]
      tileset.decodeRom(array)

      # agrego info al stats
      mystic.romStats.appendDato(0x0c, 0x1000*nroTileset, 0x1000*(nroTileset+1) , (rr, gg, bb), 'un tileset')

    # sino, para el 5to tileset
    else:
      tileset = mystic.tileset.Tileset(16,13)
      banco11 = mystic.romSplitter.banks[11]
      array = banco11[0x0000:0x0d00]
      tileset.decodeRom(array)

      # agrego info al stats
      mystic.romStats.appendDato(0x0b, 0x0000, 0x0d00, (rr, gg, bb), 'un tileset')

    tileset.exportPngFile(path + '/tileset_{:02}.png'.format(nroTileset))
    tileset.exportTiledXml(path + '/tileset_{:02}.tsx'.format(nroTileset))

    mystic.romSplitter.tilesets.append(tileset)

 
def exportTilesets():
  """ exporta el tilesets.png """

  basePath = mystic.address.basePath
  path = basePath + '/tilesets'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  tileset = mystic.tileset.Tileset(16,16*4*5)

  array = []
  # we make an array joining banks 8,9,10,11,12
  for i in range(8,13):
    banco = mystic.romSplitter.banks[i]
    array.extend(banco)

  array = array[0:0x1000*4*5]
  # and decode it as a big tileset
  tileset.decodeRom(array)
  tileset.exportPngFile(path + '/tilesets.png')
  tileset.exportTiledXml(path + '/tilesets.tsx')

  # set the tilesets on the romSplitter
  mystic.romSplitter.tilesets = tileset


def burnTilesets():

  basePath = mystic.address.basePath
  path = basePath + '/tilesets'

  tileset = mystic.tileset.Tileset(16,16*4*5)
  tileset.importPngFile(path + '/tilesets.png')
  array = tileset.encodeRom()

  # we burn the tilesets into the banks (skipping the disabled tiles)
  mystic.romSplitter.burnBank(8, 0x1A00, array[0x1A00:0x4000])
  mystic.romSplitter.burnBank(9, 0x0900, array[0x4900:0x4000*2])
  mystic.romSplitter.burnBank(10, 0x0000, array[0x4000*2:0x4000*3])
  mystic.romSplitter.burnBank(11, 0x0000, array[0x4000*3:0x4000*4])
  mystic.romSplitter.burnBank(12, 0x0000, array[0x4000*4:0x4000*5])

def burnTilesetsOld():

  basePath = mystic.address.basePath
  path = basePath + '/tilesets'
 
  # para cada uno de los cinco tilesets
  for nroTileset in range(0,5):

    # para los primeros 4 tilesets
    if(nroTileset < 4):
      tileset = mystic.tileset.Tileset(16,16)
      tileset.importPngFile(path + '/tileset_{:02}.png'.format(nroTileset))
      array = tileset.encodeRom()
      mystic.romSplitter.burnBank(12, 0x1000*nroTileset, array)

    # sino, para el 5to tileset
    else:
      tileset = mystic.tileset.Tileset(16,13)
      tileset.importPngFile(path + '/tileset_{:02}.png'.format(nroTileset))
      array = tileset.encodeRom()
      mystic.romSplitter.burnBank(11, 0x0000, array)

def burnSpriteSheets():

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheets'

  sheetNames = ['worldmap', 'city', 'inner', 'cave', 'title']
  spriteSheets = []
  # para cada una de los cinco spriteSheets 
  for nroSpriteSheet in range(0,5):

    sheet = mystic.spriteSheet.SpriteSheet(16,8,nroSpriteSheet,sheetNames[nroSpriteSheet])

    # decode from the .txt
#    filepath = path + '/sheet_{:02x}.txt'.format(nroSpriteSheet)
#    f = open(filepath, 'r', encoding="utf-8")
#    lines = f.readlines()
#    f.close()
#    sheet.decodeTxt(lines)

    filepath = path + '/sheet_{:02x}.tmx'.format(nroSpriteSheet)
    sheet.importTiledXml(filepath)

    array = sheet.encodeRom()
    strArray = mystic.util.strHexa(array)
#    print('array: ' + strArray)

    nroBank,addr = mystic.address.spriteSheetsAddr[nroSpriteSheet]
    cant = mystic.address.cantSpritesInSheet[nroSpriteSheet]
#    bank08 = mystic.romSplitter.banks[8]
#    array = bank08[addr:addr+6*cant]

    mystic.romSplitter.burnBank(nroBank, addr, array)
 

def exportSpriteSheets():
  """ exporta los spritesheets """

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheets'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  sheetNames = ['worldmap', 'city', 'inner', 'cave', 'title']
  mystic.romSplitter.spriteSheets = []
  # para cada una de los cinco spriteSheets 
  for nroSpriteSheet in range(0,5):

    sheet = mystic.spriteSheet.SpriteSheet(16,8,nroSpriteSheet,sheetNames[nroSpriteSheet])

    nroBank,addr = mystic.address.spriteSheetsAddr[nroSpriteSheet]
    cant = mystic.address.cantSpritesInSheet[nroSpriteSheet]
    bank08 = mystic.romSplitter.banks[nroBank]

    array = bank08[addr:addr+6*cant]
    sheet.decodeRom(array)
    # lo agrego a la lista
    mystic.romSplitter.spriteSheets.append(sheet)

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(nroBank, addr, addr+6*cant, (rr, gg, bb), 'sprite sheet')

    lines = sheet.encodeTxt()
    string = '\n'.join(lines)
    f = open(basePath + '/spriteSheets/sheet_{:02}_noedit.txt'.format(nroSpriteSheet), 'w', encoding="utf-8")
    f.write(string)
    f.close()

    sheet.exportPngFile(basePath + '/spriteSheets/sheet_{:02}_noedit.png'.format(nroSpriteSheet))

#    sheet.exportTiled(basePath + '/spriteSheets/sheet_{:02}.tsx'.format(nroSpriteSheet))
#    sheet.exportTiledXml(basePath + '/spriteSheets/sheet_{:02}.tsx'.format(nroSpriteSheet))
    sheet.exportTiledXml(basePath + '/spriteSheets/sheet_{:02}'.format(nroSpriteSheet))
    sheet.exportJs(basePath + '/spriteSheets/sheet_{:02}.js'.format(nroSpriteSheet))


def exportWindows():
  """ exporta las ventanas """

#  print('--- 2:1baa')

  basePath = mystic.address.basePath
  path = basePath + '/items'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  f = open(path + '/windows.txt', 'w', encoding="utf-8")
  nroBank,addr = mystic.address.addrWindows
  bank = mystic.romSplitter.banks[nroBank]

  # recorro las 34 ventanas
  for i in range(0,34):
    subArray = bank[addr + i*10: addr + (i+1)*10]
#    strArray = mystic.util.strHexa(subArray)
#    print('window: ' + strArray)

    win = mystic.inventory.Window(i)
    win.decodeRom(subArray)
#    print('win: --- ' + str(win))

    lines = win.encodeTxt()

    strWin = '\n'.join(lines)

    f.write(strWin)

  f.close()

def exportWindowsTextLabels():
  """ exporta los textos que son opciones en las ventanas """
#  print('--- 2:3cf6')

  basePath = mystic.address.basePath
  path = basePath + '/items'

#  bank = mystic.romSplitter.banks[2]
#  vaPorAddr = 0x3cf6
  bank,vaPorAddr = mystic.address.addrWindowsLabels

  data = {}

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 4,5)
  data['items'] = labels

#  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 3,5)
  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 3,6)
  data['select'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 4,7)
  data['status_upgrade'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 2,5)
#  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 3,5)
  data['yes_no'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 2,17)
#  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 3,17)
  data['level'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 1,7)
#  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 2,7)
  data['bought'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 4,16)
#  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 3,16)
  data['hello'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 2,15)
  data['not_enough'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 2,4)
  data['sell'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 3,4)
  data['buy'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 1,2)
  data['gp'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 4,6)
  data['upgrade'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 1,9)
  data['hp'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 1,6)
  data['mp'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 1,35)
  data['level_up'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 5,4)
  data['status'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 1,4)
  data['boy'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 1,4)
  data['girl'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 9,9)
  data['letters'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 2,8)
  data['cont'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 2,21)
  data['license'] = labels

  labels, vaPorAddr = _decodeWindowText(vaPorAddr, 36,19)
  data['intro'] = labels

  import json
#  strJson = json.dumps(data, indent=2)
#  strJson = json.dumps(data)
#  print('strPers: \n' + strJson)

#  f = open(filepath, 'w', encoding="utf-8")
#  f.write(strJson)
#  f.close()

  strJson = json.dumps(data, indent=2)
#  strJson = json.dumps(data)
  f = open(path + '/windowsTextLabels.js', 'w', encoding="utf-8")
  f.write('windowsTextLabels = \n' + strJson)
  f.close()


def burnWindowsTextLabels(filepath):

  array = []

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

  import json
  textLabels = json.loads(data)
#  print('labels: ' + str(labels))

  # codigo para un '\n'
  enterCode = 0x1a

  labels = textLabels['items']
  subArray = _encodeWindowText(labels, enterCode)
  # y lo agrego al array
  array.extend(subArray)

  labels = textLabels['select']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['status_upgrade']
  subArray = _encodeWindowText(labels, enterCode)
#  print('subarray: ' + mystic.util.strHexa(subArray))
  array.extend(subArray)

  labels = textLabels['yes_no']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['level']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['bought']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['hello']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['not_enough']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['sell']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['buy']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['gp']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['upgrade']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['hp']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['mp']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['level_up']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['status']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['boy']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['girl']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['letters']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['cont']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  labels = textLabels['license']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)


  lang = mystic.address.language
  if(lang in [mystic.language.ENGLISH, mystic.language.ENGLISH_UK, mystic.language.JAPAN]):
    enterCode = 0x00
  else: 
    enterCode = 0x1a

  labels = textLabels['intro']
  subArray = _encodeWindowText(labels, enterCode)
  array.extend(subArray)

  # agrego el byte de cierre
  array.append(0x01)


#  print('array: ' + mystic.util.strHexa(array))

#  nroBank,addr = 2, 0x3cf6
  nroBank,addr = mystic.address.addrWindowsLabels
  mystic.romSplitter.burnBank(nroBank, addr, array)


def _encodeWindowText(labels, enterCode):
  """ codifica lista de labels para ventana, el enterCode es el codigo de un \n """
  subArray = []

  for label in labels:

    label = label.replace('<00>', '@')

    for char in label:
      if(char == '@'):
        code = 0x00
      # lo codifico con el byte correspondiente
      elif(char == '\n'):
        code = enterCode
      elif(char == ' '):
        code = 0xff
      else:
        code = mystic.dictionary.encodeChars(char)

      # y lo agrego al array
      subArray.append(code)

  return subArray



def _decodeWindowText(addr, rows, labelWidth):

  bank = mystic.romSplitter.banks[2]
  vaPorAddr = addr

  labels = []

  for i in range(0,rows):
    label = ''
    for j in range(0,labelWidth):
      hexy = bank[vaPorAddr]
      vaPorAddr += 1
#      print('data: {:02x}'.format(hexy))
      if(hexy == 0x00):
        chars = '<00>'
      elif(hexy == 0x1a):
        chars = '\n'
      else: 
        chars = mystic.dictionary.decodeByte(hexy)
#      print('chars: ' + chars)
      label += chars
      if(hexy in [0x00, 0x1a]):
#      if(hexy in [0x00]):
        break
#    print('label: ' + label)
    labels.append(label)
  return labels, vaPorAddr




def burnWindows(filepath):
  """ quema las ventanas en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  i = 0
  windows = []
  primero = True
  subLines = []
  for line in lines:
#    print('line: ' + line)
    if('------------ window' in line):
      if(not primero):
        win = mystic.inventory.Window(i)
        win.decodeTxt(subLines)
        windows.append(win)
        i += 1
        subLines = []
      else:
        primero = False

    subLines.append(line)
  win = mystic.inventory.Window(i)
  win.decodeTxt(subLines)

  array = []
  for win in windows:
#    print('win: ' + str(win))
    subArray = win.encodeRom()
    array.extend(subArray)

  nroBank,addr = mystic.address.addrWindows
  mystic.romSplitter.burnBank(nroBank, addr, array)


def exportPersonajeStats(personajes):
  """ exporta los stat de los personajes """

#  print('--- 3:19fe')

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  f = open(path + '/personajeStats_noedit.txt', 'w', encoding="utf-8")

  bank = mystic.romSplitter.banks[0x03]

  personajeStatuses = []
  for i in range(0,0x62):
    subArray = bank[0x19fe + i*14: 0x19fe + (i+1)*14]
#    strArray = mystic.util.strHexa(subArray)
#    print('strArray: ' + strArray)

    stats = mystic.personaje.PersonajeStats(i)
    stats.decodeRom(subArray)
    personajeStatuses.append(stats)

#    print('stats: nro={:02x} '.format(stats.nroStats) + str(stats))

    lines = stats.encodeTxt(personajes)
    strStats = '\n'.join(lines)

    f.write(strStats)
 
  f.close()

  length = 14*len(personajeStatuses)
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x03, 0x19fe, 0x19fe+length, (rr, gg, bb), 'personajes stats')

def exportPersonajeStatsJs(personajes):
  """ exporta los stat de los personajes """

#  print('--- 3:19fe')

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  bank = mystic.romSplitter.banks[0x03]

  # la data del json
  data = []

  for i in range(0,0x62):
    subArray = bank[0x19fe + i*14: 0x19fe + (i+1)*14]
#    strArray = mystic.util.strHexa(subArray)
#    print('strArray: ' + strArray)

    stats = mystic.personaje.PersonajeStats(i)
    stats.decodeRom(subArray)


    # for all the personajes that use this stat
    pers = [per for per in personajes.personajes if per.stats == stats.nroStats]
    # get all their names
    names = []
    for per in pers:
      name = mystic.variables.personajes[per.nroPersonaje]
      names.append(name)

    subData = {}
    subData['comments'] = str(names)
    subData['nroStats'] = '{:02x}'.format(stats.nroStats)
    subData['speedSleep'] = '{:02x}'.format(stats.speedSleep)
    subData['hp'] = '{:02x}'.format(stats.hp)
    subData['nose2'] = '{:02x}'.format(stats.nose2)
    subData['nose3'] = '{:02x}'.format(stats.nose3)
    subData['nose4'] = '{:02x}'.format(stats.nose4)
    subData['maybeDP'] = '{:02x}'.format(stats.maybeDP)
    subData['maybeAP'] = '{:02x}'.format(stats.maybeAP)
    subData['vulnerability'] = '{:02x}'.format(stats.vulnerability)
    subData['nose6'] = '{:02x}'.format(stats.nose6)
    subData['projectile'] = '{:02x}'.format(stats.projectile)
    subData['nose7'] = '{:02x}'.format(stats.nose7)
    subData['statusInflicting'] = '{:02x}'.format(stats.statusInflicting)
    subData['maybeExp'] = '{:02x}'.format(stats.maybeExp)
    subData['maybeGP'] = '{:02x}'.format(stats.maybeGP)

    data.append(subData)

  import json
#  strJson = json.dumps(data, indent=2)
#  strJson = json.dumps(data)
#  print('strPers: \n' + strJson)

#  f = open(filepath, 'w', encoding="utf-8")
#  f.write(strJson)
#  f.close()

  strJson = json.dumps(data, indent=2)
#  strJson = json.dumps(data)
  f = open(path + '/personajeStats.js', 'w', encoding="utf-8")
  f.write('personajeStats = \n' + strJson)
  f.close()


  length = 14*len(data)
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x03, 0x19fe, 0x19fe+length, (rr, gg, bb), 'personajes stats')



def burnPersonajeStats(filepath):
  """ quema las stats de los personajes en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  i = 0
  personajeStatuses = []
  primero = True
  subLines = []
  for line in lines:
#    print('line: ' + line)
    if('------------ stats' in line):
      if(not primero):
        stats = mystic.personaje.PersonajeStats(i)
        stats.decodeTxt(subLines)
        personajeStatuses.append(stats)
        i += 1
        subLines = []
      else:
        primero = False

    subLines.append(line)
  stats = mystic.personaje.PersonajeStats(i)
  stats.decodeTxt(subLines)

  array = []
  for stats in personajeStatuses:
#    print('stats: ' + str(stats)) 
    subArray = stats.encodeRom()
    array.extend(subArray)

  mystic.romSplitter.burnBank(0x3, 0x19fe, array)



def burnPersonajeStatsJs(filepath):
  """ quema las stats de los personajes en la rom """
  
  personajeStatuses = []

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

  import json
  jsonPer = json.loads(data)

  i = 0
  for p in jsonPer:
#    print('p: ' + str(p))
    pers = mystic.personaje.PersonajeStats(i)
    pers.nroStats = int(p['nroStats'],16)
    pers.speedSleep = int(p['speedSleep'],16)
    pers.hp = int(p['hp'],16)
    pers.nose2 = int(p['nose2'],16)
    pers.nose3 = int(p['nose3'],16)
    pers.nose4 = int(p['nose4'],16)
    pers.maybeDP = int(p['maybeDP'],16)
    pers.maybeAP = int(p['maybeAP'],16)
    pers.vulnerability = int(p['vulnerability'],16)
    pers.nose6 = int(p['nose6'],16)
    pers.projectile = int(p['projectile'],16)
    pers.nose7 = int(p['nose7'],16)
    pers.statusInflicting = int(p['statusInflicting'],16)
    pers.maybeExp = int(p['maybeExp'],16)
    pers.maybeGP = int(p['maybeGP'],16)

    personajeStatuses.append(pers)
    i += 1

  array = []
  for stats in personajeStatuses:
#    print('stats: ' + str(stats)) 
    subArray = stats.encodeRom()
    array.extend(subArray)

  mystic.romSplitter.burnBank(0x3, 0x19fe, array)



def exportBosses():
  """ exporta los monstruos grandes """

#  print('--- 4:0739')

  bank = mystic.romSplitter.banks[0x04]
  bosses = mystic.bosses.Bosses()
  bosses.decodeRom(bank)

  return bosses.bosses


def burnBosses(pathBosses, pathBossesDamage, pathBehaviour, pathActions, pathMiniActions, pathPositions, pathSortTiles, pathAnimations):
  """ quema los monstruos grandes en la rom """

  bosses = mystic.bosses.Bosses()

  f = open(pathBosses, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeTxt(lines)

  f = open(pathBossesDamage, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeDamageTxt(lines)

  f = open(pathBehaviour, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeBehaviourTxt(lines)

  f = open(pathActions, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeActionsTxt(lines)

  f = open(pathMiniActions, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeMiniActionsTxt(lines)

  f = open(pathPositions, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodePositionsTxt(lines)

  f = open(pathSortTiles, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeSortTilesTxt(lines)

  f = open(pathAnimations, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeAnimationsTxt(lines)


  array = bosses.encodeRom()
  mystic.romSplitter.burnBank(0x4, 0x0739, array)


def exportHeroProjectiles():
  """ exporta database de las armas y magia que usa el heroe """

#  print('--- 1:1dcd')

  basePath = mystic.address.basePath
  path = basePath + '/projectiles'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  bank = mystic.romSplitter.banks[0x01]

  heroProjs = {}

  weaponAnims = []
  addrWeaponAnims = 0x1dcd
  vaPorAddr = addrWeaponAnims
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  for i in range(0,16):
    weaponAnim = {}
    data = bank[addrWeaponAnims+i]
#    print('data: {:02x} '.format(data) + mystic.variables.armas[i])
    weaponAnim['comment'] = mystic.variables.armas[i].encode('ascii', 'ignore').decode()
    weaponAnim['stageType'] = '{:02x}'.format(data)
    weaponAnims.append(weaponAnim)

  vaPorAddr += 16
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  magicItemsAnims = []
#  addrMagicItemsAnims = 0x1ddd
  addrMagicItemsAnims = vaPorAddr
  for i in range(0,8*8):
    magicItemAnim = {}
    data = bank[addrMagicItemsAnims+i]
    if(i < 8):
      label = mystic.variables.magias[i].encode('ascii', 'ignore').decode()
    else:
      label = mystic.variables.items[i-8].encode('ascii', 'ignore').decode()
#    print('data: {:02x} '.format(data) + label)
    magicItemAnim['comment'] = label
    magicItemAnim['stageType'] = '{:02x}'.format(data)
    magicItemsAnims.append(magicItemAnim)


  vaPorAddr += 8*8
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  tmpTableTypes = []

#  addrTableTypes = 0x1e1d
  addrTableTypes = vaPorAddr
  for j in range(0,6):
#    print('----')
    row = []
    for i in range(0,16):
      addr = bank[16*2*j + addrTableTypes + 2*i+1]*0x100 + bank[16*2*j + addrTableTypes + 2*i]
      strAddr = '{:04x}'.format(addr)
#      print('addr: ' + strAddr )
      row.append(strAddr)
    tmpTableTypes.append(row)

  vaPorAddr += 16*6*2
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  addrFireIncrements = 0x1edd
  addrFireIncrements = vaPorAddr

  fireListAddr = []
  for i in range(0,16):
    addr = bank[addrFireIncrements + 2*i+1]*0x100 + bank[addrFireIncrements + 2*i]
    strAddr = '{:04x}'.format(addr)
    fireListAddr.append(strAddr)
#    print('addr: ' + strAddr )
 
  vaPorAddr += 16*2
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  addrFireList = 0x1efd
  addrFireList = vaPorAddr


  fireList = []
  cant = 0
  while(cant < 16):
    dxdy = 0xffff
#    print('----')
    fireDxdy = {}
    fireDxdy['label'] = 'fire_{:02x}'.format(cant)
    fireDxdy['vaPorAddr'] = '{:02x}'.format(vaPorAddr)
    fireDxdy['incrementsDxdy'] = []
    while(dxdy != 0x0000):


      dx = bank[vaPorAddr + 0]
      dy = bank[vaPorAddr + 1]
      fireDxdy['incrementsDxdy'].append(['{:02x}'.format(dx), '{:02x}'.format(dy)])
      dxdy = dx*0x100+dy

      strDxdy = '{:02x} {:02x}'.format(dx,dy)
#      print('dxdy: ' + strDxdy)
      vaPorAddr += 2

    fireList.append(fireDxdy)
    cant += 1
    

  fireListLabels = []
  for fireAddr in fireListAddr:
    addr = int(fireAddr,16)-0x4000
#    print('fireAddr: {:04x}'.format(addr))

    for fireDxdy in fireList:
      if(addr == int(fireDxdy['vaPorAddr'],16)):
        label = fireDxdy['label']
#        print('label: ' + label)
        fireListLabels.append(label)


#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  projsAddr = 0x20ff
  projsAddr = vaPorAddr
#  print('projsAddr: {:04x}'.format(projsAddr))

  vaPorAddr += 48*(6 + 2*2 + 4*4*2)

#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  sortTilesAddr = 0x28df
  sortTilesAddr = vaPorAddr
#  print('sortTilesAddr: {:04x}'.format(sortTilesAddr))

  vaPorAddr += 16*12

#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  startAddr = 0x299f
  startAddr = vaPorAddr
#  print('startAddr: {:04x}'.format(startAddr))

  behavs = []
  cmds = []
  i = 0
  behav = None
  nroBehav = 0
  behav = None
  nextSound = True
  thrownAxe = False
  turnoHero = True
  while(i < 3226):
    val = bank[startAddr+i]
#    print('val: {:02x}'.format(val))

    if(nextSound):

      if(behav != None):
        behavs.append(behav)
#        print('behav: ' + str(behav))

      nextSound = False
      sound = val
#      print('------ sound: {:02x}'.format(sound))


      behav = {}
      behav['nroBehav'] = '{:02x}'.format(nroBehav)
      behav['comment'] = mystic.variables.hero_projs_behavs[nroBehav]
      behav['vaPorAddr'] = '{:04x}'.format(startAddr+i+2)
      behav['sound'] = '{:02x}'.format(sound)
      behav['cmds'] = []

      nroBehav += 1

    else:

      if(turnoHero and not thrownAxe):
        heroSpriteAction = val
#        print('heroAction: {:02x}'.format(heroSpriteAction))
        behav['cmds'].append('heroAction: {:02x}'.format(heroSpriteAction))

        turnoHero = False

        action = heroSpriteAction % 0x10
        # if thrown axe
        if(action == 0x4):
          thrownAxe = True


          i += 1
          speed = bank[startAddr+i]
#          print('speed: {:02x}'.format(speed))
          behav['cmds'].append('speed: {:02x}'.format(speed))


      # sino, es el turno del proyectil
      else:
        projSprite = val
        turnoHero = True

        if(projSprite != 0x00):
          i += 1
          yy = bank[startAddr+i]

          i += 1
          xx = bank[startAddr+i]
          vaPorAddr = startAddr + i - 2 + 0x4000
#          print('projSprite,yy,xx: {:02x}({:02x},{:02x})   vaPorAddr: {:04x}'.format(projSprite,yy,xx,vaPorAddr))
          behav['cmds'].append('projSprite,yy,xx: {:02x}({:02x},{:02x})'.format(projSprite,yy,xx))
        else:
#          print('projSprite: {:02x}'.format(projSprite))
          behav['cmds'].append('END')
          nextSound = True
          thrownAxe = False


    i += 1

  # agrego el último behaviour
  behavs.append(behav)

  lastAddr = startAddr+i
#  print('lastAddr: {:04x}'.format(lastAddr))


  projs = []
#  projsAddr = 0x20ff
  for i in range(0,48):

    heroProj = {}
    subArray = bank[projsAddr+42*i:projsAddr+42*(i+1)]

    heroProj['nroProjectil'] = '{:02x}'.format(i)
    heroProj['comment'] = mystic.variables.hero_projectiles[i]
    heroProj['vaPorAddr'] = '{:04x}'.format(projsAddr+42*i)

    heroProj['speedSleep'] = '{:02x}'.format(subArray[0])
    heroProj['collisionFlags'] = '{:02x}'.format(subArray[1])
    heroProj['vramSlot'] = '{:02x}'.format(subArray[2])

    heroProj['noseBytes'] = ['{:02x}'.format(nro) for nro in subArray[3:6]]

    offsetBank7 = subArray[7]*0x100 + subArray[6]
#    print('offsetBank7: {:04x}'.format(offsetBank7))
    heroProj['offsetBank7'] = '{:04x}'.format(offsetBank7)

    addrLoco = subArray[9]*0x100 + subArray[8]
#    print('addrLoco: {:04x}'.format(addrLoco))
    heroProj['addrSortTiles'] = '{:04x}'.format(addrLoco)

    addrs = []
    for j in range(0,4):
      addr = subArray[11+j*2]*0x100 + subArray[11+j*2-1]
      comment = '{:04x}'.format(addr)
      for behav in behavs:
        behavAddr = int(behav['vaPorAddr'],16) + 0x4000
        if(behavAddr == addr):
          comment = behav['comment']
      addrs.append(comment)
    # straight attack east,west,north,south
    heroProj['behaviourStraightAttackEastWestNorthSouth'] = addrs

    addrs = []
    for j in range(4,8):
      addr = subArray[11+j*2]*0x100 + subArray[11+j*2-1]
      comment = '{:04x}'.format(addr)
      for behav in behavs:
        behavAddr = int(behav['vaPorAddr'],16) + 0x4000
        if(behavAddr == addr):
          comment = behav['comment']
      addrs.append(comment)
    heroProj['behaviourSlideAttackEastWestNorthSouth'] = addrs

    addrs = []
    for j in range(8,12):
      addr = subArray[11+j*2]*0x100 + subArray[11+j*2-1]
      comment = '{:04x}'.format(addr)
      for behav in behavs:
        behavAddr = int(behav['vaPorAddr'],16) + 0x4000
        if(behavAddr == addr):
          comment = behav['comment']
      addrs.append(comment)
    heroProj['behaviourSpecialStraightAttackEastWestNorthSouth'] = addrs

    addrs = []
    for j in range(12,16):
      addr = subArray[11+j*2]*0x100 + subArray[11+j*2-1]
      comment = '{:04x}'.format(addr)
      for behav in behavs:
        behavAddr = int(behav['vaPorAddr'],16) + 0x4000
        if(behavAddr == addr):
          comment = behav['comment']
      addrs.append(comment)
    heroProj['behaviourSpecialSlidetAttackEastWestNorthSouth'] = addrs

#    print('heroProj: ' + str(heroProj))
    projs.append(heroProj)


#  for i in range(0,0x299f-0x28df):
#    sort = bank[0x28df + i]
#    heroProjsSortTiles.append(sort)

#  sortTilesAddr = 0x28df
  heroProjsSortTiles = []
  for i in range(0,16):
    heroProjsSortTile = []
    for j in range(0,12):
      sort = '{:02x}'.format(bank[sortTilesAddr + i*12+j])
      heroProjsSortTile.append(sort)
    heroProjsSortTiles.append(heroProjsSortTile)


  table_stage_types = []
  for i in range(0,16):
    row = {}
    row['comment'] = mystic.variables.hero_projs_animation_type[i]
    row['nroType'] = '{:01x}'.format(i)
    row['stages'] = []
#    print('------- i: {:02x} '.format(i) + mystic.variables.hero_projs_animation_type[i])
    for j in range(0,6):
      strAddr = tmpTableTypes[j][i]
#      print('strAddr: ' + strAddr)
      addr = int(strAddr,16)-0x4000

      label = 'NULL'
      for proj in projs:
        strProjAddr = proj['vaPorAddr']
#        print('projAddr: ' + strProjAddr)
        projAddr = int(strProjAddr,16)

        if(addr == projAddr):
          label = proj['comment']
#          print('lo encontró: ' + label)        
        
#      row['row'].append(strAddr)
      row['stages'].append(label)
    table_stage_types.append(row)


  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  # agrego info al stats
  mystic.romStats.appendDato(0x01, addrWeaponAnims, lastAddr , (rr, gg, bb), 'hero projectiles databases')


  heroProjs['weaponAnims'] = weaponAnims
  heroProjs['magicItemsAnims'] = magicItemsAnims
  heroProjs['table_stage_types'] = table_stage_types

  heroProjs['fire_list_labels'] = fireListLabels
  heroProjs['fire_list'] = fireList

  heroProjs['projectiles'] = projs
  heroProjs['sortTiles'] = heroProjsSortTiles
  heroProjs['behavs'] = behavs
 
  import json
#  strJson = json.dumps(data, indent=2)
#  strJson = json.dumps(data)
#  print('strPers: \n' + strJson)

#  f = open(filepath, 'w', encoding="utf-8")
#  f.write(strJson)
#  f.close()

  strJson = json.dumps(heroProjs, indent=2)
#  strJson = json.dumps(data)
  f = open(path + '/heroProjs.js', 'w', encoding="utf-8")
  f.write('heroProjs = \n' + strJson)
  f.close()




def burnHeroProjectiles(filepath):
  """ quema los hero-proyectiles en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

#  print('data: ' + data)

  import json
  jsonHeroProjs = json.loads(data)
#  print('jsonHeroProjs: ' + str(jsonHeroProjs))

  array = []

  addrWeaponAnims = 0x1dcd
  vaPorAddr = addrWeaponAnims

#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  arrayWeaponAnims = []
  for weaponAnim in jsonHeroProjs['weaponAnims']:
    stageType = int(weaponAnim['stageType'],16)
    arrayWeaponAnims.append(stageType)

  vaPorAddr += len(arrayWeaponAnims)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  addrMagicItemsAnims = 0x1ddd
  addrMagicItemsAnims = vaPorAddr
 

  magicItemsAnims = []
  for magicItemsAnim in jsonHeroProjs['magicItemsAnims']:
    stageType = int(magicItemsAnim['stageType'],16)
    magicItemsAnims.append(stageType)


  vaPorAddr += len(magicItemsAnims)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  addrProj = 0x1e1d
  addrProj = vaPorAddr

  arrayProj = []
  projectiles = jsonHeroProjs['projectiles']
  for heroProj in projectiles:
#    print('heroProj: ' + str(heroProj))
    speedSleep = int(heroProj['speedSleep'],16)
    arrayProj.append(speedSleep)

    collisionFlags = int(heroProj['collisionFlags'],16)
    arrayProj.append(collisionFlags)
 
    vramSlot = int(heroProj['vramSlot'],16)
    arrayProj.append(vramSlot) 
 
    noseBytes = [int(val,16) for val in heroProj['noseBytes']]
    arrayProj.extend(noseBytes)

    offsetBank7 = int(heroProj['offsetBank7'],16)
#    print('offsetBank7: {:04x}'.format(offsetBank7))
    arrayProj.extend([offsetBank7%0x100, offsetBank7//0x100])

    addrSortTiles = int(heroProj['addrSortTiles'],16)
    arrayProj.extend([addrSortTiles%0x100, addrSortTiles//0x100])

    for strBehav in heroProj['behaviourStraightAttackEastWestNorthSouth']:
#      print('strBehav: ' + strBehav)
      strAddr = None
      for behav in jsonHeroProjs['behavs']:
        if(behav['comment'] == strBehav):
          strAddr = behav['vaPorAddr']
#      print('strAddr: ' + strAddr)
      addr = int(strAddr,16)+0x4000
      arrayProj.extend([addr%0x100, addr//0x100])

    for strBehav in heroProj['behaviourSlideAttackEastWestNorthSouth']:
#      print('strBehav: ' + strBehav)
      strAddr = None
      for behav in jsonHeroProjs['behavs']:
        if(behav['comment'] == strBehav):
          strAddr = behav['vaPorAddr']
      addr = int(strAddr,16)+0x4000
      arrayProj.extend([addr%0x100, addr//0x100])

    for strBehav in heroProj['behaviourSpecialStraightAttackEastWestNorthSouth']:
#      print('strBehav: ' + strBehav)
      strAddr = None
      for behav in jsonHeroProjs['behavs']:
        if(behav['comment'] == strBehav):
          strAddr = behav['vaPorAddr']
      addr = int(strAddr,16)+0x4000
      arrayProj.extend([addr%0x100, addr//0x100])

    for strBehav in heroProj['behaviourSpecialSlidetAttackEastWestNorthSouth']:
#      print('strBehav: ' + strBehav)
      strAddr = None
      for behav in jsonHeroProjs['behavs']:
        if(behav['comment'] == strBehav):
          strAddr = behav['vaPorAddr']
      addr = int(strAddr,16)+0x4000
      arrayProj.extend([addr%0x100, addr//0x100])


  arraySort = []
  sortTiles = jsonHeroProjs['sortTiles']
  for sortTile in sortTiles:
#    print('sortTile: ' + str(sortTile))
    tiles = [int(strTile,16) for strTile in sortTile]
    arraySort.extend(tiles)


  arrayBehavs = []
  behavs = jsonHeroProjs['behavs']
  for behav in behavs:
    sound = int(behav['sound'],16)
#    print('sound: {:02x}'.format(sound))
    arrayBehavs.append(sound)

    for cmd in behav['cmds']:
      if(cmd.startswith('heroAction')):
#        print('heroAction: ' + cmd)
        idx0 = cmd.index(':')
        strHeroAction = cmd[idx0+1:].strip()
        heroAction = int(strHeroAction,16)
        arrayBehavs.append(heroAction)
      elif(cmd.startswith('speed')):
#        print('speed: ' + cmd)
        idx0 = cmd.index(':')
        strSpeed = cmd[idx0+1:].strip()
        speed = int(strSpeed,16)
        arrayBehavs.append(speed)


      elif(cmd.startswith('projSprite')):
#        print('projSprite: ' + cmd)
        idx0 = cmd.index(':')
        strProjSpriteYyXx = cmd[idx0+1:].strip()
#        print('strProjSpriteYyXx:' + strProjSpriteYyXx)
        projSprite = int(strProjSpriteYyXx[0:2],16)
        yy = int(strProjSpriteYyXx[3:5],16)
        xx = int(strProjSpriteYyXx[6:8],16)

        arrayBehavs.extend([projSprite,yy,xx])

      elif(cmd.startswith('END')):
#        print('END')
        arrayBehavs.append(0x00)


  matrixStage = []
  for stageType in jsonHeroProjs['table_stage_types']:
#    print('-----')
    row = []
    for stage in stageType['stages']:
#      print('stage: ' + stage)

      listado = [proj['comment'] for proj in projectiles]
      if(stage in listado):
        idx = listado.index(stage)
        strAddr = projectiles[idx]['vaPorAddr']
#        print('lo encontramos ' + strAddr)
        addr = int(strAddr,16)+0x4000
      else:
        addr = int('0000',16)
      row.append(addr)
    matrixStage.append(row)


  arrayMatrix = []
  for j in range(0,6):
#    print('-----')
    for i in range(0,len(matrixStage)):
      addr = matrixStage[i][j]
#      print('addr: {:04x}'.format(addr))
      addr1 = addr % 0x100
      addr2 = addr // 0x100
      arrayMatrix.extend([addr1,addr2])


#      for k in range(0, len(projectiles)):
#        proj = projectiles[k]
#        if(proj['comment'] == stage):

#          print('lo encontramos tipo: ' + )


  vaPorAddr += len(arrayMatrix)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  addrFireIncrements = 0x1edd
  addrFireIncrements = vaPorAddr

  vaPorAddr += 16*2
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))
#  addrFireList = 0x1efd
  addrFireList = vaPorAddr

  arrayFireIncrement = []
  for fireIncrement in jsonHeroProjs['fire_list']:
    fireIncrement['vaPorAddr'] = '{:04x}'.format(vaPorAddr)
#    print('---- vaPorAddr: {:04x}'.format(vaPorAddr))

    subArray = []
    for inc in fireIncrement['incrementsDxdy']:
      dx = int(inc[0],16)
      dy = int(inc[1],16)
#      print('dxdy: ' + dx + ', ' + dy)
      subArray.extend([dx,dy])

    vaPorAddr += len(subArray)
    arrayFireIncrement.extend(subArray)


  arrayFireAddrs = []
  for fireList in jsonHeroProjs['fire_list_labels']:
#    print('fireList: ' + fireList)

    for fireIncrement in jsonHeroProjs['fire_list']:
      label = fireIncrement['label']
#      print('label: ' + label)
      if(fireList == label):
        strAddr = fireIncrement['vaPorAddr']
#        print('lo encontró: ' + strAddr)
        addr = int(strAddr,16)+0x4000

        addr1 = addr%0x100
        addr2 = addr//0x100

        arrayFireAddrs.extend([addr1,addr2])
        



  # creo el array completo
  array.extend(arrayWeaponAnims)
  array.extend(magicItemsAnims)
  array.extend(arrayMatrix)
  array.extend(arrayFireAddrs)
  array.extend(arrayFireIncrement)
  array.extend(arrayProj)
  array.extend(arraySort)
  array.extend(arrayBehavs)
#  print('array: ' + mystic.util.strHexa(array))
  mystic.romSplitter.burnBank(0x1, 0x1dcd, array)




def exportProjectilesJs():
  """ exporta los proyectiles de los npc """
#  print('--- 9:0479')

  basePath = mystic.address.basePath
  path = basePath + '/projectiles'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  bank = mystic.romSplitter.banks[0x09]
  vaPorAddr = 0x0479
  projsAddr = vaPorAddr

  npcProjs = {}

  npcProjs['projectiles'] = []
  for i in range(0,40):
    subArray = bank[projsAddr + 16*i : projsAddr + 16*(i+1)]
    strHexa = mystic.util.strHexa(subArray)
#    print('addr: {:04x}'.format(projsAddr+16*i))

    proj = {}
    proj['nroProjectil'] = '{:02x}'.format(i)
    proj['comment'] = mystic.variables.projectiles[i]
    proj['collisionFlags'] = '{:02x}'.format(subArray[0])
    proj['speedSleep'] = '{:02x}'.format(subArray[1])
    proj['nose3'] = '{:02x}'.format(subArray[2])
    proj['nose4'] = '{:02x}'.format(subArray[3])
    proj['nose5'] = '{:02x}'.format(subArray[4])
    proj['nose6'] = '{:02x}'.format(subArray[5])
    proj['vramTileOffset'] = '{:02x}'.format(subArray[6])
    proj['cantDosTiles'] = '{:02x}'.format(subArray[7])

    off_1 = subArray[8]
    off_2 = subArray[9]
    offsetBank8 = off_2*0x100 + off_1
    proj['offsetBank8'] = '{:04x}'.format(offsetBank8)

    addr_1 = subArray[10]
    addr_2 = subArray[11]
    addrSortTiles = addr_2*0x100 + addr_1
    proj['addrSortTiles'] = '{:04x}'.format(addrSortTiles)

    addr2_1 = subArray[12]
    addr2_2 = subArray[13]
    addrDosTiles = addr2_2*0x100 + addr2_1
    proj['addrDosTiles'] = '{:04x}'.format(addrDosTiles)

    addr3_1 = subArray[14]
    addr3_2 = subArray[15]
    addr3 = addr3_2*0x100 + addr3_1
    proj['addr3'] = '{:04x}'.format(addr3)

    npcProjs['projectiles'].append(proj)



  length = 16*len(npcProjs['projectiles'])
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x09, projsAddr, projsAddr+length, (rr, gg, bb), 'projectiles')

  vaPorAddr += length

  addressesSortTiles = [int(proj['addrSortTiles'],16) for proj in npcProjs['projectiles']]
#  print('addrs: ' + str(addressesSortTiles))

  projSortTilesAddr = vaPorAddr
#  print('projSortTilesAddr: {:04x}'.format(projSortTilesAddr))

  npcProjs['sortTiles'] = []

  prevAddrSortTile = vaPorAddr
  arrayTiles = []
  nroSortTiles = 0
  primero = True
  dicSortAddr = {}
  for i in range(0,120):

    if(vaPorAddr+0x4000 in addressesSortTiles):
      if(primero):
        primero = False
      else:

        stringTile = ''
        if(vaPorAddr+0x4000 in addressesSortTiles):
          idx = addressesSortTiles.index(prevAddrSortTile+0x4000)
          stringTile = mystic.variables.projectiles[idx] + ' sort-tiles'
        strHexa = mystic.util.strHexa(arrayTiles)
#        print('--- sortTiles: {:04x} '.format(prevAddrSortTile) + stringTile + '\n' + strHexa + '\n')

        sortTiles = {}
        comment = ''
        if(vaPorAddr+0x4000 in addressesSortTiles):
          idx = addressesSortTiles.index(prevAddrSortTile+0x4000)
          comment = mystic.variables.projectiles[idx] + ' sort-tiles'
        sortTiles['nroSortTiles'] = nroSortTiles
        sortTiles['comment'] = comment
        strVaPorAddr = '{:04x}'.format(prevAddrSortTile+0x4000)
        sortTiles['vaPorAddr'] = strVaPorAddr
        dicSortAddr[strVaPorAddr] = nroSortTiles
        sortTiles['tiles'] = ['{:02x}'.format(tile) for tile in arrayTiles]
        npcProjs['sortTiles'].append(sortTiles)
        nroSortTiles += 1

        arrayTiles = []
      prevAddrSortTile = vaPorAddr

    arrayTiles.append(bank[vaPorAddr - 0x4000])
    vaPorAddr += 1

 
  stringTile = ''
  if(vaPorAddr+0x4000 in addressesSortTiles):
    idx = addressesSortTiles.index(prevAddrSortTiles+0x4000)
    stringTile = mystic.variables.bosses[idx] + ' sort-tiles'
  strHexa = mystic.util.strHexa(arrayTiles)
#  print('--- sortTiles: {:04x} '.format(prevAddrSortTile) + stringTile + '\n' + strHexa + '\n')

  sortTiles = {}
  comment = ''
  if(vaPorAddr+0x4000 in addressesSortTiles):
    idx = addressesSortTiles.index(prevAddrSortTile+0x4000)
    comment = mystic.variables.projectiles[idx] + ' sort-tiles'
  sortTiles['nroSortTiles'] = nroSortTiles
  sortTiles['comment'] = comment
  strVaPorAddr = '{:04x}'.format(prevAddrSortTile+0x4000)
  sortTiles['vaPorAddr'] = strVaPorAddr
  dicSortAddr[strVaPorAddr] = nroSortTiles
  sortTiles['tiles'] = ['{:02x}'.format(tile) for tile in arrayTiles]
  npcProjs['sortTiles'].append(sortTiles)
  nroSortTiles += 1


  for proj in npcProjs['projectiles']:

#    print('proj: ' + str(proj))
    nroSortTiles = dicSortAddr[proj['addrSortTiles']]
#    print('nroSortTile: ' + str(nroSortTile))
    proj['nroSortTiles'] = '{:02x}'.format(nroSortTiles)
 

  import json
  strJson = json.dumps(npcProjs, indent=2)
  f = open(path + '/npcProjs_noedit.js', 'w', encoding="utf-8")
  f.write('npcProjs = \n' + strJson)
  f.close()



def exportProjectiles():
  """ exporta las explosiones y cosas que arrojan los enemigos """

#  print('--- 9:0479')

  bank = mystic.romSplitter.banks[0x09]
  projs = mystic.projectiles.Projectiles()
  projs.decodeRom(bank)

  return projs.projectiles


def burnProjectiles(filepath):
  """ quema los proyectiles en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  i = 0
  projectiles = []
  primero = True
  subLines = []
  for line in lines:
#    print('line: ' + line)
    if('------------ projectile' in line):
      if(not primero):
        p = mystic.projectiles.Projectile(i)
        p.decodeTxt(subLines)
        projectiles.append(p)
        i += 1
        subLines = []
      else:
        primero = False

    subLines.append(line)
  p = mystic.projectiles.Projectile(i)
  p.decodeTxt(subLines)
  projectiles.append(p)

  array = []
  for p in projectiles:
#    print('p: ' + str(p)) 
    subArray = p.encodeRom()
    array.extend(subArray)

  mystic.romSplitter.burnBank(0x9, 0x0479, array)

def exportPersonajes():
  """ exporta los personajes """

#  print('--- 3:1f5a')

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  # si el directorio para las imágenes no existía
#  if not os.path.exists(path + '/images_noedit'):
    # lo creo
#    os.makedirs(path + '/images_noedit')

  personajes = mystic.personaje.Personajes()
  # decodifico
  personajes.decodeRom()
  # los codifico en txt
  lines = personajes.encodeTxt()
  # lo grabo
  filepath = path + '/personajes_noedit.txt'
  f = open(filepath, 'w', encoding="utf-8")
  strTxt = '\n'.join(lines)
  f.write(strTxt)
  f.close()

  personajes.exportJs(path + '/personajes.js')

  length = 24*len(personajes.personajes)
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x03, 0x1f5a, 0x1f5a+length, (rr, gg, bb), 'personajes')

  # exporto al personajes_noedit.html
#  personajes.exportHtml()

  return personajes

def burnPersonajesJs(filepath):
  """ quema los personajes en la rom """

  personajes = mystic.personaje.Personajes()
  personajes.importJs(filepath)

  array = personajes.encodeRom()
#    mystic.util.arrayToFile(array, './game/personajes/p.bin')
#    iguales = mystic.util.compareFiles('./game/banks/bank_03/bank_03.bin', './game/personajes/p.bin', 0x1f5a, len(array))
#    print('iguales = ' + str(iguales))

  mystic.romSplitter.burnBank(0x3, 0x1f5a, array)

  return personajes


def burnPersonajes(filepath):
  """ quema los personajes en la rom """

  personajes = mystic.personaje.Personajes()
  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  personajes.decodeTxt(lines)

  array = personajes.encodeRom()
#    mystic.util.arrayToFile(array, './game/personajes/p.bin')
#    iguales = mystic.util.compareFiles('./game/banks/bank_03/bank_03.bin', './game/personajes/p.bin', 0x1f5a, len(array))
#    print('iguales = ' + str(iguales))

  mystic.romSplitter.burnBank(0x3, 0x1f5a, array)

  return personajes
 

def exportGrupos3Personajes():
  """ exporta grupos de 3 personajes a cargar """

  # 3:4456  ld de,$7142
#  print('--- 3:3142')

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  vaPorAddr = 0x3142
  bank = mystic.romSplitter.banks[0x03]
  array = bank[0x3142:]

  grupos = mystic.personaje.GruposPersonajes(0x3142)
  grupos.decodeRom(array)

  lines = grupos.encodeTxt()

  strGrupos = '\n'.join(lines)

  f = open(path + '/grupos3Personajes_noedit.txt', 'w', encoding="utf-8")
  f.write(strGrupos)
  f.close()


def exportGrupos3PersonajesJs():
  """ exporta grupos de 3 personajes a cargar """

  # 3:4456  ld de,$7142
#  print('--- 3:3142')

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  vaPorAddr = 0x3142
  bank = mystic.romSplitter.banks[0x03]
  array = bank[0x3142:]

  grupos = mystic.personaje.GruposPersonajes(0x3142)
  grupos.decodeRom(array)

  grupos.exportJs(path + '/grupos3Personajes.js')


def burnGrupos3PersonajesJs(filepath, personajes):
  """ quema los personajes en la rom """

  grupos = mystic.personaje.GruposPersonajes(0x3142)
  grupos.importJs(filepath)

  array = grupos.encodeRom(personajes)
#    mystic.util.arrayToFile(array, './game/personajes/p.bin')
#    iguales = mystic.util.compareFiles('./game/banks/bank_03/bank_03.bin', './game/personajes/p.bin', 0x1f5a, len(array))
#    print('iguales = ' + str(iguales))

  mystic.romSplitter.burnBank(0x3, 0x3142, array)

  return grupos



def burnGrupos3Personajes(filepath, personajes):
  """ quema los grupos de 3 personajes """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  grupos = mystic.personaje.GruposPersonajes(0x3142)
  grupos.decodeTxt(lines)

  array = grupos.encodeRom(personajes)
  mystic.romSplitter.burnBank(0x3, 0x3142, array)

#  mystic.util.arrayToFile(array, './game/personajes/grupos.bin')
#  iguales = mystic.util.compareFiles('./game/banks/bank_03/bank_03.bin', './game/personajes/grupos.bin', 0x3142, len(array))
#  print('iguales = ' + str(iguales))
   

def exportCosasRarasPersonajes():
  """ exporta cosas raras del banco 3 """

  print('--- 3:3b56')
  bank = mystic.romSplitter.banks[0x03]
  array = bank[0x3b56:]

  line = array[:4]
  strLine = mystic.util.strHexa(line)
  print('header?     : ' + strLine)

  array = array[4:]
  line = array[:16]
  strLine = mystic.util.strHexa(line)
  print('cosasTiles? : ' + strLine)

  array = array[16:]
  line = array[:8]
  strLine = mystic.util.strHexa(line)
  print('masCositas? : ' + strLine)


def exportPersonajesAnimations():
  """ exporta las animaciones doble tiles de los personajes """

#  print('--- 3:3b72')

  bank = mystic.romSplitter.banks[0x03]

  # obtengo la lista de personajes
  personajes = []
  for i in range(0,191):
    subArray = bank[0x1f5a + i*24 : 0x1f5a + (i+1)*24]
    strSubarray = mystic.util.strHexa(subArray)
    pers = mystic.personaje.Personaje(i)
    pers.decodeRom(subArray)
    personajes.append(pers)

  # creo la lista de animaciones
  animations = []
  # recorro los personajes
  for pers in personajes:
    anim = pers.addrDosTiles
    # y agrego su animación a la lista
    animations.append(anim)

  # remuevo duplicados y ordeno
  animAddrs = sorted(set(animations))

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  f = open(path + '/personajesAnimations.txt', 'w', encoding="utf-8")

  animCounter = 1
  tiles = []
  for i in range(0,371):

    addr = 0x3b72+i*3

    if(addr + 0x4000 in animAddrs):
#      print('---animation' + str(animCounter))
      f.write('---animation' + str(animCounter) + '\n')
      animCounter += 1

    subArray = bank[0x3b72 + i*3 : 0x3b72 + (i+1)*3]
    dosTiles = mystic.tileset.DosTiles(addr)
    tiles.append(dosTiles)
    dosTiles.decodeRom(subArray)
#    print('dosTiles: ' + str(dosTiles))
    lines = dosTiles.encodeTxt()
    strDosTiles = '\n'.join(lines)
    f.write(strDosTiles + '\n')

  f.close()

  length = 3*len(tiles)
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x03, 0x3b72, 0x3b72+length, (rr, gg, bb), 'personajes animations dosTiles')



def exportPersonajesAnimationsJs():
  """ exporta las animaciones doble tiles de los personajes """

#  print('--- 3:3b72')

  bank = mystic.romSplitter.banks[0x03]

  # obtengo la lista de personajes
  personajes = []
  for i in range(0,191):
    subArray = bank[0x1f5a + i*24 : 0x1f5a + (i+1)*24]
    strSubarray = mystic.util.strHexa(subArray)
    pers = mystic.personaje.Personaje(i)
    pers.decodeRom(subArray)
    personajes.append(pers)

  # creo la lista de animaciones
  animations = []
  # recorro los personajes
  for pers in personajes:
    anim = pers.addrDosTiles
    # y agrego su animación a la lista
    animations.append(anim)

  # remuevo duplicados y ordeno
  animAddrs = sorted(set(animations))

  basePath = mystic.address.basePath
  path = basePath + '/personajes'


  data = []
  animCounter = 1
  tiles = []
  for i in range(0,371):

    addr = 0x3b72+i*3

    if(addr + 0x4000 in animAddrs):
#      print('---animation' + str(animCounter))
      animCounter += 1

    subArray = bank[0x3b72 + i*3 : 0x3b72 + (i+1)*3]
    dosTiles = mystic.tileset.DosTiles(addr)
    dosTiles.decodeRom(subArray)
#    print('dosTiles: ' + str(dosTiles))
    tiles.append(dosTiles)

    data.append({'attr': '{:02x}'.format(dosTiles.attr), 'tile1' : '{:02x}'.format(dosTiles.tile1), 'tile2' : '{:02x}'.format(dosTiles.tile2)})


  length = 3*len(tiles)
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x03, 0x3b72, 0x3b72+length, (rr, gg, bb), 'personajes animations dosTiles')


  import json
#  strJson = json.dumps(data, indent=2)
#  strJson = json.dumps(data)
#  print('strPers: \n' + strJson)

#  f = open(filepath, 'w', encoding="utf-8")
#  f.write(strJson)
#  f.close()

  strJson = json.dumps(data, indent=2)
#  strJson = json.dumps(data)
  f = open(path + '/personajeAnims.js', 'w', encoding="utf-8")
  f.write('personajeAnims = \n' + strJson)
  f.close()


def burnPersonajesAnimations(filepath):
  """ quema las animaciones doble tiles de los personajes en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  addr = 0x3b72
  tiles = []
  for line in lines:
#    print('line: ' + line)
    if('(attr,tile1,tile2)' in line):
       dosTiles = mystic.tileset.DosTiles(addr)
       addr += 3
       dosTiles.decodeTxt([line])
       tiles.append(dosTiles)

  array = []
  for dosTiles in tiles:
#    print('dosTiles: ' + str(dosTiles)) 
    subArray = dosTiles.encodeRom()
    array.extend(subArray)

  mystic.romSplitter.burnBank(0x3, 0x3b72, array)

      
def exportGolpes():
  """ exporta base de cuanto lastima golpes dados/recibidos ? """

  print('--- 4:0931')
  bank = mystic.romSplitter.banks[0x04]
  array = bank[0x0931:]

  for i in range(0,152):

    line = array[:8]

    strLine = mystic.util.strHexa(line)
    print('strGolpes: ' + strLine)

    array = array[8:]


def exportMonstruoGrandeDosTiles():
  """ exporta los doble tiles de los boss """

#  print('--- 4:3ba7')

  bank = mystic.romSplitter.banks[0x04]
  array = bank[0x3ba7:]

  for i in range(0,326):

    line = array[:3]

    modo = line[0]   # 10 = normal, 30 = espejo, ??? (attribute)
    left = line[1]   # 0:8000 + left                 (tile number)
    right = line[2]  # 0:8000 + right                (tile number)

    print('(modo, left, right) = ({:02x}, {:02x}, {:02x})'.format(modo,left,right))
    strLine = mystic.util.strHexa(line)
#    print('strLinePers: ' + strLine)

    array = array[3:]


def exportSongs(exportLilypond=False):
  """ exporta las canciones """

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank,addrMusic = mystic.address.addrMusic
  # cargo el banco 16 con las canciones
  bank = mystic.romSplitter.banks[nroBank]

  canciones = mystic.music.Canciones()
  canciones.decodeRom(bank,addrMusic)

  lines = canciones.encodeTxt()
  strCanciones = '\n'.join(lines)
  f = open(path + '/songs.txt', 'w', encoding="utf-8")
  f.write(strCanciones)
  f.close()

  for i in range(0,30):
    cancion = canciones.canciones[i]

    lines = cancion.encodeTxt()
    strCancion = '\n'.join(lines)
    f = open(path + '/song_{:02}.txt'.format(i), 'w', encoding="utf-8")
    f.write(strCancion)
    f.close()

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    addr = cancion.melody2.addr
    length = len(cancion.melody2.encodeRom())
    # agrego info al stats
    mystic.romStats.appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')

    addr = cancion.melody1.addr
    length = len(cancion.melody1.encodeRom())
    # agrego info al stats
    mystic.romStats.appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')

    addr = cancion.melody3.addr
    length = len(cancion.melody3.encodeRom())
    # agrego info al stats
    mystic.romStats.appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')

    # si quiere que compile lilypond
    if(exportLilypond):
      # exporto lilypond!
      cancion.exportLilypond()

def burnSongs(filepath):
  """ burn the songs into the rom """

  canciones = mystic.music.Canciones()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  canciones.decodeTxt(lines)


  # address of the pointer table
  nroBank,addrMusic = mystic.address.addrMusic
  arrayMusic = canciones.encodeRom(addrMusic)

  mystic.romSplitter.burnBank(0xf, addrMusic, arrayMusic)


def burnSongsOld(filepath, ignoreAddrs=False, exportLilypond=False):
  """ quema las canciones en el banco 0f real.  Si ignoreAddrs=True calcula addrs nuevas concatenando channels """

  canciones = mystic.music.Canciones()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  canciones.decodeTxt(lines)

#  vaPorAddr = canciones.canciones[0].addrCh2
  # empezamos por la dirección donde debe comenzar el primer canal de la primera canción
  vaPorAddr = 0x4ac9

#  cancion = canciones.canciones[1]
#  melody2Rom = cancion.melody2.encodeRom()
#  print('melody2Rom: ' + mystic.util.strHexa(melody2Rom))

  for cancion in canciones.canciones:
#    print('cancy: ' + str(cancion))

    melody2Rom = cancion.melody2.encodeRom()
    melody1Rom = cancion.melody1.encodeRom()
    melody3Rom = cancion.melody3.encodeRom()

    # si no ignoramos los addrs
    if(not ignoreAddrs):
        
      # quemo el puntero al addr del channel 2
      punteroAddr = 0x0a12 + 6*cancion.nro + 0
      strHexAddr = '{:02x} {:02x}'.format(cancion.addrCh2%0x100, cancion.addrCh2//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # y quemo el channel 2
      mystic.romSplitter.burnBank(0xf, cancion.addrCh2 - 0x4000, melody2Rom)

      # quemo el puntero al addr del channel 1
      punteroAddr = 0x0a12 + 6*cancion.nro + 2
      strHexAddr = '{:02x} {:02x}'.format(cancion.addrCh1%0x100, cancion.addrCh1//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # y quemo el channel 1
      mystic.romSplitter.burnBank(0xf, cancion.addrCh1 - 0x4000, melody1Rom)

      # quemo el puntero al addr del channel 3
      punteroAddr = 0x0a12 + 6*cancion.nro + 4
      strHexAddr = '{:02x} {:02x}'.format(cancion.addrCh3%0x100, cancion.addrCh3//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # y quemo el channel 3
      mystic.romSplitter.burnBank(0xf, cancion.addrCh3 - 0x4000, melody3Rom)

    else:

      # quemo el puntero al addr del channel 2
      punteroAddr = 0x0a12 + 6*cancion.nro + 0
      strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # recodifico la melody con su nuevo addr
      cancion.melody2.addr = vaPorAddr
      cancion.melody2.refreshLabels()
      melody2Rom = cancion.melody2.encodeRom()
      # y quemo el channel 2
      mystic.romSplitter.burnBank(0xf, vaPorAddr - 0x4000, melody2Rom)
      vaPorAddr += len(melody2Rom)#+0x10

      # quemo el puntero al addr del channel 1
      punteroAddr = 0x0a12 + 6*cancion.nro + 2
      strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # recodifico la melody con su nuevo addr
      cancion.melody1.addr = vaPorAddr
      cancion.melody1.refreshLabels()
      melody1Rom = cancion.melody1.encodeRom()
      # y quemo el channel 1
      mystic.romSplitter.burnBank(0xf, vaPorAddr - 0x4000, melody1Rom)
      vaPorAddr += len(melody1Rom)#+0x10

      # quemo el puntero al addr del channel 3
      punteroAddr = 0x0a12 + 6*cancion.nro + 4
      strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # recodifico la melody con su nuevo addr
      cancion.melody3.addr = vaPorAddr
      cancion.melody3.refreshLabels()
      melody3Rom = cancion.melody3.encodeRom()
      # y quemo el channel 3
      mystic.romSplitter.burnBank(0xf, vaPorAddr - 0x4000, melody3Rom)
      vaPorAddr += len(melody3Rom)#+0x10

    # si quiere que compile lilypond
    if(exportLilypond):
      # exporto lilypond!
      cancion.exportLilypond()



def burnSongsHeaders(filepath, exportLilypond=False):
  """ quema las canciones en el banco 0f real.  Agrega los headers misteriosos """

  canciones = mystic.music.Canciones()

  # el array con las canciones a quemar
  array = []

  # los tipos de headers misteriosos
  header1 = [0xe7, 0x14]
  header2 = []
  header3 = [0xD0, 0x63, 0xA3, 0x64, 0x67, 0x66]
  header4 = [0x19, 0x68, 0xBD, 0x68, 0xFF, 0x69]
  header5 = [0x57, 0x6B, 0x83, 0x6C, 0xA9, 0x6D]
  header6 = [0x8A, 0x6E, 0x5E, 0x6F, 0x31, 0x70]
  header7 = [0x70, 0x70, 0x9F, 0x70, 0xF9, 0x70]
  header8 = [0x18, 0x71, 0xAA, 0x71, 0x63, 0x72]
  header9 = [0x49, 0x73, 0x1C, 0x74, 0x6F, 0x75]
  header10 = [0xD3, 0x76, 0x1C, 0x77, 0x62, 0x77]
  header11 = [0xA8, 0x77, 0x11, 0x78, 0xA3, 0x78]
  header12 = [0xFA, 0x78, 0x24, 0x79, 0x48, 0x79]
  header13 = [0x6B, 0x79, 0x84, 0x79, 0x9A, 0x79]
  header14 = [0xB6, 0x79, 0xEA, 0x79, 0x1D, 0x7A]

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  canciones.decodeTxt(lines)

  vaPorAddr = canciones.canciones[0].addrCh2

  for i in range(0,30):
#    print('cancy: ' + str(cancion))

    localNro = i
    if(localNro == 16):
      localNro = 17
    elif(localNro == 17):
      localNro = 16

    if(i <= 12):
      array.extend(header1)
      pass
    elif(i == 13):
      array.extend(header2)
      pass
    elif(i == 14):
      array.extend(header1)
    elif(i >= 15 and i <= 17):
      array.extend(header2)
      pass
    elif(i == 18):
      array.extend(header3)
      pass
    elif(i == 19):
      array.extend(header4)
      pass
    elif(i == 20):
      array.extend(header5)
      pass
    elif(i == 21):
      array.extend(header6)
      pass
    elif(i == 22):
      array.extend(header7)
      pass
    elif(i == 23):
      array.extend(header8)
      pass
    elif(i == 24):
      array.extend(header9)
      pass
    elif(i == 25):
      array.extend(header10)
      pass
    elif(i == 26):
      array.extend(header11)
      pass
    elif(i == 27):
      array.extend(header12)
      pass
    elif(i == 28):
      array.extend(header13)
      pass
    elif(i == 29):
      array.extend(header14)
      pass

    cancion = canciones.canciones[localNro]
    melody2Rom = cancion.melody2.encodeRom()
    melody1Rom = cancion.melody1.encodeRom()
    melody3Rom = cancion.melody3.encodeRom()



    if(True):
      # quemo el puntero al addr del channel 2
      punteroAddr = 0x0a12 + 6*cancion.nro + 0
      strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
#      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # y quemo el channel 2
      mystic.romSplitter.burnBank(0xf, vaPorAddr - 0x4000, melody2Rom)
      array.extend(melody2Rom)
      vaPorAddr += len(melody2Rom)
       
      # quemo el puntero al addr del channel 1
      punteroAddr = 0x0a12 + 6*cancion.nro + 2
      strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
#      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # y quemo el channel 1
      mystic.romSplitter.burnBank(0xf, vaPorAddr - 0x4000, melody1Rom)
      array.extend(melody1Rom)
      vaPorAddr += len(melody1Rom)

      # quemo el puntero al addr del channel 3
      punteroAddr = 0x0a12 + 6*cancion.nro + 4
      strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
      addrArray = mystic.util.hexaStr(strHexAddr)
#      mystic.romSplitter.burnBank(0xf, punteroAddr, addrArray)
      # y quemo el channel 3
      mystic.romSplitter.burnBank(0xf, vaPorAddr - 0x4000, melody3Rom)
      array.extend(melody3Rom)
      vaPorAddr += len(melody3Rom)

    # si quiere que compile lilypond
    if(exportLilypond):
      # exporto lilypond!
      cancion.exportLilypond()

#  print(mystic.util.strHexa(array))
#  print('len: ' + str(len(array)))

  mystic.romSplitter.burnBank(0xf, 0x4AC7 - 0x4000, array)


def exportSpriteSheetHero():
  """ exporta sprite sheet del heroe """

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetHero'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  bank01 = mystic.romSplitter.banks[0x01]
  # los tiles se unen en spritesheets según esta tabla en 1:075e
  bankHeroSprites, addrHeroSprites = 1, 0x075e

  cantidad = 22 
  heroSpritesTable = []
  for i in range(0,cantidad):
    renglon = []
    for j in range(0,16):
      nroTile = bank01[addrHeroSprites + 16*i + j]
#      print('{:02x}, '.format(nroTile), end='')
      renglon.append('{:02x}'.format(nroTile))
#    print('')
    heroSpritesTable.append(renglon)

  import json
  # exporto a json
  strJson = json.dumps(heroSpritesTable, indent=2)
#  strJson = json.dumps(data)
  f = open(path + '/heroSpritesTable.js', 'w', encoding="utf-8")
  f.write('heroSpritesTable = \n' + strJson)
  f.close()


  # construimos el hero_noedit.png
  bank08 = mystic.romSplitter.banks[0x08]
  # los tiles del hero comienzan en 8:1a40
  bankHeroTiles, addrHeroTiles = 8, 0x1a40

  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  # agrego info al stats
#  mystic.romStats.appendDato(0x08, addrHeroTiles, 0x4000, (rr, gg, bb), 'tiles del hero')

  tiles = []
  for i in range(0,204):
    data = bank08[addrHeroTiles + i*0x10:addrHeroTiles + (i+1)*0x10]
    tile = mystic.tileset.Tile()
    tile.decodeRom(data)
    tiles.append(tile)

  extraTiles = []
  for i in range(0,cantidad):

#    for j in range(0,8):
#      nroTile = bank01[addrHeroSprites + 16*i+2*j]
#      tile = tiles[nroTile]
#      extraTiles.append(tile)

#    for j in range(0,8):
#      nroTile = bank01[addrHeroSprites + 16*i+2*j+1]
#      tile = tiles[nroTile]
#      extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+2]
    tile2 = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    tile2b = mystic.tileset.Tile()
    tile2b.tileData = tile2.tileData
    tile2b.flipX()
    tile2 = tile2b
    extraTiles.append(tile2)

    nroTile = bank01[addrHeroSprites + 16*i+0]
    tile0 = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    tile0b = mystic.tileset.Tile()
    tile0b.tileData = tile0.tileData
    tile0b.flipX()
    tile0 = tile0b
    extraTiles.append(tile0)

    nroTile = bank01[addrHeroSprites + 16*i+4]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+6]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+8]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+10]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+12]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+14]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+3]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    tile2 = mystic.tileset.Tile()
    tile2.tileData = tile.tileData
    tile2.flipX()
    extraTiles.append(tile2)

    nroTile = bank01[addrHeroSprites + 16*i+1]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    tile2 = mystic.tileset.Tile()
    tile2.tileData = tile.tileData
    tile2.flipX()
    extraTiles.append(tile2)

    nroTile = bank01[addrHeroSprites + 16*i+5]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+7]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+9]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+11]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+13]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

    nroTile = bank01[addrHeroSprites + 16*i+15]
    tile = tiles[nroTile] if nroTile != 0xff else mystic.tileset.Tile()
    extraTiles.append(tile)

  tileset = mystic.tileset.Tileset(8,2*cantidad)
#  tileset = mystic.tileset.Tileset(2,48)
#  tileset.tiles = [tile0, tile1, tile2, tile3]
#  tileset.tiles = tiles
  tileset.tiles = extraTiles
  tileset.exportPngFile(path + '/hero_noedit.png')


def burnSpriteSheetHero():

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetHero'

  filepath = path + '/heroSpritesTable.js'

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

#  print('data: ' + data)


  import json
  jsonHero = json.loads(data)

#  print('jsonHero: ' + str(jsonHero))

  array = []
  for renglon in jsonHero:
#    print('renglon: ' + str(renglon))
    subArray = [int(val,16) for val in renglon]
    array.extend(subArray)


#  for stats in personajeStatuses:
#    subArray = stats.encodeRom()
#    array.extend(subArray)

  # los tiles se unen en spritesheets según esta tabla en 1:075e
  bankHeroSprites, addrHeroSprites = 1, 0x075e
  mystic.romSplitter.burnBank(bankHeroSprites, addrHeroSprites, array)



def exportSpriteSheetMonster():
  """ exporta sprite sheet de los monstruos """

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetMonster'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  bank0b = mystic.romSplitter.banks[0x0b]

  tiles = []
  for i in range(0,16*2):
    data = bank0b[0x3e00 + i*0x10:0x3e00 + (i+1)*0x10]
    tile = mystic.tileset.Tile()
    tile.decodeRom(data)
    tiles.append(tile)

#  for i in range(0,16):
#    extraTiles.append(tiles[i])


  extraTiles = []
  for j in range(0,2):
    extraTiles.append(tiles[0 + 16*j])
    extraTiles.append(tiles[1 + 16*j])
    extraTiles.append(tiles[8 + 16*j])
    extraTiles.append(tiles[9 + 16*j])

    extraTiles.append(tiles[2 + 16*j])
    extraTiles.append(tiles[3 + 16*j])
    extraTiles.append(tiles[10 + 16*j])
    extraTiles.append(tiles[11 + 16*j])

    extraTiles.append(tiles[4 + 16*j])
    extraTiles.append(tiles[5 + 16*j])
    extraTiles.append(tiles[12 + 16*j])
    extraTiles.append(tiles[13 + 16*j])

    extraTiles.append(tiles[6 + 16*j])
    extraTiles.append(tiles[7 + 16*j])
    extraTiles.append(tiles[14 + 16*j])
    extraTiles.append(tiles[15 + 16*j])

  tileset = mystic.tileset.Tileset(4,8)
#  tileset = mystic.tileset.Tileset(2,48)
#  tileset.tiles = [tile0, tile1, tile2, tile3]
#  tileset.tiles = tiles
  tileset.tiles = extraTiles
  tileset.exportPngFile(path + '/monster_10.png')

  bank04 = mystic.romSplitter.banks[0x04]
  # tabla de los 21 monstruos grandes
  for i in range(0,21):
    # 24 bytes por monstruo
    array = bank04[0x0739 + 24*i:0x0739 + 24*(i+1)]

#    print('{:02} | '.format(i) + mystic.util.strHexa(array))


  bank = mystic.romSplitter.banks[0x04]
  bosses = mystic.bosses.Bosses()
  bosses.decodeRom(bank)

  boss = bosses.bosses[0x10]
  print('boss: ' + str(boss))

  print('offset: {:04x}'.format(boss.offsetBank8))
  offset = 8*0x4000 + boss.offsetBank8
  print('offset2: {:04x}'.format(offset))

  nroBank = offset//0x4000
  off = offset%0x4000

  # cada tile ocupa 0x10 bytes
  byteSize = 0x10*2*boss.cantDosTiles

  print('bank {:04x} off {:04x} fin {:04x}'.format(nroBank, off, off + byteSize))

  bank = mystic.romSplitter.banks[nroBank]

  # creo el tileset
  tileset = mystic.tileset.Tileset(0x10,2*boss.cantDosTiles//0x10)

#  array = bank[offset:offset + 0x200]
  array = bank[off: off + byteSize]

  tileset.decodeRom(array)

  tileset.exportPngFile(path + '/monster_10_tiles.png')

  print('addr sort {:04x}'.format(boss.addrSortTiles)) 
#  for sortTiles in bosses.bossesSortTiles:
#    strHexa = mystic.util.strHexa(sortTiles)
#    print('hexa: ' + strHexa)
  sortTiles = bosses.bossesSortTiles[2]
  strHexa = mystic.util.strHexa(sortTiles)


  vramTiles = []
  for i in range(0, 0x10*8):
    tile = mystic.tileset.Tile()
    vramTiles.append(tile)

  for i in range(0, 2*boss.cantDosTiles):
    sort = sortTiles[i]

#    print('off+sort*0x10 {:04x}'.format(off+sort*0x10))

    data = bank[off + sort*0x10:off + (sort+1)*0x10]
    tile = mystic.tileset.Tile()
    tile.decodeRom(data)
    vramTiles[boss.vramTileOffset+i] = tile


#  tileset = mystic.tileset.Tileset(0x10,2*boss.cantDosTiles//0x10)
#  tileset = mystic.tileset.Tileset(2,48)
#  tileset.tiles = [tile0, tile1, tile2, tile3]
#  tileset.tiles = tiles
#  tileset.exportPngFile(path + '/monster_10_sorted.png')

  vramTileset = mystic.tileset.Tileset(0x10, 8)
  vramTileset.tiles = vramTiles
  vramTileset.exportPngFile(path + '/monster_10_vram.png')



  dosTiles = bosses.dosTiles[4]
#  print('dosTiles: ' + str(dosTiles))

  catSprites = []
  i = 0
  for dosTile in dosTiles: 
    print('dosTile: ' + str(dosTile))

    tiles = []
    # si hay que reflejar la imagen X-flip
    if(dosTile.attr == 0x30):
      vramTileset.tiles[dosTile.tile1].flipX()
      vramTileset.tiles[dosTile.tile2].flipX()
      vramTileset.tiles[dosTile.tile1+1].flipX()
      vramTileset.tiles[dosTile.tile2+1].flipX()

    tiles.append(vramTileset.tiles[dosTile.tile1])
    tiles.append(vramTileset.tiles[dosTile.tile2])
    tiles.append(vramTileset.tiles[dosTile.tile1+1])
    tiles.append(vramTileset.tiles[dosTile.tile2+1])

    tileset = mystic.tileset.Tileset(2,2)
    tileset.tiles = tiles
#    tileset.exportPngFile(path + '/monster_sprite_{:02}.png'.format(i))
    catSprites.append(tileset)

    i += 1

  screenSprites = []
  for j in range(0,8):
    row = []
    for i in range(0,10):
      tileset = mystic.tileset.Tileset(2,2)
      tile = mystic.tileset.Tile()
#      tile.tileData = [0x02]*16
      tileset.tiles.append(tile)
      tileset.tiles.append(tile)
      tileset.tiles.append(tile)
      tileset.tiles.append(tile)
#      tileset.tiles.append(mystic.tileset.Tile())
#      tileset.tiles.append(mystic.tileset.Tile())
#      tileset.tiles.append(mystic.tileset.Tile())

      row.append(tileset)
    screenSprites.append(row)


  # head
  sprite = catSprites[0x0a]
  sprite.exportPngFile(path + '/monster_sprite_0a.png')
  screenSprites[2][2] = sprite
  # body
  sprite = catSprites[0x08]
  sprite.exportPngFile(path + '/monster_sprite_08.png')
  screenSprites[1][1] = sprite

  sprite = catSprites[0x0b]
  sprite.exportPngFile(path + '/monster_sprite_0b.png')
  screenSprites[1][2] = sprite

  sprite = catSprites[0x09]
  sprite.exportPngFile(path + '/monster_sprite_09.png')
  screenSprites[2][1] = sprite

  tileset = mystic.tileset.Tileset(10*2,8*2)

  data = [mystic.tileset.Tile()]*10*8*4
  for j in range(0,8):
    for i in range(0,10):

      tile0 = screenSprites[j][i].tiles[0]
      tile1 = screenSprites[j][i].tiles[1]
      tile2 = screenSprites[j][i].tiles[2]
      tile3 = screenSprites[j][i].tiles[3]

      data[2*(2*j*10)+2*(0*10)+2*i+0] = tile0
      data[2*(2*j*10)+2*(0*10)+2*i+1] = tile1
      data[2*(2*j*10)+2*(1*10)+2*i+0] = tile2
      data[2*(2*j*10)+2*(1*10)+2*i+1] = tile3





  print('len data: ' + str(len(data)))
  tileset.tiles = data
  tileset.exportPngFile(path + '/monster_loco.png')
  
    

def exportSpriteSheetPersonajes():
  """ exporta los spriteSheet de personajes """

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetPersonajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  for banco in range(0,0x10):
    for nro in range(0,4):

      bank = mystic.romSplitter.banks[banco]
      array = bank[0x1000*nro:0x1000*(nro+1)]

      w, h = 8,8
#      w, h = 4,16
      sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)

      sheetPers.decodeRom(array)
      sheetData = sheetPers.encodePng()

      filepath = basePath + '/banks/bank_{:02}/sheetPers_{:02}_{:02}.png'.format(banco, banco, nro)
      # lo exporto a png
      mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

  i = 1
  banco = 8
  bank = mystic.romSplitter.banks[banco]
  array = bank[0x1a00:0x2000]
  w, h = 8,3
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  sheetPers.decodeRom(array)
  sheetData = sheetPers.encodePng()
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

  i = 2
  banco = 8
  bank = mystic.romSplitter.banks[banco]
  array = bank[0x2000:0x3000]
  w, h = 4,7
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  sheetPers.decodeRom(array)
  sheetData = sheetPers.encodePng()
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

  i = 3
  banco = 8
  bank = mystic.romSplitter.banks[banco]
  array = bank[0x3000:0x4000]
  w, h = 8,8
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  sheetPers.decodeRom(array)
  sheetData = sheetPers.encodePng()
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

  bancoAddrPosta = [                 (0x09, 0x1000), (0x09, 0x2000), (0x09,0x3000),
                     (0x0a, 0x0000), (0x0a, 0x1000), (0x0a, 0x2000), (0x0a,0x3000) ]

  i = 5
  # para cada spriteSheetPersonaje posta
  for banco, addr in bancoAddrPosta:

    bank = mystic.romSplitter.banks[banco]
    array = bank[addr:]
    w, h = 8,8
#    w, h = 4,16
    sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
    sheetPers.decodeRom(array)
    sheetData = sheetPers.encodePng()
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    # agrego info al stats
    mystic.romStats.appendDato(banco, addr, addr + 0x1000, (rr, gg, bb), 'un spriteSheetPersonaje')

    i += 1

def burnSpriteSheetPersonajes():

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetPersonajes'

  i = 1
  banco = 8
  addr = 0x1a00
  w, h = 8,3
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  array = mystic.util.pngToArray(filepath)
  sheetPers.decodePng(array)
  array = sheetPers.encodeRom()
  mystic.romSplitter.burnBank(banco, addr, array)

  i = 2
  banco = 8
  addr = 0x2000
  w, h = 4,7
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  array = mystic.util.pngToArray(filepath)
  sheetPers.decodePng(array)
  array = sheetPers.encodeRom()
  mystic.romSplitter.burnBank(banco, addr, array)

  i = 3
  banco = 8
  addr = 0x3000
  w, h = 8,8
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  array = mystic.util.pngToArray(filepath)
  sheetPers.decodePng(array)
  array = sheetPers.encodeRom()
  mystic.romSplitter.burnBank(banco, addr, array)


  bancoAddrPosta = [                 (0x09, 0x1000), (0x09, 0x2000), (0x09,0x3000),
                     (0x0a, 0x0000), (0x0a, 0x1000), (0x0a, 0x2000), (0x0a,0x3000) ]

  i = 5
  # para cada spriteSheetPersonaje posta
  for banco, addr in bancoAddrPosta:

    bank = mystic.romSplitter.banks[banco]
    array = bank[addr:]
    w, h = 8,8
#    w, h = 4,16
    sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    array = mystic.util.pngToArray(filepath)
    sheetPers.decodePng(array)
    array = sheetPers.encodeRom()
    mystic.romSplitter.burnBank(banco, addr, array)

    i += 1


def exportMapas(exportPngFile):
  """ genera los mapa-wrappers """

  basePath = mystic.address.basePath
  path = basePath + '/mapas'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  mapas = mystic.maps.Mapas()
  # decodifico
  mapas.decodeRom()
  # los codifico en txt
  lines = mapas.encodeTxt()
  # lo grabo
  filepath = path + '/mapas_noedit.txt'
  f = open(filepath, 'w', encoding="utf-8")
  strTxt = '\n'.join(lines)
  f.write(strTxt)
  f.close()

#  mapa = mapas.mapas[0]
#  if(True):
  # para cada mapa
  for mapa in mapas.mapas:

    print('mapa: {:02x}'.format(mapa.nroMapa))

    # lo exporto a .txt
    lines = mapa.encodeTxt()
    strMapa = '\n'.join(lines)
    f = open(path + '/mapa_{:02}_{:02x}_noedit.txt'.format(mapa.nroMapa, mapa.nroMapa), 'w', encoding="utf-8")
    f.write(strMapa + '\n')
    f.close()

    # exporto a formato .tmx para Tiled
    mapa.exportTiledXml(path + '/mapa_{:02}_{:02x}.tmx'.format(mapa.nroMapa, mapa.nroMapa))

    # exporto a formato .json
    mapa.exportJs(path + '/mapa_{:02}_{:02x}.js'.format(mapa.nroMapa, mapa.nroMapa))

    if(exportPngFile):
      mapa.exportPngFile(path + '/mapa_{:02}_{:02x}_noedit.png'.format(mapa.nroMapa, mapa.nroMapa))

    # verifico volviendo a encodearlo
    subArray = mapa.encodeRom(mapa.mapAddr)

#    filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#    mystic.util.arrayToFile(subArray, filepath)
#    iguales = mystic.util.compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#    print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    length = len(subArray)
    # agrego info al stats
    mystic.romStats.appendDato(mapa.mapBank, mapa.mapAddr, mapa.mapAddr+length, (rr, gg, bb), 'un mapa')


def burnMapas(filepath):

  basePath = mystic.address.basePath
  path = basePath + '/mapas'

  mapas = mystic.maps.Mapas()
  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  mapas.decodeTxt(lines)


  # donde va el addr en cada uno de los bancos de mapas (5,6,7)
#  vaPorBank = 0x05
#  vaPorAddr = 0x0000
  vaPorBank, vaPorAddr = mystic.address.addrMaps
#  print('vaPorBank: {:02x} vaPorAddr: {:04x}'.format(vaPorBank, vaPorAddr))

  sortMapas = [0,9, 1,15,14,10,8, 3,2,13,4,5,11,12,6,7]

  # por cada mapa
  for i in range(0,0x10):

    sortedNro = sortMapas[i]
    # lo agarro en el orden a quemar en la rom
    mapa = mapas.mapas[sortedNro]

#    print('mapa: ' + str(mapa))
#    mapa.exportPngFile('./game/mapas/mapa_{:02x}.png'.format(mapa.nroMapa))

    # lo codifico para calcular el tamaño que ocupa
    subArray = mapa.encodeRom(mapa.mapAddr)

#    filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#    mystic.util.arrayToFile(subArray, filepath)
#    iguales = mystic.util.compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#    print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

    if(vaPorAddr + len(subArray) >= 0x4000):
      vaPorBank += 1
      vaPorAddr = 0x0000

    # actualizo el addr !!
    mapa.mapBank = vaPorBank
    mapa.mapAddr = vaPorAddr
    # vuelvo a encodearlo para ajustar los punteros addr de los bloques !!
    subArray = mapa.encodeRom(mapa.mapAddr)
    # lo quemo en la rom
    mystic.romSplitter.burnBank(mapa.mapBank, mapa.mapAddr, subArray)

#    print('i: {:02x} vaPorAddr: {:02x}:{:04x} mapAddr: {:02x}:{:04x}'.format(sortedNro, vaPorBank, vaPorAddr, mapa.mapBank, mapa.mapAddr))

    vaPorAddr += len(subArray)

#    print('quedó en: {:04x}'.format(vaPorAddr))



  array = []
  # para cada mapa
  for nroMapa in range(0,0x10):

    mapa = mapas.mapas[nroMapa]
    subArray = []
    subArray.append(0x00) 
    subArray.append(mapa.nroSpriteSheet*0x10)
    subArray.append(mapa.nose)
    subArray.extend([mapa.spriteAddr%0x100,mapa.spriteAddr//0x100])
    subArray.append(mapa.cantSprites)
    subArray.append(mapa.mapBank)
    subArray.extend([(mapa.mapAddr+0x4000)%0x100,(mapa.mapAddr+0x4000)//0x100])
    subArray.extend([mapa.noseAddr%0x100,mapa.noseAddr//0x100])

#    print('mapa: ' + str(mapa.nroMapa))
#    strHex = mystic.util.strHexa(subArray)
#    print('strHex: ' + strHex + '\n')

    array.extend(subArray)

  mystic.romSplitter.burnBank(0x08, 0x0000, array)


def burnMapasJs():
  """ quema los mapas usando los .json """

  basePath = mystic.address.basePath
  path = basePath + '/mapas'

  mapas = mystic.maps.Mapas()

  # por cada mapa
#  for i in range(0,1):
  for i in range(0,0x10):

    filepath = path + '/mapa_{:02}_{:02x}.js'.format(i,i)
#    print('burn mapa json: ' + filepath)

    f = open(filepath, 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()
    # elimino el primer renglón (no es json)
    lines.pop(0)
    data = '\n'.join(lines)

    import json
    jsonMapa = json.loads(data)


    nroMapa = int(jsonMapa['property']['nroMapa'],16)
    nroSpriteSheet = int(jsonMapa['property']['nroSpriteSheet'],16)
    nose = int(jsonMapa['property']['nose'],16)
    spriteAddr = int(jsonMapa['property']['spriteAddr'],16)
    cantSprites = int(jsonMapa['property']['cantSprites'],16)
    mapBank = int(jsonMapa['property']['mapBank'],16)
    mapAddr = int(jsonMapa['property']['mapAddr'],16)
    noseAddr = int(jsonMapa['property']['noseAddr'],16)

    mapa = mystic.maps.Mapa(nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr)
    mapa.importJs(filepath)
    mapas.mapas.append(mapa)

  # quemo los mapas en la rom
  _burnMapas(mapas)


def burnMapasTiledXml():
  """ quema los mapas usando los .tmx del Tiled """

  basePath = mystic.address.basePath
  path = basePath + '/mapas'

  mapas = mystic.maps.Mapas()

  # por cada mapa
#  for i in range(0,1):
  for i in range(0,0x10):

    filepath = path + '/mapa_{:02}_{:02x}.tmx'.format(i,i)
    f = open(filepath, 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()
    data = '\n'.join(lines)

    import xml.etree.ElementTree as ET

    myroot = ET.fromstring(data)
#    print(myroot[0][0].attrib)

    for prop in myroot[0]:

      if(prop.attrib['name'] == 'nroMapa'):
        nroMapa = int(prop.attrib['value'], 16)
      elif(prop.attrib['name'] == 'nroSpriteSheet'):
        nroSpriteSheet = int(prop.attrib['value'], 16)
      elif(prop.attrib['name'] == 'nose'):
        nose = int(prop.attrib['value'], 16)
      elif(prop.attrib['name'] == 'spriteAddr'):
        spriteAddr = int(prop.attrib['value'], 16)
      elif(prop.attrib['name'] == 'cantSprites'):
        cantSprites = int(prop.attrib['value'], 16)
      elif(prop.attrib['name'] == 'mapBank'):
        mapBank = int(prop.attrib['value'], 16)
      elif(prop.attrib['name'] == 'mapAddr'):
        mapAddr = int(prop.attrib['value'], 16)
      elif(prop.attrib['name'] == 'noseAddr'):
        noseAddr = int(prop.attrib['value'], 16)

    mapa = mystic.maps.Mapa(nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr)
    mapa.importTiledXml(filepath)
    mapas.mapas.append(mapa)

  # quemo los mapas en la rom
  _burnMapas(mapas)



def _burnMapas(mapas):

  # donde va el addr en cada uno de los bancos de mapas (5,6,7)
#  vaPorBank = 0x05
#  vaPorAddr = 0x0000
  vaPorBank, vaPorAddr = mystic.address.addrMaps
#  print('vaPorBank: {:02x} vaPorAddr: {:04x}'.format(vaPorBank, vaPorAddr))

  sortMapas = [0,9, 1,15,14,10,8, 3,2,13,4,5,11,12,6,7]

#  mystic.romSplitter.cleanBank(5)

  # por cada mapa
  for i in range(0,0x10):
#  for i in range(0,1):

    sortedNro = sortMapas[i]
    # lo agarro en el orden a quemar en la rom
    mapa = mapas.mapas[sortedNro]

#    print('mapa: ' + str(mapa))
#    mapa.exportPngFile('./game/mapas/mapa_{:02x}.png'.format(mapa.nroMapa))

    # lo codifico para calcular el tamaño que ocupa
    subArray = mapa.encodeRom(mapa.mapAddr)

#    filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#    mystic.util.arrayToFile(subArray, filepath)
#    iguales = mystic.util.compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#    print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

    if(vaPorAddr + len(subArray) >= 0x4000):
      vaPorBank += 1
      vaPorAddr = 0x0000

    # actualizo el addr !!
    mapa.mapBank = vaPorBank
    mapa.mapAddr = vaPorAddr
    # vuelvo a encodearlo para ajustar los punteros addr de los bloques !!
    subArray = mapa.encodeRom(mapa.mapAddr)
    # lo quemo en la rom
    mystic.romSplitter.burnBank(mapa.mapBank, mapa.mapAddr, subArray)

#    print('i: {:02x} vaPorAddr: {:02x}:{:04x} mapAddr: {:02x}:{:04x}'.format(sortedNro, vaPorBank, vaPorAddr, mapa.mapBank, mapa.mapAddr))

    vaPorAddr += len(subArray)

#    print('quedó en: {:04x}'.format(vaPorAddr))


  array = []
  # para cada mapa
  for nroMapa in range(0,0x10):
#  for nroMapa in range(0,1):

    mapa = mapas.mapas[nroMapa]
    subArray = []
    subArray.append(0x00) 
    subArray.append(mapa.nroSpriteSheet*0x10)
    subArray.append(mapa.nose)
    subArray.extend([mapa.spriteAddr%0x100,mapa.spriteAddr//0x100])
    subArray.append(mapa.cantSprites)
    subArray.append(mapa.mapBank)
    subArray.extend([(mapa.mapAddr+0x4000)%0x100,(mapa.mapAddr+0x4000)//0x100])
    subArray.extend([mapa.noseAddr%0x100,mapa.noseAddr//0x100])

#    print('mapa: ' + str(mapa.nroMapa))
#    strHex = mystic.util.strHexa(subArray)
#    print('strHex: ' + strHex + '\n')

    array.extend(subArray)

  mystic.romSplitter.burnBank(0x08, 0x0000, array)



def exportTexto():
  """ convierte los banks .bin en .txt """

  basePath = mystic.address.basePath
#  romName = mystic.address.romName
#  filePath = basePath + '/hex_texto.txt'
#  rom = mystic.romSplitter.rom
   # lo exporto a texto
#  mystic.romSplitter._exportTexto(rom, filePath)

  # para cada banco
  for i in range(0,0x10):

    filePath = basePath + '/banks/bank_{:02}/bank_{:02}.txt'.format(i,i)
    bank = mystic.romSplitter.banks[i]
    # lo exporto a texto
    mystic.romSplitter._exportTexto(bank, filePath)

def _exportTexto(array, filePath):

  g = open(filePath, 'w', encoding="utf-8")

  i = 1
  renglon = []
  for hexa in array:
    renglon.append(hexa)

    if(i % 16 == 0):
      strhexs = ''
      traduc = ''
      for hexy in renglon:
        strhexs += '{:02x}'.format(hexy) + ' '
        chars = mystic.dictionary.decodeByte(hexy)
        traduc += chars
      addr = '{:04x}'.format(i - 0x10)
      g.write(addr + ' | ' + strhexs + '| ' + traduc + '\n')
      renglon = []

    i+=1

  g.close()



def scriptDecode(addr):
  script = Script(addr)

  banco = 0x0d
  if(addr >= 0x4000):
    banco = 0x0e
    addr -= 0x4000
  array = mystic.romSplitter.banks[banco]
  # creo un array desde donde empieza el script
  array = array[addr:]

  script.decodeRom(array)
  return script


def exportIntro():
  """ exporta el intro.txt """

  nroBank,address = mystic.address.addrIntro
  bank02 = mystic.romSplitter.banks[nroBank]

  array = bank02[address:]
#  strHexa = mystic.util.strHexa(array)
#  print('strHexa: ' + strHexa)

  string = ''
  # para cada byte del array
  for code in array:

    # lo decodifico
    if(code in [0x00, 0x1a]):
      # 'en' and 'en_uk' rom uses 0x00, but 'fr' and 'de' roms use 0x1a for <enter>
      char = '\n'
    elif(code == 0xff):
      char = ' '
    elif(code == 0x01):
      break
    else:
      char = mystic.dictionary.decodeByte(code)

    # y lo agrego al string
    string += char

#  print('string: ' + string)

  romName = mystic.address.romName
  path = './' + romName + '/intro.txt'
  # lo exporto al intro.txt
  f = open(path, 'w', encoding="utf-8")
  f.write(string)
  f.close()

def burnIntro():
  """ quema el intro.txt en la rom """

  romName = mystic.address.romName
  path = './' + romName + '/intro.txt'
  f = open(path, 'r', encoding="utf-8")
  string = f.read()
  f.close()

  array = []
  # para cada char del string
  for char in string:
    # lo codifico con el byte correspondiente
    if(char == '\n'):

      lang = mystic.address.language
      if(lang in [mystic.language.ENGLISH, mystic.language.ENGLISH_UK, mystic.language.JAPAN]):
        code = 0x00
      else: 
        code = 0x1a

    elif(char == ' '):
      code = 0xff
    else:
      code = mystic.dictionary.encodeChars(char)

    # y lo agrego al array
    array.append(code)

  # agrego el byte de cierre
  array.append(0x01)

#  strHexa = mystic.util.strHexa(array)
#  print('strHexa: ' + strHexa)

  nroBank,address = mystic.address.addrIntro
  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, address, array)


def burnInitialScript(nroScript):
  """ setea el script inicial a ejecutar cuando inicia el juego sin battery """

  bank02 = mystic.romSplitter.banks[0x02]
#  address = mystic.address.addrScriptAddrDic
  address = 0x3cfe

  byte1 = nroScript // 0x100
  byte2 = nroScript % 0x100
  array = [byte2, byte1]
  # lo quemo en el banco
  mystic.romSplitter.burnBank(0x02, address, array)
 
     
def exportMScripts():

  basePath = mystic.address.basePath
  path = basePath + '/scripts'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  scripts = mystic.mscripts.MScripts()
  # decodifico los scripts
  scripts.decodeRom()
  # los codifico en txt
  lines= scripts.encodeTxt()
  # lo grabo
  filepath = path + '/mscripts.txt'
  f = open(filepath, 'w', encoding="utf-8")
  strTxt = '\n'.join(lines)
  f.write(strTxt)
  f.close()

def exportJScripts():

  basePath = mystic.address.basePath
  path = basePath + '/scripts'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  scripts = mystic.jscripts.JScripts()
  # decodifico los scripts
  scripts.decodeRom()
  # los codifico en txt
  lines= scripts.encodeTxt()
  # lo grabo
  filepath = path + '/jscripts.js'
  f = open(filepath, 'w', encoding="utf-8")
  strTxt = '\n'.join(lines)
  f.write(strTxt)
  f.close()


  shutil.copyfile('./mystic/__index.html', basePath + '/index.html')
  shutil.copyfile('./mystic/jscriptsEngine.js', basePath + '/jscriptsEngine.js')


def burnMScripts(filepath):
  """ compila el script.txt indicado y quema los scripts en los bancos 0x0d y 0x0e, y el dicionario de addrs en banco 0x08 """

  scripts = mystic.mscripts.MScripts()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  scripts.decodeTxt(lines)

  # codifico los banks 0x0d y 0x0e
#  array0d, array0e = scripts.encodeRom()
  encodedBanks = scripts.encodeRom()

  basePath = mystic.address.basePath
  # creo los binarios para comparar
#  mystic.util.arrayToFile(array0d, basePath+'/scripts/scripts0d.bin')
#  mystic.util.arrayToFile(array0e, basePath+'/scripts/scripts0e.bin')
#  iguales = mystic.util.compareFiles(basePath+'/banks/bank_13/bank_13.bin', basePath+'/scripts/scripts0d.bin', 0, len(array0d))
#  print('iguales 0d: ' + str(iguales))
#  iguales = mystic.util.compareFiles(basePath+'/banks/bank_14/bank_14.bin', basePath+'/scripts/scripts0e.bin', 0, len(array0e))
#  print('iguales 0e: ' + str(iguales))

  vaPorBank = 0x0d
  for encodedBank in encodedBanks:

#    print('va por bank: {:02x}'.format(vaPorBank))
#    print('len(bank): {:04x}'.format(len(encodedBank)))

    mystic.util.arrayToFile(encodedBank, basePath+'/scripts/scripts{:02x}.bin'.format(vaPorBank))

    # quemo los banks 0x0d y 0x0e
    mystic.romSplitter.burnBank(vaPorBank, 0x0000, encodedBank)
    vaPorBank += 1
 
  # quemo los banks 0x0d y 0x0e
#  mystic.romSplitter.burnBank(0x0d, 0x0000, array0d)
#  mystic.romSplitter.burnBank(0x0e, 0x0000, array0e)


  bank,addr = mystic.address.addrScriptAddrDic
  array = []
  # por cada script
  for script in scripts.scripts:

#    print('script addr: {:04x}'.format(script.addr))

    # agarro su addr
    byte1 = script.addr // 0x100
    byte2 = script.addr % 0x100
    # y la agrego al array
    array.extend([byte2, byte1])

  # quemo el diccionario de addr en el bank08
  mystic.romSplitter.burnBank(bank, addr, array)

#  mystic.util.arrayToFile(array, './de/scripts/dic.bin')
#  iguales = mystic.util.compareFiles('./de/banks/bank_08/bank_08.bin', './de/scripts/dic.bin', addr, len(array))
#  print('iguales dic: ' + str(iguales))


def burnJScripts(filepath):
  """ compila el script.js indicado y quema los scripts en los bancos 0x0d y 0x0e, y el dicionario de addrs en banco 0x08 """

  scripts = mystic.jscripts.JScripts()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  scripts.decodeTxt(lines)

  # codifico los banks 0x0d y 0x0e
#  array0d, array0e = scripts.encodeRom()
  encodedBanks = scripts.encodeRom()

  basePath = mystic.address.basePath
  # creo los binarios para comparar
#  mystic.util.arrayToFile(array0d, basePath+'/scripts/scripts0d.bin')
#  mystic.util.arrayToFile(array0e, basePath+'/scripts/scripts0e.bin')
#  iguales = mystic.util.compareFiles(basePath+'/banks/bank_13/bank_13.bin', basePath+'/scripts/scripts0d.bin', 0, len(array0d))
#  print('iguales 0d: ' + str(iguales))
#  iguales = mystic.util.compareFiles(basePath+'/banks/bank_14/bank_14.bin', basePath+'/scripts/scripts0e.bin', 0, len(array0e))
#  print('iguales 0e: ' + str(iguales))

  vaPorBank = 0x0d
  for encodedBank in encodedBanks:

#    print('va por bank: {:02x}'.format(vaPorBank))
#    print('len(bank): {:04x}'.format(len(encodedBank)))

    mystic.util.arrayToFile(encodedBank, basePath+'/scripts/scripts{:02x}.bin'.format(vaPorBank))

    # quemo los banks 0x0d y 0x0e
    mystic.romSplitter.burnBank(vaPorBank, 0x0000, encodedBank)
    vaPorBank += 1
 
  # quemo los banks 0x0d y 0x0e
#  mystic.romSplitter.burnBank(0x0d, 0x0000, array0d)
#  mystic.romSplitter.burnBank(0x0e, 0x0000, array0e)


  bank,addr = mystic.address.addrScriptAddrDic
  array = []
  # por cada script
  for script in scripts.scripts:

#    print('script addr: {:04x}'.format(script.addr))

    # agarro su addr
    byte1 = script.addr // 0x100
    byte2 = script.addr % 0x100
    # y la agrego al array
    array.extend([byte2, byte1])

  # quemo el diccionario de addr en el bank08
  mystic.romSplitter.burnBank(bank, addr, array)

#  mystic.util.arrayToFile(array, './de/scripts/dic.bin')
#  iguales = mystic.util.compareFiles('./de/banks/bank_08/bank_08.bin', './de/scripts/dic.bin', addr, len(array))
#  print('iguales dic: ' + str(iguales))



def burnBank(bank, idx0, hexs):

  i = idx0
  for hexa in hexs:

    if(i >= 0x4000):
      return False

    banco = mystic.romSplitter.banks[bank]
#    print('banco: ' + str(banco))

#    print('grabando hexa {:02x} en i {:04x}'.format(hexa, i))

    banco[i] = hexa
    i += 1

  return True


def exportExpTable():
  """ exporta la tabla de experiencia para subir de nivel """

  nroBank, addr = mystic.address.addrExpTable
  bank = mystic.romSplitter.banks[nroBank]
  array = bank[addr:]

  lines = []
  for i in range(0,101):
    hexExp = array[3*i:3*(i+1)]

    exp = hexExp[0]*0x100**2 + hexExp[1]*0x100 + hexExp[2] 
    lines.append('level {:03}: {:06x} '.format(i+1, exp))

  string = '\n'.join(lines)

  romName = mystic.address.romName
  path = './' + romName + '/exp.txt'
  # lo exporto al exp.txt
  f = open(path, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  length = 3*101
  # agrego info al stats
  mystic.romStats.appendDato(0x08, addr, addr+length, (rr, gg, bb), 'exp table')


def burnExpTable(filepath):
  """ quema el exp.txt en la rom """

  print('quemando la tabla de experiencia')

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  array = []
  for line in lines:
    idx0 = line.index(':')
    strHexa = line[idx0+1:].strip()
    exp = int(strHexa, 16)

    byte1 = exp//0x10000
    byte2 = (exp % 0x010000)//0x100
    byte3 = (exp % 0x000100)

    array.extend([byte1, byte2, byte3])

#    print('exp: {:06x}: {:02x} {:02x} {:02x}'.format(exp, byte1, byte2, byte3))

  nroBank,addr = mystic.address.addrExpTable
#  print('current addr: {:04x}'.format(addr))

  strArray = mystic.util.strHexa(array)
#  print('strArray: ' + strArray)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, addr, array)



def exportItems():
  """ exporta los items """

  basePath = mystic.address.basePath
  path = basePath + '/items'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank,addr = mystic.address.addrMagic
  data = mystic.romSplitter.banks[nroBank]

  string = ''
  # para cada magia
  for i in range(0,8):
    magicOffset = addr + i*0x10
    magicArray = data[magicOffset:magicOffset+0x10]
#    magic = Magic()
    magic = mystic.inventory.Item('magic')
    # la decodifico
    magic.decodeRom(magicArray)
#    Cosas.instance().addMagic(magic)

    lines = magic.encodeTxt()
    subString = '\n'.join(lines)
    string += subString

  filePath = path + '/00_magic.txt'
  # lo exporto al magic.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  addr = magicOffset + 0x10
  string = ''
  # para cada item
  for i in range(0,57):
    itemOffset = addr + i*0x10
    itemArray = data[itemOffset:itemOffset+0x10]
    item = mystic.inventory.Item('item')
    # lo decodifico
    item.decodeRom(itemArray)
#    Cosas.instance().addItem(item)

    lines = item.encodeTxt()
    subString = '\n'.join(lines)
    string += subString

  filePath = path + '/01_items.txt'
  # lo exporto al items.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  addr = itemOffset + 0x10
  string = ''
  # para cada weapon
  for i in range(0,46):
    weaponOffset = addr + i*0x10
    weaponArray = data[weaponOffset:weaponOffset+0x10]
    weapon = mystic.inventory.Item('weapon')
    # la decodifico
    weapon.decodeRom(weaponArray)
#    Cosas.instance().addWeapon(weapon)

    lines = weapon.encodeTxt()
    subString = '\n'.join(lines)
    string += subString

  filePath = path + '/02_weapons.txt'
  # lo exporto al weapons.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()


  lines = []

  # apdp
  addr = weaponOffset + 0x10
  ap = mystic.inventory.Apdp()
  ap.decodeRom(data[addr:])
  subLines = ap.encodeTxt()
  lines.extend(subLines)

  lines.append('')

  addr += 0x10
  dp = mystic.inventory.Apdp()
  dp.decodeRom(data[addr:])
  subLines = dp.encodeTxt()
  lines.extend(subLines)

  string = '\n'.join(lines)

  filePath = path + '/03_apdp.txt'
  # lo exporto al apdp.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  lines = []
  addr += 0x10
  for i in range(0,17):
    subArray = data[addr:addr+16]
#    strHexa = mystic.util.strHexa(subArray)
#    print('vendor: ' + strHexa)
    vendor = mystic.inventory.Vendor()
    vendor.decodeRom(subArray)
#    print(str(vendor))
    subLines = vendor.encodeTxt()
    lines.extend(subLines)

    addr += 0x10

  string = '\n'.join(lines)

  filePath = path + '/04_vendor.txt'
  # lo exporto al vendor.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  # exporto las weapons iniciales
  mystic.romSplitter.exportInitialWeapons()

  # exporto los items especiales
  mystic.romSplitter.exportSpecialItems()

def exportInitialWeapons():
  """ exporta las weapons con que inicia el juego """

  basePath = mystic.address.basePath
  path = basePath + '/items'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank, addr = mystic.address.addrInitialWeapons
  data = mystic.romSplitter.banks[nroBank]
#  print('bank, addr: {:02x} {:04x}'.format(nroBank, addr))
#  strHexa = mystic.util.strHexa(data[addr:addr+6])
#  print('hexa: ' + strHexa)

  lines = []
  lines.append('weapon: {:02x}'.format(data[addr+0]))
  lines.append('helmet: {:02x}'.format(data[addr+1]))
  lines.append('ap:     {:02x}'.format(data[addr+2]))
  lines.append('armor:  {:02x}'.format(data[addr+3]))
  lines.append('dp:     {:02x}'.format(data[addr+4]))
  lines.append('shield: {:02x}'.format(data[addr+5]))

  string = '\n'.join(lines)

  filePath = path + '/06_initialWeapons.txt'
  # lo exporto al initialWeapons.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

def burnInitialWeapons(filepath, nroBank, offset):
  """ quema el specialItems.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  for line in lines:
    if(line.startswith('weapon:')):
      weapon = int(line[len('weapon:'):].strip(),16)
    elif(line.startswith('helmet:')):
      helmet = int(line[len('helmet:'):].strip(),16)
    elif(line.startswith('ap:')):
      ap = int(line[len('ap:'):].strip(),16)
    elif(line.startswith('armor:')):
      armor = int(line[len('armor:'):].strip(),16)
    elif(line.startswith('dp:')):
      dp = int(line[len('dp:'):].strip(),16)
    elif(line.startswith('shield:')):
      shield = int(line[len('shield:'):].strip(),16)

  array = []
  array.append(weapon)
  array.append(helmet)
  array.append(ap)
  array.append(armor)
  array.append(dp)
  array.append(shield)
 
  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

def exportSpecialItems():
  """ exporta los listados de items especiales """

  basePath = mystic.address.basePath
  path = basePath + '/items'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)


  nroBank, vaPorAddr = mystic.address.addrLoadStateStrangeBytes
  data = mystic.romSplitter.banks[nroBank]

  lines = []

  for i in range(0,4):
    lines.append('-------strangeBytes' + str(i))
    num = 0xffff
    while(num != 0x0000):
      num0 = data[vaPorAddr]
      num1 = data[vaPorAddr+1]
      num = num1*0x100 + num0
      lines.append('{:04x}'.format(num))
      vaPorAddr += 2
   
  specialItems = ['curative items', 'healing items', 'levelup items', 'sleep items', 'mute items', 'japan items', 'crystal items', 'fire items' ]

  for i in range(0,8):
 
    lines.append('-------' + specialItems[i])
    nroItem = 0xff
    while(nroItem != 0x00):
      nroItem = data[vaPorAddr]
#      print('nroItem: {:02x}'.format(nroItem))
      vaPorAddr += 1

      if(nroItem <= 8):
        itemName = mystic.variables.magias[nroItem-1]
      else:
        itemName = mystic.variables.items[nroItem-9]
#      print('item: ' + str(item))

      if(nroItem != 0x00):
        lines.append('{:02x}    # '.format(nroItem) + str(itemName))
      else:
        lines.append('{:02x}'.format(nroItem))


  string = '\n'.join(lines)

  filePath = path + '/10_specialItems.txt'
  # lo exporto al specialItems.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()



def burnItems(tipo, filepath, nroBank, offset):
  """ quema el magic.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  items = []
  primerItem = True
  subLines = []
  for line in lines:

    if('nro:' in line):
      if(not primerItem):
        item = mystic.inventory.Item(tipo)
        item.decodeTxt(subLines)
        items.append(item)
      else:
        primerItem = False

      subLines = []
    subLines.append(line)
  item = mystic.inventory.Item(tipo)
  item.decodeTxt(subLines)
  items.append(item)

  array = []
  for item in items:
#    print('item: ' + str(item))
    subArray = item.encodeRom()
    array.extend(subArray)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

  vaPorAddr = offset + len(array)
  return vaPorAddr

def burnApdp(filepath, nroBank, offset):
  """ quema el apdp.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  array = []

  ap = mystic.inventory.Apdp()
  ap.decodeTxt(lines[0:3])
  subArray = ap.encodeRom()
  array.extend(subArray)
 
  dp = mystic.inventory.Apdp()
  dp.decodeTxt(lines[4:7])
  subArray = dp.encodeRom()
  array.extend(subArray)

#  strHexa = mystic.util.strHexa(array)
#  print('strHexa: ' + strHexa)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

  vaPorAddr = offset + len(array)
  return vaPorAddr

def burnVendor(filepath, nroBank, offset):
  """ quema el vendor.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  array = []

#  print('lines: ' + str(lines))

  vendors = []
  primerVendor = True
  subLines = []
  for line in lines:

    if('--- vendor:' in line):
      if(not primerVendor):
        vend = mystic.inventory.Vendor()
        vend.decodeTxt(subLines)
        vendors.append(vend)
      else:
        primerVendor = False

      subLines = []
    subLines.append(line)

  vend = mystic.inventory.Vendor()
  vend.decodeTxt(subLines)
  vendors.append(vend)
 
  array = []
  for vend in vendors:
#    print('vend: ' + str(vend))
    subArray = vend.encodeRom()
#    strHexa = mystic.util.strHexa(subArray)
#    print('strHexa: ' + strHexa)
    array.extend(subArray)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

  vaPorAddr = offset + len(array)
  return vaPorAddr

def burnSpecialItems(filepath, nroBank, offset):
  """ quema el specialItems.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  cambio = False
  strangeLines = []
  specialLines = []
  for line in lines:

    if(line.startswith('-------curative items')):
      cambio = True

    if(not cambio):
      strangeLines.append(line)
    else:
      specialLines.append(line)


  array = []

  listados = []
  listado = [] 
  primerListado = True 
  for line in strangeLines:
#    print('line: ' + line)

    if(line.startswith('-------')):
      if(not primerListado):
#        print('encontro listado: ' + str(listado))
        listados.append(listado)
        listado = []
      primerListado = False
    else:
      num = int(line.strip()[0:5],16)
#      print('num: {:04x}'.format(num))
      listado.append(num)

#  print('encontro listado: ' + str(listado))
  listados.append(listado)


  for listado in listados:
#    print('listado----')
    for num in listado:
#      print('num: {:04x}'.format(num))
      byte0 = num // 0x100
      byte1 = num % 0x100

#      print('byte0: {:02x}'.format(byte0))
#      print('byte1: {:02x}'.format(byte1))

      array.extend([byte1, byte0])

  specials = []
  special = [] 
  primerSpecial = True 
  for line in specialLines:
#    print('line: ' + line)

    if(line.startswith('-------')):
      if(not primerSpecial):
#        print('encontro special: ' + str(special))
        specials.append(special)
        special = []
      primerSpecial = False
    else:
      num = int(line.strip()[0:5],16)
#      print('num: {:04x}'.format(num))
      special.append(num)

#  print('encontro special: ' + str(special))
  specials.append(special)


  for special in specials:
#    print('special----')
    for num in special:
#      print('num: {:02x}'.format(num))
      array.append(num)
 
  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

  vaPorAddr = offset + len(array)
  return vaPorAddr


def exportSolarus():

  print('exportando a solarus...')

#  basePath = mystic.address.basePath
#  path = basePath + '/scripts'
  path = './solarusQuest'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  # exporto los spriteSheets
  for k in range(0,5):
    sheet = mystic.romSplitter.spriteSheets[k]

    lines = []
    lines.append('background_color{ 255, 255, 255 }')
    sheet.exportPngFile('./solarusQuest/data/tilesets/sheet_{:02}.tiles.png'.format(k))
    i = 0
    for sprite in sheet.sprites:
#      print('sprite: {:02x}'.format(sprite.bloqueo))

      x = (i%16)
      y = (i//16)

      lines.append('tile_pattern{')
      lines.append(' id = "' + str(i) + '",')
      ground = 'traversable'
#      ground = 'traversable' if sprite.bloqueo == 0x30 else 'wall'
      lines.append(' ground = "' + ground + '",')
      lines.append(' default_layer = 0,')
      lines.append(' x = ' + str(16*x) + ',')
      lines.append(' y = ' + str(16*y) + ',')
      lines.append(' width = 16,')
      lines.append(' height = 16,')
      lines.append('}')

      i += 1

    f = open('./solarusQuest/data/tilesets/sheet_{:02}.dat'.format(k), 'w', encoding="utf-8")
    f.write('\n'.join(lines))
    f.close()

  mapas = Mapas()
  # decodifico los scripts
  mapas.decodeRom()

  for m in range(0, 0x10):
    mapa = mapas.mapas[m]

    width = mapa.mapa.sizeX
    height = mapa.mapa.sizeY
    nroSpriteSheet = mapa.nroSpriteSheet
    for k in range(0, width*height):
      bloque = mapa.mapa.bloques[k]

      bloquex = k % width
      bloquey = k // width

      lines = []

      lines.append('properties{')
      lines.append('  x = 0,')
      lines.append('  y = 0,')
      lines.append('  width = 160,')
      lines.append('  height = 128,')
      lines.append('  min_layer = 0,')
      lines.append('  max_layer = 2,')
      lines.append('  tileset = "sheet_{:02}",'.format(nroSpriteSheet))
      lines.append('}\n')


      for j in range(0,8):
        for i in range(0,10):
          nro = bloque.getSprites()[j][i]
          print('sprite: ' + str(nro))

 
          lines.append('tile{')
          lines.append('  layer = 0,')
          lines.append('  x = ' + str(16*i) + ',')
          lines.append('  y = ' + str(16*j) + ',')
          lines.append('  width = 16,')
          lines.append('  height = 16,')
          lines.append('  pattern = "' + str(nro) + '",')
          lines.append('}\n')

      lines.append('teletransporter{')
      lines.append('  layer = 0,')
      lines.append('  x = 160,')
      lines.append('  y = 0,')
      lines.append('  width = 16,')
      lines.append('  height = 128,')
      lines.append('  transition = "scrolling",')
      lines.append('  destination_map = "mapa_{:02x}_{:02}_{:02}_map",'.format( m, (width+bloquex+1)%width, bloquey ))
      lines.append('  destination = "_side",')
      lines.append('}\n')

      lines.append('teletransporter{')
      lines.append('  layer = 0,')
      lines.append('  x = -16,')
      lines.append('  y = 0,')
      lines.append('  width = 16,')
      lines.append('  height = 128,')
      lines.append('  transition = "scrolling",')
      lines.append('  destination_map = "mapa_{:02x}_{:02}_{:02}_map",'.format( m, (width+bloquex-1)%width, bloquey ))
      lines.append('  destination = "_side",')
      lines.append('}\n')

      lines.append('teletransporter{')
      lines.append('  layer = 0,')
      lines.append('  x = 0,')
      lines.append('  y = -16,')
      lines.append('  width = 160,')
      lines.append('  height = 16,')
      lines.append('  transition = "scrolling",')
      lines.append('  destination_map = "mapa_{:02x}_{:02}_{:02}_map",'.format( m, bloquex, (height+bloquey-1)%height ))
      lines.append('  destination = "_side",')
      lines.append('}\n')

      lines.append('teletransporter{')
      lines.append('  layer = 0,')
      lines.append('  x = 0,')
      lines.append('  y = 128,')
      lines.append('  width = 160,')
      lines.append('  height = 16,')
      lines.append('  transition = "scrolling",')
      lines.append('  destination_map = "mapa_{:02x}_{:02}_{:02}_map",'.format( m, bloquex, (height+bloquey+1)%height ))
      lines.append('  destination = "_side",')
      lines.append('}\n')

      f = open('./solarusQuest/data/maps/mapa_{:02x}_{:02}_{:02}_map.dat'.format(m, bloquex, bloquey), 'w', encoding="utf-8")
      f.write('\n'.join(lines))
      f.close()

