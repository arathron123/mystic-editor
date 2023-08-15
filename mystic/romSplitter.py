import os
import shutil

import mystic.address
import mystic.tileset
import mystic.spriteSheet
import mystic.romStats
import mystic.spritePersonaje
import mystic.npc
import mystic.bosses
import mystic.projectiles
import mystic.windows
import mystic.heroProjectiles
import mystic.mscripts
import mystic.jscripts
import mystic.maps
import mystic.music
import mystic.audio
import mystic.sounds
import mystic.ippy

# la rom
#self.rom = []
# los bancos
banks = []
# the big tilesets data
tilesets = None
# los cinco tilesets
tilesetsLevel2 = []
# los cinco spriteSheets
spriteSheets = []
# los mapas
#mapas = None


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


def exportSongsRom(filepath):
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


def exportSoundsRom(filepath):
  """ exporta a una rom con efectos de sonido """

  # cargo el gbs rom
#  gbsRom = mystic.util.fileToArray('./roms/audio.gb')
  # me quedo con el bank00
#  gbsRom = gbsRom[0:0x4000]
  gbsRom = mystic.util.fileToArray('./gbsBank00.bin')

#  titulo = 'Final Fantasy Adventure'
  titulo = 'Mystic Sounds'
  listTitulo = list(titulo.encode())
  listTitulo.extend([0x00 for i in range(0, 32-len(listTitulo))])

#  autor = 'Kenji Ito'
  autor = ''
  listAutor = list(autor.encode())
  listAutor.extend([0x00 for i in range(0, 32-len(listAutor))])

#  date = '1991 Square'
  date = ''
  listDate = list(date.encode())
  listDate.extend([0x00 for i in range(0, 32-len(listDate))])

  for i in range(0, 32):
    gbsRom[0x3F74 + i] = listTitulo[i]
    gbsRom[0x3F94 + i] = listAutor[i]
    gbsRom[0x3FB4 + i] = listDate[i]

  cantSounds = 37
  # seteo los números de efectos
  for i in range(0,cantSounds):
    gbsRom[0x3F00+i] = i+1
  # cambio 1E por 25 para setear la cantidad de efectos de sonido
  gbsRom[0x3F68] = 0x25
  # cambio E2 por 00 para que los números de efectos los busque a partir del 3F00
  gbsRom[0x3FD5] = 0x00
  # cambio 90 por 92 para cambiar música por efectos de sonido
  gbsRom[0x3FE0] = 0x92

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


def exportDictionary():

  basePath = mystic.address.basePath
  path = basePath + '/dictionary'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  mystic.dictionary.decodeRom()

  # export the .js
  mystic.dictionary.exportJs(path + '/dictionary.js')




def burnDictionary(filepath):
  # import the .js
  mystic.dictionary.importJs(filepath)

  numBank,addrDictionary = mystic.address.addrDictionary

  arrayDict = mystic.dictionary.encodeRom()
#  print('arrayDict: ' + mystic.util.strHexa(arrayDict))

  mystic.romSplitter.burnBank(numBank, addrDictionary, arrayDict)

  basePath = mystic.address.basePath
  path = basePath + '/dictionary'
  initAddr = 0x4000*numBank + addrDictionary
  dataSize = len(arrayDict)
  dataFilepath = path + '/dictionary.js'
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)


def exportFont():

  basePath = mystic.address.basePath
  path = basePath + '/tilesetsLevel2'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  bank = mystic.romSplitter.banks[8]
  # creo el tileset
  tileset = mystic.tileset.Tileset(16,9)

  array = bank[0x1000*2+7*0x100:0x1000*(2+1)]

  tileset.decodeRom(array)
  tileset.exportPngFile(basePath + '/tilesetsLevel2/font.png')

def burnFont():

  basePath = mystic.address.basePath
  tileset = mystic.tileset.Tileset(16,9)
  tileset.importPngFile(basePath + '/tilesetsLevel2/font.png')
  array = tileset.encodeRom()

  mystic.romSplitter.burnBank(8, 0x1000*2+7*0x100, array)


def exportMultiTilesets():
  """ exporta los cinco tilesets """

  basePath = mystic.address.basePath
  path = basePath + '/tilesetsLevel2'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  mystic.romSplitter.tilesetsLevel2 = []
  # para cada uno de los cinco tilesets
  for nroTileset in range(0,5):

    # para los primeros 4 tilesets
    if(nroTileset < 4):
      tileset = mystic.tileset.Tileset(16,16)
      banco12 = mystic.romSplitter.banks[12]
      array = banco12[0x1000*nroTileset:0x1000*(nroTileset+1)]
      tileset.decodeRom(array)

    # sino, para el 5to tileset
    else:
      tileset = mystic.tileset.Tileset(16,13)
      banco11 = mystic.romSplitter.banks[11]
      array = banco11[0x0000:0x0d00]
      tileset.decodeRom(array)

    tileset.exportPngFile(path + '/tileset_{:02}.png'.format(nroTileset))
    tileset.exportTiledXml(path + '/tileset_{:02}.tsx'.format(nroTileset))

    mystic.romSplitter.tilesetsLevel2.append(tileset)

def burnMultiTilesets():

  basePath = mystic.address.basePath
  path = basePath + '/tilesetsLevel2'
 
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

  for i in range(0, len(mystic.address.baseSubtile)):
    subtilesetOffset = mystic.address.baseSubtile[i]+1
    filename = 'sub_tileset_{:02x}'.format(i)
    # exports the subtileset...
    _exportSubTileset(path, filename, subtilesetOffset)


def _exportSubTileset(path, filename, vaPorTile):
  """ exports a sub-tileset """
#  print('exporting sub-tileset')

  width = 16
  height = 16
  # el id a ir incrementando
  iidd = 1

  import xml.etree.cElementTree as ET

  root = ET.Element("map", version='1.9', tiledversion="1.9.2", orientation="orthogonal", renderorder="right-down", width=str(width), height=str(height), tilewidth="8", tileheight="8", infinite="0", nextlayerid="3", nextobjectid="14")

#  tileset = ET.SubElement(root, "tileset", firstgid="1", source='../tilesets/tileset_{:02x}.tsx'.format(self.nroTileset))
  tileset = ET.SubElement(root, "tileset", firstgid="1", source='tilesets.tsx')

  layer1 = ET.SubElement(root, "layer", id=str(iidd), name="Tile Layer 1", width=str(width), height=str(height))
  iidd += 1
  data = ET.SubElement(layer1, "data", encoding="csv")

  renglones = []
  renglones.append("")
  for j in range(0,height):
    renglon = ''
    for i in range(0,width):
#      renglon += '0'
      renglon += str(vaPorTile)
      vaPorTile += 1

      if(i != width-1 or j != height-1):
        renglon += ','
    renglones.append(renglon)

  renglones.append("")
  textData = '\n'.join(renglones)
  data.text = textData

  tree = ET.ElementTree(root)
#  printed_xml = tree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True)
  ET.indent(root, space=" ", level=0)
  tree.write(path + '/' + filename + '.tmx', xml_declaration=True, encoding='utf-8')
#  print('ET: ' + str(ET.tostring(root, encoding='UTF-8')))


  # y ahora exporto el .tsx para utilizarlo como subtileset de los spriteSheets
#  root = ET.Element("tileset", version='1.9', tiledversion="1.9.2", self.name, tilewidth="8", tileheight="8", tilecount=str(16*16), columns="16")
  root = ET.Element("tileset", version='1.9', tiledversion="1.9.2", name=filename, tilewidth="8", tileheight="8", tilecount=str(16*16), columns="16")

  img = ET.SubElement(root, "image", source=filename + '.tmx', width="128", height="128")

  tree = ET.ElementTree(root)
  ET.indent(root, space=" ", level=0)
  tree.write(path + '/' + filename + '.tsx', xml_declaration=True, encoding='utf-8')
#  print('ET: ' + str(ET.tostring(root, encoding='UTF-8')))



def burnTilesets():

  basePath = mystic.address.basePath
  path = basePath + '/tilesets'
  dataFilepath = path + '/tilesets.png'

  tileset = mystic.tileset.Tileset(16,16*4*5)
  tileset.importPngFile(dataFilepath)
  array = tileset.encodeRom()

  # we burn the tilesets into the banks (skipping the disabled tiles)
  mystic.romSplitter.burnBank(8, 0x1A00, array[0x1A00:0x4000])
  mystic.romSplitter.burnBank(9, 0x0900, array[0x4900:0x4000*2])
  mystic.romSplitter.burnBank(10, 0x0000, array[0x4000*2:0x4000*3])
  mystic.romSplitter.burnBank(11, 0x0000, array[0x4000*3:0x4000*4])
  mystic.romSplitter.burnBank(12, 0x0000, array[0x4000*4:0x4000*5])

  initAddr = 0x4000*8 + 0x1A00
  dataSize = len(array[0x1A00:0x4000])
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  initAddr = 0x4000*9 + 0x0900
  dataSize = len(array[0x4900:0x4000*2])
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  initAddr = 0x4000*10
  dataSize = 0x4000
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  initAddr = 0x4000*11
  dataSize = 0x4000
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  initAddr = 0x4000*12
  dataSize = 0x4000
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)


def exportSpriteSheets(level2):
  """ exporta los spritesheets.  If level2 == True, it uses the optional tilesetsLevel2 """

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

    lines = sheet.encodeTxt()
    string = '\n'.join(lines)
    f = open(basePath + '/spriteSheets/sheet_{:02}_noedit.txt'.format(nroSpriteSheet), 'w', encoding="utf-8")
    f.write(string)
    f.close()

    sheet.exportPngFile(basePath + '/spriteSheets/sheet_{:02}_noedit.png'.format(nroSpriteSheet))

#    sheet.exportTiled(basePath + '/spriteSheets/sheet_{:02}.tsx'.format(nroSpriteSheet))
#    sheet.exportTiledXml(basePath + '/spriteSheets/sheet_{:02}.tsx'.format(nroSpriteSheet))
    sheet.exportTiledXml(basePath + '/spriteSheets/sheet_{:02}'.format(nroSpriteSheet), level2)
    sheet.exportJs(basePath + '/spriteSheets/sheet_{:02}.js'.format(nroSpriteSheet))

#    sheet.exportPyxelEdit(basePath + '/spriteSheets/sheet_{:02}.pyxel'.format(nroSpriteSheet))

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

    numBank,addr = mystic.address.spriteSheetsAddr[nroSpriteSheet]
    cant = mystic.address.cantSpritesInSheet[nroSpriteSheet]
#    bank08 = mystic.romSplitter.banks[8]
#    array = bank08[addr:addr+6*cant]

    mystic.romSplitter.burnBank(numBank, addr, array)

    initAddr = 0x4000*numBank + addr
    dataSize = len(array)
    dataFilepath = basePath + '/spriteSheets/sheet_{:02}.js'.format(nroSpriteSheet)
    mystic.romStats.appendData(initAddr, dataSize, dataFilepath)


def exportWindows():
  """ exporta las ventanas """

#  print('--- 2:1baa')

  basePath = mystic.address.basePath
  path = basePath + '/windows'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

#  nroBank,addr = mystic.address.addrWindows
#  bank = mystic.romSplitter.banks[nroBank]
  # the total number of windows
#  numWindows = 34

#  currentAddr = addr
#  print('currentAddr: {:04x}'.format(currentAddr))

  wins = mystic.windows.Windows()
  wins.decodeRom()

  import json
  # for allowing kana characters in json ensure_ascii=False
  strJson = json.dumps(wins.jsonWindows, indent=2, ensure_ascii=False)
#  strJson = json.dumps(data)
  f = open(path + '/windows.js', 'w', encoding="utf-8")
  f.write('windows = \n' + strJson)
  f.close()

def burnWindows(filepath):

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

#  print('data: ' + data)

  import json
  jsonWindows = json.loads(data)
#  print('jsonWindows: ' + str(jsonWindows))

  wins = mystic.windows.Windows()
  wins.jsonWindows = jsonWindows

  arrayWindows, arrayLevelUp, arrayWindowsAddr, arrayItems, arrayInitialWeapons, arrayDoor, arrayLabels, arrayLabels2, arrayIntro = wins.encodeRom()

  basePath = mystic.address.basePath
  path = basePath + '/windows'
  dataFilepath = path + '/windows.js'



#  print('arrayWindows: \n' + mystic.util.strHexa(arrayWindows))
  numBank,addrWindows = mystic.address.addrWindows
  mystic.romSplitter.burnBank(numBank, addrWindows, arrayWindows)

  initAddr = 0x4000*numBank + addrWindows
  dataSize = len(arrayWindows)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  numBank,addrLevelUp = mystic.address.addrLevelUp
  mystic.romSplitter.burnBank(numBank, addrLevelUp, arrayLevelUp)

  initAddr = 0x4000*numBank + addrLevelUp
  dataSize = len(arrayLevelUp)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  numBank,addrWindowsAddr = mystic.address.addrWindowsAddr
  mystic.romSplitter.burnBank(numBank, addrWindowsAddr, arrayWindowsAddr)

  initAddr = 0x4000*numBank + addrWindowsAddr
  dataSize = len(arrayWindowsAddr)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  numBank,addrMagic = mystic.address.addrMagic
  mystic.romSplitter.burnBank(numBank, addrMagic, arrayItems)

  initAddr = 0x4000*numBank + addrMagic
  dataSize = len(arrayItems)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  numBank,addrInitialWeapons = mystic.address.addrInitialWeapons
  mystic.romSplitter.burnBank(numBank, addrInitialWeapons, arrayInitialWeapons)

  initAddr = 0x4000*numBank + addrInitialWeapons
  dataSize = len(arrayInitialWeapons)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  numBank,addrDoor = mystic.address.addrDoorTileLocations
  mystic.romSplitter.burnBank(numBank, addrDoor, arrayDoor)

  initAddr = 0x4000*numBank + addrDoor
  dataSize = len(arrayDoor)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  numBank,addrLabels = mystic.address.addrWindowsLabels
  mystic.romSplitter.burnBank(numBank, addrLabels, arrayLabels)

  initAddr = 0x4000*numBank + addrLabels
  dataSize = len(arrayLabels)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  numBank,addrLabels2 = mystic.address.addrWindowsLabels2
  mystic.romSplitter.burnBank(numBank, addrLabels2, arrayLabels2)

  initAddr = 0x4000*numBank + addrLabels2
  dataSize = len(arrayLabels2)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  numBank,addrIntro = mystic.address.addrIntro
  mystic.romSplitter.burnBank(numBank, addrIntro, arrayIntro)

  initAddr = 0x4000*numBank + addrIntro
  dataSize = len(arrayIntro)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)


def exportBosses():
  """ exporta los monstruos grandes """

#  print('--- 4:0739')

  basePath = mystic.address.basePath
  path = basePath + '/bosses'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  numBank,addrBoss = mystic.address.addrBoss
  bank = mystic.romSplitter.banks[numBank]
  numberBoss = mystic.address.numberBoss

  bosses = mystic.bosses.Bosses()
  bosses.decodeRom(bank, addrBoss, numberBoss)

  import json
  # for allowing kana characters in json ensure_ascii=False
  strJson = json.dumps(bosses.jsonBosses, indent=2, ensure_ascii=False)
#  strJson = json.dumps(data)
  f = open(path + '/bosses.js', 'w', encoding="utf-8")
  f.write('bosses = \n' + strJson)
  f.close()

def burnBosses(filepath):

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

#  print('data: ' + data)

  import json
  jsonBosses = json.loads(data)
#  print('jsonBosses: ' + str(jsonBosses))

  bosses = mystic.bosses.Bosses()
  bosses.jsonBosses = jsonBosses

  numBank,addrBoss = mystic.address.addrBoss
  array = bosses.encodeRom(addrBoss)

  mystic.romSplitter.burnBank(numBank, addrBoss, array)

  basePath = mystic.address.basePath
  path = basePath + '/bosses'
  initAddr = 0x4000*numBank + addrBoss
  dataSize = len(array)
  dataFilepath = path + '/bosses.js'
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)


def exportHeroProjectiles():
  """ exports the hero-projectiles """

#  print('--- 1:1dcd')

  basePath = mystic.address.basePath
  path = basePath + '/projectiles'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  numBank,addrHeroProjs = mystic.address.addrHeroProjs
  bank = mystic.romSplitter.banks[numBank]

  heroProj = mystic.heroProjectiles.HeroProjectiles()
  heroProj.decodeRom(bank, addrHeroProjs)

  array = heroProj.encodeRom(addrHeroProjs)
  lastAddr = addrHeroProjs + len(array)
#  print('addrHeroProjs: {:04x}'.format(addrHeroProjs))
#  print('lastAddr: {:04x}'.format(lastAddr))

  import json
  # for allowing kana characters in json ensure_ascii=False
  strJson = json.dumps(heroProj.jsonHeroProjs, indent=2, ensure_ascii=False)
#  strJson = json.dumps(data)
  f = open(path + '/heroProjs.js', 'w', encoding="utf-8")
  f.write('heroProjs = \n' + strJson)
  f.close()


def burnHeroProjectiles(filepath):
  """ burn the hero-projectiles """

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

  heroProj = mystic.heroProjectiles.HeroProjectiles()
  heroProj.jsonHeroProjs = jsonHeroProjs

  numBank,addrHeroProjs = mystic.address.addrHeroProjs

  array = heroProj.encodeRom(addrHeroProjs)
  mystic.romSplitter.burnBank(numBank, addrHeroProjs, array)

  basePath = mystic.address.basePath
  path = basePath + '/projectiles'
  initAddr = 0x4000*numBank + addrHeroProjs
  dataSize = len(array)
  dataFilepath = path + '/heroProjs.js'
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)



def exportProjectiles():
  """ exports the projectiles """

#  print('--- 9:0479')

  basePath = mystic.address.basePath
  path = basePath + '/projectiles'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  numBank,addrProjectiles = mystic.address.addrProjectiles
  bank = mystic.romSplitter.banks[numBank]
  numberProjectiles = mystic.address.numberProjectiles

  npcs = mystic.projectiles.Projectiles()
  npcs.decodeRom(bank, addrProjectiles, numberProjectiles)

  import json
  # for allowing kana characters in json ensure_ascii=False
  strJson = json.dumps(npcs.jsonProjectiles, indent=2, ensure_ascii=False)
#  strJson = json.dumps(data)
  f = open(path + '/projectiles.js', 'w', encoding="utf-8")
  f.write('projectiles = \n' + strJson)
  f.close()

def burnProjectiles(filepath):
  """ burn the projectiles """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

#  print('data: ' + data)

  import json
  jsonProjectiles = json.loads(data)
#  print('jsonProjectiles: ' + str(jsonProjectiles))

  projectiles = mystic.projectiles.Projectiles()
  projectiles.jsonProjectiles = jsonProjectiles

  numBank,addrProjectiles = mystic.address.addrProjectiles

  array = projectiles.encodeRom(addrProjectiles)
  mystic.romSplitter.burnBank(numBank, addrProjectiles, array)

  basePath = mystic.address.basePath
  path = basePath + '/projectiles'
  initAddr = 0x4000*numBank + addrProjectiles
  dataSize = len(array)
  dataFilepath = path + '/projectiles.js'
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)




def exportNpc():
  """ exports the npcs """

#  print('--- 3:19fe')

  basePath = mystic.address.basePath
  path = basePath + '/npc'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  numBank,addrNpc = mystic.address.addrNpc
  bank = mystic.romSplitter.banks[numBank]
  numberNpcStats = mystic.address.numberNpcStats
  numberNpc = mystic.address.numberNpc
  numberNpcGroup = mystic.address.numberNpcGroup

  npcs = mystic.npc.Npcs()
  npcs.decodeRom(bank, addrNpc, numberNpcStats, numberNpc, numberNpcGroup)

  import json
  # for allowing kana characters in json ensure_ascii=False
  strJson = json.dumps(npcs.jsonNpcs, indent=2, ensure_ascii=False)
#  strJson = json.dumps(data)
  f = open(path + '/npcs.js', 'w', encoding="utf-8")
  f.write('npcs = \n' + strJson)
  f.close()

def burnNpc(filepath):

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

#  print('data: ' + data)

  import json
  jsonNpcs = json.loads(data)
#  print('jsonNpcs: ' + str(jsonNpcs))

  npcs = mystic.npc.Npcs()
  npcs.jsonNpcs = jsonNpcs

  numBank,addrNpc = mystic.address.addrNpc
  numBank0,addrSnowman = mystic.address.addrSnowmanSpriteGroup

  arraySpriteGroup1, array = npcs.encodeRom(addrNpc, addrSnowman)

  mystic.romSplitter.burnBank(numBank0, addrSnowman, arraySpriteGroup1)
  mystic.romSplitter.burnBank(numBank, addrNpc, array)


  basePath = mystic.address.basePath
  path = basePath + '/npc'
  dataFilepath = path + '/npcs.js'

  initAddr = 0x4000*numBank + addrNpc
  dataSize = len(array)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  initAddr = 0x4000*numBank0 + addrSnowman
  dataSize = len(arraySpriteGroup1)
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)



      
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


def exportAudioJson():
  """ exporta el audio en formato json """

  nroBank,addrMusic = mystic.address.addrMusic
  # cargo el banco 16 con las canciones
  bank = mystic.romSplitter.banks[nroBank]

  canciones = mystic.music.Canciones()
  canciones.decodeRom(bank,addrMusic)

  # grabo las canciones en audio_noedit.js
  _exportSongsJson(canciones, 'audio_noedit.js')

def _exportSongsJson(canciones, filename):

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  songsData = {}

  for i in range(0,len(canciones.canciones)):
    cancion = canciones.canciones[i]

    lines = cancion.encodeTxt()
    strCancion = '\n'.join(lines)
#    print('strCancion: ' + strCancion)

#    songsData[i] = lines

    songsData[i+1] = {}

    subLines = cancion.melody2.encodeTxt()
    songsData[i+1][2] = subLines[2:] # (salteo header)
    subLines = cancion.melody1.encodeTxt()
    songsData[i+1][1] = subLines[2:]
    subLines = cancion.melody3.encodeTxt()
    songsData[i+1][3] = subLines[2:]

  import json
  # exporto a json
  strJson = json.dumps(songsData, indent=2)
#  strJson = json.dumps(data)
  f = open(path + '/' + filename, 'w', encoding="utf-8")
  f.write('audio = \n' + strJson)
  f.close()



def exportSongsXml():
  """ exporta las canciones en formato xml """

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


  import xml.etree.cElementTree as ET
  root = ET.Element("songs")

  for i in range(0,30):
    cancion = canciones.canciones[i]

    lines = cancion.encodeTxt()
    strCancion = '\n'.join(lines)
#    print('strCancion: ' + strCancion)

    song = ET.SubElement(root, "song")
    song.text = strCancion

  tree = ET.ElementTree(root)
#  printed_xml = tree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True)
  ET.indent(root, space=" ", level=0)
  tree.write('./en/audio/songs.xml', xml_declaration=True, encoding='utf-8')
#  print('ET: ' + str(ET.tostring(root, encoding='UTF-8')))



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
  f = open(path + '/01_songs.txt', 'w', encoding="utf-8")
  f.write(strCanciones)
  f.close()

  for i in range(0,30):
    cancion = canciones.canciones[i]

    lines = cancion.encodeTxt()
    strCancion = '\n'.join(lines)
    f = open(path + '/song_{:02}.txt'.format(i), 'w', encoding="utf-8")
    f.write(strCancion)
    f.close()

    addr = cancion.melody2.addr
    length = len(cancion.melody2.encodeRom())

    addr = cancion.melody1.addr
    length = len(cancion.melody1.encodeRom())

    addr = cancion.melody3.addr
    length = len(cancion.melody3.encodeRom())

    # si quiere que compile lilypond
    if(exportLilypond):
      # exporto lilypond!
      cancion.exportLilypond()

def burnSongs(filepath, numBank, addrMusic):
  """ burn the songs into the rom """

  canciones = mystic.music.Canciones()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the songs from the txt
  canciones.decodeTxt(lines)

  # export to lilypond
  canciones.exportLilypond()

  # grabo las canciones en audio_noedit.js
  _exportSongsJson(canciones, 'audio_noedit.js')

  # address of the pointer table
#  nroBank,addrMusic = mystic.address.addrMusic
  arrayMusic = canciones.encodeRom(addrMusic)
  # burn into the rom
  mystic.romSplitter.burnBank(numBank, addrMusic, arrayMusic)

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  initAddr = 0x4000*numBank + addrMusic
  dataSize = len(arrayMusic)
  dataFilepath = path + '/01_songs.txt'
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

  vaPorAddr = addrMusic + len(arrayMusic)
  return vaPorAddr

def exportAudio():
  """ exports audio settings """

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

#  nroBank,addrAudio = mystic.address.addrAudio
  nroBank,addrAudio = 0x0f, 0x3a4f
  # cargo el banco 16 con los sonidos
  bank = mystic.romSplitter.banks[nroBank]
  vaPorAddr = addrAudio

  vibratos = mystic.audio.Vibratos()
  vibratos.decodeRom(bank, addrAudio)

  lines = vibratos.encodeTxt()
#  lines.append('')
#  lines.append('')

  strVibrato = '\n'.join(lines)
  f = open(path + '/02_vibrato.txt', 'w', encoding="utf-8")
  f.write(strVibrato)
  f.close()

  array = vibratos.encodeRom(vaPorAddr)
  vaPorAddr += len(array)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  volumes = mystic.audio.Volumes()
  volumes.decodeRom(bank, vaPorAddr)
  lines = volumes.encodeTxt()

  strVolume = '\n'.join(lines)
  f = open(path + '/03_volume.txt', 'w', encoding="utf-8")
  f.write(strVolume)
  f.close()

  array = volumes.encodeRom(vaPorAddr)
  vaPorAddr += len(array)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  waves = mystic.audio.Waves()
  waves.decodeRom(bank, vaPorAddr)
  lines = waves.encodeTxt()

  strWaves = '\n'.join(lines)
  f = open(path + '/04_waves.txt', 'w', encoding="utf-8")
  f.write(strWaves)
  f.close()

#  array = waves.encodeRom(vaPorAddr)
#  vaPorAddr += len(array)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))



def burnAudio(pathVibrato, pathVolume, pathWaves):
  """ burn the audio settings """

  array = []

  vibratos = mystic.audio.Vibratos()

  f = open(pathVibrato, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the audio from the txt
  vibratos.decodeTxt(lines)

#  lines = vibratos.encodeTxt()
#  strVibratos = '\n'.join(lines)
#  print('strVibratos: ' + strVibratos)

  # address of the pointer table
#  nroBank,addrAudio = mystic.address.addrAudio
  nroBank,addrAudio = 0x0f, 0x3a4f
  vaPorAddr = addrAudio

  arrayVibrato = vibratos.encodeRom(vaPorAddr)
  array.extend(arrayVibrato)
  vaPorAddr += len(arrayVibrato)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))



  volumes = mystic.audio.Volumes()

  f = open(pathVolume, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the audio from the txt
  volumes.decodeTxt(lines)

  arrayVolume = volumes.encodeRom(vaPorAddr)
#  print('arrayVolume: ' + mystic.util.strHexa(arrayVolume))
  array.extend(arrayVolume)
  vaPorAddr += len(arrayVolume)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))



  waves = mystic.audio.Waves()

  f = open(pathWaves, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the audio from the txt
  waves.decodeTxt(lines)

  arrayWaves = waves.encodeRom(vaPorAddr)
#  print('arrayWaves: ' + mystic.util.strHexa(arrayWaves))
  array.extend(arrayWaves)
  vaPorAddr += len(arrayWaves)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  # burn into the rom
  mystic.romSplitter.burnBank(0xf, addrAudio, array)



def exportSounds():
  """ exports the sound effects """

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

#  nroBank,addrSounds = mystic.address.addrSounds
  nroBank,addrSounds = 0x0f, 0x3b3c
  # cargo el banco 16 con los sonidos
  bank = mystic.romSplitter.banks[nroBank]

  sounds = mystic.sounds.Sounds()
  sounds.decodeRom(bank,addrSounds)

  lines = sounds.encodeTxt()
#  lines.append('')
#  lines.append('')

  strSFX = '\n'.join(lines)
  f = open(path + '/05_sounds.txt', 'w', encoding="utf-8")
  f.write(strSFX)
  f.close()

def burnSounds(filepath):
  """ burn the SFX into the rom """

  sounds = mystic.sounds.Sounds()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the songs from the txt
  sounds.decodeTxt(lines)

#  lines = sounds.encodeTxt()
#  strSFX = '\n'.join(lines)
#  print('strSFX: ' + strSFX)

  # address of the pointer table
#  nroBank,addrMusic = mystic.address.addrSounds
  numBank,addrSounds = 0x0f, 0x3b3c
  arraySounds = sounds.encodeRom(addrSounds)

#  print('arraySounds: ' + mystic.util.strHexa(arraySounds))
  # burn into the rom
  mystic.romSplitter.burnBank(0xf, addrSounds, arraySounds)
#  mystic.romSplitter.burnBank(0xf, 0x3bd0, arraySounds)

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  initAddr = 0x4000*numBank + addrSounds
  dataSize = len(arraySounds)
  dataFilepath = path + '/05_sounds.txt'
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)




def exportHero():
  """ exports the hero sprite data """

#  print('--- 1:0752')

  basePath = mystic.address.basePath
  path = basePath + '/npc'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  numBank,addrHero = mystic.address.addrHero
  bank = mystic.romSplitter.banks[numBank]


  jsonHero = {}
  jsonHero['spriteGroups'] = []


  spriteGroup = {}
  spriteGroup['idSpriteGroup'] = 0
  spriteGroup['comment'] = 'hero'
  spriteGroup['sprites'] = []

  currentAddr = addrHero

  for j in range(0,4):
   
    subArray = bank[currentAddr:currentAddr+3]
#    print('subArray: ' + mystic.util.strHexa(subArray))

    attrib = subArray[0]
    tile1 = subArray[1]
    tile2 = subArray[2]

    strAttrib = '{:02x}'.format(attrib)
    strTile1 = '{:02x}'.format(tile1)
    strTile2 = '{:02x}'.format(tile2)

    spriteGroup['sprites'].append({'idSprite' : j, 'attrib' : strAttrib, 'tile1' : strTile1, 'tile2' : strTile2})
    currentAddr += 3

  jsonHero['spriteGroups'].append(spriteGroup)

  jsonHero['sortTiles'] = []

  cantidad = 22
  for j in range(0,cantidad):
   
    subArray = bank[currentAddr:currentAddr+16]

    strSortTiles = mystic.util.strHexa(subArray)
#    print('subArray: ' + strSortTiles)

    jsonHero['sortTiles'].append({'idSortTiles' : j, 'comment' : mystic.variables.hero[j], 'sorting' : strSortTiles})
    currentAddr += 16


  import json
  # for allowing kana characters in json ensure_ascii=False
  strJson = json.dumps(jsonHero, indent=2, ensure_ascii=False)
#  strJson = json.dumps(data)
  f = open(path + '/hero.js', 'w', encoding="utf-8")
  f.write('hero = \n' + strJson)
  f.close()

def burnHero(filepath):

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

  numBank,addrHero = mystic.address.addrHero

  array = []

  arraySpriteGroup = []
  spriteGroups = jsonHero['spriteGroups']
  spriteGroup = spriteGroups[0]
  for sprite in spriteGroup['sprites']:
#    print('sprite: ' + str(sprite))
    attrib = int(sprite['attrib'],16)
    tile1 = int(sprite['tile1'],16)
    tile2 = int(sprite['tile2'],16)
    subArray = [attrib, tile1, tile2]
    arraySpriteGroup.extend(subArray)
#    currentAddr += 3
  
  arraySortTiles = []

  i = 0
  for sortTile in jsonHero['sortTiles']:
#    print(' --- sortTile: ' + str(sortTile))
#    dicSortTiles[i] = currentAddr
    strSortT = sortTile['sorting']
    subArray = mystic.util.hexaStr(strSortT.strip())
#    print('subArray: ' + mystic.util.strHexa(subArray))
    arraySortTiles.extend(subArray)
#    currentAddr += len(subArray)
    i += 1

#  print('currentAddr: {:04x}'.format(currentAddr))
  
  array.extend(arraySpriteGroup)
  array.extend(arraySortTiles)

  mystic.romSplitter.burnBank(numBank, addrHero, array)

  basePath = mystic.address.basePath
  path = basePath + '/npc'
  initAddr = 0x4000*numBank + addrHero
  dataSize = len(array)
  dataFilepath = path + '/hero.js'
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)


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
#  path = basePath + '/spriteSheetPersonajes'
  path = basePath + '/tilesetsLevel2'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

#  if(True):
  if(False):
    for banco in range(0,0x10):
      for nro in range(0,4):

        bank = mystic.romSplitter.banks[banco]
        array = bank[0x1000*nro:0x1000*(nro+1)]

        w, h = 8,8
#        w, h = 4,16
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

    i += 1

def burnSpriteSheetPersonajes():

  basePath = mystic.address.basePath
#  path = basePath + '/spriteSheetPersonajes'
  path = basePath + '/tilesetsLevel2'


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
  path = basePath + '/maps'
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
  filepath = path + '/maps_noedit.txt'
  f = open(filepath, 'w', encoding="utf-8")
  strTxt = '\n'.join(lines)
  f.write(strTxt)
  f.close()

#  mapa = mapas.mapas[0]
#  if(True):
  # para cada mapa
  for mapa in mapas.mapas:

    print('map: {:02x}'.format(mapa.nroMapa))

    # lo exporto a .txt
    lines = mapa.encodeTxt()
    strMapa = '\n'.join(lines)
    f = open(path + '/map_{:02}_{:02x}_noedit.txt'.format(mapa.nroMapa, mapa.nroMapa), 'w', encoding="utf-8")
    f.write(strMapa + '\n')
    f.close()

    # exporto a formato .tmx para Tiled
    mapa.exportTiledXml(path + '/map_{:02}_{:02x}.tmx'.format(mapa.nroMapa, mapa.nroMapa))

    # exporto a formato .json
    mapa.exportJs(path + '/map_{:02}_{:02x}.js'.format(mapa.nroMapa, mapa.nroMapa))

    if(exportPngFile):
      mapa.exportPngFile(path + '/map_{:02}_{:02x}_noedit.png'.format(mapa.nroMapa, mapa.nroMapa))

    # verifico volviendo a encodearlo
    subArray = mapa.encodeRom(mapa.mapAddr)

#    filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#    mystic.util.arrayToFile(subArray, filepath)
#    iguales = mystic.util.compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#    print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))


def burnMapas(filepath):

  basePath = mystic.address.basePath
  path = basePath + '/maps'

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
  path = basePath + '/maps'

  mapas = mystic.maps.Mapas()

  # por cada mapa
#  for i in range(0,1):
  for i in range(0,0x10):

    filepath = path + '/map_{:02}_{:02x}.js'.format(i,i)
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
  path = basePath + '/maps'

  mapas = mystic.maps.Mapas()

  # por cada mapa
#  for i in range(0,1):
  for i in range(0,0x10):

    filepath = path + '/map_{:02}_{:02x}.tmx'.format(i,i)
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

#    print('burning map {:02x} at {:02x}:{:04x}'.format(sortedNro, mapa.mapBank, mapa.mapAddr))
#    print('burning map at {:02x}:{:04x}'.format(mapa.mapBank, mapa.mapAddr))

    basePath = mystic.address.basePath
    path = basePath + '/maps'
    initAddr = 0x4000*mapa.mapBank + mapa.mapAddr
    dataSize = len(subArray)
    dataFilepath = path + '/map_{:02}_{:02x}.tmx'.format(sortedNro, sortedNro)
    mystic.romStats.appendData(initAddr, dataSize, dataFilepath)



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
        chars = mystic.dictionary.decodeByte(hexy, True)
        traduc += chars
      addr = '{:04x}'.format(i - 0x10)
      g.write(addr + ' | ' + strhexs + '| ' + traduc + '\n')
      renglon = []

    i+=1

  g.close()



def burnInitialScript(nroScript):
  """ setea el script inicial a ejecutar cuando inicia el juego sin battery """

  bank02 = mystic.romSplitter.banks[0x02]
#  address = mystic.address.addrScriptAddrDic
#  address = 0x3cfe
  address = 0x3cec

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
  shutil.copyfile('./mystic/sound-engine.js', basePath + '/sound-engine.js')


def burnMScripts(filepath):
  """ compila el mscripts.txt indicado y quema los scripts en los bancos 0x0d y 0x0e, y el dicionario de addrs en banco 0x08 """

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

    basePath = mystic.address.basePath
    path = basePath + '/scripts'
    initAddr = 0x4000*vaPorBank + 0x0000
    dataSize = len(encodedBank)
    dataFilepath = path + '/jscripts.js'
    mystic.romStats.appendData(initAddr, dataSize, dataFilepath)

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


def burnExpTable(filepath):
  """ quema el exp.txt en la rom """

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

  numBank,addrExp = mystic.address.addrExpTable

  strArray = mystic.util.strHexa(array)
#  print('strArray: ' + strArray)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(numBank, addrExp, array)

  basePath = mystic.address.basePath
  path = basePath
  initAddr = 0x4000*numBank + addrExp
  dataSize = len(array)
  dataFilepath = path + '/exp.txt'
  mystic.romStats.appendData(initAddr, dataSize, dataFilepath)


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

