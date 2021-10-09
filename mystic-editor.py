#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

# command line arguments
import sys

# pip3 install pypng
import png

# los idiomas
ENGLISH = 0
FRENCH = 1
GERMAN = 2
JAPAN = 3

# los md5sum de las rom stock originales
stockRomsMd5 = ['24cd3bdf490ef2e1aa6a8af380eccd78',
                '2efe1569e3be81e7e19b13eafc60cd24',
                'b6a08c7e3af4ec8c9559cd268115d97c',
                '3b359e9fec183bff5f964e25b599b246']

# los idiomas de las rom stock originales
stockRomsLang = ['en', 'fr', 'de', 'jp']
stockRomsLanguage = ['english', 'french', 'deutsch', 'japan']


def printHelp():
  print('mystic-editor v0.95')
  print('Usage:')
  print('  mystic-editor.py <command>')
  print('    where <command> should be one of "-d", "--decode", "-e", "--encode" ')
  print('Examples:')
  print('  mystic-editor.py -d         (decodes a rom)')
  print('  mystic-editor.py -e         (encodes a rom)')
  print('The rom should be placed in this folder')
  print('------------------------------------------------------------')


############################################
class Singleton:
  """
  A non-thread-safe helper class to ease implementing singletons.
  This should be used as a decorator -- not a metaclass -- to the
  class that should be a singleton.

  The decorated class can define one `__init__` function that
  takes only the `self` argument. Also, the decorated class cannot be
  inherited from. Other than that, there are no restrictions that apply
  to the decorated class.

  To get the singleton instance, use the `instance` method. Trying
  to use `__call__` will result in a `TypeError` being raised.
  """

  def __init__(self, decorated):
    self._decorated = decorated

  def instance(self):
    """
    Returns the singleton instance. Upon its first call, it creates a
    new instance of the decorated class and calls its `__init__` method.
    On all subsequent calls, the already created instance is returned.
    """
    try:
      return self._instance
    except AttributeError:
      self._instance = self._decorated()
      return self._instance

  def __call__(self):
    raise TypeError('Singletons must be accessed through `instance()`.')

  def __instancecheck__(self, inst):
    return isinstance(inst, self._decorated)


##########################################################
@Singleton
class Util:
 
  def fileToArray(self, filepath):

    array = []

    dataBytes = []
    with open(filepath, 'rb') as f:
      # leo el .bpp
      dataBytes = f.read()

    for byte in dataBytes:
      array.append(byte)

    return array

  def arrayToFile(self, array, filepath):

    f = open(filepath, 'wb')
    f.write( bytes(array) )
    f.close()


  def md5sum(self, filepath):
    """ calcula el md5sum de un archivo """
    import hashlib
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


  def strHexa(self, bytes):
    """ convierte array de bytes en string hexa """

    string = ''
    for byte in bytes:
      string += '{:02x} '.format(byte)
    return string

  def hexaStr(self, strHexa):
    """ convierte string hexa en array de bytes """

    hexas = []
    strHexas = strHexa.split(' ')
    for strHexa in strHexas:
      hexa = int(strHexa, 16)
#      print('strHexa: ' + strHexa)
#      print('hexa: {:02x}'.format(hexa))
      hexas.append(hexa)

    return hexas

  def pngToArray(self, filepath):
    """ dado un archivo.png devuelve matriz de int con sus colores """

    f = open(filepath, 'rb')
    r = png.Reader(f)
    data = r.read()

    rows = list(data[2])

    array = []
    for row in rows:
      newRow = []
      for color in row:
        # invierto los colores (en el gb funcionan asi)
#        newColor = 3 - color
        newColor = 3 - color//(255//3)
        newRow.append(newColor)

      array.append(newRow)

    return array

  def arrayToPng(self, array, w, h, filepath):
    """ dada una matriz de int representando colores, sus dimensiones, y el filepath, lo graba en un archivo.png """

    for j in range(0,h):
      for i in range(0,w):
        # invierto los colores (en el gb funcionan asi)
#        array[j][i] = 3 - array[j][i]
        array[j][i] = 255 - array[j][i]*(255//3)

    f = open(filepath, 'wb')
#    w = png.Writer(w, h, greyscale=True, bitdepth=2)
    w = png.Writer(w, h, greyscale=True)
    w.write(f, array)
    f.close()


  def compareFiles(self, filepath1, filepath2, idx0, cantBytes):
    """ compara si dos archivos binarios son iguales entre los índices indicados """

    iguales = True

    f = open(filepath1, 'rb')
    g = open(filepath2, 'rb')
    array1 = f.read()
    array2 = g.read()
    f.close()
    g.close()

    for i in range(0, cantBytes):

      byte1 = array1[idx0 + i]
      byte2 = array2[i]

#      print('addr: {:04x} - byte1: {:02x} - byte2: {:02x}'.format(idx0 + i, byte1,byte2))

      # si son distintos
      if(byte1 != byte2):
        iguales = False

        print('byte1, byte2 = {:02x}, {:02x}'.format(byte1,byte2))

        print('diferencia en addr: {:04x}'.format(idx0 + i))
        break

    return iguales

##########################################################
@Singleton
class Address:
  """ los addr según el idioma """

  def __init__(self):

    # valor por default
    self.language = ENGLISH
    self.romPath = './roms/en.gb'
    self.romName = 'en'
    self.basePath = './en'

    # cosas de scripts
    self.addrScriptAddrDic_en = 0x0f05
    self.addrScriptAddrDic_de = 0x0f11
    self.addrScriptAddrDic_fr = 0x0f11
    self.addrScriptAddrDic_jp = 0x0ef9
    self.addrScriptAddrDic = self.addrScriptAddrDic_en

    self.cantScripts_en = 0x054a
    self.cantScripts_de = 0x054d
    self.cantScripts_fr = 0x054d
    self.cantScripts = self.cantScripts_en

    # cosas del diccionario
    self.addrDictionary_en = 0x3f1d
    self.addrDictionary_de = 0x3f3f
    self.addrDictionary_fr = 0x3f30
    self.addrDictionary_jp = 0x3f72
    self.addrDictionary = self.addrDictionary_en

    self.cantDictionary_en = 112
    self.cantDictionary_de = 96
    self.cantDictionary_fr = 96
    self.cantDictionary_jp = 0 # no se usa
    self.cantDictionary = self.cantDictionary_en

    # la intro en el bank02
    self.addrIntro_en = 0x3e8a
    self.addrIntro_de = 0x3ed8
    self.addrIntro_fr = 0x3eb3
    self.addrIntro_jp = 0x3e48
    self.addrIntro = self.addrIntro_en

    # listado de magia en el bank02
    self.addrMagic_en = 0x1dda
    self.addrMagic_de = 0x1de4
    self.addrMagic_fr = 0x1de4
    self.addrMagic_jp = 0x1f65
    self.addrMagic = self.addrMagic_en


    # los offsets de 'world map', 'village', 'interior casa', 'interior cueva' y 'intro' respectivamente en el bank08
    self.spriteSheetsAddr = [0x00b0, 0x03b0, 0x06b0, 0x0938, 0x0c1a]
    # cantidad de sprites de cada spriteSheet
    self.cantSpritesInSheet = [0x80, 0x80, 0x6c, 0x7b, 0x4d]


  def detectRomLanguage(self, romPath):
    """ detecta el idioma de la rom """

    # si no existe la rom
    if not os.path.exists(romPath):
      print(romPath + ': file not found')
      # termino con mensaje de error
      sys.exit(1)

    # sino
    else:

      # abro la rom
      array = Util.instance().fileToArray(romPath)
      # agarro los dos últimos bytes del bank0
      subArray = array[0x4000-2 : 0x4000]
      val = subArray[1]*0x100 + subArray[0]
#      print('val {:04x}'.format(val))

      if(val == 0x0000):
        lang = ENGLISH
        print(romPath + ': english rom detected')
      elif(val == 0xA34A):
        lang = FRENCH
        print(romPath + ': french rom detected')
      elif(val == 0xA3DA):
        lang = GERMAN
        print(romPath + ': german rom detected')
      elif(val == 0xcf00):
        lang = JAPAN
        print(romPath + ': japan rom detected')

      else:
        lang = -1
        print(romPath + ': unable to detect language')
        # termino con mensaje de error
        sys.exit(1)

    # configuro el address
    self.configure(romPath, lang)

    return lang

  def configure(self, romPath, language):

    # el idioma de la rom
    self.language = language

    # el romPath (ej: './roms/de.gb')
    self.romPath = romPath
    idx0 = romPath.rindex('/')+1
    idx1 = romPath.rindex('.')
    romName = romPath[idx0:idx1]
    # el romName (ej: 'de')
    self.romName = romName
    # el path a la carpeta de base
    self.basePath = './' + self.romName

    if(self.language == ENGLISH):
      self.addrDictionary = self.addrDictionary_en
      self.cantDictionary = self.cantDictionary_en
      self.addrScriptAddrDic = self.addrScriptAddrDic_en
      self.cantScripts = self.cantScripts_en

      self.addrIntro = self.addrIntro_en
      self.addrMagic = self.addrMagic_en

    elif(self.language == FRENCH):
      self.addrDictionary = self.addrDictionary_fr
      self.cantDictionary = self.cantDictionary_fr
      self.addrScriptAddrDic = self.addrScriptAddrDic_fr
      self.cantScripts = self.cantScripts_fr

      self.addrIntro = self.addrIntro_fr
      self.addrMagic = self.addrMagic_fr

    elif(self.language == GERMAN):
      self.addrDictionary = self.addrDictionary_de
      self.cantDictionary = self.cantDictionary_de
      self.addrScriptAddrDic = self.addrScriptAddrDic_de
      self.cantScripts = self.cantScripts_de
 
      self.addrIntro = self.addrIntro_de
      self.addrMagic = self.addrMagic_de

    elif(self.language == JAPAN):
      self.addrDictionary = self.addrDictionary_jp
      self.cantDictionary = self.cantDictionary_jp
      self.addrScriptAddrDic = self.addrScriptAddrDic_jp
      self.cantScripts = self.cantScripts_en # ??

      self.addrIntro = self.addrIntro_jp
      self.addrMagic = self.addrMagic_jp


##########################################################
@Singleton
class RomStats:
  """ estadísticas de los banks """

  def __init__(self):
    # los bancoDatas
    self.banks = []

    for k in range(0,0x10):
      # los creo en gris
      bancoData = [ (0xe0, 0xe0, 0xe0) for i in range(0,0x80 * 0x80)]
      self.banks.append(bancoData)

    # los datos de que info hay en que parte de que bloques
    self.datos = []

  def appendDato(self, banco, iniAddr, finAddr, color, descrip):
    """ agrega un dato a la info de los bancos """
    self.datos.append( (banco, iniAddr, finAddr, color, descrip) )

  def exportPng(self):

    from PIL import Image, ImageColor

    # creo data en blanco para contener los 16 bancos
    imgData = [ (0xff, 0xff, 0xff) ]*(0x200*0x200)

    width, height = 0x200, 0x200
    img = Image.new('RGB', (width, height))
    img.putdata(imgData)
    pixels = img.load()

    # para cada dato
    for dato in self.datos:
      banco   = dato[0]
      iniAddr = dato[1]
      finAddr = dato[2]
      color   = dato[3]
      descrip = dato[4]

#      print('procesando en banco: {:02x}'.format(banco))

      # agarro el bancoData correspondiente
      bancoData = self.banks[banco]

      # el intervalo indicado
      for i in range(iniAddr, finAddr):
        # lo coloreo del color indicado
        bancoData[i] = color

#      self.banks[banco] = bancoData

    # para cada uno de los 16 bancos
    for j in range(0,4):
      for i in range(0,4):

        # agarro el bancoData correspondiente
        bancoData = self.banks[j*4+i]

        imgBank = Image.new('RGB', (0x80, 0x80))
        imgBank.putdata(bancoData)

        x = 0x80*i
        y = 0x80*j
        img.paste(imgBank, (x,y, x+0x80, y+0x80))


    # creo las rayas horizontales
    for i in range(0,0x200):
      j = 1*0x200//4
      pixels[i,j] = (0x00, 0x00, 0x00)
      j = 2*0x200//4
      pixels[i,j] = (0x00, 0x00, 0x00)
      j = 3*0x200//4
      pixels[i,j] = (0x00, 0x00, 0x00)
    # y verticales
    for j in range(0,0x200):
      i = 1*0x200//4
      pixels[i,j] = (0x00, 0x00, 0x00)
      i = 2*0x200//4
      pixels[i,j] = (0x00, 0x00, 0x00)
      i = 3*0x200//4
      pixels[i,j] = (0x00, 0x00, 0x00)


    basePath = Address.instance().basePath
    # grabo la imagen
    img.save(basePath + '/rom_info.png')




 
##########################################################
@Singleton
class RomSplitter:
  """ splitea una rom en bankos de 0x4000 """

  def __init__(self):
    # la rom
    self.rom = []
    # los bancos
    self.banks = []
    # los cinco tilesets
    self.tilesets = []
    # los cinco spriteSheets
    self.spriteSheets = []
    # los mapas
#    self.mapas = None


  def get(self, bank, offset):
    hexa = self.banks[bank][offset]
    return hexa

  def set(self, bank, offset, hexa):
    self.banks[bank][offset] = hexa

  def getTileset(self, nroTileset):
    tileset = self.tilesets[nroTileset]
    return tileset

  def protectStockRoms(self):
    """ hace copia de seguridad de las roms stock """

    basePath = Address.instance().basePath
    path = './stockRoms'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    mypath = './'
    # agarro la lista de archivos de la carpeta actual
    files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

    # para cada archivo
    for fil in files:
      # calculo su md5
      md5 = Util.instance().md5sum(fil)
#      print(md5 + ' - ' + fil)
      # si es un md5 de stock rom original
      if(md5 in stockRomsMd5):
        idx = stockRomsMd5.index(md5)
        # me fijo en que idioma está
        lang = stockRomsLang[idx]
        langPath = './stockRoms/' + lang + '.gb'
        # si no está entre las roms stock
        if not os.path.exists(langPath):
          # copio la rom
          shutil.copyfile(fil, langPath)

        romPath = langPath
        language = idx
        Address.instance().configure(romPath, language)
        RomSplitter.instance().configure()
        # exporto música gbs
        RomSplitter.instance().exportGbsRom('./stockRoms/gbs_' + lang + '.gb')


  def configure(self):
    """ lo preparo para splitear la rom indicada """

    romPath = Address.instance().romPath

    self.rom = []
    self.banks = []
    f = open(romPath, 'rb')
    while True:
      piece = f.read(0x4000)

      listPiece = list(piece)

      if(len(piece) == 0):
        break

      # lo agrego a la lista de bancos
      self.banks.append(listPiece)
      self.rom.extend(listPiece)

    f.close()


  def cleanBank(self, banco):
    """ pone un banco en 0x00 """

    clean = [0x00] * 0x4000
    self.banks[banco] = clean

  def clean(self):
    """ borro la carpeta de split de la rom indicada """

    romName = Address.instance().romName

    # si el directorio existía
    if os.path.exists(romName):
      # lo borro 
      shutil.rmtree(romName)


  def split(self):
    """ parte una rom en banks """

    basePath = Address.instance().basePath
    romPath = Address.instance().romPath
    romName = Address.instance().romName

    # si el directorio no existía
    if not os.path.exists(romName):
      # lo creo
      os.makedirs(romName)

    # copio la rom
    shutil.copyfile(romPath, basePath + '/' + romName + '.gb')

#    for i in range(0, 0x10):
    i = 0x00
    for bank in self.banks:
      bank = self.banks[i]

#      banco = 'bank_' + hex(i)[2:].zfill(2)
      banco = 'bank_' + str(i).zfill(2)
      folderName = romName + '/banks/' + banco 

      # si el directorio no existía
      if not os.path.exists(folderName):
        # creo la carpeta del banco
        os.makedirs(folderName)

      # creo el archivo binario del banco
      filepath = romName + '/banks/' + banco + '/' + banco + '.bin'
      RomSplitter.instance().exportBank(i, filepath)
      i += 1


  def exportBank(self, nroBank, filepath):

    # creo el archivo binario del banco
    g = open(filepath, 'wb')
    bank = self.banks[nroBank]
    bytesbank = bytes(bank)
    g.write(bytesbank)
    g.close()



  def pattern(self):

#    pattern = 'abbba'
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

    array = RomSplitter.instance().rom

    iArr = 0
    for byty in array:

#      print('byty: ' + hex(byty))

      # agarro la letra del pattern que toca
      patKey = pattern[iPat]
#      print('patKey: ' + patKey)

      if(patKey == '*'):
        iPat += 1
      else:

        # si la letra ya estaba en el dic
        if(patKey in dic.keys()):
          # agarro el byty pattern
          bytyPat = dic[patKey]
#          print('tenia bytyPat: ' + hex(bytyPat))
        # sino
        else:

          # si el byty no estaba en los values anteriores
          if(byty not in dic.values()):
            # creo el byty pattern
            bytyPat = byty
            # lo seteo a la letra
            dic[patKey] = bytyPat
#            print('creamos bytyPat: ' + hex(bytyPat))
          # sino, el key ya estaba
          else:
            bytyPat = None
#            print('poniendo noneee!')


        # si el byty pattern coincide con el byty
        if(bytyPat == byty):
          # incremento la cuenta
          iPat += 1
        else:
          iPat = 0
          dic = {}

      if(iPat == len(pattern)):
#        print(' --- byty: ' + hex(byty)[2:].zfill(2) + ' - key: ' + pattern[0:iPat+1])
        patron = array[iArr - iPat + 1: iArr+1]
#        print('patron: ' + str(patron))

        strhex = ''
        for num in patron:
          strhex += hex(num)[2:].zfill(2) + ' '
#        strhex = self.bytesDecode(patron)
        print('addr: ' + hex(iArr)[2:].zfill(6) + ' - strhex: ' + strhex)
        iPat = 0
        dic = {}

      iArr += 1
   

  def pattern2(self):

#    pattern = 'ababababababab'

    array = RomSplitter.instance().rom

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


#        strhex = self.bytesDecode(patron)
        print('addr: ' + hex(iArr)[2:].zfill(6) + ' - strhex: ' + strhex)
 
      iArr += 1

  def exportGfx(self):
    """ convierte los banks .bin en .png """

    basePath = Address.instance().basePath

    i = 0x00
    for bank in self.banks:
      # para cada una de las 4 paletas del banko
      for nroTileset in range(0,4):
        # creo el tileset
        tileset = Tileset(16,16)

        array = bank[0x1000*nroTileset:0x1000*(nroTileset+1)]        

        tileset.decodeRom(array)

        filepath = basePath + '/banks/bank_{:02}/tileset_{:02}_{:02}.png'.format(i, i, nroTileset)
#        print(filepath)
        tileset.exportPngFile(filepath)
      i += 1


  def exportFont(self):

    basePath = Address.instance().basePath

    bank = RomSplitter.instance().banks[8]
    # creo el tileset
    tileset = Tileset(16,9)

    array = bank[0x1000*2+7*0x100:0x1000*(2+1)]

    tileset.decodeRom(array)
    tileset.exportPngFile(basePath + '/font.png')

  def burnFont(self):

    basePath = Address.instance().basePath

    tileset = Tileset(16,9)
    tileset.importPngFile(basePath + '/font.png')
    array = tileset.encodeRom()

    RomSplitter.instance().burnBank(8, 0x1000*2+7*0x100, array)

  def exportTilesets(self):
    """ exporta los cinco tilesets """

    basePath = Address.instance().basePath
    path = basePath + '/tilesets'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    self.tilesets = []
    # para cada uno de los cinco tilesets
    for nroTileset in range(0,5):

      import random
      rr = random.randint(0,0xff)
      gg = random.randint(0,0xff)
      bb = random.randint(0,0xff)

      # para los primeros 4 tilesets
      if(nroTileset < 4):
        tileset = Tileset(16,16)
        banco12 = RomSplitter.instance().banks[12]
        array = banco12[0x1000*nroTileset:0x1000*(nroTileset+1)]
        tileset.decodeRom(array)

        # agrego info al stats
        RomStats.instance().appendDato(0x0c, 0x1000*nroTileset, 0x1000*(nroTileset+1) , (rr, gg, bb), 'un tileset')

      # sino, para el 5to tileset
      else:
        tileset = Tileset(16,13)
        banco11 = RomSplitter.instance().banks[11]
        array = banco11[0x0000:0x0d00]
        tileset.decodeRom(array)

        # agrego info al stats
        RomStats.instance().appendDato(0x0b, 0x0000, 0x0d00, (rr, gg, bb), 'un tileset')


      tileset.exportPngFile(path + '/tileset_{:02}.png'.format(nroTileset))

      self.tilesets.append(tileset)

  def burnTilesets(self):

    basePath = Address.instance().basePath
    path = basePath + '/tilesets'
 
    # para cada uno de los cinco tilesets
    for nroTileset in range(0,5):

      # para los primeros 4 tilesets
      if(nroTileset < 4):
        tileset = Tileset(16,16)
        tileset.importPngFile(path + '/tileset_{:02}.png'.format(nroTileset))
        array = tileset.encodeRom()
        RomSplitter.instance().burnBank(12, 0x1000*nroTileset, array)

      # sino, para el 5to tileset
      else:
        tileset = Tileset(16,13)
        tileset.importPngFile(path + '/tileset_{:02}.png'.format(nroTileset))
        array = tileset.encodeRom()
        RomSplitter.instance().burnBank(11, 0x0000, array)


  def exportSpriteSheets(self):
    """ exporta los spritesheets del bank 12 """

    basePath = Address.instance().basePath
    path = basePath + '/spriteSheets'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    sheetNames = ['worldmap', 'city', 'inner', 'cave', 'title']
    self.spriteSheets = []
    # para cada una de los cinco spriteSheets 
    for nroSpriteSheet in range(0,5):

      sheet = SpriteSheet(16,8,nroSpriteSheet,sheetNames[nroSpriteSheet])

      addr = Address.instance().spriteSheetsAddr[nroSpriteSheet]
      cant = Address.instance().cantSpritesInSheet[nroSpriteSheet]
      bank08 = RomSplitter.instance().banks[8]
      array = bank08[addr:addr+6*cant]
      sheet.decodeRom(array)
      # lo agrego a la lista
      self.spriteSheets.append(sheet)

      lines = sheet.encodeTxt()
      string = '\n'.join(lines)
      f = open(basePath + '/spriteSheets/sheet_{:02}.txt'.format(nroSpriteSheet), 'w')
      f.write(string)
      f.close()

      sheet.exportPngFile(basePath + '/spriteSheets/sheet_{:02}.png'.format(nroSpriteSheet))

      sheet.exportTiled(basePath + '/spriteSheets/sheet_{:02}.tsx'.format(nroSpriteSheet))


  def exportPersonajes(self):
    """ exporta los personajes """

#    print('--- 3:1f5a')

    basePath = Address.instance().basePath
    path = basePath + '/personajes'

    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    f = open(path + '/personajes.txt', 'w')

    bank = RomSplitter.instance().banks[0x03]
    array = bank[0x1f5a:]

    personajes = []
#    for i in range(0,10):
    for i in range(0,191):
      subArray = array[:24]
      strSubarray = Util.instance().strHexa(subArray)
#      print('strSub: {:02x} {:03} {:04x} = '.format(i,i, 0x1f5a+i*24) + strSubarray)
      array = array[24:]

      pers = Personaje(i)
      pers.decodeRom(subArray)
      personajes.append(pers)

      lines = pers.encodeTxt()
      strPersona = '\n'.join(lines)

      f.write(strPersona)
      
#      print('pers {:02x} {:03} {:04x} := '.format(i, i, 0x1f5a+i*24) + str(pers))
#      personajes.append( (i,pers) )

#    for i,pers in personajes:
#      if(pers.amistad != 0x81):
#        print('pers {:02x} {:03} {:04x} := '.format(i, i, 0x1f5a+i*24) + str(pers))
#    print('----')
#    for i,pers in personajes:
#      if(pers.amistad == 0x81):
#        print('pers {:02x} {:03} {:04x} := '.format(i, i, 0x1f5a+i*24) + str(pers))
#    print('----')

    f.close()

#    ies = [0x7b, 0x7c]
#    ies = [0x12, 0x13]
#    ies = [0x12, 0x13, 0x7b, 0x7c]
#    for i in ies:
#    i = 0x7b  #nena
#    i = 0x7c  #nene
#      array = bank[0x1f5a:]
#      nene = array[24*i:]
#      subArray = nene[:24]
#      strSubarray = Util.instance().strHexa(subArray)
#      print('strSub: {:02x} {:03} {:04x} = '.format(i,i, 0x1f5a+i*24) + strSubarray)

#      pers = Personaje(i)
#      pers.decodeRom(subArray)
#      print('pers {:02x} {:03} {:04x} := '.format(i, i, 0x1f5a+i*24) + str(pers))

    length = 24*len(personajes)
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    RomStats.instance().appendDato(0x03, 0x1f5a, 0x1f5a+length, (rr, gg, bb), 'personajes')

  def burnPersonajes(self, filepath):
    """ quema los personajes en la rom """

    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()

    i = 0
    personajes = []
    primero = True
    subLines = []
    for line in lines:
#      print('line: ' + line)
      if('------------ personaje' in line):
        if(not primero):
          p = Personaje(i)
          p.decodeTxt(subLines)
          personajes.append(p)
          i += 1
          subLines = []
        else:
          primero = False

      subLines.append(line)
    p = Personaje(i)
    p.decodeTxt(subLines)

    array = []
    for p in personajes:
#      print('p: ' + str(p)) 
      subArray = p.encodeRom()
      array.extend(subArray)

#    Util.instance().arrayToFile(array, './game/personajes/p.bin')
#    iguales = Util.instance().compareFiles('./game/banks/bank_03/bank_03.bin', './game/personajes/p.bin', 0x1f5a, len(array))
#    print('iguales = ' + str(iguales))

    RomSplitter.instance().burnBank(0x3, 0x1f5a, array)




  def exportGrupos3Personajes(self):
    """ exporta grupos de 3 personajes a cargar """

    basePath = Address.instance().basePath
    path = basePath + '/personajes'

    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    # 3:4456  ld de,$7142
#    print('--- 3:3142')

    vaPorAddr = 0x3142
    bank = RomSplitter.instance().banks[0x03]
    array = bank[0x3142:]

    grupos = GruposPersonajes(0x3142)
    grupos.decodeRom(array)

    lines = grupos.encodeTxt()

    strGrupos = '\n'.join(lines)

    f = open(path + '/grupos3Personajes.txt', 'w')
    f.write(strGrupos)
    f.close()


  def burnGrupos3Personajes(self, filepath):
    """ quema los grupos de 3 personajes """

    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()

    grupos = GruposPersonajes(0x3142)
    grupos.decodeTxt(lines)

    array = grupos.encodeRom()

    RomSplitter.instance().burnBank(0x3, 0x3142, array)

#    Util.instance().arrayToFile(array, './game/personajes/grupos.bin')
#    iguales = Util.instance().compareFiles('./game/banks/bank_03/bank_03.bin', './game/personajes/grupos.bin', 0x3142, len(array))
#    print('iguales = ' + str(iguales))

   

  def exportCosasRarasPersonajes(self):
    """ exporta cosas raras del banco 3 """

    print('--- 3:3b56')
    bank = RomSplitter.instance().banks[0x03]
    array = bank[0x3b56:]

    line = array[:4]
    strLine = Util.instance().strHexa(line)
    print('header?     : ' + strLine)

    array = array[4:]
    line = array[:16]
    strLine = Util.instance().strHexa(line)
    print('cosasTiles? : ' + strLine)

    array = array[16:]
    line = array[:8]
    strLine = Util.instance().strHexa(line)
    print('masCositas? : ' + strLine)



  def exportPersonajesDobleTile(self):
    """ exporta los doble tiles de los personajes """

    print('--- 3:3b72')
    bank = RomSplitter.instance().banks[0x03]
    array = bank[0x3b72:]

    for i in range(0,371):

#      line = array[:3]

      modo  = array[3*i+0]   # 10 = normal, 30 = espejo, ??? (attribute)
      left  = array[3*i+1]   # 0:8000 + left                 (tile number)
      right = array[3*i+2]  # 0:8000 + right                (tile number)

      print('addr {:04x} (modo, left, right) = ({:02x}, {:02x}, {:02x})'.format(0x3b72+3*i,modo,left,right))
      strLine = Util.instance().strHexa(array[3*i:3*(i+1)])
#      print('strLinePers: ' + strLine)

#      array = array[3:]

  def exportGolpes(self):
    """ exporta base de cuanto lastima golpes dados/recibidos ? """

    print('--- 4:0931')
    bank = RomSplitter.instance().banks[0x04]
    array = bank[0x0931:]

    for i in range(0,152):

      line = array[:8]

      strLine = Util.instance().strHexa(line)
      print('strGolpes: ' + strLine)

      array = array[8:]


  def exportMonstruoGrandeDobleTile(self):
    """ exporta los doble tiles de los boss """

    print('--- 4:3ba7')
    bank = RomSplitter.instance().banks[0x04]
    array = bank[0x3ba7:]

    for i in range(0,326):

      line = array[:3]

      modo = line[0]   # 10 = normal, 30 = espejo, ??? (attribute)
      left = line[1]   # 0:8000 + left                 (tile number)
      right = line[2]  # 0:8000 + right                (tile number)

      print('(modo, left, right) = ({:02x}, {:02x}, {:02x})'.format(modo,left,right))
      strLine = Util.instance().strHexa(line)
#      print('strLinePers: ' + strLine)

      array = array[3:]


  def exportSongs(self, exportLilypond=False):
    """ exporta las canciones """

    basePath = Address.instance().basePath
    path = basePath + '/audio'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    # cargo el banco 16 con las canciones
    bank = RomSplitter.instance().banks[0x0F]

    canciones = Canciones()
    canciones.decodeRom(bank)

    lines = canciones.encodeTxt()
    strCanciones = '\n'.join(lines)
    f = open(path + '/songs.txt', 'w')
    f.write(strCanciones)
    f.close()

    for i in range(0,30):
      cancion = canciones.canciones[i]

      lines = cancion.encodeTxt()
      strCancion = '\n'.join(lines)
      f = open(path + '/song_{:02}.txt'.format(i), 'w')
      f.write(strCancion)
      f.close()

      import random
      rr = random.randint(0,0xff)
      gg = random.randint(0,0xff)
      bb = random.randint(0,0xff)
      addr = cancion.melody2.addr
      length = len(cancion.melody2.encodeRom())
      # agrego info al stats
      RomStats.instance().appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')

      addr = cancion.melody1.addr
      length = len(cancion.melody1.encodeRom())
      # agrego info al stats
      RomStats.instance().appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')

      addr = cancion.melody3.addr
      length = len(cancion.melody3.encodeRom())
      # agrego info al stats
      RomStats.instance().appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')


      # si quiere que compile lilypond
      if(exportLilypond):
        # exporto lilypond!
        cancion.exportLilypond()


  def burnSongs(self, filepath, ignoreAddrs=False):
    """ quema las canciones en el banco 0f real.  Si ignoreAddrs=True calcula addrs nuevas concatenando channels """

    canciones = Canciones()

    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    canciones.decodeTxt(lines)

#    vaPorAddr = canciones.canciones[0].addrCh2
    # empezamos por la dirección donde debe comenzar el primer canal de la primera canción
    vaPorAddr = 0x4ac9

    for cancion in canciones.canciones:
#      print('cancy: ' + str(cancion))

      melody2Rom = cancion.melody2.encodeRom()
      melody1Rom = cancion.melody1.encodeRom()
      melody3Rom = cancion.melody3.encodeRom()

      # si no ignoramos los addrs
      if(not ignoreAddrs):
        
        # quemo el puntero al addr del channel 2
        punteroAddr = 0x0a12 + 6*cancion.nro + 0
        strHexAddr = '{:02x} {:02x}'.format(cancion.addrCh2%0x100, cancion.addrCh2//0x100)
        addrArray = Util.instance().hexaStr(strHexAddr)
        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # y quemo el channel 2
        RomSplitter.instance().burnBank(0xf, cancion.addrCh2 - 0x4000, melody2Rom)

        # quemo el puntero al addr del channel 1
        punteroAddr = 0x0a12 + 6*cancion.nro + 2
        strHexAddr = '{:02x} {:02x}'.format(cancion.addrCh1%0x100, cancion.addrCh1//0x100)
        addrArray = Util.instance().hexaStr(strHexAddr)
        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # y quemo el channel 1
        RomSplitter.instance().burnBank(0xf, cancion.addrCh1 - 0x4000, melody1Rom)

        # quemo el puntero al addr del channel 3
        punteroAddr = 0x0a12 + 6*cancion.nro + 4
        strHexAddr = '{:02x} {:02x}'.format(cancion.addrCh3%0x100, cancion.addrCh3//0x100)
        addrArray = Util.instance().hexaStr(strHexAddr)
        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # y quemo el channel 3
        RomSplitter.instance().burnBank(0xf, cancion.addrCh3 - 0x4000, melody3Rom)

      else:

        # quemo el puntero al addr del channel 2
        punteroAddr = 0x0a12 + 6*cancion.nro + 0
        strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
        addrArray = Util.instance().hexaStr(strHexAddr)
        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # recodifico la melody con su nuevo addr
        cancion.melody2.addr = vaPorAddr
        cancion.melody2.refreshLabels()
        melody2Rom = cancion.melody2.encodeRom()
        # y quemo el channel 2
        RomSplitter.instance().burnBank(0xf, vaPorAddr - 0x4000, melody2Rom)
        vaPorAddr += len(melody2Rom)#+0x10

        # quemo el puntero al addr del channel 1
        punteroAddr = 0x0a12 + 6*cancion.nro + 2
        strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
        addrArray = Util.instance().hexaStr(strHexAddr)
        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # recodifico la melody con su nuevo addr
        cancion.melody1.addr = vaPorAddr
        cancion.melody1.refreshLabels()
        melody1Rom = cancion.melody1.encodeRom()
        # y quemo el channel 1
        RomSplitter.instance().burnBank(0xf, vaPorAddr - 0x4000, melody1Rom)
        vaPorAddr += len(melody1Rom)#+0x10

        # quemo el puntero al addr del channel 3
        punteroAddr = 0x0a12 + 6*cancion.nro + 4
        strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
        addrArray = Util.instance().hexaStr(strHexAddr)
        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # recodifico la melody con su nuevo addr
        cancion.melody3.addr = vaPorAddr
        cancion.melody3.refreshLabels()
        melody3Rom = cancion.melody3.encodeRom()
        # y quemo el channel 3
        RomSplitter.instance().burnBank(0xf, vaPorAddr - 0x4000, melody3Rom)
        vaPorAddr += len(melody3Rom)#+0x10


  def burnSongsHeaders(self, filepath):
    """ quema las canciones en el banco 0f real.  Agrega los headers misteriosos """

    canciones = Canciones()

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


    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    canciones.decodeTxt(lines)

    vaPorAddr = canciones.canciones[0].addrCh2

    for i in range(0,30):
#      print('cancy: ' + str(cancion))

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
        addrArray = Util.instance().hexaStr(strHexAddr)
#        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # y quemo el channel 2
#        RomSplitter.instance().burnBank(0xf, vaPorAddr - 0x4000, melody2Rom)
        array.extend(melody2Rom)
        vaPorAddr += len(melody2Rom)
       
        # quemo el puntero al addr del channel 1
        punteroAddr = 0x0a12 + 6*cancion.nro + 2
        strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
        addrArray = Util.instance().hexaStr(strHexAddr)
#        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # y quemo el channel 1
#        RomSplitter.instance().burnBank(0xf, vaPorAddr - 0x4000, melody1Rom)
        array.extend(melody1Rom)
        vaPorAddr += len(melody1Rom)

        # quemo el puntero al addr del channel 3
        punteroAddr = 0x0a12 + 6*cancion.nro + 4
        strHexAddr = '{:02x} {:02x}'.format(vaPorAddr%0x100, vaPorAddr//0x100)
        addrArray = Util.instance().hexaStr(strHexAddr)
#        RomSplitter.instance().burnBank(0xf, punteroAddr, addrArray)
        # y quemo el channel 3
#        RomSplitter.instance().burnBank(0xf, vaPorAddr - 0x4000, melody3Rom)
        array.extend(melody3Rom)
        vaPorAddr += len(melody3Rom)

#    print(Util.instance().strHexa(array))
    print('len: ' + str(len(array)))

    RomSplitter.instance().burnBank(0xf, 0x4AC7 - 0x4000, array)

  def exportSpriteSheetHero(self):
    """ exporta sprite sheet del heroe """

    basePath = Address.instance().basePath
    path = basePath + '/spriteSheetHero'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)


    bank08 = RomSplitter.instance().banks[0x08]

    tiles = []
    for i in range(0,96 + 16*7):
      data = bank08[0x1a00 + i*0x10:0x1a00 + (i+1)*0x10]
      tile = Tile()
      tile.decodeRom(data)
      tiles.append(tile)

    extraTiles = []
    for i in range(0,8):
      extraTiles.append(tiles[i])
    extraTiles.append(tiles[4])
    extraTiles.append(tiles[5])
    for i in range(8,14):
      extraTiles.append(tiles[i])
    extraTiles.append(tiles[10])
    extraTiles.append(tiles[11])
    for i in range(14,64):
      extraTiles.append(tiles[i])
    extraTiles.append(tiles[28]) # estos dos no se si estan bien
    extraTiles.append(tiles[29]) #
    extraTiles.append(tiles[64])
    extraTiles.append(tiles[65])

    extraTiles.append(tiles[66]) # estos dos tampoco se
    extraTiles.append(tiles[67]) #
    extraTiles.append(tiles[68])
    extraTiles.append(tiles[69])

    extraTiles.append(tiles[70])
    extraTiles.append(tiles[71])
    extraTiles.append(tiles[72])
    extraTiles.append(tiles[73])

#    extraTiles.append(tiles[74]) # estos dos nose para que se usan
#    extraTiles.append(tiles[75]) #

    extraTiles.append(tiles[76])
    extraTiles.append(tiles[77])
    extraTiles.append(tiles[78])
    extraTiles.append(tiles[79])

    extraTiles.append(tiles[80])
    extraTiles.append(tiles[81])
    extraTiles.append(tiles[82])
    extraTiles.append(tiles[83])

    extraTiles.append(tiles[84])
    extraTiles.append(tiles[85])
    extraTiles.append(tiles[82])
    extraTiles.append(tiles[83])

    extraTiles.append(tiles[86])
    extraTiles.append(tiles[87])
    extraTiles.append(tiles[88])
    extraTiles.append(tiles[89])

    extraTiles.append(tiles[86])
    extraTiles.append(tiles[90])
    extraTiles.append(tiles[88])
    extraTiles.append(tiles[89])

    extraTiles.append(tiles[91])
    extraTiles.append(tiles[92])
    extraTiles.append(tiles[93])
    extraTiles.append(tiles[94]) # el tile 95 está en blanco?
 
    for i in range(96,96+16*7):
      extraTiles.append(tiles[i])

    tileset = Tileset(2,2*(26+28))
#    tileset = Tileset(2,48)
#    tileset.tiles = [tile0, tile1, tile2, tile3]
#    tileset.tiles = tiles
    tileset.tiles = extraTiles
    tileset.exportPngFile(path + '/hero.png')


  def exportSpriteSheetMonster(self):
    """ exporta sprite sheet de los monstruos """

    basePath = Address.instance().basePath
    path = basePath + '/spriteSheetMonster'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)


    bank0b = RomSplitter.instance().banks[0x0b]


    tiles = []
    for i in range(0,16*2):
      data = bank0b[0x3e00 + i*0x10:0x3e00 + (i+1)*0x10]
      tile = Tile()
      tile.decodeRom(data)
      tiles.append(tile)

#    for i in range(0,16):
#      extraTiles.append(tiles[i])


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

    tileset = Tileset(4,8)
#    tileset = Tileset(2,48)
#    tileset.tiles = [tile0, tile1, tile2, tile3]
#    tileset.tiles = tiles
    tileset.tiles = extraTiles
    tileset.exportPngFile(path + '/monster_10.png')

    bank04 = RomSplitter.instance().banks[0x04]
    # tabla de los 21 monstruos
    for i in range(0,21):
      # 24 bytes por monstruo
      array = bank04[0x0739 + 24*i:0x0739 + 24*(i+1)]

#      print('{:02} | '.format(i) + Util.instance().strHexa(array))


#00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23
#                              \/ \/             \___/ \___/ \___/ 
#                              Z   X               Y    addr comportamiento
#
# X renglón de donde saca los sprites!
# Z paleta de colores?
# Y que le hace daño (espada?)

# ejemplo para el monstruo 0x10
#
#                        size? Z  X              sword?
#                        /---\ /\ /\             /---\ /---------\
#05 02 00 00 06 16 46 02 40 10 00 fe 87 79 70 7c 19 4d 4d 4f 15 4e 73 54

  def exportSpriteSheetPersonajes(self):
    """ exporta los spriteSheet de personajes """

    basePath = Address.instance().basePath
    path = basePath + '/spriteSheetPersonajes'

    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    for banco in range(0,0x10):
      for nro in range(0,4):

        bank = RomSplitter.instance().banks[banco]
        array = bank[0x1000*nro:0x1000*(nro+1)]

        w, h = 8,8
#        w, h = 4,16
        sheetPers = SpriteSheetPersonaje(w,h)

        sheetPers.decodeRom(array)
        sheetData = sheetPers.encodePng()

        filepath = basePath + '/banks/bank_{:02}/sheetPers_{:02}_{:02}.png'.format(banco, banco, nro)
        # lo exporto a png
        Util.instance().arrayToPng(sheetData, 16*w, 16*h, filepath)

    i = 1
    banco = 8
    bank = RomSplitter.instance().banks[banco]
    array = bank[0x1a00:0x2000]
    w, h = 8,3
    sheetPers = SpriteSheetPersonaje(w,h)
    sheetPers.decodeRom(array)
    sheetData = sheetPers.encodePng()
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    Util.instance().arrayToPng(sheetData, 16*w, 16*h, filepath)

    i = 2
    banco = 8
    bank = RomSplitter.instance().banks[banco]
    array = bank[0x2000:0x3000]
    w, h = 4,7
    sheetPers = SpriteSheetPersonaje(w,h)
    sheetPers.decodeRom(array)
    sheetData = sheetPers.encodePng()
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    Util.instance().arrayToPng(sheetData, 16*w, 16*h, filepath)

    i = 3
    banco = 8
    bank = RomSplitter.instance().banks[banco]
    array = bank[0x3000:0x4000]
    w, h = 8,8
    sheetPers = SpriteSheetPersonaje(w,h)
    sheetPers.decodeRom(array)
    sheetData = sheetPers.encodePng()
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    Util.instance().arrayToPng(sheetData, 16*w, 16*h, filepath)

    bancoAddrPosta = [                 (0x09, 0x1000), (0x09, 0x2000), (0x09,0x3000),
                       (0x0a, 0x0000), (0x0a, 0x1000), (0x0a, 0x2000), (0x0a,0x3000) ]

    i = 5
    # para cada spriteSheetPersonaje posta
    for banco, addr in bancoAddrPosta:

      bank = RomSplitter.instance().banks[banco]
      array = bank[addr:]
      w, h = 8,8
#      w, h = 4,16
      sheetPers = SpriteSheetPersonaje(w,h)
      sheetPers.decodeRom(array)
      sheetData = sheetPers.encodePng()
      filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
      Util.instance().arrayToPng(sheetData, 16*w, 16*h, filepath)

      import random
      rr = random.randint(0,0xff)
      gg = random.randint(0,0xff)
      bb = random.randint(0,0xff)
      # agrego info al stats
      RomStats.instance().appendDato(banco, addr, addr + 0x1000, (rr, gg, bb), 'un spriteSheetPersonaje')

      i += 1

  def burnSpriteSheetPersonajes(self):

    basePath = Address.instance().basePath
    path = basePath + '/spriteSheetPersonajes'

    i = 1
    banco = 8
    addr = 0x1a00
    w, h = 8,3
    sheetPers = SpriteSheetPersonaje(w,h)
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    array = Util.instance().pngToArray(filepath)
    sheetPers.decodePng(array)
    array = sheetPers.encodeRom()
    RomSplitter.instance().burnBank(banco, addr, array)

    i = 2
    banco = 8
    addr = 0x2000
    w, h = 4,7
    sheetPers = SpriteSheetPersonaje(w,h)
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    array = Util.instance().pngToArray(filepath)
    sheetPers.decodePng(array)
    array = sheetPers.encodeRom()
    RomSplitter.instance().burnBank(banco, addr, array)

    i = 3
    banco = 8
    addr = 0x3000
    w, h = 8,8
    sheetPers = SpriteSheetPersonaje(w,h)
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    array = Util.instance().pngToArray(filepath)
    sheetPers.decodePng(array)
    array = sheetPers.encodeRom()
    RomSplitter.instance().burnBank(banco, addr, array)


    bancoAddrPosta = [                 (0x09, 0x1000), (0x09, 0x2000), (0x09,0x3000),
                       (0x0a, 0x0000), (0x0a, 0x1000), (0x0a, 0x2000), (0x0a,0x3000) ]

    i = 5
    # para cada spriteSheetPersonaje posta
    for banco, addr in bancoAddrPosta:

      bank = RomSplitter.instance().banks[banco]
      array = bank[addr:]
      w, h = 8,8
#      w, h = 4,16
      sheetPers = SpriteSheetPersonaje(w,h)
      filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
      array = Util.instance().pngToArray(filepath)
      sheetPers.decodePng(array)
      array = sheetPers.encodeRom()
      RomSplitter.instance().burnBank(banco, addr, array)

      i += 1



  def exportMapas(self, exportPngFile):
    """ genera los mapa-wrappers """

    basePath = Address.instance().basePath
    path = basePath + '/mapas'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    mapas = Mapas()
    # decodifico los scripts
    mapas.decodeRom()
    # los codifico en txt
    lines = mapas.encodeTxt()
    # lo grabo
    filepath = path + '/mapas.txt'
    f = open(filepath, 'w')
    strTxt = '\n'.join(lines)
    f.write(strTxt)
    f.close()

    # para cada mapa
    for mapa in mapas.mapas:

      print('mapa: {:02x}'.format(mapa.nroMapa))

      # lo exporto a .txt
      lines = mapa.encodeTxt()
      strMapa = '\n'.join(lines)
      f = open(path + '/mapa_{:02}_{:02x}.txt'.format(mapa.nroMapa, mapa.nroMapa), 'w')
      f.write(strMapa + '\n')
      f.close()

      # exporto a formato .tmx para Tiled
      mapa.exportTiled(path + '/mapa_{:02}_{:02x}.tmx'.format(mapa.nroMapa, mapa.nroMapa))

      if(exportPngFile):
        mapa.exportPngFile(path + '/mapa_{:02}_{:02x}.png'.format(mapa.nroMapa, mapa.nroMapa))

      # verifico volviendo a encodearlo
      subArray = mapa.encodeRom(mapa.mapAddr)
#      filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#      Util.instance().arrayToFile(subArray, filepath)
#      iguales = Util.instance().compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#      print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

      import random
      rr = random.randint(0,0xff)
      gg = random.randint(0,0xff)
      bb = random.randint(0,0xff)
      length = len(subArray)
      # agrego info al stats
      RomStats.instance().appendDato(mapa.mapBank, mapa.mapAddr, mapa.mapAddr+length, (rr, gg, bb), 'un mapa')


  def burnMapas(self, filepath):

    basePath = Address.instance().basePath
    path = basePath + '/mapas'

    mapas = Mapas()
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    mapas.decodeTxt(lines)

    # donde va el addr en cada uno de los bancos de mapas (5,6,7)
    vaPorBank = 0x05
    vaPorAddr = 0x0000
    sortMapas = [0,9, 1,15,14,10,8, 3,2,13,4,5,11,12,6,7]

    # por cada mapa
    for i in range(0,0x10):

      sortedNro = sortMapas[i]
      # lo agarro en el orden a quemar en la rom
      mapa = mapas.mapas[sortedNro]

#      print('mapa: ' + str(mapa))
#      mapa.exportPngFile('./game/mapas/mapa_{:02x}.png'.format(mapa.nroMapa))

      # lo codifico para calcular el tamaño que ocupa
      subArray = mapa.encodeRom(mapa.mapAddr)

#      filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#      Util.instance().arrayToFile(subArray, filepath)
#      iguales = Util.instance().compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#      print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

      if(vaPorAddr + len(subArray) >= 0x4000):
        vaPorBank += 1
        vaPorAddr = 0x0000

      # actualizo el addr !!
      mapa.mapBank = vaPorBank
      mapa.mapAddr = vaPorAddr
      # vuelvo a encodearlo para ajustar los punteros addr de los bloques !!
      subArray = mapa.encodeRom(mapa.mapAddr)
      # lo quemo en la rom
      RomSplitter.instance().burnBank(mapa.mapBank, mapa.mapAddr, subArray)

#      print('i: {:02x} vaPorAddr: {:02x}:{:04x} mapAddr: {:02x}:{:04x}'.format(sortedNro, vaPorBank, vaPorAddr, mapa.mapBank, mapa.mapAddr))

      vaPorAddr += len(subArray)

#      print('quedó en: {:04x}'.format(vaPorAddr))



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

#      print('mapa: ' + str(mapa.nroMapa))
#      strHex = Util.instance().strHexa(subArray)
#      print('strHex: ' + strHex + '\n')

      array.extend(subArray)

    RomSplitter.instance().burnBank(0x08, 0x0000, array)

  def burnMapasTiled(self):
    """ quema los mapas usando los .tmx del Tiled """

    basePath = Address.instance().basePath
    path = basePath + '/mapas'

    # donde va el addr en cada uno de los bancos de mapas (5,6,7)
    vaPorBank = 0x05
    vaPorAddr = 0x0000
    sortMapas = [0,9, 1,15,14,10,8, 3,2,13,4,5,11,12,6,7]

    mapas = Mapas()

    # por cada mapa
    for i in range(0,0x10):
#    for i in range(0,2):
#    for i in range(0,3):

      filepath = path + '/mapa_{:02}_{:02x}.tmx'.format(i,i)
      f = open(filepath, 'r')
      lines = f.readlines()
      f.close()

      for line in lines:
        if('property name="nroMapa"' in line):
          idx = line.index('value=')
          subLine = line[idx:]
          strLine = subLine.split('"')[1]
          nroMapa = int(strLine, 16)
        elif('property name="nroSpriteSheet"' in line):
          idx = line.index('value=')
          subLine = line[idx:]
          strLine = subLine.split('"')[1]
          nroSpriteSheet = int(strLine, 16)
        elif('property name="nose"' in line):
          idx = line.index('value=')
          subLine = line[idx:]
          strLine = subLine.split('"')[1]
          nose = int(strLine, 16)
        elif('property name="spriteAddr"' in line):
          idx = line.index('value=')
          subLine = line[idx:]
          strLine = subLine.split('"')[1]
          spriteAddr = int(strLine, 16)
        elif('property name="cantSprites"' in line):
          idx = line.index('value=')
          subLine = line[idx:]
          strLine = subLine.split('"')[1]
          cantSprites = int(strLine, 16)
        elif('property name="mapBank"' in line):
          idx = line.index('value=')
          subLine = line[idx:]
          strLine = subLine.split('"')[1]
          mapBank = int(strLine, 16)
        elif('property name="mapAddr"' in line):
          idx = line.index('value=')
          subLine = line[idx:]
          strLine = subLine.split('"')[1]
          mapAddr = int(strLine, 16)
        elif('property name="noseAddr"' in line):
          idx = line.index('value=')
          subLine = line[idx:]
          strLine = subLine.split('"')[1]
          noseAddr = int(strLine, 16)
 
      print('nroMapa {:02x}, nroSpriteSheet {:02x}, nose {:02x}, spriteAddr {:04x}, cantSprites {:02x}, mapBank {:02x}, mapAddr {:04x}, noseAddr {:04x}'.format(nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr)) 

      mapa = Mapa(nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr)
      mapa.importTiled(filepath)
      mapas.mapas.append(mapa)

    # por cada mapa
    for i in range(0,0x10):
#    for i in range(0,1):

      sortedNro = sortMapas[i]
      # lo agarro en el orden a quemar en la rom
      mapa = mapas.mapas[sortedNro]

#      print('mapa: ' + str(mapa))
#      mapa.exportPngFile('./game/mapas/mapa_{:02x}.png'.format(mapa.nroMapa))

      # lo codifico para calcular el tamaño que ocupa
      subArray = mapa.encodeRom(mapa.mapAddr)

#      filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#      Util.instance().arrayToFile(subArray, filepath)
#      iguales = Util.instance().compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#      print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

      if(vaPorAddr + len(subArray) >= 0x4000):
        vaPorBank += 1
        vaPorAddr = 0x0000

      # actualizo el addr !!
      mapa.mapBank = vaPorBank
      mapa.mapAddr = vaPorAddr
      # vuelvo a encodearlo para ajustar los punteros addr de los bloques !!
      subArray = mapa.encodeRom(mapa.mapAddr)
      # lo quemo en la rom
      RomSplitter.instance().burnBank(mapa.mapBank, mapa.mapAddr, subArray)

#      print('i: {:02x} vaPorAddr: {:02x}:{:04x} mapAddr: {:02x}:{:04x}'.format(sortedNro, vaPorBank, vaPorAddr, mapa.mapBank, mapa.mapAddr))

      vaPorAddr += len(subArray)

#      print('quedó en: {:04x}'.format(vaPorAddr))



    array = []
    # para cada mapa
    for nroMapa in range(0,0x10):
#    for nroMapa in range(0,1):

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

#      print('mapa: ' + str(mapa.nroMapa))
#      strHex = Util.instance().strHexa(subArray)
#      print('strHex: ' + strHex + '\n')

      array.extend(subArray)

    RomSplitter.instance().burnBank(0x08, 0x0000, array)
























  def exportTexto(self):
    """ convierte los banks .bin en .txt """

    basePath = Address.instance().basePath
#    romName = Address.instance().romName
#    filePath = basePath + '/hex_texto.txt'
#    rom = RomSplitter.instance().rom
     # lo exporto a texto
#    self._exportTexto(rom, filePath)

    # para cada banco
    for i in range(0,0x10):

      filePath = basePath + '/banks/bank_{:02}/bank_{:02}.txt'.format(i,i)
      bank = RomSplitter.instance().banks[i]
      # lo exporto a texto
      self._exportTexto(bank, filePath)

  def _exportTexto(self, array, filePath):

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
          chars = Dictionary.instance().decodeByte(hexy)
          traduc += chars
        addr = '{:04x}'.format(i - 0x10)
        g.write(addr + ' | ' + strhexs + '| ' + traduc + '\n')
        renglon = []

      i+=1

    g.close()



  def scriptDecode(self, addr):
    script = Script()
    script.addr = addr

    banco = 0x0d
    if(addr >= 0x4000):
      banco = 0x0e
      addr -= 0x4000
    array = RomSplitter.instance().banks[banco]
    # creo un array desde donde empieza el script
    array = array[addr:]

    script.decodeRom(array)
    return script


  def exportIntro(self):
    """ exporta el intro.txt """

    bank02 = RomSplitter.instance().banks[0x02]

    address = Address.instance().addrIntro

    array = bank02[address:]
#    strHexa = Util.instance().strHexa(array)
#    print('strHexa: ' + strHexa)

    string = ''
    # para cada byte del array
    for code in array:

      # lo decodifico
      if(code in [0x00, 0x1a]):
        # 'en' rom uses 0x00, 'fr' and 'de' roms use 0x1a for <enter>
        char = '\n'
      elif(code == 0xff):
        char = ' '
      elif(code == 0x01):
        break
      else:
        char = Dictionary.instance().decodeByte(code)

      # y lo agrego al string
      string += char

#    print('string: ' + string)

    romName = Address.instance().romName
    path = './' + romName + '/intro.txt'
    # lo exporto al intro.txt
    f = open(path, 'w')
    f.write(string)
    f.close()

  def burnIntro(self):
    """ quema el intro.txt en la rom """

    romName = Address.instance().romName
    path = './' + romName + '/intro.txt'
    f = open(path, 'r')
    string = f.read()
    f.close()

    array = []
    # para cada char del string
    for char in string:
      # lo codifico con el byte correspondiente
      if(char == '\n'):

        lang = Address.instance().language
        if(lang == ENGLISH):
          code = 0x00
        else: 
          code = 0x1a

      elif(char == ' '):
        code = 0xff
      else:
        code = Dictionary.instance().encodeChars(char)

      # y lo agrego al array
      array.append(code)

    # agrego el byte de cierre
    array.append(0x01)

#    strHexa = Util.instance().strHexa(array)
#    print('strHexa: ' + strHexa)

    address = Address.instance().addrIntro
    # lo quemo en el banco
    RomSplitter.instance().burnBank(0x02, address, array)


  def burnInitialScript(self, nroScript):
    """ setea el script inicial a ejecutar cuando inicia el juego sin battery """

    bank02 = RomSplitter.instance().banks[0x02]
#    address = Address.instance().addrScriptAddrDic
    address = 0x3cfe

    byte1 = nroScript // 0x100
    byte2 = nroScript % 0x100
    array = [byte2, byte1]
    # lo quemo en el banco
    RomSplitter.instance().burnBank(0x02, address, array)
 
     
  def exportScripts(self):

    basePath = Address.instance().basePath
    path = basePath + '/scripts'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    scripts = Scripts()
    # decodifico los scripts
    scripts.decodeRom()
    # los codifico en txt
    lines= scripts.encodeTxt()
    # lo grabo
    filepath = path + '/scripts.txt'
    f = open(filepath, 'w', encoding="utf-8")
    strTxt = '\n'.join(lines)
    f.write(strTxt)
    f.close()

  def exportRom(self, filepath):
    """ vuelve a juntar los bancos en una rom """

    hexs = []

    for bank in self.banks:
      hexs.extend(bank)

    f = open(filepath, 'wb')
    f.write( bytes(hexs) )
    f.close()

  def gameGenieHacks(self):
    """ cambia un par de bytes para que no reste HP """

    # gamegenie hacks!
    bank0 = RomSplitter.instance().banks[0]
    val = bank0[0x3e3a]
#    print('val1: {:02x}'.format(val))
    # cambio la resta 'sub l' por un nop (no resta hp los golpes, si el veneno)
    bank0[0x3e3a] = 0x00

    bank2 = RomSplitter.instance().banks[2]
    val = bank2[0x396c]
#    print('val2: {:02x}'.format(val))
    # cambio la resta 'sub l' por 'sub h' para que reste 0x00 el daño por veneno
    bank2[0x396c] = 0x94


  def exportGbsRom(self, filepath):
    """ exporta a una rom musical gbs """

    # cargo el gbs rom
#    gbsRom = Util.instance().fileToArray('./roms/audio.gb')
    # me quedo con el bank00
#    gbsRom = gbsRom[0:0x4000]
    gbsRom = Util.instance().fileToArray('./gbsBank00.bin')
    # agarro el bank0f
    bank0f = RomSplitter.instance().banks[0x0f]
    # los concateno
    gbsRom.extend(bank0f)
    # creo la rom gbs de salida
    Util.instance().arrayToFile(gbsRom, filepath)


  def testRom(self, filepath, emulator):
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
#      comando = 'vba ' + filepath
      comando = '../visualboyadvance-m/build/visualboyadvance-m ' + filepath
      os.system(comando)



  def burnScripts(self, filepath):
    """ compila el script.txt indicado y quema los scripts en los bancos 0x0d y 0x0e, y el dicionario de addrs en banco 0x08 """

    scripts = Scripts()

    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    scripts.decodeTxt(lines)

    # codifico los banks 0x0d y 0x0e
    array0d, array0e = scripts.encodeRom()

    basePath = Address.instance().basePath
    # creo los binarios para comparar
#    Util.instance().arrayToFile(array0d, basePath+'/scripts/scripts0d.bin')
#    Util.instance().arrayToFile(array0e, basePath+'/scripts/scripts0e.bin')
#    iguales = Util.instance().compareFiles(basePath+'/banks/bank_13/bank_13.bin', basePath+'/scripts/scripts0d.bin', 0, len(array0d))
#    print('iguales 0d: ' + str(iguales))
#    iguales = Util.instance().compareFiles(basePath+'/banks/bank_14/bank_14.bin', basePath+'/scripts/scripts0e.bin', 0, len(array0e))
#    print('iguales 0e: ' + str(iguales))

    # quemo los banks 0x0d y 0x0e
    RomSplitter.instance().burnBank(0x0d, 0x0000, array0d)
    RomSplitter.instance().burnBank(0x0e, 0x0000, array0e)

    bank = 0x08
    addr = Address.instance().addrScriptAddrDic
    array = []
    # por cada script
    for script in scripts.scripts:
      # agarro su addr
      byte1 = script.addr // 0x100
      byte2 = script.addr % 0x100
      # y la agrego al array
      array.extend([byte2, byte1])
    # quemo el diccionario de addr en el bank08
    RomSplitter.instance().burnBank(bank, addr, array)

#    Util.instance().arrayToFile(array, './de/scripts/dic.bin')
#    iguales = Util.instance().compareFiles('./de/banks/bank_08/bank_08.bin', './de/scripts/dic.bin', addr, len(array))
#    print('iguales dic: ' + str(iguales))

  def burnBank(self, bank, idx0, hexs):

    i = idx0
    for hexa in hexs:

      if(i >= 0x4000):
        return False

      banco = RomSplitter.instance().banks[bank]
#      print('banco: ' + str(banco))

      banco[i] = hexa
      i += 1

    return True


  def exportItems(self):
    """ exporta los items """

    data = RomSplitter.instance().banks[0x02]

    addr = Address.instance().addrMagic
    string = ''
    # para cada magia
    for i in range(0,8):
      magicOffset = addr + i*0x10
      magicArray = data[magicOffset:magicOffset+0x10]
#      magic = Magic()
      magic = Item('magic')
      # la decodifico
      magic.decodeRom(magicArray)
      Cosas.instance().addMagic(magic)

      lines = magic.encodeTxt()
      subString = '\n'.join(lines)
      string += subString

    romName = Address.instance().romName
    path = './' + romName + '/magic.txt'
    # lo exporto al magic.txt
    f = open(path, 'w')
    f.write(string)
    f.close()

    addr = magicOffset + 0x10
    string = ''
    # para cada item
    for i in range(0,57):
      itemOffset = addr + i*0x10
      itemArray = data[itemOffset:itemOffset+0x10]
      item = Item('item')
      # lo decodifico
      item.decodeRom(itemArray)
      Cosas.instance().addItem(item)

      lines = item.encodeTxt()
      subString = '\n'.join(lines)
      string += subString

    romName = Address.instance().romName
    path = './' + romName + '/items.txt'
    # lo exporto al items.txt
    f = open(path, 'w', encoding="utf-8")
    f.write(string)
    f.close()

    addr = itemOffset + 0x10
    string = ''
    # para cada weapon
    for i in range(0,46):
      weaponOffset = addr + i*0x10
      weaponArray = data[weaponOffset:weaponOffset+0x10]
      weapon = Item('weapon')
      # la decodifico
      weapon.decodeRom(weaponArray)
      Cosas.instance().addWeapon(weapon)

      lines = weapon.encodeTxt()
      subString = '\n'.join(lines)
      string += subString

    romName = Address.instance().romName
    path = './' + romName + '/weapons.txt'
    # lo exporto al weapons.txt
    f = open(path, 'w', encoding="utf-8")
    f.write(string)
    f.close()


  def burnItems(self, tipo, filepath):
    """ quema el magic.txt en la rom """

    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()

    items = []
    primerItem = True
    subLines = []
    for line in lines:

      if('nro:' in line):
        if(not primerItem):
          item = Item(tipo)
          item.decodeTxt(subLines)
          items.append(item)
        else:
          primerItem = False

        subLines = []
      subLines.append(line)
    item = Item(tipo)
    item.decodeTxt(subLines)
    items.append(item)

    array = []
    for item in items:
#      print('item: ' + str(item))
      subArray = item.encodeRom()
      array.extend(subArray)

    if(tipo == 'magic'):
      address = Address.instance().addrMagic
    elif(tipo == 'item'):
      address = Address.instance().addrMagic + 8*16
    elif(tipo == 'weapon'):
      address = Address.instance().addrMagic + 0x08*16 + 0x39*16

    # lo quemo en el banco
    RomSplitter.instance().burnBank(0x02, address, array)

  def exportSolarus(self):

    print('exportando a solarus...')

#    basePath = Address.instance().basePath
#    path = basePath + '/scripts'
    path = './solarusQuest'
    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    # exporto los spriteSheets
    for k in range(0,5):
      sheet = RomSplitter.instance().spriteSheets[k]

      lines = []
      lines.append('background_color{ 255, 255, 255 }')
      sheet.exportPngFile('./solarusQuest/data/tilesets/sheet_{:02}.tiles.png'.format(k))
      i = 0
      for sprite in sheet.sprites:
#        print('sprite: {:02x}'.format(sprite.bloqueo))

        x = (i%16)
        y = (i//16)

        lines.append('tile_pattern{')
        lines.append(' id = "' + str(i) + '",')
        ground = 'traversable'
#        ground = 'traversable' if sprite.bloqueo == 0x30 else 'wall'
        lines.append(' ground = "' + ground + '",')
        lines.append(' default_layer = 0,')
        lines.append(' x = ' + str(16*x) + ',')
        lines.append(' y = ' + str(16*y) + ',')
        lines.append(' width = 16,')
        lines.append(' height = 16,')
        lines.append('}')

        i += 1

      f = open('./solarusQuest/data/tilesets/sheet_{:02}.dat'.format(k), 'w')
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

        f = open('./solarusQuest/data/maps/mapa_{:02x}_{:02}_{:02}_map.dat'.format(m, bloquex, bloquey), 'w')
        f.write('\n'.join(lines))
        f.close()


##########################################################
class Comando:
  """ representa un comando de un script """

  def __init__(self, addr):
    # el addr del comando
    self.addr = addr

    self.array = None
    self.lines = None

    # en principio no tiene script propio (solo FOR, IF)
    self.script = None

    self.nro = None
    self.strCode = None
    self.strHex = None
    self.hexs = []

    self.textMode = None

    # label al cual hace CALL este comando
    self.jumpLabel = ''
    # lista de labels que se usan para saltar a este comando
    self.labels = []

  def decodeRom(self, array, textMode):
    """ lo decodifica """
    self.array = array

    self.textMode = textMode
    # si el array está vacío
    if(len(self.array) == 0):
      # es que terminó un bloque de IF
      self.strCode = 'ENDIF\n'
      self.size = 0
      self.strHex = '' # Util.instance().strHexa(self.array[0:self.size])
      return

    # si no está en modo texto
    if(textMode == False):
      textMode = self.decodeNormal()
    # sino, está en modo texto
    else:
      textMode = self.decodeTextMode()

    return textMode

  def decodeTextMode(self):

    textMode = True

    # el número de comando es el primer byte
    self.nro = self.array[0]

    self.strHex = Util.instance().strHexa(self.array[0:20])
    self.strCode = 'ERROR_TEXT: ' + self.strHex + '\n'
    self.size = 0 

    # si es texto
    if(self.nro in Dictionary.instance().keys()):


      # agarro el char (o par de chars)
      char = Dictionary.instance().decodeByte(self.nro)

#      print('llegó: {:02x} '.format(self.nro) + char)

#      print('decodeByte {:02x}: '.format(self.nro) + char) 

      self.strCode = char 
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

      # si es <TEXT_MODE_OFF>
      if(self.nro == 0x00):
        # le agrego un enter
        self.strCode = '<TEXT_MODE_OFF>\n'
        # y salgo del modo texto
        textMode = False
 
    return textMode

  def decodeNormal(self):
    """ decodifica en modo normal (no en modo texto) """

    # asumo que no es en modo texto
    textMode = False
   
    # el número de comando es el primer byte
    self.nro = self.array[0]

#    print('nro: {:02x}'.format(self.nro))

#    print('array: ' + Util.instance().strHexa(self.array))
#    print('array: ' + Util.instance().strHexa(self.array[:min(20,len(self.array))]))

    self.strHex = Util.instance().strHexa(self.array[0:20])
    self.strCode = 'ERROR: ' + self.strHex + '\n'
    self.size = 0 


    if(self.nro in [0x05, 0x06, 0x1a, 0x1b, 0x2a, 0x88, 0x89, 0x90, 0x94, 0x95, 0x96, 0x97, 0x98, 0x9a, 0x9b, 0xa0, 0xa1, 0xa2, 0xa3, 0xa9, 0xab, 0xaf, 0xb6, 0xbc, 0xbe, 0xc7, 0xcc, 0xdc, 0xdd, 0xde, 0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xee, 0xfb]):
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
      self.strCode = 'NI_IDEA_0: ' + self.strHex + '\n'

    elif(self.nro in [0x8b, 0x91, 0x9c, 0xc2, 0xc5, 0xd4, 0xd5, 0xd8, 0xd9]):
      arg1 = self.array[1]
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
      self.strCode = 'NI_IDEA_1: ' + self.strHex + '\n'

    elif(self.nro in [0x99, 0xc9, 0xca, 0xef]):

#      print(Util.instance().strHexa(self.array[:min(20,len(self.array))]))

      arg1 = self.array[1]
      arg2 = self.array[2]
      self.size = 3
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
      self.strCode = 'NI_IDEA_2: ' + self.strHex + '\n'

    elif(self.nro == 0x12):
      self.strCode = 'PAUSE'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0x00):
      self.size = 1
      self.strCode = 'END\n'

      self.strHex = Util.instance().strHexa(self.array[0:self.size])


    elif(self.nro == 0x01):
      arg1 = self.array[1]
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
      self.strCode = 'SMALL_JUMP_FW {:02x}\n'.format(arg1)



    elif(self.nro == 0x02):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg1*0x100 + arg2
      self.strCode = 'CALL {:04x}\n'.format(arg)
      self.size = 3
      self.strHex = Util.instance().strHexa(self.array[0:self.size])


    elif(self.nro == 0x03):
      cant = self.array[1]
      cantBytes = self.array[2] 
      self.strCode = 'FOR 0 <= i < {:02x}\n'.format(cant)
      self.size = 3 + cantBytes
      self.strHex = Util.instance().strHexa(self.array[0:3])

      bloque = Script(self.addr + 3)
      bloqueArray = self.array[3:3+cantBytes]
      bloque.decodeRom(bloqueArray)
      self.script = bloque



    # IF
    elif(self.nro in [0x08, 0x09]):

      conds = []
      cond = self.array[1]
      i = 1
      while(cond != 0x00):
        conds.append(cond)
        cond = self.array[1+i]
        i += 1


      strConds = ''
      for cond in conds:
        strCond = Variables.instance().getLabel(cond) + ' '
        strConds += strCond
        cantBytes = self.array[1+i]

      if(self.nro == 0x08):
        self.strCode = 'IF(' + strConds + ')\n' 
      else:
        strConds = Util.instance().strHexa(conds)
        # condición sobre lo que tengo en la mano?
        self.strCode = 'IF_EQUIP(' + strConds + ')\n' 

      self.size = 2 + i + cantBytes
      self.strHex = Util.instance().strHexa(self.array[0:i+2])

      bloque = Script(self.addr + len(conds) + 3)
      bloqueArray = self.array[2+i:2+i+cantBytes]
      bloque.decodeRom(bloqueArray)
      self.script = bloque

    # IF raro
    elif(self.nro in [0x0a, 0x0b, 0x0c]):

      conds = []
      cond = self.array[1]
      i = 1
      while(cond != 0x00):
        conds.append(cond)
        cond = self.array[1+i]
        i += 1

      strConds = Util.instance().strHexa(conds)
      arg = self.array[1+i]

      if(self.nro == 0x0a):
        self.strCode = 'STRANGE_IF1(' + strConds + ') {:02x}'.format(arg) +'\n' 
      elif(self.nro == 0x0b):
        self.strCode = 'STRANGE_IF2(' + strConds + ') {:02x}'.format(arg) +'\n' 
      elif(self.nro == 0x0c):
        self.strCode = 'STRANGE_IF3(' + strConds + ') {:02x}'.format(arg) +'\n' 

      self.size = 2 + i 
      self.strHex = Util.instance().strHexa(self.array[0:i+2])

#      print(self.strCode)

    # extras
    elif(self.nro >= 0x10 and self.nro < 0x80):

#      print('nro: {:02x}'.format(self.nro))
      primer = self.nro // 0x10
      segund = self.nro % 0x10
#      print('primer: {:01x}'.format(primer))
#      print('segund: {:01x}'.format(segund))

      # si es movimiento de personajes extras
      if(segund in [0,1,4,5,6,7,8,9]):

        strExtra = 'EXTRA' + str(primer) + '_'

        strInstr = 'NI_IDEA'
        if(segund == 0):
          strInstr = 'PASO_ADELANTE'
        elif(segund == 1):
          strInstr = 'PASO_ATRAS'
        elif(segund == 4):
          strInstr = 'MIRAR_ARRIBA'
        elif(segund == 5):
          strInstr = 'MIRAR_ABAJO'
        elif(segund == 6):
          strInstr = 'MIRAR_DERECHA'
        elif(segund == 7):
          strInstr = 'MIRAR_IZQUIERDA'
        elif(segund == 8):
          strInstr = 'HIDE'

        self.strCode = strExtra + strInstr + '\n'
        self.size = 1
        self.strHex = Util.instance().strHexa(self.array[0:self.size])

        if(segund == 9):

          xx = self.array[1]
          yy = self.array[2]
          strXx = '{:02x}'.format(xx)
          strYy = '{:02x}'.format(yy)

          # cambia las coordenadas del extra dentro del bloque actual
          strInstr = 'BLOQUE_TELEPORT (XX,YY) = (' + strXx + ',' + strYy + ')'

          self.strCode = strExtra + strInstr + '\n'
          self.size = 3
          self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0x80):
      self.strCode = 'HEROE_PASO_ADELANTE\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0x81):
      self.strCode = 'HEROE_PASO_ATRAS\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0x84):
      self.strCode = 'HEROE_MIRAR_ARRIBA\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0x85):
      self.strCode = 'HEROE_MIRAR_ABAJO\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0x86):
      self.strCode = 'HEROE_MIRAR_DERECHA\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0x87):
      self.strCode = 'HEROE_MIRAR_IZQUIERDA\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0x8a):
      xx = self.array[1]
      yy = self.array[2]
      strXx = '{:02x}'.format(xx)
      strYy = '{:02x}'.format(yy)
      # cambia las coordenadas del hero dentro del bloque actual
      self.strCode = 'BLOQUE_TELEPORT (XX,YY) = (' + strXx + ',' + strYy + ')\n'
      self.size = 3
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xa4):
      # estado normal
      self.strCode = 'HEROE_DE_PIE\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0xa5):
      # cuando cae por la catarata
      self.strCode = 'HEROE_DESPATARRADO\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0xa6):
      # cuando depierta despues de haber caido
      self.strCode = 'HEROE_ACOSTADO\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xac):
      self.strCode = 'MUESTRA_MAPITA1\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0xad):
      self.strCode = 'MUESTRA_MAPITA2\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])
    elif(self.nro == 0xae):
      self.strCode = 'MUESTRA_MAPITA3\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])






    elif(self.nro == 0xb0):
      nn = self.array[1]
      xx = self.array[2]
      yy = self.array[3]

      strNn = '{:02x}'.format(nn)
      strXx = '{:02x}'.format(xx)
      strYy = '{:02x}'.format(yy)

      # cambia el sprite de fondo por el indicado en NN, en las coordenadas XX,YY del bloque actual
      self.strCode = 'SPRITE (NN,XX,YY) = (' + strNn + ',' + strXx + ',' + strYy + ')\n'
      self.size = 4
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro in [0xba]):
      tipo = self.array[1]
      xx = self.array[2]
      yy = self.array[3]

      strTipo = '{:02x}'.format(tipo)
      strXx = '{:02x}'.format(xx)
      strYy = '{:02x}'.format(yy)

      self.strCode = 'ATTACK_EFFECT (TT,XX,YY) = (' + strTipo + ',' + strXx + ',' + strYy + ')\n'
      self.size = 4
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xbc):
      self.strCode = 'FADE_IN\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xbd):
      self.strCode = 'FADE_OUT\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xbf):
      self.strCode = 'PARPADEO\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])


    elif(self.nro == 0xc0):
      self.strCode = 'REFRESH_HP\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xc1):
      self.strCode = 'REFRESH_MP\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xc4):
      # bitwise del argumento 
      # [][][][a][b][f][d][p]
      # p = poison
      # d = darkness
      # f = fells (no puede caminar)
      # b = bann
      # a = avisar que se enfermó (0 = avisa, 1 = no avisa) (para curar: 0x10 = 0b10000)
      arg = self.array[1]
      self.strCode = 'DISEASE {:02x}\n'.format(arg)
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xc6):
      self.strCode = 'INPUT_NAMES_SUMO_FUJI\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])


    elif(self.nro == 0xc8):
      self.strCode = 'RESET_GAME\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xd1):
      arg1 = self.array[1]
      arg2 = self.array[2]
      self.strCode = 'COMPARE_GOLD {:02x} {:02x}\n'.format(arg1,arg2)
      self.size = 3
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xda):
      arg = self.array[1]
      label = Variables.instance().getLabel(arg)
      self.strCode = 'SET_ON ' + label + '\n'
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xdb):
      arg = self.array[1]
      label = Variables.instance().getLabel(arg)
      self.strCode = 'SET_OFF ' + label + '\n'
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xd6):
      arg = self.array[1]
      self.strCode = 'OBTAINS_MAGIC {:02x}\n'.format(arg)
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xe8):
      # la pantalla hace scroll al bloque hacia abajo
      self.strCode = 'SCROLL_ABAJO\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xe9):
      # la pantalla hace scroll al bloque hacia abajo
      self.strCode = 'SCROLL_ARRIBA\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xea):
      # la pantalla hace scroll al bloque de la izquierda
      self.strCode = 'SCROLL_IZQUIERDA\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xeb):
      # la pantalla hace scroll al bloque de la derecha
      self.strCode = 'SCROLL_DERECHA\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xec):
      # salta al script que se ejecuta al entrar a dicho bloque?
      self.strCode = 'SCRIPT_ENTRAR_BLOQUE\n'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xf3):
      mm = self.array[1]
      bb = self.array[2]
      xx = self.array[3]
      yy = self.array[4]

      strMm = '{:02x}'.format(mm)
      strBb = '{:02x}'.format(bb)
      strXx = '{:02x}'.format(xx)
      strYy = '{:02x}'.format(yy)

      # creo que la diferencia con el otro teleport está en que este no refresca los tiles de cambio de mapa?
      self.strCode = 'TELEPORT2 (MM,BB,XX,YY) = (' + strMm + ',' + strBb + ',' + strXx + ',' + strYy + ')\n'
      self.size = 5
      self.strHex = Util.instance().strHexa(self.array[0:self.size])



    elif(self.nro == 0xf4):
      mm = self.array[1]
      bb = self.array[2]
      xx = self.array[3]
      yy = self.array[4]

      strMm = '{:02x}'.format(mm)
      strBb = '{:02x}'.format(bb)
      strXx = '{:02x}'.format(xx)
      strYy = '{:02x}'.format(yy)

      self.strCode = 'TELEPORT (MM,BB,XX,YY) = (' + strMm + ',' + strBb + ',' + strXx + ',' + strYy + ')\n'
      self.size = 5
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xf6):
      # validos: del 0x00 al 0x10 inclusive
      arg = self.array[1]
      self.strCode = 'VENDEDOR {:02x}\n'.format(arg)
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xf8):
      # indico como mapea con el número de canción del banco 0x0f
      # 0x00 -> silencio
      # 0x01 -> 1
      # 0x02 -> 6
      # 0x03 -> 7
      # 0x04 -> 8
      # 0x05 -> 9
      # 0x06 -> 10
      # 0x07 -> 11
      # 0x08 -> 12
      # 0x09 -> 13
      # 0x0a -> 5
      # 0x0b -> 14
      # 0x0c -> 15
      # 0x0d -> 16
      # 0x0e -> 4
      # 0x0f -> 17
      # 0x10 -> 18
      # 0x11 -> 19
      # 0x12 -> 20
      # 0x13 -> 21
      # 0x14 -> 22
      # 0x15 -> 23
      # 0x16 -> 24
      # 0x17 -> 3
      # 0x18 -> 25
      # 0x19 -> 26
      # 0x1a -> 2
      # 0x1b -> 27
      # 0x1c -> 28
      # 0x1d -> 29
      # 0x1e -> 30
      arg = self.array[1]
      self.strCode = 'MUSIC {:02x}\n'.format(arg)
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xf9):
      arg = self.array[1]
      self.strCode = 'SOUND_EFFECT {:02x}\n'.format(arg)
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xfc):
      arg = self.array[1]
      self.strCode = 'LOAD_PERSONAJE {:02x}\n'.format(arg)
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xfd):
      arg = self.array[1]
      self.strCode = 'ADD_PERSONAJE {:02x}\n'.format(arg)
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xfe):
      arg = self.array[1]
      label = Variables.instance().getLabelMonstruo(arg)
#      self.strCode = 'ADD_MONSTRUO_GRANDE {:02x}\n'.format(arg)
      self.strCode = 'ADD_MONSTRUO_GRANDE ' + label + '\n'
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0xf0):
      arg = self.array[1]
      self.strCode = 'SLEEP {:02x}\n'.format(arg)
      self.size = 2
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

    elif(self.nro == 0x04):
      # pasamos a text mode
      self.strCode = '<TEXT_MODE_ON>'
      self.size = 1
      self.strHex = Util.instance().strHexa(self.array[0:self.size])

      textMode = True


#    print('strCode: ' + self.strCode)
    return textMode


  def decodeTxt(self, lines):
    """ lo decodifica """

    self.textMode = False

    self.lines = lines

    line = self.lines[0].strip()
    self.strCode = line + '\n'
#    print('cmd line: ' + line)

    # si es un comentario
    if(line.startswith('#') or len(line) == 0):

#      self.hexs.append(0x00)
      # el sizeLines es la cantidad de renglones del comando (1 salvo FOR, IF que tienen script propio)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

      # retorno sin mas
      return


    if(line == 'END'):
      self.hexs.append(0x00)
      # el sizeLines es la cantidad de renglones del comando (1 salvo FOR, IF que tienen script propio)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
      return

    elif(line.startswith('ENDIF')):

      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)



    if(line.startswith('NI_IDEA')):

      idx0 = line.find(':')
      argTxt = line[idx0+2: ]
#      print('argTxt: ' + argTxt)

      argsTxt = argTxt.split(' ')

      args = []
      for strArg in argsTxt:
#        print('strArg: ' + strArg)
        arg = int(strArg, 16)
#        print('arg: {:02x}'.format(arg))
        args.append(arg)

      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('INPUT_NAMES_SUMO_FUJI')):
      self.hexs.append(0xc6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('HEROE_PASO_ADELANTE')):
      self.hexs.append(0x80)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('HEROE_PASO_ATRAS')):
      self.hexs.append(0x81)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('HEROE_MIRAR_ARRIBA')):
      self.hexs.append(0x84)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('HEROE_MIRAR_ABAJO')):
      self.hexs.append(0x85)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('HEROE_MIRAR_DERECHA')):
      self.hexs.append(0x86)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('HEROE_MIRAR_IZQUIERDA')):
      self.hexs.append(0x87)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('EXTRA')):

      strNro = line[5]
      nroExtra = int(strNro)
      cmd = line[7:]
      cmdDict = { 'PASO_ADELANTE' : 0, 'PASO_ATRAS' : 1, 'MIRAR_ARRIBA' : 4, 'MIRAR_ABAJO' : 5, 'MIRAR_DERECHA' : 6, 'MIRAR_IZQUIERDA' : 7, 'HIDE' : 8 }

      if(not cmd.startswith('BLOQUE_TELEPORT')):
        nroCmd = cmdDict[cmd]
        hexa = nroExtra * 0x10 + nroCmd
        self.hexs.append(hexa)
      # sino, es un bloque teleport del extra
      else:

        idx0 = line.rfind('(')
        idx1 = line.rfind(')')
        strArgs = line[idx0+1:idx1]
        strArgs = strArgs.split(',')
        arg1 = int(strArgs[0], 16)
        arg2 = int(strArgs[1], 16)

        hexa = nroExtra * 0x10 + 9
        self.hexs.append(hexa)
        self.hexs.append(arg1)
        self.hexs.append(arg2)

      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)



    # extras
#    elif(self.nro >= 0x10 and self.nro < 0x80):

#      primer = self.nro // 0x10
#      segund = self.nro % 0x10

      # si es movimiento de personajes extras
#      if(segund in [0,1,4,5,6,7,8,9]):

#        strExtra = 'EXTRA' + str(primer) + '_'

#        strInstr = 'NI_IDEA'
#        if(segund == 0):
#          strInstr = 'PASO_ADELANTE'
#        elif(segund == 1):
#          strInstr = 'PASO_ATRAS'
#        elif(segund == 4):
#          strInstr = 'MIRAR_ARRIBA'
#        elif(segund == 5):
#          strInstr = 'MIRAR_ABAJO'
#        elif(segund == 6):
#          strInstr = 'MIRAR_DERECHA'
#        elif(segund == 7):
#          strInstr = 'MIRAR_IZQUIERDA'
#        elif(segund == 8):
#          strInstr = 'HIDE'

#        self.strCode = strExtra + strInstr + '\n'
#        self.size = 1
#        self.strHex = Util.instance().strHexa(self.array[0:self.size])

#        if(segund == 9):

#          xx = self.array[1]
#          yy = self.array[2]
#          strXx = '{:02x}'.format(xx)
#          strYy = '{:02x}'.format(yy)

          # cambia las coordenadas del extra dentro del bloque actual
#          strInstr = 'BLOQUE_TELEPORT (XX,YY) = (' + strXx + ',' + strYy + ')'

#          self.strCode = strExtra + strInstr + '\n'
#          self.size = 3
#          self.strHex = Util.instance().strHexa(self.array[0:self.size])



    elif(line.startswith('RESET_GAME')):
      self.hexs.append(0xc8)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('MUESTRA_MAPITA1')):
      self.hexs.append(0xac)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('MUESTRA_MAPITA2')):
      self.hexs.append(0xad)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('MUESTRA_MAPITA3')):
      self.hexs.append(0xae)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)





    elif(line.startswith('HEROE_DE_PIE')):
      self.hexs.append(0xa4)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('HEROE_DESPATARRADO')):
      self.hexs.append(0xa5)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('HEROE_ACOSTADO')):
      self.hexs.append(0xa6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('FADE_IN')):
      self.hexs.append(0xbc)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('FADE_OUT')):
      self.hexs.append(0xbd)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('PARPADEO')):
      self.hexs.append(0xbf)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('REFRESH_HP')):
      self.hexs.append(0xc0)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('REFRESH_MP')):
      self.hexs.append(0xc1)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('SCROLL_ABAJO')):
      self.hexs.append(0xe8)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('SCROLL_ARRIBA')):
      self.hexs.append(0xe9)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('SCROLL_IZQUIERDA')):
      self.hexs.append(0xea)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('SCROLL_DERECHA')):
      self.hexs.append(0xeb)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('SCRIPT_ENTRAR_BLOQUE')):
      self.hexs.append(0xec)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('SCRIPT_ENTRAR_BLOQUE')):
      self.hexs.append(0xec)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('LOAD_PERSONAJE')):
      argTxt = line[len('LOAD_PERSONAJE')+1:]
      arg = int(argTxt, 16)
      self.hexs.append(0xfc)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('ADD_PERSONAJE')):
      argTxt = line[len('ADD_PERSONAJE')+1:]
      arg = int(argTxt, 16)
      self.hexs.append(0xfd)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('VENDEDOR')):
      argTxt = line[len('VENDEDOR')+1:]
      arg = int(argTxt, 16)
      self.hexs.append(0xf6)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('DISEASE')):
      argTxt = line[len('DISEASE')+1:]
      arg = int(argTxt, 16)
      self.hexs.append(0xc4)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('SLEEP')):
      argTxt = line[len('SLEEP')+1:]
      arg = int(argTxt, 16)
      self.hexs.append(0xf0)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('SOUND_EFFECT')):
      argTxt = line[len('SOUND_EFFECT')+1:]
      arg = int(argTxt, 16)
      self.hexs.append(0xf9)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('COMPARE_GOLD')):
      argTxt = line[len('COMPARE_GOLD')+1:]
#      arg = int(argTxt, 16)

      argsTxt = argTxt.split(' ')
      args = []
      for strArg in argsTxt:
        arg = int(strArg, 16)
        args.append(arg)

      self.hexs.append(0xd1)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)



    elif(line.startswith('SET_ON')):
      argTxt = line[len('SET_ON')+1:]
#      arg = int(argTxt, 16)
      arg = Variables.instance().getVal(argTxt)
      self.hexs.append(0xda)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('SET_OFF')):
      argTxt = line[len('SET_OFF')+1:]
#      arg = int(argTxt, 16)
      arg = Variables.instance().getVal(argTxt)
      self.hexs.append(0xdb)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('OBTAINS_MAGIC')):
      argTxt = line[len('OBTAINS_MAGIC')+1:]
      arg = int(argTxt, 16)
      self.hexs.append(0xd6)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('SMALL_JUMP_FW')):

      argTxt = line[len('SMALL_JUMP_FW')+1:]
      arg = int(argTxt, 16)

      self.hexs.append(0x01)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('MUSIC')):

      argTxt = line[len('MUSIC')+1:]
      arg = int(argTxt, 16)

      self.hexs.append(0xf8)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('ADD_MONSTRUO_GRANDE')):
      argTxt = line[len('ADD_MONSTRUO_GRANDE')+1:].strip()
#      arg = int(argTxt, 16)
      arg = Variables.instance().getValMonstruo(argTxt)
      self.hexs.append(0xfe)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('CALL')):

      argTxt = line[len('CALL')+1:]
      strArg1 = argTxt[1:3]
      strArg2 = argTxt[3:5]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)
      args = [arg1, arg2]

      self.jumpLabel = '${:04x}'.format(arg1*0x100 + arg2)
      self.hexs.append(0x02)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('BLOQUE_TELEPORT')):

      argTxt = line[len('BLOQUE_TELEPORT')+1:]
      idx0 = line.rfind('(')
      idx1 = line.rfind(')')
      argTxt = line[idx0+1:idx1]
      strArgs = argTxt.split(',')
      arg1 = int(strArgs[0], 16)
      arg2 = int(strArgs[1], 16)

      self.hexs.append(0x8a)
      self.hexs.append(arg1)
      self.hexs.append(arg2)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('SPRITE')):

#      argTxt = line[len('SPRITE')+1:]
      idx0 = line.rfind('(')
      idx1 = line.rfind(')')
      argTxt = line[idx0+1:idx1]
      strArgs = argTxt.split(',')
      nn = int(strArgs[0], 16)
      xx = int(strArgs[1], 16)
      yy = int(strArgs[2], 16)

      self.hexs.append(0xb0)
      self.hexs.append(nn)
      self.hexs.append(xx)
      self.hexs.append(yy)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('ATTACK_EFFECT')):

      idx0 = line.rfind('(')
      idx1 = line.rfind(')')
      argTxt = line[idx0+1:idx1]
      strArgs = argTxt.split(',')
      tt = int(strArgs[0], 16)
      xx = int(strArgs[1], 16)
      yy = int(strArgs[2], 16)

      self.hexs.append(0xba)
      self.hexs.append(tt)
      self.hexs.append(xx)
      self.hexs.append(yy)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('TELEPORT')):

      idx0 = line.find('=')
      strArgs = line[idx0+3: len(line)-1]
#      print('strArgs: ' + strArgs)
      strArgsSplit = strArgs.split(',')
      args = [ int(u, 16) for u in strArgsSplit ]
#      print('args: ' + str(args))

      # si es el teleport 1
      if(not line[8] == '2'): 
        self.hexs.append(0xf4)
      # sino, es el teleport 2
      else:
        self.hexs.append(0xf3)

      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    # si es texto
    elif(line.startswith('<')):
      # indico que es en modo texto
      self.textMode = True

#      print('LINE: ' + line)

      compactLine = line.replace('<TEXT_MODE_ON>',         u'\U0001F60A')
      compactLine = compactLine.replace('<TEXT_MODE_OFF>', u'\U0001F61E')
      compactLine = compactLine.replace('<TEXTBOX_SHOW>',  u'\U0001F639')
      compactLine = compactLine.replace('<TEXTBOX_HIDE>',  u'\U0001F63F')
      compactLine = compactLine.replace('<PAUSE>',         u'\U0001F610')
      compactLine = compactLine.replace('<ENTER>',         u'\U0001F618')
      compactLine = compactLine.replace('<SUMO>',          u'\U0001F466')
      compactLine = compactLine.replace('<FUJI>',          u'\U0001F467')
      compactLine = compactLine.replace('<CLS>',           u'\U0001F61D')
      compactLine = compactLine.replace('<BACKSPACE>',     u'\U0001F61E')
      compactLine = compactLine.replace('<CARRY>',         u'\U0001F634')
      compactLine = compactLine.replace('<NI_IDEA>',       u'\U0001F624')
      compactLine = compactLine.replace('<ICON a0>', u'\U00002200')
      compactLine = compactLine.replace('<ICON a1>', u'\U00002201')
      compactLine = compactLine.replace('<ICON a2>', u'\U00002202')
      compactLine = compactLine.replace('<ICON a3>', u'\U00002203')
      compactLine = compactLine.replace('<ICON a4>', u'\U00002204')
      compactLine = compactLine.replace('<ICON a5>', u'\U00002205')
      compactLine = compactLine.replace('<ICON a6>', u'\U00002206')
      compactLine = compactLine.replace('<ICON a7>', u'\U00002207')
      compactLine = compactLine.replace('<ICON a8>', u'\U00002208')
      compactLine = compactLine.replace('<ICON a9>', u'\U00002209')
      compactLine = compactLine.replace('<ICON aa>', u'\U0000220a')
      compactLine = compactLine.replace('<ICON ab>', u'\U0000220b')
      compactLine = compactLine.replace('<ICON ac>', u'\U0000220c')
      compactLine = compactLine.replace('<ICON ad>', u'\U0000220d')
      compactLine = compactLine.replace('<ICON ae>', u'\U0000220e')
      compactLine = compactLine.replace('<ICON af>', u'\U0000220f')


#      print('compactLine: ' + compactLine)

      sizeLine = len(compactLine)
      i = 0
      while(i < sizeLine):
        char = compactLine[i]

        if(char == u'\U0001F60A'):
          self.hexs.append(0x04)
        elif(char == u'\U0001F61E'):
          self.hexs.append(0x00)
        elif(char == u'\U0001F639'):
          self.hexs.append(0x10)
        elif(char == u'\U0001F63F'):
          self.hexs.append(0x11)
        elif(char == u'\U0001F610'):
          self.hexs.append(0x12)
        elif(char == u'\U0001F618'):
          self.hexs.append(0x1a)
        elif(char == u'\U0001F466'):
          self.hexs.append(0x14)
        elif(char == u'\U0001F467'):
          self.hexs.append(0x15)
        elif(char == u'\U0001F61D'):
          self.hexs.append(0x1b)
        elif(char == u'\U0001F634'):
          self.hexs.append(0x1f)
        elif(char == u'\U0001F624'):
          self.hexs.append(0x13)
        elif(char == u'\U00002200'):
          self.hexs.append(0xa0)
        elif(char == u'\U00002201'):
          self.hexs.append(0xa1)
        elif(char == u'\U00002202'):
          self.hexs.append(0xa2)
        elif(char == u'\U00002203'):
          self.hexs.append(0xa3)
        elif(char == u'\U00002204'):
          self.hexs.append(0xa4)
        elif(char == u'\U00002205'):
          self.hexs.append(0xa5)
        elif(char == u'\U00002206'):
          self.hexs.append(0xa6)
        elif(char == u'\U00002207'):
          self.hexs.append(0xa7)
        elif(char == u'\U00002208'):
          self.hexs.append(0xa8)
        elif(char == u'\U00002209'):
          self.hexs.append(0xa9)
        elif(char == u'\U0000220a'):
          self.hexs.append(0xaa)
        elif(char == u'\U0000220b'):
          self.hexs.append(0xab)
        elif(char == u'\U0000220c'):
          self.hexs.append(0xac)
        elif(char == u'\U0000220d'):
          self.hexs.append(0xad)
        elif(char == u'\U0000220e'):
          self.hexs.append(0xae)
        elif(char == u'\U0000220f'):
          self.hexs.append(0xaf)

        else:
          # agarro dos chars seguidos
          chars = compactLine[i:i+2]

#          if(chars in Dictionary.instance().invDeDict.keys()):
          if(chars in Dictionary.instance().chars()):
#            hexy = Dictionary.instance().invDeDict[chars]
            hexy = Dictionary.instance().encodeChars(chars)
#            print('chars: ' + chars + ' - hex: {:02x}'.format(hexy))

            i += 1
          else:
            char = chars[0]
#            hexy = Dictionary.instance().invDeDict[char]
            hexy = Dictionary.instance().encodeChars(char)
#            print('char: ' + char + ' - hex: {:02x}'.format(hexy))
          
          self.hexs.append(hexy)

        i += 1

      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('FOR')):

      idx0 = line.rfind('<')
      strI = line[idx0+1:]
      i = int(strI,16)

      sizeLines = 1
      deep = 1
      bloqueLines = []
      while( deep != 0 ):

        subLine = self.lines[sizeLines].strip()
        bloqueLines.append(subLine)
        sizeLines += 1

        if(subLine.startswith('FOR')):
          deep += 1
        elif(subLine == 'END'):
          deep -= 1

      bloque = Script(self.addr + 3)
      bloque.decodeTxt(bloqueLines)
      self.script = bloque

      self.hexs.append(0x03)
      self.hexs.append(i)

      hexs = bloque.encodeRom()

      strHex = Util.instance().strHexa(hexs)
#      print('strHex: ' + strHex)
      self.hexs.append( len(hexs) )

      self.sizeLines = sizeLines
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('IF')):

      idx0 = line.find('(')
      idx1 = line.find(')')

      argTxt = line[idx0+1: idx1]
#      print('argTxt: ' + argTxt)

      argsTxt = argTxt.split(' ')
      # elimino el último (está vacío, por el espacio al final antes del paréntesis)
      argsTxt.pop()

      sizeLines = 1
      deep = 1
      bloqueLines = []
      while( deep != 0 ):

        subLine = self.lines[sizeLines].strip()
        bloqueLines.append(subLine)
        sizeLines += 1

        if(subLine.startswith('IF')):
          deep += 1
        elif(subLine.startswith('ENDIF')):
          deep -= 1

      if(line.startswith('IF(')):
        self.hexs.append(0x08)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
#          arg = int(strArg, 16)
          arg = Variables.instance().getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3)
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

      elif(line.startswith('IF_EQUIP(')):
        self.hexs.append(0x09)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = Variables.instance().getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3)
        bloque.decodeTxt(bloqueLines)
        self.script = bloque




      self.hexs.extend(args)
      self.hexs.append(0x00)

      hexs = bloque.encodeRom()
      strHex = Util.instance().strHexa(hexs)
#      print('strHex: ' + strHex)

      self.hexs.append( len(hexs) )
      self.sizeLines = sizeLines
      self.sizeBytes = len(self.hexs)



    elif(line.startswith('STRANGE_IF')):

      idx0 = line.find('(')
      idx1 = line.find(')')

      argTxt = line[idx0+1: idx1]
#      print('argTxt: ' + argTxt)

      argsTxt = argTxt.split(' ')
      # elimino el último (está vacío, por el espacio al final antes del paréntesis)
      argsTxt.pop()

      args = []
      for strArg in argsTxt:
#        print('strArg: ' + strArg)
        arg = int(strArg, 16)
#        print('arg: {:02x}'.format(arg))
        args.append(arg)

      strEjec = line[idx1+1:]
      ejec = int(strEjec, 16)

      # si es el if raro 1
      if(line[10] == '1'):
        self.hexs.append(0x0a)
      elif(line[10] == '2'):
        self.hexs.append(0x0b)
      elif(line[10] == '3'):
        self.hexs.append(0x0c)
 
      self.hexs.extend( args )
      self.hexs.append( 0x00 )
      self.hexs.append( ejec )
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


  def __str__(self):
#    return self.strCode + ' | ' + self.strHex
    return self.strCode
#    return '\n{:04x} '.format(self.addr) + self.strCode
#    return '(' + self.strHex + ')' + self.strCode 

##########################################################
@Singleton
class Variables:

  def __init__(self):
    # diccionario de variables
    self.variables = {}
    for i in range(0,0x78):
      self.variables[i] = 'var_{:02x}'.format(i)
    for i in range(0x78,0x80):
      self.variables[i] = 'var_sinbatt_{:02x}'.format(i)

    # diccionario de monstruos
    self.monstruos = {}
    for i in range(0,0x15):
      self.monstruos[i] = 'monst_{:02x}'.format(i)

    self.equipamiento = {}
    # 0x09 empieza los items de items
    # 0x42 empieza los items de armas

    self.items = []
    self.items.append('💧Cure')
    self.items.append('💧X-Cure')
    self.items.append('💧Ether')
    self.items.append('💧X-Ether')
    self.items.append('💧Elixir')
    self.items.append('💧Pure')
    self.items.append('💧Eyedrp')
    self.items.append('💧Soft')
    self.items.append('💧Moogle')
    self.items.append('💧Unicorn')
    self.items.append('🔮Silence')
    self.items.append('🔮Pillow')
    self.items.append('0c af e5')
    self.items.append('0d d7 e5')
    self.items.append('🔮Flame')
    self.items.append('🔮Blaze')
    self.items.append('🔮Blizrd')
    self.items.append('🔮Frost')
    self.items.append('🔮Litblt')
    self.items.append('🔮Thundr')
    self.items.append('🍬Candy')
    self.items.append('15 8a a7')
    self.items.append('🔑Key')
    self.items.append('🔑Bone')
    self.items.append('🔑Bronze')
    self.items.append('19 a4 a2')
    self.items.append('1a 94 50')
    self.items.append('1b 8a 8e')
    self.items.append('1c 8a 8f')
    self.items.append('1d da d0')
    self.items.append('1e ff c6')
    self.items.append('1f db c8')
    self.items.append('20 c8 cb')
    self.items.append('💧Amanda')
    self.items.append('22 63 e2')
    self.items.append('23 dc f2')
    self.items.append('💧Oil')
    self.items.append('25 c7 d0')
    self.items.append('26 c7 d0')
    self.items.append('27 c7 d0')
    self.items.append('28 c7 d0')
    self.items.append('💎Crystal')
    self.items.append('2a dc f2')
    self.items.append('💎Nectar')
    self.items.append('💎Stamina')
    self.items.append('💎Wisdom')
    self.items.append('💎Will')
    self.items.append('2f 99 8b')
    self.items.append('30 62 e7')
    self.items.append('💰Gold')
    self.items.append('💰Fang')
    self.items.append('33 4a 8b')
    self.items.append('34 de f2')
    self.items.append('𐇞Mattok')
    self.items.append('💰Ruby')
    self.items.append('💰Opal')
    self.items.append('38 e3 59')

    self.magias = []
    self.magias.append('Cure')
    self.magias.append('Heal')
    self.magias.append('Mute')
    self.magias.append('Slep')
    self.magias.append('Fire')
    self.magias.append('Ice ')
    self.magias.append('Lit ')
    self.magias.append('Nuke')

    self.armas = []
    self.armas.append('🗡Broad')
    self.armas.append('🪓Battle')
    self.armas.append('🔨Sickle')
    self.armas.append('🔗Chain')
    self.armas.append('🗡Silver')
    self.armas.append('🡔Wind')
    self.armas.append('🪓Were')
    self.armas.append('💣Star')
    self.armas.append('🗡Blood')
    self.armas.append('🗡Dragon')
    self.armas.append('🔗Flame')
    self.armas.append('🗡Ice')
    self.armas.append('🪓Zeus')
    self.armas.append('🗡Rusty')
    self.armas.append('🡔Thunder')
    self.armas.append('🗡XCalibr')
    self.armas.append('👕Bronze')
    self.armas.append('👕Iron')
    self.armas.append('👕Silver')
    self.armas.append('👕Gold')
    self.armas.append('👕Flame')
    self.armas.append('👕Ice')
    self.armas.append('👕Dragon')
    self.armas.append('👕Samurai')
    self.armas.append('👕Opal')
    self.armas.append('19 e1 e6')
    self.armas.append('1a e1 e6')
    self.armas.append('⛨Bronze')
    self.armas.append('⛨Iron')
    self.armas.append('⛨Silver')
    self.armas.append('⛨Gold')
    self.armas.append('⛨Flame')
    self.armas.append('⛨Dragon')
    self.armas.append('⛨Aegis')
    self.armas.append('⛨Opal')
    self.armas.append('⛨Ice')
    self.armas.append('24 99 9c')
    self.armas.append('25 99 9c')
    self.armas.append('🎩Bronze')
    self.armas.append('🎩Iron')
    self.armas.append('🎩Silver')
    self.armas.append('🎩Gold')
    self.armas.append('🎩Opal')
    self.armas.append('🎩Samurai')
    self.armas.append('2c 8f 51')
    self.armas.append('2d 8f 51')


#    nombresOriginales = False
    nombresOriginales = True
    # si esta seteado mostrar los nombres originales
    if(nombresOriginales):
      # se setea automáticamente si al intentar agregar un item resulta que estaba lleno
      self.variables[0x05] = 'INVENTARIO_LLENO' 
      # se setea automáticamente si no alcanza el dinero luego de comparar
      self.variables[0x06] = 'ORO_INSUFICIENTE' 
      # se setea automáticamente cuando mate a todos en el bloque?
      self.variables[0x07] = 'MATO_TODOS' 
      self.variables[0x08] = 'MURIO_WILLY'
      self.variables[0x09] = 'DARK_LORD_ME_DESCUBRIO'
      self.variables[0x0a] = 'RESCATAMOS_FUJI_HONGOS'
      self.variables[0x0b] = 'FUJI_SE_PRESENTO'
      self.variables[0x0c] = 'BOGARD_NOS_DIO_MATTOCK'
      self.variables[0x0d] = 'DRACULA_SECUESTRO_FUJI'
      self.variables[0x0e] = 'SUMO_RESCATO_FUJI_ATAUD'
      self.variables[0x10] = 'FUJI_VIO_SU_MADRE_WENDEL'
      self.variables[0x11] = 'JULIUS_SECUESTRO_FUJI_WENDEL'
      self.variables[0x12] = 'EMERGIO_TORRE_DESIERTO'
      self.variables[0x13] = 'VENCIMOS_METAL_CRAB_CANGREJO'
      self.variables[0x14] = 'ENCONTRAMOS_PLATA'
      self.variables[0x15] = 'VENCIMOS_MANTIS_ANT_COATI_GIGANTE'
      self.variables[0x16] = 'DESPEGO_ZEPELIN'
      self.variables[0x17] = 'VENCIMOS_DRAGON_ROJO'
      self.variables[0x18] = 'VENCIMOS_JULIUS2'
      self.variables[0x19] = 'NACIO_CHOCOBO'
      self.variables[0x1a] = 'DAVIAS_NOS_CONTO_CUEVA_MEDUZA'
      self.variables[0x1b] = 'AMANDA_SE_DISCULPO_POR_ROBAR_AMULETO'
      self.variables[0x1c] = 'SACRIFICAMOS_A_AMANDA'
      self.variables[0x1d] = 'LESTER_SE_CURO_DE_SER_PAPAGAYO'
      self.variables[0x1e] = 'RESCATAMOS_FUJI_DARK_LORD'
      self.variables[0x1f] = 'BOGARD_DISCUTIO_SUMO'
      self.variables[0x20] = 'SARAH_NOS_CONTO_ACCIDENTE_BOGARD'
      self.variables[0x21] = 'LISTO_CHOCOBOT'
      self.variables[0x22] = 'ESPADA_OXIDADA_RECUPERA_SU_ENERGIA'
      self.variables[0x23] = 'VENCIMOS_DRAGON_2_CABEZAS'
      self.variables[0x24] = 'VENCIMOS_LOBITO'
      self.variables[0x25] = 'VENCIMOS_LEE_DRACULA'
      self.variables[0x26] = 'VENCIMOS_MEGAPEDE_CIENPIES'
      self.variables[0x27] = 'VENCIMOS_MEDUSA'
      self.variables[0x28] = 'VENCIMOS_DAVIAS'
      self.variables[0x29] = 'VENCIMOS_CYCLOPE_DEJA_MORNINGSTAR'
      self.variables[0x2a] = 'VENCIMOS_CHIMERA_LEON_ALAS'
      self.variables[0x2b] = 'VENCIMOS_GOLEM_ROBOT_MORNINGSTAR'
      self.variables[0x2c] = 'VENCIMOS_DARK_LORD'
      self.variables[0x2d] = 'VENCIMOS_KARY_HIELO'
      self.variables[0x2e] = 'VENCIMOS_KRAKEN_PUENTE'
      self.variables[0x2f] = 'VENCIMOS_PIRUS_IFLYTE_BOLA_SOL'
      self.variables[0x30] = 'VENCIMOS_LICH_SENSEMANN_ESQUELETO'
      self.variables[0x31] = 'VENCIMOS_GARUDA_AGUILA'
      self.variables[0x32] = 'VENCIMOS_DRAGON'
      self.variables[0x34] = 'VENCIMOS_DRAGON_ZOMBIE'
      self.variables[0x35] = 'OBTUVIMOS_LAGRIMA_AMANDA'
      self.variables[0x36] = 'DESCUBRIMOS_CUEVA_DESIERTO'
      self.variables[0x37] = 'SE_DERRUMBO_PUENTE'
      self.variables[0x38] = 'OBTUVIMOS_EXCALIBUR'
      self.variables[0x39] = 'OBTUVIMOS_ROPA_ORO'
      self.variables[0x3a] = 'OBTUVIMOS_ESPADA_HIELO'
      self.variables[0x3b] = 'OBTUVIMOS_ESPADA_OXIDADA'
      self.variables[0x3c] = 'OBTUVIMOS_ESPADA_SANGRE'
      self.variables[0x3d] = 'OBTUVIMOS_ESCUDO_AEGIS'
      self.variables[0x3e] = 'OBTUVIMOS_HACHA_ZEUS'
      self.variables[0x3f] = 'OBTUVIMOS_HACHA_WERE'
      self.variables[0x40] = 'ENCONTRAMOS_LATIGO'
      self.variables[0x41] = 'ENCONTRAMOS_STICKLE'
      self.variables[0x43] = 'OBTUVIMOS_ESCUDO_DRAGON'
      self.variables[0x44] = 'OBTUVIMOS_ROPA_DRAGON'
      self.variables[0x46] = 'OBTUVIMOS_ESPADA_MISTERIOSA'
      self.variables[0x47] = 'ENTRAMOS_CUEVA_DESIERTO'
      self.variables[0x48] = 'ENCONTRAMOS_ESPEJO'
      self.variables[0x49] = 'ENCONTRAMOS_MAGIA_FUEGO'
      self.variables[0x4a] = 'ENCONTRAMOS_MAGIA_HIELO'
      self.variables[0x4c] = 'OBTUVIMOS_ESPADA_DRAGON'
      self.variables[0x4d] = 'ENCONTRAMOS_MATTOCK'
      self.variables[0x4e] = 'ENCONTRAMOS_MORNING_STAR'
      self.variables[0x4f] = 'ENCONTRAMOS_ESCUDO_HIELO'
      self.variables[0x51] = 'FUJI_ACOMPANIA'
      self.variables[0x52] = 'JULIUS_ACOMPANIA'
      self.variables[0x53] = 'WATTS_ACOMPANIA'
      self.variables[0x54] = 'BOGARD_ACOMPANIA'
      self.variables[0x55] = 'AMANDA_ACOMPANIA'
      self.variables[0x56] = 'LESTER_ACOMPANIA'
      self.variables[0x57] = 'MARCIE_ACOMPANIA'
      self.variables[0x58] = 'CHOCOBO_ACOMPANIA'
      self.variables[0x5b] = 'DEJE_CHOCOBO_EN_01'
      self.variables[0x5c] = 'DEJE_CHOCOBO_EN_02'
      self.variables[0x5d] = 'DEJE_CHOCOBO_EN_03'
      self.variables[0x5e] = 'DEJE_CHOCOBO_EN_04'
      self.variables[0x5f] = 'DEJE_CHOCOBO_EN_05'
      self.variables[0x60] = 'DEJE_CHOCOBO_EN_06'
      self.variables[0x61] = 'DEJE_CHOCOBO_EN_07'
      self.variables[0x62] = 'DEJE_CHOCOBO_EN_08'
      self.variables[0x63] = 'DEJE_CHOCOBO_EN_09'
      self.variables[0x64] = 'DEJE_CHOCOBO_EN_10'
      self.variables[0x65] = 'DEJE_CHOCOBO_EN_11'
      self.variables[0x66] = 'DEJE_CHOCOBO_EN_12'
      self.variables[0x67] = 'DEJE_CHOCOBO_EN_13'
      self.variables[0x68] = 'DEJE_CHOCOBO_EN_14'
      self.variables[0x69] = 'DEJE_CHOCOBO_EN_15'
      self.variables[0x6a] = 'DEJE_CHOCOBO_EN_16'
      self.variables[0x6b] = 'DEJE_CHOCOBO_EN_17'
      self.variables[0x6c] = 'DEJE_CHOCOBO_EN_18'
      self.variables[0x6d] = 'DEJE_CHOCOBO_EN_19'
      self.variables[0x6e] = 'DEJE_CHOCOBO_EN_20'
      self.variables[0x6f] = 'ARRIBA_DEL_CHOCOBO'
      self.variables[0x70] = 'CHOCOBOT_SOBRE_AGUA'
      # cuando nos hacen una pregunta si-no
      self.variables[0x7f] = 'ELIGIMOS_NO'

      # nombres de los monstruos grandes
      self.monstruos[0x00] = 'LEE_DRACULA'
      self.monstruos[0x01] = 'DRAGON_AGUA_2_CABEZAS'
      self.monstruos[0x02] = 'MEDUSA'
      self.monstruos[0x03] = 'MEGAPEDE_CIENPIES'
      self.monstruos[0x04] = 'DAVIAS'
      self.monstruos[0x05] = 'GOLEM_ROBOT_MORNINGSTAR'
      self.monstruos[0x06] = 'CYCLOPE_DEJA_MORNINGSTAR'
      self.monstruos[0x07] = 'CHIMERA_LEON_ALAS'
      self.monstruos[0x08] = 'KARY_HIELO'
      self.monstruos[0x09] = 'KRAKEN_PUENTE'
      self.monstruos[0x0a] = 'PIRUS_IFLYTE_BOLA_SOL'
      self.monstruos[0x0b] = 'LICH_SENSEMANN_ESQUELETO'
      self.monstruos[0x0c] = 'GARUDA_AGUILA'
      self.monstruos[0x0d] = 'DRAGON'
      self.monstruos[0x0e] = 'JULIUS2'
      self.monstruos[0x0f] = 'DRAGON_ZOMBIE'
      self.monstruos[0x10] = 'MONSTRUO_INICIO'
      self.monstruos[0x11] = 'JULIUS3'
      self.monstruos[0x12] = 'METAL_CRAB_CANGREJO'
      self.monstruos[0x13] = 'MANTIS_ANT_COATI_GIGANTE'
      self.monstruos[0x14] = 'DRAGON_ROJO'


  def getLabel(self, val):
    # el primer bit indica si hay que negar la variable
    neg = val >= 0x80
    if(neg):
      val -= 0x80
    strNeg = '' if not neg else '!'
#    strVar = 'var[{:02x}] '.format(cond)
    strVar = self.variables[val]
    label = strNeg + strVar
    return label

  def getVal(self, label):
    retVal = -1
#    print('ejecutando getVal(\'' + label + '\')')

    neg = False
    # si esta negada
    if(label.startswith('!')):
      # lo indico
      neg = True
      # y quito el '!' del label 
      label = label[1:]

    # por cada valor del diccionario de variables
    for val in self.variables.keys():
      # me fijo el label
      lbl = self.variables[val]
      # si lo encontré
      if(lbl == label):
        retVal = val
        # si estaba negada
        if(neg):
          # seteamos el primer bit
          retVal += 0x80

        break

    return retVal


  def getLabelMonstruo(self, val):
    label = self.monstruos[val]
    return label
  def getValMonstruo(self, label):
    # por cada monstruo 
    for val in self.monstruos.keys():
      # me fijo el label
      lbl = self.monstruos[val]
      # si lo encontré
      if(lbl == label):
        retVal = val
        break
    return retVal



##########################################################
class Scripts:
  """ representa el conjunto de scripts """

  def __init__(self):
    self.scripts = []


  def getAddr(self, nroScript):
    """ retorna el addr del script indicado """

    script = self.scripts[nroScript]
    addr = script.addr
    return addr

  def getScript(self, addr):
    """ retorna el script del addr indicado """

    # para cada script
    for script in self.scripts:
      # si es el del addr indicado
      if(script.addr == addr):
        # lo retorno
        return script
    # si llegó acá no está el script del addr indicado
    return None


  def decodeRom(self):
    self.scripts = []

    bank08 = RomSplitter.instance().banks[0x08]

    address = Address.instance().addrScriptAddrDic
    cantScripts = Address.instance().cantScripts

    # por cada nroScript
    for nroScript in range(0,cantScripts):

      addr8 = address + 2*nroScript 
#      print('---addr8: {:04x} '.format(addr8))

      addr = bank08[addr8:addr8+2]
      addr1 = addr[0]
      addr2 = addr[1]
      # obtengo su addr
      addr = addr2*0x100 + addr1
#      print('addr: {:04x}'.format(addr))

      script = Script(addr)
      script.nro = nroScript

      banco = 0x0d
      if(addr >= 0x4000):
        banco = 0x0e
        addr -= 0x4000
      array = RomSplitter.instance().banks[banco]
      # creo un array desde donde empieza el script
      array = array[addr:]

      # decodifico el script
      vaPorAddr = script.decodeRom(array)
      # y lo agrego a la lista de scripts 
      self.scripts.append(script)
#      print('script: ' + str(script))


      import random
      rr = random.randint(0,0xff)
      gg = random.randint(0,0xff)
      bb = random.randint(0,0xff)
      # grabo las romstats
      if(script.addr < 0x4000):
        RomStats.instance().appendDato(0x0d, script.addr, vaPorAddr, (rr, gg, bb), 'un script')
      else:
        RomStats.instance().appendDato(0x0e, script.addr - 0x4000, vaPorAddr - 0x4000, (rr, gg, bb), 'un script')
#      print('romstats {:04x} {:04x}'.format(script.addr, vaPorAddr))



  def encodeTxt(self):
    newLines = []

    for val in Variables.instance().variables.keys():
      var = Variables.instance().variables[val]
#      print('key: ' + labelVar + ' value: ' + str(nroVar))
      newLines.append('let ' + var + ' = var[{:02x}]'.format(val))

    txt = ''

    # para cada script
    for script in self.scripts:
      txt += script.encodeTxt()


    # 2da pasada (rellena CALLs)
#    filepath = path + '/scripts_00.txt'
#    f = open(filepath, 'r')
#    txt = f.read()
#    f.close()

    lines = txt.splitlines()
    # para cada renglón
    for line in lines:
      # si no tiene CALL
      if('CALL' not in line):
        # lo deja como está
        newLines.append(line)
      # sino, el renglón tiene un CALL
      else:
        idx0 = line.find('CALL')

        # busco si tiene label
        idxLabel = line.find('$')
        # si no tiene label (tiene addr físico)
        if(idxLabel == -1):

          strAddr = line[idx0+5: idx0+9]
          addr = int(strAddr,16)
          # traduzco el addr en nroScript
          script = self.getScript(addr)
          strNroScript = '{:04x}'.format(script.nro)
          newLine = line[0:idx0+5] + '$' + strNroScript
          # y lo agrego
#          newLines.append('# old: ' + line)
          newLines.append(newLine)

        # sino, ya tiene label
        else:
          # salteo el símbolo '$'
          strLabel = line[idx0+6: idx0+10]

          newLine = line[0:idx0+5] + strLabel
          # y lo agrego
#          newLines.append('# old: ' + line)
          newLines.append(newLine)

    return newLines


  def decodeTxt(self, lines):

    self.scripts = []

    script = None
    # los renglones del script actual
    subLines = []

    for line in lines:
      # comienza un nuevo script
      if('script:' in line):

        # si había un script anterior
        if(script != None):

          # lo decodifico
          script.decodeTxt(subLines)
          # lo agrego a la lista
          self.scripts.append(script)
          # reinicio los renglones para el próximo script
          subLines = []

        lineSplit = line.split()
        nroScript = int(lineSplit[2],16)
        addr = int(lineSplit[4],16)
#        print('nroScript: {:04x} addr: {:04x}'.format(nroScript, addr))

        # creo el script
        script = Script(addr)
        script.nro = nroScript

#      elif('CALL:' in line):
#        print('callll: ' + line)

      else:
        if(line.strip().startswith('let')):
          line = line.strip()
          subLine = line[3:].strip()
          idx0 = subLine.index('=')
          var = subLine[:idx0].strip()
          strVal = subLine[idx0+1:].strip()
          idx1 = strVal.index('[')
          idx2 = strVal.index(']')
          strVal = strVal[idx1+1:idx2].strip()
          val = int(strVal,16)
#          print('var: ' + var + ' --- val: {:02x}'.format(val))
          Variables.instance().variables[val] = var

          
        else:
          subLines.append(line)

    # lo decodifico
    script.decodeTxt(subLines)
    # lo agrego a la lista
    self.scripts.append(script)
    # reinicio los renglones para el próximo script
    subLines = []

  def _refreshLabels(self, nroBanco, ultimoNroScriptBanco0d):
    """ refresca los labels de los CALLs con su addr física, según si es para el banco 0x0d ó 0x0e """

    # recorro todos los scripts
    for script in self.scripts:
      string, calls = script.iterarRecursivoRom(0)

      for cmd in calls:
        label = cmd.jumpLabel
#        print('label: ' + label)

        strNroScript = label[1:5]
#        print('strNroScript: ' + strNroScript)
        nroScript = int(strNroScript, 16)

        addr = self.getAddr(nroScript)
#        print('addr: {:04x}'.format(addr))

        addr1 = addr // 0x100
        addr2 = addr % 0x100

#        print('addr1 addr2 {:02x} {:02x}'.format(addr1, addr2))

        # actualizo su addr
        cmd.hexs = [0x02, addr1, addr2]
        # actualizo el call con el addr físico
        cmd.strCode = 'CALL {:04x}'.format(addr)
 

        # si es para el banco 0x0d pero el script no entra
        if(nroBanco == 0x0d and script.nro > ultimoNroScriptBanco0d):
          # seteo addr en 0x0000
          cmd.hexs = [0x02, 0x00, 0x00]
          cmd.strCode = 'CALL {:04x}'.format(0x0000)



  def encodeRom(self):
    # los bancos a devolver 
    array0d = []
    array0e = []

    vaPorAddr = 0x0000
    # el último script que entró en el banco 0d
    ultimoNroScriptBanco0d = -1

    lang = Address.instance().language

    # para cada script
#    for script in self.scripts:
    for i in range(0,len(self.scripts)):
      script = self.scripts[i]
      # lo codifico
      subArray = script.encodeRom()

      # calculo addr donde termina
      proxAddr = vaPorAddr + len(subArray)
      # si empieza antes pero termina después de 0x4000 (rom 'de' y custom)
      if(vaPorAddr < 0x4000 and proxAddr >= 0x4000):
        # cambio al bank siguiente
        vaPorAddr = 0x4000
        # el script anterior fué el último en entrar completo en el banco
        ultimoNroScriptBanco0d = script.nro - 1

        # si la rom es 'en' ó 'fr'
        if(lang in [ENGLISH, FRENCH]):
          # el script anterior se vuelve a copiar al principio del banco siguiente
          self.scripts[i-1].addr = 0x4000
          vaPorAddr += len(self.scripts[i-1].encodeRom())
          ultimoNroScriptBanco0d = script.nro - 2

#      print('script {:04x} addrAnt {:04x} addrNew {:04x}'.format(script.nro, script.addr, vaPorAddr))

      # si no es un script vacío
      if(len(script.listComandos) > 0):
        # actualizo el addr del script !!
        script.addr = vaPorAddr
        # sumo para el addr del próximo script
        vaPorAddr += len(subArray)
      # sino, está en NULL
      else:
        # seteo su addr en 0x0000 
        script.addr = 0x0000


    self._refreshLabels(0x0d, ultimoNroScriptBanco0d)

    # recorro todos los scripts
    for script in self.scripts:

#      if(True):
      if(script.nro <= ultimoNroScriptBanco0d):
        subArray = script.encodeRom()

        # voy extendiendo el array
        array0d.extend(subArray)

    self._refreshLabels(0x0e, ultimoNroScriptBanco0d)

    # recorro todos los scripts
    for script in self.scripts:

      if(script.nro > ultimoNroScriptBanco0d):
        subArray = script.encodeRom()

        # voy extendiendo el array
        array0e.extend(subArray)

    size0d = min(len(array0d),0x4000)
    size0e = min(len(array0e),0x4000)

    return array0d[:size0d], array0e[:size0e]

##########################################################
class Script:
  """ representa un script """

  def __init__(self, addr):
    # el address en la rom 'd' o 'e' (si es >= 0x4000)
    self.addr = addr

    # el nroScript
    self.nro = 0x0000

    # la lista de comandos
    self.listComandos = []


  def iterarRecursivoRom(self, depth):

    string = ''
    calls = []

    for cmd in self.listComandos:
#      print('cmd: ' + (' ' * 2*depth) + ' ' + str(cmd))
#      string += (' ' * 2*depth) + ' ' + str(cmd) + '\n'
#      string += (' ' * 2*depth) + str(cmd) 
#      string += str(cmd) 

      # si no está en modo texto
      if(cmd.textMode == False):
        # hay que tabular
        renglon = (' ' * 2*depth) + str(cmd) 
      # sino, es modo texto
      else:
        # y no hay que tabular
        renglon = str(cmd) 

#      print('textMode: ' + str(cmd.textMode) + ' | ' + renglon)
      string += renglon

      # si es un CALL (y no está comentado)
#      if(cmd.nro == 0x02):
#      if('CALL' in cmd.strCode and not cmd.strCode.startswith('#')):
      if(cmd.strCode.startswith('CALL')):
#        calls.append(cmd.strCode)
        calls.append(cmd)

      # si tiene script propio
      if(cmd.script != None):
        # lo llamo recursivamente
        newString,newCalls = cmd.script.iterarRecursivoRom(depth + 1)
        string += newString
        calls.extend(newCalls)

    return string, calls


  def decodeRom(self, array):
    """ decodifica un script """

    # inicializo por que addr vamos
    vaPorAddr = self.addr

    idx = 0
    # si está en modo texto o no
    textMode = False
    while(True):

      cmd = Comando(vaPorAddr)
      textMode = cmd.decodeRom(array[idx:], textMode)
#      print('cmd: ' + str(cmd))
      idx += cmd.size

#      vaPorAddr += len(cmd.hexs)
      vaPorAddr += cmd.size

      self.listComandos.append(cmd)

#      print('strCode: ' + cmd.strCode)

#      if(cmd.strCode.strip() in ['ERROR', 'END']):
      if(cmd.strCode[:3] in ['ERR', 'END']):
#        break
        return vaPorAddr

  def decodeTxt(self, lines):
    """ decodifica un script txt """

    # si está en NULL
    if(len(lines)>0):
      firstLine = lines[0].strip()
      if(firstLine == 'NULL'):
        # seteo el addr en 0
        self.addr = 0x0000
        # y retorno sin hacer mas nada
        return

    vaPorAddr = self.addr
    idx = 0
    while(True):

      cmd = Comando(vaPorAddr)
      cmd.decodeTxt(lines[idx:])
#      print('cmd: ' + str(cmd))
      idx += cmd.sizeLines

      vaPorAddr += len(cmd.hexs)
#      vaPorAddr += cmd.size 

      self.listComandos.append(cmd)

#      print('strCode: ' + cmd.strCode)

#      if(cmd.strCode.strip() in ['ERROR', 'END']):
      if(cmd.strCode[:3] in ['ERR', 'END']):
        break

  def encodeTxt(self):
    string = ''

#    string += '\n--------------------\n'
#    string += 'script: {:04x}'.format(self.nro) + '\n'
#    string += 'addr: {:04x}'.format(self.addr) + '\n'
    string += '\n--- script: {:04x} addr: {:04x} ------------------\n'.format(self.nro, self.addr)

    # cuando devuelve 0x0000 no es un script usado
    if(not (self.addr == 0x0000 and self.nro > 0)):
      strScript, newCalls = self.iterarRecursivoRom(depth=0)
      string += strScript
    else:
      string += 'NULL\n'

    return string


  def encodeRom(self):
    array = []

    for cmd in self.listComandos:
      array.extend(cmd.hexs)
      # si tiene script propio
      if(cmd.script != None):
        # lo llamo recursivamente
        newHexs = cmd.script.encodeRom()
        array.extend(newHexs)
    return array

  def __str__(self):
    return 'Script {:04x}'.format(self.nro)


##########################################################
class SpriteSheetPersonaje:
  """ representa un spriteSheet de personajes """

  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.sprites = []

  def decodeRom(self, array):

    # para cada spritePersonaje del sheet
    for k in range(0, self.w*self.h):

      spritePers = SpritePersonaje()
      spritePers.decodeRom(array)
      self.sprites.append(spritePers)

      array = array[16*4:]

  def encodePng(self):

    w = self.w
    h = self.h

    sheetData = [ [0x03 for i in range(0,16*w) ] for j in range(0,16*h) ]

    # los junto en un sheetData
    for k in range(0,self.w*self.h):
      sprite = self.sprites[k]
      for j in range(0,16):
        for i in range(0,16):
          sheetData[16*(k//w) + j][16*(k%w) + i] = sprite.spriteData[j][i]

    return sheetData

  def decodePng(self, sheetData):

    w = self.w
    h = self.h

    # los junto en un sheetData
    for k in range(0,self.w*self.h):

#      sprite = self.sprites[k]

      # para cada spritePersonaje
      sprite = SpritePersonaje()

      for j in range(0,16): 
        for i in range(0,16): 
          sprite.spriteData[j][i] = sheetData[16*(k//w) + j][16*(k%w) + i] 

      self.sprites.append(sprite)

  def encodeRom(self):

    array = []

    for spritePers in self.sprites:
      subArray = spritePers.encodeRom()
      array.extend(subArray)

    return array


  def encodeTxt(self):
    lines = []

    w = self.w
    h = self.h

    sheetData = self.encodePng()
#    print('sheetData: ' + str(sheetData))
      
#    chars = [ ' ', '.', '*', 'X' ]
    chars = [ '.', '+', '*', 'X' ]
#    chars = [ '0', '1', '2', '3' ]

    for j in range(0,h*16):
      line = ''
      for i in range(0,w*16):

        val = sheetData[j][i]
#        print('val = {:02x}'.format(val))

        line += chars[val]

#      print('line: ' + line)
      lines.append(line)

    return lines

##########################################################
class SpritePersonaje:
  """ representa un sprite de un personaje """

  def __init__(self):
    self.spriteData = [ [0x03 for i in range(0,16) ] for j in range(0,16) ]

  def decodeRom(self, array):

    tiles = []

    # agarro los 4 tiles
    for i in range(0,4):
      tile = Tile()
      tile.decodeRom(array)
      tiles.append(tile)
      array = array[16:]

    # los junto en un spriteData
    for k in range(0,4):
      tile = tiles[k]
      for j in range(0,8): 
        for i in range(0,8): 
          self.spriteData[8*(k//2) + j][8*(k%2) + i] = tile.tileData[j*8+i]

  def encodePng(self):
    return self.spriteData

  def decodePng(self, spriteData):
    self.spriteData = spriteData

  def encodeRom(self):
    array = []

    # para cada uno de lo 4 tiles
    for k in range(0,4):
      tile = Tile()
      # armo su tileData
      for j in range(0,8): 
        for i in range(0,8): 
          tile.tileData[j*8+i] = self.spriteData[8*(k//2) + j][8*(k%2) + i]

      # lo encodeo
      subArray = tile.encodeRom()
      # y lo agrego al array
      array.extend(subArray)

    return array


  def encodeTxt(self):
    lines = []
      
#    chars = [ ' ', '.', '*', 'X' ]
    chars = [ '.', '+', '*', 'X' ]
#    chars = [ '0', '1', '2', '3' ]

    for j in range(0,16):
      line = ''
      for i in range(0,16):
        val = self.spriteData[j][i]
        line += chars[val]

#      print('line: ' + line)
      lines.append(line)

    return lines

##########################################################
class Tile:
  """ representa un tile de 8x8 """

  def __init__(self):

#    self.tileData = [ [0x03 for i in range(0,8) ] for j in range(0,8) ]
    self.tileData = [ 0x03 for i in range(0,8*8) ]

  def decodeRom(self, array):

    # para cada renglón
    for j in range(0,8):
      # para cada bit (columna)
      for i in range(0,8):

#        b0isSet = array[2*j]   & (2**(7-i)) != 0
#        b1isSet = array[2*j+1] & (2**(7-i)) != 0
#        b0 = 1 if b0isSet else 0
#        b1 = 1 if b1isSet else 0

        b0 = int('{:08b}'.format(array[2*j])[i])
        b1 = int('{:08b}'.format(array[2*j+1])[i])
        color = (2*b1 + b0)

#        print('(i,j) = ' + str(i) + ', ' + str(j))
#        print('color = ' + str(color))
#        s[j][i] = color

#        self.tileData[j][i] = color
        self.tileData[i + 8*j] = color


  def encodePng(self):
    return self.tileData

  def decodePng(self, tileData):
    self.tileData = tileData

  def encodeRom(self):

    array = []

    # por cada renglón
    for j in range(0,8):
      byte0 = 0b00000000
      byte1 = 0b00000000

      # por cada columna
      for i in range(0,8):

        color =  self.tileData[i + 8*j]

        if(color == 3):
          byte0 = byte0 | 2**(7-i)
          byte1 = byte1 | 2**(7-i)
        elif(color == 2):
          byte1 = byte1 | 2**(7-i)
        elif(color == 1):
          byte0 = byte0 | (2**(7-i))

#      print('bytes: {:02x}, {:02x}'.format(byte0, byte1))
      # genero los 2 bytes y los agrego
      array.extend( [byte0, byte1] )

    return array

  def encodeTxt(self):
    lines = []

#    chars = [ ' ', '.', '*', 'X' ]
    chars = [ '.', '+', '*', 'X' ]
#    chars = [ '0', '1', '2', '3' ]

    line = ''
    for k in range(0,8*8):
 
      val = self.tileData[k]
      line += chars[val]
      if(k%8 == 7):
        lines.append(line)
        line = ''
      
    return lines

  def decodeTxt(self, lines):

#    chars = [ ' ', '.', '*', 'X' ]
    chars = [ '.', '+', '*', 'X' ]

    k = 0
    for line in lines:
      for char in line:
#        print('char: ' + char)
        idx = chars.index(char)
        self.tileData[k] = idx
        k += 1


  def exportPngFile(self, filepath):
    """ exporta a un archivo .png de 8x8 pixels """

#    w = png.Writer(8, 8, greyscale=True, bitdepth=2)
    w = png.Writer(8, 8)
    tileData = self.encodePng()

    # creo el array
    s = []
    for j in range(8):
      row = []
      for i in range(8):
        color = 255 - tileData[i+8*j]*255//3
        row.append(color)
      s.append(row)

    f = open(filepath, 'wb')
    w.write(f, s)
    f.close()

  def importPngFile(self, filepath):
    """ importa de un archivo .png de 8x8 pixels """

    r = png.Reader(filepath)
    w,h,rows,info = r.read()

    k = 0
    for row in rows:
      for val in row:
        print('val: {:02x}'.format(val))
        self.tileData[k] = (255-val)*3//255
        k += 1


##########################################################
class Tileset:
  """ representa un tileset """

  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.tiles = []

  def decodeRom(self, array):

    for i in range(0,self.w*self.h):
      subArray = array[i*0x10:(i+1)*0x10]

      tile = Tile()
      tile.decodeRom(subArray)
      self.tiles.append(tile)

  def encodeRom(self):
    array = []

    for tile in self.tiles:
      subArray = tile.encodeRom()
      array.extend(subArray)

    return array

  def exportPngFile(self, filepath):
    """ exporta a un archivo .png """

    # inicializo el array
    s = []
    for j in range(8*self.h):
      row = []
      for i in range(8*self.w):
        row.append(3)
      s.append(row)

    k = 0
    for tile in self.tiles:

      u = k % self.w
      v = k // self.w

      # para cada renglón
      for j in range(0,8):
        # para cada bit (columna)
        for i in range(0,8):

          val = tile.tileData[i+8*j]
          b0 = val % 2
          b1 = val // 2

          color = 255 - (2*b1 + b0)*255//3

#          print('(i,j) = ' + str(i) + ', ' + str(j))
#          print('color = ' + str(color))
#          s[j][i] = color

          s[8*v+j][8*u+i] = color

      k += 1

    f = open(filepath, 'wb')
#    w = png.Writer(8*self.w, 8*self.h, greyscale=True, bitdepth=2)
    w = png.Writer(8*self.w, 8*self.h)
    w.write(f, s)
    f.close()

  def importPngFile(self, filepath):
    """ importa de un archivo .png de tileset """

    # inicializo el array
    s = []
    for j in range(8*self.h):
      row = []
      for i in range(8*self.w):
        row.append(3)
      s.append(row)


    r = png.Reader(filepath)
    w,h,rows,info = r.read()
    i,j = 0,0
    for row in rows:
      for val in row:
        s[j][i] = val
        i += 1
      j += 1
      i = 0


    for v in range(0, self.h):
      for u in range(0, self.w):

        tileData = []
        # para cada renglón
        for j in range(0,8):
          # para cada bit (columna)
          for i in range(0,8):

            val = (255 - s[8*v+j][8*u+i])*3//255
#            print('val {:02x}'.format(val))
            tileData.append(val)
#          print('\n')

        tile = Tile()
        tile.tileData = tileData
        self.tiles.append(tile)
           

##########################################################
class MapaInterior:
  """ representa un mapa interior """

  def __init__(self, nroMapa):
    self.nroMapa = nroMapa
    self.tipo = 0 # 0=exterior, 1=interior
    self.compress = None
    self.sizeX = None
    self.sizeY = None
    self.headerLoco = None
    # los sprites del fondo de la habitación (igual para todo el mapa)
    self.spritesFondo = [ [0x00 for i in range(0,10)] for j in range(0,8) ]
    self.bloques = []

  def decodeRom(self, array):

    # agarro el header de 4 bytes
    tipo          = array[0]
    # c3f9: 3 o 4 (cuantas veces se repite el sprite cuando comprime)
    compress = array[1]
    sizeY    = array[2]
    sizeX    = array[3]
#    print('tipo,compress,sizeY,sizeX = {:02x},{:02x},{:02x},{:02x}'.format(tipo,compress,sizeY,sizeX))
    self.tipo, self.compress, self.sizeX, self.sizeY = tipo, compress, sizeX, sizeY

    # salteo el header
    array = array[4:]

    # salteo puntero a habitación interior
    array = array[2:]

    # agarro el headerLoco
    headerLoco = array[:24]
    strHeaderLoco = Util.instance().strHexa(headerLoco)
    self.headerLoco = headerLoco
#    print('headerLoco: ' + strHeaderLoco)

    # salteo el headerLoco
    array = array[24:]
    
    # salteo los punteros (addr absolutos) (4 bytes por bloque)
    array = array[4*sizeX*sizeY:]

    # agarro el bloque de sprites para la habitación
    bloqueInterior = BloqueExterior()
    bloqueInterior._decodeRomSprites(array, compress)
    self.spritesFondo = bloqueInterior.sprites

    subArray = bloqueInterior._encodeRomSprites(compress, disabledSpriteBytes=8)
    strSprites = Util.instance().strHexa(subArray)

    # salteo el bloque de sprites para la habitación
    array = array[len(subArray):]

    # para cada bloque
    for i in range(0, sizeX*sizeY):

#      print('----- bloque: ' + str(i))

      bloque = BloqueInterior()
      bloque.mapa = self
      bloque.decodeRom(array)

      subArray = bloque.encodeRom()

#      strArray = Util.instance().strHexa(subArray)
#      print('----------------------- strArray: ' + strArray)
      array = array[len(subArray):]

      self.bloques.append(bloque)

  def encodeTxt(self):

    lines = []

    lines.append('tipo: {:02x}'.format(self.tipo))
    lines.append('compress: {:02x}'.format(self.compress))
    lines.append('width: {:02x}'.format(self.sizeX))
    lines.append('height: {:02x}'.format(self.sizeY))

    # el bloque interior
    bloqueInterior = BloqueExterior()
    bloqueInterior.sprites = self.spritesFondo
    subLines = bloqueInterior._encodeTxtSprites()
    lines.extend(subLines)

    strHeaderLoco = Util.instance().strHexa(self.headerLoco)
    lines.append('headerLoco: ' + strHeaderLoco)

    i = 0
    for bloque in self.bloques:

      yy = i // self.sizeX
      xx = i % self.sizeX

      lines.append('\n--------------------')
      lines.append('bloque (x,y) = ({:02x},{:02x})'.format(xx,yy))

      subLines = bloque.encodeTxt()
      lines.extend(subLines)

      i += 1

    return lines

  def decodeTxt(self, lines):

    strTipo = lines[0][6:]
    strCompress = lines[1][10:]
    strSizeX = lines[2][7:]
    strSizeY = lines[3][8:]

    tipo = int(strTipo,16)
    compress = int(strCompress,16)
    sizeX = int(strSizeX,16)
    sizeY = int(strSizeY,16)

    self.tipo, self.compress, self.sizeX, self.sizeY = tipo, compress, sizeX, sizeY

    # salteo el header
    lines = lines[4:]

    # el bloque interior
    bloqueInterior = BloqueExterior()
    bloqueInterior._decodeTxtSprites(lines)
    self.spritesFondo = bloqueInterior.sprites
#    bloqueInterior.sprites = self.spritesFondo
#    subLines = bloqueInterior._encodeTxtSprites()
#    lines.extend(subLines)

    # salteo el bloque interior
    lines = lines[8:]

    # agarro el headerLoco
    strHeaderLoco = lines[0][12:].strip()
    headerLoco = Util.instance().hexaStr(strHeaderLoco)
    self.headerLoco = headerLoco

    # salteo el headerLoco
    lines = lines[1:]

    for i in range(0, len(lines)):
      line = lines[i]

      if(line.startswith('bloque')):

        bloque = BloqueInterior()
        bloque.mapa = self
        bloque.decodeTxt(lines[i+1:])
        self.bloques.append(bloque)


  def encodeRom(self, idx0):
    """ el idx0 es el addr donde comienza el mapa en el banko (para armar los índices) """

    array = []

    array.append(self.tipo)
    array.append(self.compress)
    array.append(self.sizeY)
    array.append(self.sizeX)

    tipo, compress, sizeX, sizeY = self.tipo, self.compress, self.sizeX, self.sizeY

    bloqueInterior = BloqueExterior()
    bloqueInterior.sprites = self.spritesFondo
    subArray = bloqueInterior._encodeRomSprites(compress, disabledSpriteBytes=8)
    
    # calculo donde se graba bloqueInterior
    idx0 += 4 + 4*sizeX*sizeY + 0x4000 + 2 + len(self.headerLoco)
    nro1 = idx0 // 0x100
    nro2 = idx0 % 0x100
    # lo agrego
    array.extend([nro2, nro1])

    # agrego el bloqueInterior
    bloqueInterior = BloqueExterior()
    bloqueInterior.sprites = self.spritesFondo
    subArrayBloqueInterior = bloqueInterior._encodeRomSprites(compress, disabledSpriteBytes=8)

    # agrego el headerLoco
    array.extend(self.headerLoco)

    idx0 += len(subArrayBloqueInterior)

    # creo los índices 
    indices = []

    bloquesArray = []
    for bloque in self.bloques:

      indices.append(idx0)
      subArray = bloque._encodeRomEvents()
      bloquesArray.extend(subArray)
      idx0 += len(subArray)

      indices.append(idx0)
      subArray = bloque._encodeRomSprites()
      bloquesArray.extend(subArray)
      idx0 += len(subArray)

    idxArray = []
    for index in indices:

      nro1 = index // 0x100
      nro2 = index % 0x100

      idxArray.append(nro2)
      idxArray.append(nro1)

    # agrego los índices
    array.extend(idxArray)

    # agrego el bloqueInterior
    array.extend(subArrayBloqueInterior)

    # y los bloques
    array.extend(bloquesArray)

    return array

  def exportPngFile(self, filepath, sheet):

    # creo un array vacío 
    newSprites = []

    for j in range(0, self.sizeY):
      for v in range(0, 8):
        for i in range(0, self.sizeX):
          for u in range(0, 10):

            bloque = self.bloques[j*self.sizeX + i]
            nroSpriteEncontrado = self.spritesFondo[v][u]

            sprites = bloque.getSprites()
            nroSprite = sprites[v][u]
            if(nroSprite != None):
              nroSpriteEncontrado = nroSprite

            sprite = sheet.sprites[nroSpriteEncontrado]
            newSprites.append(sprite)


    dibu = SpriteSheet(10*self.sizeX,8*self.sizeY, sheet.nroSpriteSheet, 'png')
    dibu.sprites = newSprites

    # y exporto el .png
    dibu.exportPngFile(filepath)


##########################################################
class BloqueInterior:
  """ representa un bloque de un mapa interior """

  def __init__(self):

    # el nroScript que se ejecuta al ingresar al bloque (y nroScript+1 se ejecuta al salir del bloque)
    self.eventoEntrada = None
    self.listEvents = []

    self.doorRight = None
    self.doorLeft  = None
    self.doorNorth = None
    self.doorSouth = None
    self.listSprites = []

    # los bloques interiores siempre estan habilitados? (ponen eventoEntrada 0xffff para deshabilitar?)
    self.enabled = True

    # el mapa al cual pertenece
    self.mapa = None

  def getSprites(self):
    """ devuele los sprites, agregando el mapa de fondo """

    w, h = 10, 8

    # creo matriz de nroSprites en 0x00
    sprites = [ [None for i in range(0,w)] for j in range(0,h) ]

    der, izq, arr, aba = self.doorRight, self.doorLeft, self.doorNorth, self.doorSouth

    # 0x00 = abierto
    # 0x01 = puerta sin llave
    # 0x02 = pared
    # 0x05 = puerta con llave
    # 0x08 = nroScript 008

    # si a la der hay pared
    if(der == 0x02):
      sprites[4][9] = 0x45
      sprites[3][9] = 0x15
    if(izq == 0x02):
      sprites[4][0] = 0x40
      sprites[3][0] = 0x10
    if(arr == 0x02):
      sprites[0][4] = 0x28
      sprites[0][5] = 0x04
    if(aba == 0x02):
      sprites[7][4] = 0x51
      sprites[7][5] = 0x54
   
    for j in range(0,h):
      for i in range(0,w):

        nroSprite = None

        # en principio lo inicializo con el fondo
        if(self.mapa != None):
          nroSpriteFondo = self.mapa.spritesFondo[j][i]
          nroSprite = nroSpriteFondo

        pos = j*0x10+i
        nroSpriteItem = self.getSprite(pos)
        
        if(nroSpriteItem != None):
          nroSprite = nroSpriteItem

        if(nroSprite == None):
          nroSprite = 0

        sprites[j][i] = nroSprite

    return sprites


  def getSprite(self, posDado):
    """ devuelve el nroSprite correspondiente al pos indicado, si tiene alguno """

    nroSpriteEncontrado = None

    for pos, nroSprite in self.listSprites:
      
      if(posDado == pos):
        nroSpriteEncontrado = nroSprite
        break

    return nroSpriteEncontrado

  def decodeRom(self, array):

    self._decodeRomEvents(array)

    subArray = self._encodeRomEvents()
    array = array[len(subArray):]

    self._decodeRomSprites(array)


  def encodeTxt(self):
    lines = []

    subLines = self._encodeTxtEvents()
    lines.extend(subLines)
    subLines = self._encodeTxtSprites()
    lines.extend(subLines)

    return lines

  def decodeTxt(self, lines):
    self._decodeTxtEvents(lines)
    self._decodeTxtSprites(lines[2:])


  def encodeRom(self):
    array = []

    subArray = self._encodeRomEvents()
    array.extend(subArray)
    subArray = self._encodeRomSprites()
    array.extend(subArray)

    return array

  def _decodeRomEvents(self, array):

    # reseteo los valores
    self.eventoEntrada = None
    self.listEvents = []

    nroScript = array[1] * 0x100 + array[0]
    self.eventoEntrada = nroScript
#    print('eventoEntrada: {:04x}'.format(nroScript))

    i = 2
    pos = array[i]
    # mientras no termine el listado
    while(pos != 0xFF):

      # obtengo nro de script
      nroScript = array[i+2] * 0x100 + array[i+1]
      
      # lo agrego con su posición en el bloque 
      self.listEvents.append( (pos, nroScript) )
#      print('evento: {:02x}, {:04x}'.format(pos, nroScript))

      i += 3
      pos = array[i]

  def _decodeRomSprites(self, array):

    # reseteo los valores
    self.listSprites = []

    # info sobre las salidas
    right, left, north, south = array[0], array[1], array[2], array[3]
    # 0x00 = abierto
    # 0x01 = puerta del otro lado?
    # 0x02 = pared
    # 0x05 = puerta con llave?
    self.doorRight = right
    self.doorLeft  = left
    self.doorNorth = north
    self.doorSouth = south
#    print('right, left, north, south = {:02x}, {:02x}, {:02x}, {:02x}'.format(right,left,north,south))

    i = 4
    nroSprite = array[i]
    # mientras no termine el listado
    while(nroSprite != 0xFF):
      pos = array[i+1]
      self.listSprites.append( (pos, nroSprite) )
      i += 2
      nroSprite = array[i]


  def _encodeTxtEvents(self):
    lines = []

    lines.append('eventoEntrada: {:04x}'.format(self.eventoEntrada))

    strEventos = ''
    for pos, nroScript in self.listEvents:
      strEventos += '({:02x},{:04x})'.format(pos, nroScript)
#      lines.append('evento: {:02x}, {:04x}'.format(pos, nroScript))

    lines.append('eventos: ' + strEventos)

    return lines


  def _encodeTxtSprites(self):

    lines = []

    right, left, north, south = self.doorRight, self.doorLeft, self.doorNorth, self.doorSouth
    lines.append('right,left,north,south = {:02x},{:02x},{:02x},{:02x}'.format(right,left,north,south))

    strSprites = '' 
    for pos, nroSprite in self.listSprites:
      strSprites += '({:02x},{:02x})'.format(pos, nroSprite)
#      lines.append('sprite: {:02x}, {:04x}'.format(pos, nroSprite))

    lines.append('sprites: ' + strSprites)

    return lines


  def _decodeTxtEvents(self, lines):

    # reseteo los valores
    self.eventoEntrada = None
    self.listEvents = []

    strEventoEntrada = lines[0][15:15+4]
    self.eventoEntrada = int(strEventoEntrada, 16)

    strListEventos = lines[1][9:]
    strEventos = strListEventos.split('(')

    for strEvento in strEventos:
      if(strEvento not in ['', '\n']):
        strPos = strEvento[0:2]
        strNroScript = strEvento[3:3+4] 

        pos = int(strPos, 16)
        nroScript = int(strNroScript, 16)

        self.listEvents.append( (pos, nroScript) )


  def _encodeRomEvents(self):

    array = []

    nro1 = self.eventoEntrada // 0x100
    nro2 = self.eventoEntrada % 0x100
    array.extend( [nro2, nro1] )

    for pos, nroScript in self.listEvents:
      array.append(pos)
      
      nro1 = nroScript // 0x100
      nro2 = nroScript % 0x100
      array.extend( [nro2, nro1] )

    array.append(0xff)

    return array


  def _decodeTxtSprites(self, lines):

    # reseteo los valores
    self.listSprites = []
 
    line = lines[0]
    strRight = line[25:27]
    strLeft  = line[28:30]
    strNorth = line[31:33]
    strSouth = line[34:36]
    right = int(strRight,16)
    left  = int(strLeft,16)
    north = int(strNorth,16)
    south = int(strSouth, 16)

    self.doorRight, self.doorLeft, self.doorNorth, self.doorSouth = right,left,north,south

    strListSprites = lines[1][9:]
#    print('strListSprites: ' + strListSprites)

    strSprites = strListSprites.split('(')

    for strSprite in strSprites:
      strSprite = strSprite.strip()
      # si no es renglón vacío
      if(len(strSprite) > 0):
        strPos = strSprite[0:2]
        strNroSprite = strSprite[3:3+2] 
        pos = int(strPos, 16)
        nroSprite = int(strNroSprite, 16)

        self.listSprites.append( (pos, nroSprite) )


  def _encodeRomSprites(self):
    array = []


    right, left, north, south = self.doorRight, self.doorLeft, self.doorNorth, self.doorSouth
    array.extend( [right, left, north, south] )

    for pos, nroSprite in self.listSprites:
      array.extend( [nroSprite, pos] )

    array.extend( [0xFF, 0xFF] )

    return array

  def exportPngFile(self, filepath, sheet):

    w, h = 10, 8
    # creo un spriteSheet vacío
    dibu = SpriteSheet(w,h,sheet.nroSpriteSheet, 'png')

    sprites = self.getSprites()

    newSprites = []
    for j in range(0,h):
      for i in range(0,w): 

        nroSprite = sprites[j][i]
        sprite = sheet.sprites[nroSprite]
        newSprites.append(sprite)

    dibu.sprites = newSprites

    # y exporto el .png
    dibu.exportPngFile(filepath)




##########################################################
class Mapas:
  """ representa el listado de mapas """

  def __init__(self):
    # el listado de mapas
    self.mapas = []

  def decodeRom(self):

    bank08 = RomSplitter.instance().banks[0x08]
    # para cada mapa
    for nroMapa in range(0,0x10):

      mapArray = bank08[11*nroMapa:11*(nroMapa+1)]

      # el nro de spriteSheet
      nroSpriteSheet = mapArray[1]//0x10
      # por ahora no se para que es este byte
      nose = mapArray[2]
      # el address del spriteSheet
      spriteAddr = mapArray[4] * 0x100 + mapArray[3]
      # el tamaño en cantidad de sprites (6 bytes por sprite)
      cantSprites = mapArray[5]
      # el banco del palette
      mapBank = mapArray[6]
      # el address del mapa
      mapAddr = mapArray[8] * 0x100 + mapArray[7] - 0x4000
      # por ahora no se para que es este addr
      noseAddr = mapArray[10] * 0x100 + mapArray[9]


      array = RomSplitter.instance().banks[mapBank]
      array = array[mapAddr:]

      # creo el mapa-wrapper
      mapa = Mapa(nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr)
      mapa.decodeRom(array)
      # lo agrego a la lista
      self.mapas.append(mapa)

  def encodeTxt(self):

    lines = []

    for mapa in self.mapas:

      subLines = mapa.encodeTxt()
      lines.extend(subLines)

    return lines

  def decodeTxt(self, lines):

    self.mapas = []
    mapa = None
    subLines = []

    for line in lines:

      subLines.append(line)

#      print('line: ' + line)
      if('nroMapa:' in line):
#        print(line)

        idx0 = line.find('nroMapa:')
        strMapa = line[idx0+9:idx0+9+2]
        nroMapa = int(strMapa,16)
#        print('nroMapa: {:02x}'.format(nroMapa))

        idx0 = line.find('nroSpriteSheet:')
        strNroSpriteSheet = line[idx0+16:idx0+16+2]
        nroSpriteSheet = int(strNroSpriteSheet,16)
#        print('nroSpriteSheet: {:02x}'.format(nroSpriteSheet))

        idx0 = line.find('spriteAddr:')
        strSpriteAddr = line[idx0+12:idx0+12+4]
        spriteAddr = int(strSpriteAddr,16)
#        print('spriteAddr: {:02x}'.format(spriteAddr))

        idx0 = line.find('nose:')
        strNose = line[idx0+6:idx0+6+2]
        nose = int(strNose,16)
#        print('nose: {:02x}'.format(nose))

        idx0 = line.find('cantSprites:')
        strCantSprites = line[idx0+13:idx0+13+2]
        cantSprites = int(strCantSprites,16)
#        print('cantSprites: {:02x}'.format(cantSprites))

        idx0 = line.find('mapBank:')
        strMapBank = line[idx0+9:idx0+9+2]
        mapBank = int(strMapBank,16)
#        print('mapBank: {:02x}'.format(mapBank))

        idx0 = line.find('mapAddr:')
        strMapAddr = line[idx0+9:idx0+9+4]
        mapAddr = int(strMapAddr,16)
#        print('mapAddr: {:02x}'.format(mapAddr))

        idx0 = line.find('noseAddr:')
        strNoseAddr = line[idx0+10:idx0+10+4]
        noseAddr = int(strNoseAddr,16)
#        print('noseAddr: {:04x}'.format(noseAddr))

        # si había un mapa anterior
        if(mapa != None):
          mapa.decodeTxt(subLines)
          self.mapas.append(mapa)
        mapa = Mapa(nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr)
        subLines = []


    mapa.decodeTxt(subLines)
    self.mapas.append(mapa)
##########################################################
class Mapa:
  """ representa el wrapper de un mapa """

  def __init__(self, nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr):

    self.mapa = None

    self.nroMapa = nroMapa
    self.nroSpriteSheet = nroSpriteSheet
    self.nose = nose
    self.spriteAddr = spriteAddr
    self.cantSprites = cantSprites
    self.mapBank = mapBank
    self.mapAddr = mapAddr
    self.noseAddr = noseAddr

  def decodeRom(self, array):

    # --- obtengo el mapa
    TIPO_EXTERIOR = 0
    TIPO_INTERIOR = 1

#    array = RomSplitter.instance().banks[self.mapBank]
#    array = array[self.mapAddr:]

    tipo     = array[0]
    # c3f9: 3 o 4 (cuantas veces se repite el sprite cuando comprime)
    compress = array[1]
    sizeY    = array[2]
    sizeX    = array[3]

    if(tipo == TIPO_EXTERIOR):
      mapa = MapaExterior(self.nroMapa)
      mapa.decodeRom(array)
    else:
      mapa = MapaInterior(self.nroMapa)
      mapa.decodeRom(array)

    self.mapa = mapa

  def encodeRom(self, mapAddr):
    subArray = self.mapa.encodeRom(mapAddr)
    return subArray

  def encodeTxt(self):
    lines = []

    line = '\n---------- nroMapa: {:02x} nroSpriteSheet: {:02x} nose: {:02x} spriteAddr: {:04x} cantSprites: {:02x} mapBank: {:02x} mapAddr: {:04x} noseAddr: {:04x}'.format(self.nroMapa, self.nroSpriteSheet, self.nose, self.spriteAddr, self.cantSprites, self.mapBank, self.mapAddr, self.noseAddr)
    lines.append(line)

    subLines = self.mapa.encodeTxt()
    lines.extend(subLines)
    return lines

  def decodeTxt(self, lines):

    TIPO_EXTERIOR = 0
    TIPO_INTERIOR = 1

    line = lines[0]
    idx0 = line.find('tipo:')
    strTipo = line[idx0+6:idx0+6+2]
#    print('strTipo: ' + strTipo)
    tipo = int(strTipo,16)
#    print('tipo: {:02x}'.format(tipo))

    if(tipo == TIPO_EXTERIOR):
      mapa = MapaExterior(self.nroMapa)
      mapa.decodeTxt(lines)
    else:
      mapa = MapaInterior(self.nroMapa)
      mapa.decodeTxt(lines)

    self.mapa = mapa

  def exportPngFile(self, filepath):

    basePath = Address.instance().basePath

    # agarro el spriteSheet del nroSpriteSheet indicado
    sheet = RomSplitter.instance().spriteSheets[self.nroSpriteSheet]

    filepath = basePath + '/mapas/mapa_{:02}_{:02x}.png'.format(self.nroMapa, self.nroMapa)
    self.mapa.exportPngFile(filepath, sheet)


  def exportTiled(self, filepath):


    lines = []

    # --- obtengo el mapa
    TIPO_EXTERIOR = 0
    TIPO_INTERIOR = 1

    tipo = self.mapa.tipo

    width  = self.mapa.sizeX*10
    height = self.mapa.sizeY*8

    # el id a ir incrementando
    iidd = 1

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<map version="1.5" tiledversion="1.5.0" orientation="orthogonal" renderorder="right-down" width="' + str(width) + '" height="' + str(height) + '" tilewidth="16" tileheight="16" infinite="0" nextlayerid="4" nextobjectid="13">')

    lines.append(' <properties>')
    lines.append(' <property name="nroMapa" value="{:02x}"/>'.format(self.nroMapa))
    lines.append(' <property name="nroSpriteSheet" value="{:02x}"/>'.format(self.nroSpriteSheet))
    lines.append(' <property name="nose" value="{:02x}"/>'.format(self.nose))
    lines.append(' <property name="spriteAddr" value="{:04x}"/>'.format(self.spriteAddr))
    lines.append(' <property name="cantSprites" value="{:02x}"/>'.format(self.cantSprites))
    lines.append(' <property name="mapBank" value="{:02x}"/>'.format(self.mapBank))
    lines.append(' <property name="mapAddr" value="{:04x}"/>'.format(self.mapAddr))
    lines.append(' <property name="noseAddr" value="{:04x}"/>'.format(self.noseAddr))

    lines.append(' <property name="tipo" value="{:02x}"/>'.format(self.mapa.tipo))
    lines.append(' <property name="compress" value="{:02x}"/>'.format(self.mapa.compress))
    lines.append(' <property name="sizeY" value="{:02x}"/>'.format(self.mapa.sizeY))
    lines.append(' <property name="sizeX" value="{:02x}"/>'.format(self.mapa.sizeX))

    # si el mapa es interior
    if(self.mapa.tipo == TIPO_INTERIOR):
      # exporto el headerLoco
      headerLoco = self.mapa.headerLoco
      strHeaderLoco = Util.instance().strHexa(headerLoco)
      lines.append(' <property name="headerLoco" value="' + strHeaderLoco + '"/>')

    lines.append('</properties>')


    # le asocio el tileset correcto
    lines.append(' <tileset firstgid="1" source="../spriteSheets/sheet_{:02x}.tsx"/>'.format(self.nroSpriteSheet))
    # creo el mapa
    lines.append(' <layer id="' + str(iidd) + '" name="Tile Layer 1" width="' + str(width) + '" height="' + str(height) + '">')
    iidd += 1
    lines.append('  <data encoding="csv">')

    for j in range(0,height):
      renglon = ''
      for i in range(0,width):

#        renglon += '0'

        bloquex = i//10
        bloquey = j//8
        bloque = self.mapa.bloques[bloquey*self.mapa.sizeX + bloquex]

#        nroSprite = bloque.sprites[j%8][i%10]
        nroSprite = bloque.getSprites()[j%8][i%10]

        renglon += str(nroSprite+1)

        if(i != width-1 or j != height-1):
          renglon += ','
      lines.append(renglon)
        
    lines.append('  </data>')
    lines.append(' </layer>')

    # creo bloquesA
    lines.append(' <objectgroup color="#005500" id="' + str(iidd) + '" name="Object Layer bloquesA">')
    iidd += 1
    for j in range(0,self.mapa.sizeY):
      for i in range(0,self.mapa.sizeX):
        bloque = self.mapa.bloques[j*self.mapa.sizeX + i]
        enabled = 'true'
        if(bloque.enabled == False):
          enabled = 'false'
        eventoEntrada = '{:04x}'.format(bloque.eventoEntrada)
        if( (i+j) % 2 == 0):
          lines.append('  <object id="' + str(iidd) + '" type="bloqueA" x="' + str(i*10*16) + '" y="' + str(j*8*16) + '" width="160" height="127">')
          iidd += 1
          lines.append('   <properties>')
          lines.append('    <property name="enabled" type="bool" value="' + enabled + '"/>')
          lines.append('    <property name="eventoEntrada" value="' + eventoEntrada + '"/>')
          if(self.mapa.tipo == TIPO_INTERIOR):
            lines.append('    <property name="right,left,north,south" value="{:02x},{:02x},{:02x},{:02x}"/>'.format(bloque.doorRight,bloque.doorLeft,bloque.doorNorth,bloque.doorSouth))
          lines.append('   </properties>')
          lines.append('  </object>')
    lines.append(' </objectgroup>')

    # creo bloquesB
    lines.append(' <objectgroup color="#aa0000" id="' + str(iidd) + '" name="Object Layer bloquesB">')
    iidd += 1
    for j in range(0,self.mapa.sizeY):
      for i in range(0,self.mapa.sizeX):
        bloque = self.mapa.bloques[j*self.mapa.sizeX + i]
        enabled = 'true'
        if(bloque.enabled == False):
          enabled = 'false'
        eventoEntrada = '{:04x}'.format(bloque.eventoEntrada)
        if( (i+j) % 2 != 0):
          lines.append('  <object id="' + str(iidd) + '" type="bloqueB" x="' + str(i*10*16) + '" y="' + str(j*8*16) + '" width="160" height="127">')
          iidd += 1
          lines.append('   <properties>')
          lines.append('    <property name="enabled" type="bool" value="' + enabled + '"/>')
          lines.append('    <property name="eventoEntrada" value="' + eventoEntrada + '"/>')
          if(self.mapa.tipo == TIPO_INTERIOR):
            lines.append('    <property name="right,left,north,south" value="{:02x},{:02x},{:02x},{:02x}"/>'.format(bloque.doorRight,bloque.doorLeft,bloque.doorNorth,bloque.doorSouth))
          lines.append('   </properties>')
          lines.append('  </object>')
    lines.append(' </objectgroup>')


    # creo eventos
    lines.append(' <objectgroup color="#ffaaff" id="' + str(iidd) + '" name="Object Layer eventos">')
    iidd += 1

    for j in range(0,self.mapa.sizeY):
      for i in range(0,self.mapa.sizeX):
        bloque = self.mapa.bloques[j*self.mapa.sizeX + i]

        for evt in bloque.listEvents:
          pos = evt[0]
          nroScript = evt[1]
          strNroScript = '{:04x}'.format(nroScript)

          posx = pos%0x10
          posy = pos//0x10

          evtx = i*10*16 + posx*16
          evty = j*8*16 + posy*16

          lines.append('  <object id="' + str(iidd) + '" type="Evento" x="' + str(evtx) + '" y="' + str(evty) + '" width="16" height="16">')
          iidd += 1
          lines.append('   <properties>')
          lines.append('    <property name="nroScript" value="' + strNroScript + '"/>')
          lines.append('   </properties>')
          lines.append('  </object>')

    lines.append(' </objectgroup>')

    lines.append('</map>')

    strTxt = '\n'.join(lines)

    f = open(filepath, 'w')
    f.write(strTxt)
    f.close()

  def importTiled(self, filepath):

    # --- obtengo el mapa
    TIPO_EXTERIOR = 0
    TIPO_INTERIOR = 1

    # el tipo es exterior
    tipo = TIPO_EXTERIOR
    # salvo que use nroSpriteSheets 2 ó 3
    if(self.nroSpriteSheet in [2,3]):
      # en cuyo caso es interior
      tipo = TIPO_INTERIOR


    if(tipo == TIPO_EXTERIOR):
      mapa = MapaExterior(self.nroMapa)
#      mapa.importTiled(filepath)
    else:
      mapa = MapaInterior(self.nroMapa)
#      mapa.importTiled(filepath)


    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()

    renglonesSprites = False
    listSprites = []
    renglonesA = False
    listBloquesA = []
    renglonesB = False
    listBloquesB = []
    renglonesEvento = False
    listEventos = []


    for line in lines:
#      print('line: ' + line)

      if('property name="tipo"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        tipo = int(strLine, 16)
      elif('property name="compress"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        compress = int(strLine, 16)
      elif('property name="sizeY"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        sizeY = int(strLine, 16)
      elif('property name="sizeX"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        sizeX = int(strLine, 16)

      elif('property name="headerLoco"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        headerLoco = strLine.split()
        headerLoco = [int(num,16) for num in headerLoco]


      if('</data>' in line):
        renglonesSprites = False
      if(renglonesSprites):
#        print('tiles: ' + line)
        tiles = line.strip().split(',')
#        print('tiles1: ' + str(tiles))
        tiles = [tile for tile in tiles if len(tile) > 0]
#        print('tiles2: ' + str(tiles))
        tiles = [int(tile)-1 for tile in tiles]
#        print('tiles3: ' + str(tiles))
        listSprites.extend(tiles)

      if('<data encoding="csv">' in line):
        renglonesSprites = True


      if('</object>' in line):

        if(renglonesA):
          renglonesA = False
          if(tipo == TIPO_EXTERIOR):
            listBloquesA.append( [enabled, eventoEntrada, bloqueX, bloqueY] )
          else:
            listBloquesA.append( [enabled, eventoEntrada, bloqueX, bloqueY, doors] )

        if(renglonesB):
          renglonesB = False
          if(tipo == TIPO_EXTERIOR):
            listBloquesB.append( [enabled, eventoEntrada, bloqueX, bloqueY] )
          else:
            listBloquesB.append( [enabled, eventoEntrada, bloqueX, bloqueY, doors] )

        if(renglonesEvento):
          renglonesEvento = False
          listEventos.append( [nroScript, evtX, evtY] )


      if('property name="enabled"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        enabled = (strLine == "true")
      elif('property name="eventoEntrada"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        eventoEntrada = int(strLine, 16)
      elif('property name="right,left,north,south"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        doors = strLine.split(',')
        doors = [int(door,16) for door in doors]
#        print('puertas: ' + str(doors))
      elif('property name="nroScript"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        nroScript = int(strLine, 16)
 
 
      if('type="bloqueA"' in line):
        renglonesA = True

        idx0 = line.index('x=')
        subLine = line[idx0+3:]
        idx1 = line.index('"',idx0+3)
        string = line[idx0+3:idx1]
#        print('stringx: ' + string)
        bloqueX = int(string)//(16*10)
 
        idx0 = line.index('y=')
        subLine = line[idx0+3:]
        idx1 = line.index('"',idx0+3)
        string = line[idx0+3:idx1]
#        print('stringy: ' + string)
        bloqueY = int(string)//(16*8)
#        print('coord: ' + str(bloqueX) + ', ' + str(bloqueY))
        
      if('type="bloqueB"' in line):
        renglonesB = True

        idx0 = line.index('x=')
        subLine = line[idx0+3:]
        idx1 = line.index('"',idx0+3)
        string = line[idx0+3:idx1]
#        print('stringx: ' + string)
        bloqueX = int(string)//(16*10)
 
        idx0 = line.index('y=')
        subLine = line[idx0+3:]
        idx1 = line.index('"',idx0+3)
        string = line[idx0+3:idx1]
#        print('stringy: ' + string)
        bloqueY = int(string)//(16*8)
#        print('coord: ' + str(bloqueX) + ', ' + str(bloqueY))
 

      if('type="Evento"' in line):
        renglonesEvento = True

        idx0 = line.index('x=')
        subLine = line[idx0+3:]
        idx1 = line.index('"',idx0+3)
        string = line[idx0+3:idx1]
#        print('stringx: ' + string)
        evtX = int(string)//(16)
 
        idx0 = line.index('y=')
        subLine = line[idx0+3:]
        idx1 = line.index('"',idx0+3)
        string = line[idx0+3:idx1]
#        print('stringy: ' + string)
        evtY = int(string)//(16)
#        print('coord: ' + str(evtX) + ', ' + str(evtY))
 

#    self.tipo, self.compress, self.sizeX, self.sizeY = tipo, compress, sizeX, sizeY
    mapa.tipo, mapa.compress, mapa.sizeX, mapa.sizeY = tipo, compress, sizeX, sizeY

    # si es mapa exterior
    if(tipo == TIPO_EXTERIOR):
      # creo los bloques
      bloques = [ [BloqueExterior() for i in range(0,sizeX)] for j in range(0,sizeY) ]
    # sino, es mapa interior
    else:
      mapa.headerLoco = headerLoco
      # creo los bloques
      bloques = [ [BloqueInterior() for i in range(0,sizeX)] for j in range(0,sizeY) ]

      # genero los sprites de fondo
      spritesFondo = [ [0x00 for i in range(0,10)] for j in range(0,8) ]
      # tomando como referencia el último bloque del mapa.  VOY POR ACA HAY QUE MEJORAR ESTO!!
      i,j = sizeX-1,sizeY-1
      # recorro los sprites interiores del primer bloque
      for v in range(0,8):
        for u in range(0,10):
          nroSprite = listSprites[j*8*10*sizeX + i*10 + v*sizeX*10+ u]
          # si está dentro del bloque
          if(u>0 and v>0 and u<9 and v<7):
            # lo limpio
            nroSprite = 0x00
          spritesFondo[v][u] = nroSprite
      mapa.spritesFondo = spritesFondo





#    print('len: ' + str(len(listSprites)))
#    print('sprites: ' + str(listSprites))

    for j in range(0, sizeY):
      for i in range(0, sizeX):

#        print('va por bloque: ' + str(i) + ', ' + str(j))
        bloque = bloques[j][i]
#        bloque.mapa = self
        bloque.mapa = mapa

        # si es mapa exterior
        if(tipo == TIPO_EXTERIOR):

          for enabled, eventoEntrada, bloqueX, bloqueY in listBloquesA:
            if(i == bloqueX and j == bloqueY):
              bloque.enabled = enabled
              bloque.eventoEntrada = eventoEntrada
#              print('encontro evento: {:04x}'.format(eventoEntrada))

          for enabled, eventoEntrada, bloqueX, bloqueY in listBloquesB:
            if(i == bloqueX and j == bloqueY):
              bloque.enabled = enabled
              bloque.eventoEntrada = eventoEntrada
#              print('encontro evento: {:04x}'.format(eventoEntrada))

          subSprites = [ [0x00 for i in range(0,10)] for j in range(0,8) ]
          for v in range(0,8):
            for u in range(0,10):
#              subSprites[v][u] = listSprites[j*sizeX*10+i*10 + u]
              subSprites[v][u] = listSprites[j*8*10*sizeX + i*10 + v*sizeX*10+ u]
          bloque.sprites = subSprites

        # sino, es tipo interior
        else:

          for enabled, eventoEntrada, bloqueX, bloqueY, doors in listBloquesA:
            if(i == bloqueX and j == bloqueY):
              bloque.enabled = enabled
              bloque.eventoEntrada = eventoEntrada
              bloque.doorRight, bloque.doorLeft, bloque.doorNorth, bloque.doorSouth = doors[0], doors[1], doors[2], doors[3]

          for enabled, eventoEntrada, bloqueX, bloqueY, doors in listBloquesB:
            if(i == bloqueX and j == bloqueY):
              bloque.enabled = enabled
              bloque.eventoEntrada = eventoEntrada
              bloque.doorRight, bloque.doorLeft, bloque.doorNorth, bloque.doorSouth = doors[0], doors[1], doors[2], doors[3]

          subListSprites = []
          # recorro los sprites
          for v in range(0,8):
            for u in range(0,10):
              nroSprite = listSprites[j*8*10*sizeX + i*10 + v*sizeX*10+ u]
              nroSpriteFondo = spritesFondo[v][u]
              # si cambió respecto al fondo
              if(nroSprite != nroSpriteFondo):
                pos = v*0x10 + u
                # lo agrego a la lista con su posición
                subListSprites.append( [pos, nroSprite] )
          # seteo la lista de sprites
          bloque.listSprites = subListSprites


    # recorro los eventos
    for nroScript, evtX, evtY in listEventos:
#      print('evento: {:04x} x: {:2} y: {:2}'.format(nroScript, evtX, evtY))
      # calculo coordenadas del bloque
      bloqueX = evtX//10
      bloqueY = evtY//8
      bloque = bloques[bloqueY][bloqueX]
      # y del evento dentro del bloque
      subX = evtX%10
      subY = evtY%8
      pos = subY*0x10+subX
      # y lo agrego a la lista de sus eventos
      bloque.listEvents.append( [pos, nroScript] )


#        subArray = bloque.encodeRom(compress, disabledSpriteBytes=8)

#        strHex = Util.instance().strHexa(subArray)
#        print('strHex: ' + strHex)

#        array = array[len(subArray):]

#        self.bloques.append(bloque)

    # convierto los bloques en un listado
    listBloques = []
    for j in range(0, sizeY):
      for i in range(0, sizeX):
        bloque = bloques[j][i]
        listBloques.append(bloque)
    # y los seteo como bloques de este mapa
#    self.bloques = listBloques
    mapa.bloques = listBloques


    if(False):
#    if(True):
#    if(mapa.nroMapa == 2):

      array = mapa.encodeRom(self.mapAddr)
#      array = mapa.encodeRom(0x0871)
      Util.instance().arrayToFile(array, './game/mapu_{:02x}.bin'.format(self.nroMapa))

      iguales = Util.instance().compareFiles('./game/banks/bank_{:02x}/bank_{:02x}.bin'.format(self.mapBank, self.mapBank), './game/mapu_{:02x}.bin'.format(self.nroMapa), self.mapAddr, len(array))
      print('mapa iguales = ' + str(iguales))



#      sheet = RomSplitter.instance().spriteSheets[2]
#      mapa.exportPngFile('./game/mapu.png', sheet)
#      bloque.exportPngFile('./game/mapu.png', sheet)
#      primerBloque.exportPngFile('./game/mapu.png', sheet)
      lines = mapa.encodeTxt()
      strTxt = '\n'.join(lines)

      f = open('./game/mapu_{:02x}.txt'.format(mapa.nroMapa), 'w')
      f.write(strTxt)
      f.close()

    self.mapa = mapa


  def __str__(self):
    strMapa = '{:02x}'.format(self.nroMapa)
    return strMapa


##########################################################
class MapaExterior:
  """ representa un mapa exterior """

  def __init__(self, nroMapa):
    self.nroMapa = nroMapa
    self.tipo = 0 # 0=exterior, 1=interior
    self.compress = None
    self.sizeX = None
    self.sizeY = None
    self.bloques = []

  def decodeRom(self, array):

    if(self.nroMapa == 0x0e):
      disabledSpriteBytes=16
    else:
      disabledSpriteBytes=8

    tipo          = array[0]
    # c3f9: 3 o 4 (cuantas veces se repite el sprite cuando comprime)
    compress = array[1]
    sizeY    = array[2]
    sizeX    = array[3]
#    print('tipo,compress,sizeY,sizeX = {:02x},{:02x},{:02x},{:02x}'.format(tipo,compress,sizeY,sizeX))
    self.tipo, self.compress, self.sizeX, self.sizeY = tipo, compress, sizeX, sizeY

    array = array[4:]
    # salteo los punteros (addr absolutos) (4 bytes por bloque)
    array = array[4*sizeX*sizeY:]

    # para cada bloque
    for i in range(0, sizeX*sizeY):

#      print('----- bloque: ' + str(i))

      bloque = BloqueExterior()
      bloque.mapa = self
      bloque.decodeRom(array, compress)

      subArray = bloque.encodeRom(compress, disabledSpriteBytes)

      strArray = Util.instance().strHexa(subArray)
#      print('strArray: ' + strArray)
      array = array[len(subArray):]

      self.bloques.append(bloque)

  def encodeTxt(self):

    lines = []

    lines.append('tipo: {:02x}'.format(self.tipo))
    lines.append('compress: {:02x}'.format(self.compress))
    lines.append('width: {:02x}'.format(self.sizeX))
    lines.append('height: {:02x}'.format(self.sizeY))

    i = 0
    for bloque in self.bloques:

      yy = i // self.sizeX
      xx = i % self.sizeX

      lines.append('\n--------------------')
      lines.append('bloque (x,y) = ({:02x},{:02x})'.format(xx,yy))

      subLines = bloque.encodeTxt()
      lines.extend(subLines)

      i += 1

    return lines

  def decodeTxt(self, lines):

    strTipo = lines[0][6:]
    strCompress = lines[1][10:]
    strSizeX = lines[2][7:]
    strSizeY = lines[3][8:]

    tipo = int(strTipo,16)
    compress = int(strCompress,16)
    sizeX = int(strSizeX,16)
    sizeY = int(strSizeY,16)

    self.tipo, self.compress, self.sizeX, self.sizeY = tipo, compress, sizeX, sizeY

    i = 5
    for i in range(5, len(lines)):
      line = lines[i]

      if(line.startswith('bloque')):

        bloque = BloqueExterior()
        bloque.mapa = self
        bloque.decodeTxt(lines[i+1:])
        self.bloques.append(bloque)

  def encodeRom(self, idx0):
    """ el idx0 es el addr donde comienza el mapa en el banko (para armar los índices) """

    if(self.nroMapa == 0x0e):
      disabledSpriteBytes=16
    else:
      disabledSpriteBytes=8

    array = []

    array.append(self.tipo)
    array.append(self.compress)
    array.append(self.sizeY)
    array.append(self.sizeX)

    tipo, compress, sizeX, sizeY = self.tipo, self.compress, self.sizeX, self.sizeY

    idx0 += 4 + 4*sizeX*sizeY + 0x4000

    # creo los índices 
    indices = []

    bloquesArray = []
    for bloque in self.bloques:

      indices.append(idx0)
      subArray = bloque._encodeRomEvents()
      bloquesArray.extend(subArray)
      idx0 += len(subArray)

      indices.append(idx0)
      subArray = bloque._encodeRomSprites(compress, disabledSpriteBytes)
      bloquesArray.extend(subArray)
      idx0 += len(subArray)

    idxArray = []
    for index in indices:

      nro1 = index // 0x100
      nro2 = index % 0x100

      idxArray.append(nro2)
      idxArray.append(nro1)

    # agrego los índices
    array.extend(idxArray)
    # y los bloques
    array.extend(bloquesArray)

    return array

  def exportPngFile(self, filepath, sheet):

    # creo un array vacío 
    sprites = []

    for j in range(0, self.sizeY):
      for v in range(0, 8):
        for i in range(0, self.sizeX):
          for u in range(0, 10):

            bloque = self.bloques[j*self.sizeX + i]
            nroSprite = bloque.sprites[v][u]

            sprite = sheet.sprites[nroSprite]
#            if(nroSprite < len(sheet.sprites)):
#              sprite = sheet.sprites[nroSprite]
#            else:
#              sprite = sheet.sprites[0]
            sprites.append(sprite)

    dibu = SpriteSheet(10*self.sizeX,8*self.sizeY, sheet.nroSpriteSheet, 'png')
    dibu.sprites = sprites

    # y exporto el .png
    dibu.exportPngFile(filepath)


 
##########################################################
class BloqueExterior:
  """ representa un bloque de un mapa exterior """

  def __init__(self):

    # el nroScript que se ejecuta al ingresar al bloque (y nroScript+1 se ejecuta al salir del bloque)
    self.eventoEntrada = None
    self.listEvents = []
    self.sprites = [ [0x00 for i in range(0,10)] for j in range(0,8) ]

    # si está habilitado
    self.enabled = True

    # el mapa al cual pertenece
    self.mapa = None

  def getSprites(self):
    return self.sprites

  def decodeRom(self, array, compress):

    self._decodeRomEvents(array)

    subArray = self._encodeRomEvents()
    array = array[len(subArray):]

    self._decodeRomSprites(array, compress)


  def encodeTxt(self):
    lines = []

    subLines = self._encodeTxtEvents()
    lines.extend(subLines)
    subLines = self._encodeTxtSprites()
    lines.extend(subLines)

    return lines

  def decodeTxt(self, lines):
    self._decodeTxtEvents(lines)
    self._decodeTxtSprites(lines[3:])

  def encodeRom(self, compress, disabledSpriteBytes):
    array = []

    subArray = self._encodeRomEvents()
    array.extend(subArray)
    subArray = self._encodeRomSprites(compress, disabledSpriteBytes)
    array.extend(subArray)

    return array


  def _decodeRomEvents(self, array):

    # reseteo los valores
    self.eventoEntrada = None
    self.listEvents = []

    nroScript = array[1] * 0x100 + array[0]
    self.eventoEntrada = nroScript
#    print('eventoEntrada: {:04x}'.format(nroScript))

    # si el nroScript es FFFF considero que el bloque está anulado
    if(nroScript == 0xffff):
      # lo deshabilito
      self.enabled = False

    i = 2
    pos = array[i]
    # mientras no termine el listado
    while(pos != 0xFF):

      # obtengo nro de script
      nroScript = array[i+2] * 0x100 + array[i+1]
      
      # lo agrego con su posición en el bloque 
      self.listEvents.append( (pos, nroScript) )
#      print('evento: {:02x}, {:04x}'.format(pos, nroScript))

      i += 3
      pos = array[i]

  def _decodeRomSprites(self, array, compress):

    # reseteo los valores
    self.sprites = [ [0x00 for i in range(0,10)] for j in range(0,8) ]

    # si no está habilitado
    if(not self.enabled):
      # ni hago nada
      return

    cantSprites = 0
    i = 0
    sprites = []
    # mientras no estén los 80 sprites del bloque (8 filas x 10 cols)
    while(cantSprites < 80):
      byty = array[i]

      cant = 1
      nroSprite = byty & 0x7F
      comp = byty & (0xFF - 0x7F)
      if(comp != 0):
        cant = compress

      for j in range(cant):
        sprites.append(nroSprite)
        cantSprites += 1

      i += 1

    i = 0
    j = 0
    # para cada sprite de los 80 sprites del bloque (10 cols x 8 fils)
    for u in range(0,80):
      # si tiene sprite
      if(u < len(sprites)):
        # lo agarro
        nroSprite = sprites[u]
        # y seteo
        self.sprites[j][i] = nroSprite
      # sino, se acabaron los sprites
      else:
        # seteo en None
        self.sprites[j][i] = None

      i += 1
      if( i == 10 ):
        i = 0
        j += 1


  def _encodeTxtEvents(self):
    lines = []

    if(not self.enabled):
      lines.append('enabled: False')
    else:
      lines.append('enabled: True')

    lines.append('eventoEntrada: {:04x}'.format(self.eventoEntrada))
    strEventos = ''
    for pos, nroScript in self.listEvents:
      strEventos += '({:02x},{:04x})'.format(pos, nroScript)
    lines.append('eventos: ' + strEventos)

    return lines


  def _encodeTxtSprites(self):
    lines = []

    if(not self.enabled):
      return lines

    for j in range(0,8):
      line = ''
      for i in range(0,10):

        nroSprite = self.sprites[j][i]
        # si tiene sprite
        if(nroSprite != None):
          # lo seteo
          line += '{:02x} '.format(self.sprites[j][i])
        # sino
        else:
          # seteo None con 'xx'
          line += 'xx '

      lines.append(line)

    return lines 

  def _decodeTxtEvents(self, lines):

    # reseteo los valores
    self.eventoEntrada = None
    self.listEvents = []

    strEnabled = lines[0][9:].strip()
    if(strEnabled == 'False'):
      self.enabled = False
    else:
      self.enabled = True

    lines = lines[1:]

    strEventoEntrada = lines[0][15:15+4]
    self.eventoEntrada = int(strEventoEntrada, 16)

    strListEventos = lines[1][9:]
    strEventos = strListEventos.split('(')

    for strEvento in strEventos:
      if(strEvento not in ['', '\n']):
        strPos = strEvento[0:2]
        strNroScript = strEvento[3:3+4] 

        pos = int(strPos, 16)
        nroScript = int(strNroScript, 16)

        self.listEvents.append( (pos, nroScript) )

  def _encodeRomEvents(self):

    array = []

#    if(not self.enabled):
#      return [0xff]*3

    nro1 = self.eventoEntrada // 0x100
    nro2 = self.eventoEntrada % 0x100
    array.extend( [nro2, nro1] )

    for pos, nroScript in self.listEvents:
      array.append(pos)
      
      nro1 = nroScript // 0x100
      nro2 = nroScript % 0x100
      array.extend( [nro2, nro1] )

    array.append(0xff)

    return array


  def _decodeTxtSprites(self, lines):

    # reseteo los valores
    self.sprites = [ [0x00 for i in range(0,10)] for j in range(0,8) ]

    if(not self.enabled):
      return

    # para cada fila
    for j in range(0,8):
      strLine = lines[j].strip()

      renglon = []
      strHexas = strLine.split(' ')
      for strHexa in strHexas:
        # si está en None
        if(strHexa == 'xx'):
          hexa = None
        # sino
        else:
          # debería ser un hexa bien formado
          hexa = int(strHexa, 16)
        renglon.append(hexa)

      # para cada columna
      for i in range(0,10):
        # agarro el nroSprite
        nroSprite = renglon[i]
        # y lo seteo
        self.sprites[j][i] = nroSprite

  def _encodeRomSprites(self, compress, disabledSpriteBytes):
    """" disabledSpritesBytes = cuantos 0xff pone cuando está disabled """

    array = []

    if(not self.enabled):
      return [0xff]*disabledSpriteBytes

    fin = False
    j = 0
    # para cada renglón
    while(j < 8 and not fin):
      # lo agarro
      line = self.sprites[j]
      # lo comprimo  
      arrRenglon, fin = self._compressLine(line, compress)
      # y voy acumulando
      array.extend(arrRenglon)
      j += 1

    return array


  def _compressLine(self, line, compress):
    """ comprime un renglón del bloque """

    array = []
    # leo el 1er sprite
    new = line[0]
    oldies = [new]
    old = new
    i=1
    # mientras no se acabe el renglón ni la data
    while(i < 10 and new != None):
      # leo un nuevo sprite
      new = line[i]

      # si es diferente al anterior
      if(new != old):
        # vacio el buffer de oldies
        array.extend(oldies)
        oldies = [new]
        old = new
      # sino, son iguales
      else:

        # lo acumulo en el buffer de oldies
        oldies.append(new)

        # si se llenó el buffer de oldies (llegó a compress)
        if(len(oldies) == compress):
          # le seteo el bit de comprimido
          byty = old | 0x80 
          # lo agrego en un sólo byte
          array.append(byty)
          # y vacío el buffer de oldies
          oldies = []
      i += 1


    # si se acabó la data, indico el fin
    fin = (new == None)
    if(not fin):
      array.extend(oldies)

    return array, fin

  def exportPngFile(self, filepath, sheet):


    w, h = 10, 8
    # creo un spriteSheet vacío
    dibu = SpriteSheet(w,h,sheet.nroSpriteSheet, 'png')

    sprites = []
    for j in range(0,h):
      for i in range(0,w): 

        nroSprite = self.sprites[j][i]
        sprite = sheet.sprites[nroSprite]
        sprites.append(sprite)

    dibu.sprites = sprites

    # y exporto el .png
    dibu.exportPngFile(filepath)



##########################################################
class Sprite:
  """ representa un sprite de 2x2 tiles """

  def __init__(self, nroTileset):
    self.nroTileset = nroTileset
    # array con los 4 nros de tiles
    self.tiles = []
    # si bloquea al caminar
    self.bloqueo = 0x00
    # si lastima, resbala, etc
    self.tipo = 0x00

# -------------- byte 5 (indica nivel de bloqueo)
#
# 00  xx  (todo bloqueado)
#     xx              
#
# 10  xx
#     .x  (hay algun tile libre abajo)
#
# 20  x.  (hay algun tile libre arriba)
#     xx
#
# 30  ..  (todo libre)
#     ..
# 31 (un palo para agarrarse con el latigo)

# 02 (pote que puede romperse con mattock)
# 07 el palo para cambiar dirección del tren


# ----------- byte 6 (indica tipo de sprite)
# el primer digito puede ser   0: no pasa nada
#                            1-3: lastima?
#                            4-5: desliza en algun costado (hielo, tren)
#                            6-7: desliza arriba o abajo
#                              8: puede tener evento

#
# 00 aparece en una pared?
# 01 el coso magico que deja pasar hielo pero no caminar
# 02 precipicio abajo derecha
# 03 una baldoza rara?
# 04 cosa/objeto/pared/gate/caracol
# 05 tierra/piso/aire
# 06 precipicio abajo izquierda
# 07 agua/puente?
# 0d enredadera/trepable
# 10 lastima
# 84 puerta puedo entrar
# 85 agujero en el piso/ baldoza magica/escalera sube
# 95 agujero en el piso peligroso?

# 8? el 8 indica que puede contener un evento

# 74 pared con tierrita arriba (acantilado)
# 77 cataratas?
# 75 aire nubes?

# 37 lava

# 21 pinches en el piso
# 31 cosas lastima en el piso (el primer digito indicara el nivel de daño?)

 
  def decodeRom(self, array):
    self.tiles = [array[0], array[1], array[2], array[3]]
    self.bloqueo = array[4]
    self.tipo = array[5]

  def encodeRom(self):
    array = []

    array.extend(self.tiles)
    array.append(self.bloqueo)
    array.append(self.tipo)

    return array

  def encodeTxt(self):
    lines = []

    lines.append('-----')
#    lines.append('nroTileset: {:02}'.format(self.nroTileset))
    lines.append('tiles:      {:02x} {:02x} {:02x} {:02x}'.format(self.tiles[0], self.tiles[1], self.tiles[2], self.tiles[3]))
    lines.append('bloqueo:    {:02x}'.format(self.bloqueo))
    lines.append('tipo:       {:02x}'.format(self.tipo))

    return lines

  def decodeTxt(self, lines):
    for line in lines:
      if('nroTileset:' in line):
        strNroTileset = line[11:].strip()
        self.nroTileset = int(strNroTileset,16)
      elif('tiles:' in line):
        sTiles = line[6:].strip().split()
        tile0 = int(sTiles[0],16)
        tile1 = int(sTiles[1],16)
        tile2 = int(sTiles[2],16)
        tile3 = int(sTiles[3],16)
        self.tiles = [tile0, tile1, tile2, tile3]
        
      elif('bloqueo:' in line):
        strBloqueo = line[8:].strip()
        self.bloqueo = int(strBloqueo, 16)
 
      elif('tipo:' in line):
        strTipo = line[5:].strip()
        self.tipo = int(strTipo, 16)

  def exportPngFile(self, filepath):

    tileset = RomSplitter.instance().tilesets[self.nroTileset]
    dibu = Tileset(2,2)
    tiles = [tileset.tiles[self.tiles[i]] for i in range(0,4)]
    dibu.tiles = tiles

    # y lo grabo
    dibu.exportPngFile(filepath)


##########################################################
class SpriteSheet:

#  def __init__(self):
  def __init__(self, w, h, nroSpriteSheet, name):
    self.nroSpriteSheet = nroSpriteSheet
    self.name = name
    self.w = w # 16
    self.h = h # 8
    self.sprites = []

    # el nroTileset coincide con el nroSpriteSheet
    self.nroTileset = nroSpriteSheet
    # salvo para el 5to spriteSheet
#    if(nroSpriteSheet == 4):
      # que tiene nroTileset 4
#      self.nroTileset = 4

  def decodeRom(self, array):

    # mientras queden bytes por procesar
    while(len(array)>0):
      # agarro 6 bytes
      subArray = array[0:6]
      sprite = Sprite(self.nroTileset)
      # decodifico el sprite
      sprite.decodeRom(subArray)
      # lo agrego a la lista
      self.sprites.append(sprite)
      # y paso a los próximos 6 bytes
      array = array[6:]

  def encodeRom(self):
    array = []

    for sprite in self.sprites:
      subArray = sprite.encodeRom()
      array.extend(subArray)

    return array

  def encodeTxt(self):
    lines = []

    lines.append('---------- nroSpriteSheet: {:02x} nroTileset: {:02x}'.format(self.nroSpriteSheet, self.nroTileset))
    for sprite in self.sprites:
      subLines = sprite.encodeTxt()
      lines.extend(subLines)

    return lines

  def decodeTxt(self, lines):

    self.sprites = []

    # las sublines para decodificar cada sprite
    subLines = []

    for line in lines: 
#      print(line)
      if('nroSpriteSheet:' in line):
        idx0 = line.find('nroSpriteSheet:')
        idx1 = line.find('nroTileset:')
        strNroSpriteSheet = line[idx0+15:idx1].strip()
        self.nroSpriteSheet = int(strNroSpriteSheet,16)

        strNroTileset = line[idx1+11:].strip()
        self.nroTileset = int(strNroTileset,16)

      # si dice tipo
      elif('tipo:' in line):
        # es el último renglón del sprite
        subLines.append(line)
        # y ya podemos decodificarlo
        sprite = Sprite(self.nroTileset)
        sprite.decodeTxt(subLines)

        # y lo agrego al listado
        self.sprites.append(sprite)

        # reseteamos renglones para el próximo sprite
        subLines = []

      else:
        subLines.append(line)

  def exportPngFile(self, filepath):

    w = self.w
    h = self.h
    dibu = Tileset(2*w,2*h)

    # agarro el tileset para colorear
    tileset = RomSplitter.instance().tilesets[self.nroTileset]

    # creo un array de tiles vacío 
    tiles = [None for i in range(0, 4*w*h)]
    # los ordeno con el orden preciso para que se visualize bien el .png
    for j in range(0,h):
      for i in range(0,w): 

        if(w*j+i < len(self.sprites)):
          sprite = self.sprites[w*j + i]
        else:
          sprite = self.sprites[0]

        for k in range(0,4):

          dx = k % 2
          dy = k // 2
#          print('(dx,dy) = ' + str(dx) + ', ' + str(dy))

          u = 2*i + dx 
          v = 2*j + dy
#          print('(u,v) = ' + str(u) + ', ' + str(v))
          tiles[2*w*v + u] = tileset.tiles[sprite.tiles[k]]


    # seteo los tiles en el orden adecuado    
    dibu.tiles = tiles

    # y exporto el .png
    dibu.exportPngFile(filepath)

  def exportTiled(self, filepath):
    lines = []

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<tileset version="1.5" tiledversion="1.5.0" name="' + self.name + '" tilewidth="16" tileheight="16" tilecount="128" columns="16">')
    lines.append(' <image source="sheet_{:02x}.png" width="256" height="128"/>'.format(self.nroSpriteSheet))
#    lines.append(' <tile id="125" type="Otracosa"/>')
#    lines.append(' <tile id="126" type="Evento"/>')
    lines.append('</tileset>')

    strTxt = '\n'.join(lines)

    f = open(filepath, 'w')
    f.write(strTxt)
    f.close()


##########################################################
@Singleton
class Dictionary:
  """ diccionario para de/codificar el texto """

  def __init__(self):

  # en ingles:
  # ar = 2e
  # ba = 92

  # en aleman:
  # ie = 2a
  # ma = 5a
  # nd = 32 
  # tt = 53
  # er = 23
  # le = 39
  # ar = 47
  # a_ = 89
  # or = 58
  # _B = 6f
  # n_ = 25
  # r_ = 26
  # ei = 2e

  # '04 10 14' = Sumo  El '14' es Sumo
  # '15' es fuji
  # '12 1b 00' (new box?)


    self.dict = {}


    self.listCharsCmds = ['·','·','·','·','·','·','·','·','·','·','·','·','·','·','·','·',
                          '<TEXTBOX_SHOW>','<TEXTBOX_HIDE>','<PAUSE>','<NI_IDEA>','<SUMO>','<FUJI>','·','·','·','·','<ENTER>','<CLS>','·','<BACKSPACE>','·','<CARRY>']
    self.listCharsSpecial = ['ℍ','ℙ','𝕄','𝕊','ℝ','𝕃','𝔼','/','[','▏','█','▎','▌','▊',']','©' ]
    self.listCharsDe = [ '·','·','·','·','·','·','·','·','·',"Ä","Ö","Ü","ä","ö","ü","ß" ]
#    self.listCharsIcons = ['🛡️','🎩','👕','🡔','🗡️','🪓','🔨','💣','🔗','💧','🔑','🍬','⛏️','💰','💎','🔮']
    self.listCharsIcons = ['⛨','🎩','👕','🡔','🗡','🪓','🔨','💣','🔗','💧','🔑','🍬','𐇞','💰','💎','🔮']


    self.listCharsEn = [
                       '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',
                       'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
                       'W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l',
                       'm','n','o','p','q','r','s','t','u','v','w','x','y','z',"'",",",
                       ".","…",'-','!','?',':','/',"┌","─","┐","├","┤","└","┴","┘",' ']
    # 0x40 empieza dakuten en か
    self.listCharsJpLow = [
                       'が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど','ば',
                       'び','ぶ','べ','ぼ','ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ',
                       'ヅ','デ','ド','バ','ビ','ブ','ボ','ぱ','ぴ','ぷ','ぺ','ぽ','パ','ピ','プ','ポ' ]
    self.listCharsJp = [
                       '0','1','2','3','4','5','6','7','8','9','あ','い','う','え','お','か',
                       'き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','な','に',
                       'ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','や','ゆ','よ',
                       'ら','り','る','れ','ろ','わ','を','ん','っ','ゃ','ゅ','ょ','ア','イ','ウ','エ',
                       'オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト',
                       'ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','…','ホ','マ','ミ','ム','メ','モ','ヤ',
                       'ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','「','ン','ァ','ィ','ッ','ャ','ュ','ョ',
                       "゛","゜",'-','!','?','ェ','ォ',"┌","─","┐","├","┤","└","┴","┘",' ']

    # en alemán (old, ya se puede borrar)
    self.deDict2 = {
0x20 : 'ch', 0x21 : 'de', 0x22 : 'e ', 0x23 : 'er', 0x24 : 'en', 0x25 : 'n ', 0x26 : 'r ', 
0x28 : 't ', 0x29 : 'in', 0x2a : 'ie', 0x2b : 'ge', 0x2c : ': ', 0x2d : 'st', 0x2e : 'ei', 0x2f : 'te',

0x30 : ' d', 0x31 : 'be', 0x32 : 'nd', 0x33 : 's ', 0x34 : 'an', 0x35 : 'ic', 0x36 : 'es', 0x37 : 'un',
0x38 : 'h ', 0x39 : 'le', 0x3a : ' i', 0x3b : 'se', 0x3c : 'as', 0x3d : ' D', 0x3e : 'au', 0x3f : 'he',

0x40 : 'ne', 0x41 : ', ', 0x42 : ' e', 0x43 : 'n.', 0x44 : 'is', 0x45 : 'Du', 0x46 : ' s', 0x47 : 'ar',
0x48 : 'rd', 0x49 : 'u ', 0x4a : ' g', 0x4b : 'ht', 0x4c : ' b', 0x4d : ' w', 0x4e : 'da', 0x4f : 're',

0x50 : 'ir', 0x52 : ' M', 0x51 : 'it', 0x53 : 'tt', 0x54 : 'm ', 0x55 : 'll', 0x56 : 'el', 0x57 : ' m',
0x59 : 'Ma', 0x5a : 'ma', 0x58 : 'or', 0x5b : 'us', 0x5c : 'em', 0x5d : 'al', 0x5e : ' W', 0x5f : 'li',

0x60 : 't.', 0x61 : ' n', 0x62 : 'nn', 0x63 : 'ng', 0x64 : 'sc', 0x65 : ' h', 0x66 : '. ', 0x67 : 'ef', 
0x68 : 'mi', 0x69 : 'we', 0x6a : 'd ', 0x6b : 'et', 0x6c : 'si', 0x6d : ' v', 0x6e : 'mm', 0x6f : ' B',

0x80 : 'rt', 0x81 : ' a', 0x82 : 'me', 0x83 : ' G', 0x84 : 'ac', 0x85 : 'di', 0x86 : 'Di', 0x87 : 'na',
0x88 : 'Da', 0x89 : 'a ', 0x8a : 'eh', 0x8b : 'ns', 0x8c : 'ha', 0x8d : 'Ic', 0x8e : 'ra', 0x8f : 'eg',


            0x99 : "Ä", 0x9a : "Ö", 0x9b : "Ü", 0x9c : "ä", 0x9d : "ö", 0x9e : "ü", 0x9f : "ß",

0xb0 : "0", 0xb1 : "1", 0xb2 : "2", 0xb3 : "3", 0xb4 : "4", 0xb5 : "5", 0xb6 : "6", 0xb7 : "7",
0xb8 : "8", 0xb9 : "9", 0xba : "A", 0xbb : "B", 0xbc : "C", 0xbd : "D", 0xbe : "E", 0xbf : "F",

0xc0 : "G", 0xc1 : "H", 0xc2 : "I", 0xc3 : "J", 0xc4 : "K", 0xc5 : "L", 0xc6 : "M", 0xc7 : "N",
0xc8 : "O", 0xc9 : "P", 0xca : "Q", 0xcb : "R", 0xcc : "S", 0xcd : "T", 0xce : "U", 0xcf : "V",

0xd0 : "W", 0xd1 : "X", 0xd2 : "Y", 0xd3 : "Z", 0xd4 : "a", 0xd5 : "b", 0xd6 : "c", 0xd7 : "d",
0xd8 : "e", 0xd9 : "f", 0xda : "g", 0xdb : "h", 0xdc : "i", 0xdd : "j", 0xde : "k", 0xdf : "l",

0xe0 : "m", 0xe1 : "n", 0xe2 : "o", 0xe3 : "p", 0xe4 : "q", 0xe5 : "r", 0xe6 : "s", 0xe7 : "t",
0xe8 : "u", 0xe9 : "v", 0xea : "w", 0xeb : "x", 0xec : "y", 0xed : "z", 0xee : "'", 0xef : ",",

0xf0 : ".", 0xf1 : "…", 0xf2 : "-", 0xf3 : "!", 0xf4 : "?", 0xf5 : ":", 0xf6 : "/", 0xf7 : "┌",
0xf8 : "─", 0xf9 : "┐", 0xfa : "├", 0xfb : "┤", 0xfc : "└", 0xfd : "┴", 0xfe : "┘", 0xff : " "
                  }
    # old (ya se puede borrar)
    self.invDeDict2 = {v: k for k, v in self.deDict2.items()}

  def decodeRom(self):

    lang = Address.instance().language

    if(lang == ENGLISH):

      listCharsCmds = Dictionary.instance().listCharsCmds
      # seteo los comandos
      for i in range(0x00, 0x20):
        self.dict[i] = listCharsCmds[i]

      listCharsSpecial = Dictionary.instance().listCharsSpecial
      # seteo las letras especiales
      for i in range(0x70, 0x80):
        self.dict[i] = listCharsSpecial[i-0x70]

      listCharsIcons = Dictionary.instance().listCharsIcons
      # seteo las letras iconos
      for i in range(0xa0, 0xb0):
        self.dict[i] = listCharsIcons[i-0xa0]

      listCharsEn = Dictionary.instance().listCharsEn
      # seteo las letras normales
      for i in range(0xb0, 0x100):
        self.dict[i] = listCharsEn[i-0xb0]

      # cargo el banco 0
      bank0 = RomSplitter.instance().banks[0x00]
      addr = Address.instance().addrDictionary
      cant = Address.instance().cantDictionary
      for i in range(0,cant):
        # agarro el valor
        val0 = bank0[addr+2*i]
        val1 = bank0[addr+2*i+1]
        char0 = Dictionary.instance().decodeByte(val0)
        char1 = Dictionary.instance().decodeByte(val1)
        chary = char0 + char1
        index = 0x20+i
        # se saltea el renglón 0x70 (especiales)
        if(index >= 0x70):
          index += 0x10
        # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
        if(chary != '..' and chary != 'LA'):
          # las demás combinaciones si se comprimen
          self.dict[index] = chary


    elif(lang == FRENCH):

      listCharsCmds = Dictionary.instance().listCharsCmds
      # seteo los comandos
      for i in range(0x00, 0x20):
        self.dict[i] = listCharsCmds[i]

      listCharsSpecial = Dictionary.instance().listCharsSpecial
      # seteo las letras especiales
      for i in range(0x70, 0x80):
        self.dict[i] = listCharsSpecial[i-0x70]

      listCharsDe = Dictionary.instance().listCharsDe
      # seteo las letras especiales deutsch
      for i in range(0x90, 0xa0):
        self.dict[i] = listCharsDe[i-0x90]

      listCharsIcons = Dictionary.instance().listCharsIcons
      # seteo las letras iconos
      for i in range(0xa0, 0xb0):
        self.dict[i] = listCharsIcons[i-0xa0]

      listCharsEn = Dictionary.instance().listCharsEn
      # seteo las letras normales
      for i in range(0xb0, 0x100):
        self.dict[i] = listCharsEn[i-0xb0]

      # cargo el banco 0
      bank0 = RomSplitter.instance().banks[0x00]
      addr = Address.instance().addrDictionary
      cant = Address.instance().cantDictionary
      for i in range(0,cant):
        # agarro el valor
        val0 = bank0[addr+2*i]
        val1 = bank0[addr+2*i+1]
        char0 = Dictionary.instance().decodeByte(val0)
        char1 = Dictionary.instance().decodeByte(val1)
        chary = char0 + char1
        index = 0x20+i
        # se saltea el renglón 0x70 (especiales)
        if(index >= 0x70):
          index += 0x10
        # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
        if(chary != '..' and chary != 'LA'):
          # las demás combinaciones si se comprimen
          self.dict[index] = chary

    elif(lang == GERMAN):

      listCharsCmds = Dictionary.instance().listCharsCmds
      # seteo los comandos
      for i in range(0x00, 0x20):
        self.dict[i] = listCharsCmds[i]

      listCharsSpecial = Dictionary.instance().listCharsSpecial
      # seteo las letras especiales
      for i in range(0x70, 0x80):
        self.dict[i] = listCharsSpecial[i-0x70]

      listCharsDe = Dictionary.instance().listCharsDe
      # seteo las letras especiales deutsch
      for i in range(0x90, 0xa0):
        self.dict[i] = listCharsDe[i-0x90]

      listCharsIcons = Dictionary.instance().listCharsIcons
      # seteo las letras iconos
      for i in range(0xa0, 0xb0):
        self.dict[i] = listCharsIcons[i-0xa0]

      listCharsEn = Dictionary.instance().listCharsEn
      # seteo las letras normales
      for i in range(0xb0, 0x100):
        self.dict[i] = listCharsEn[i-0xb0]

      # cargo el banco 0
      bank0 = RomSplitter.instance().banks[0x00]
      addr = Address.instance().addrDictionary
      cant = Address.instance().cantDictionary
      for i in range(0,cant):
        # agarro el valor
        val0 = bank0[addr+2*i]
        val1 = bank0[addr+2*i+1]
        char0 = Dictionary.instance().decodeByte(val0)
        char1 = Dictionary.instance().decodeByte(val1)
        chary = char0 + char1
        index = 0x20+i
        # se saltea el renglón 0x70 (especiales)
        if(index >= 0x70):
          index += 0x10
        # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
        if(chary != '..' and chary != 'LA'):
          # las demás combinaciones si se comprimen
          self.dict[index] = chary

    elif(lang == JAPAN):

      listCharsCmds = Dictionary.instance().listCharsCmds
      # seteo los comandos
      for i in range(0x00, 0x20):
        self.dict[i] = listCharsCmds[i]

      listCharsJpLow = Dictionary.instance().listCharsJpLow
      # seteo las letras con dakuten
      for i in range(0x40, 0x70):
        self.dict[i] = listCharsJpLow[i-0x40]

      listCharsSpecial = Dictionary.instance().listCharsSpecial
      # seteo las letras especiales
      for i in range(0x70, 0x80):
        self.dict[i] = listCharsSpecial[i-0x70]

      listCharsJp = Dictionary.instance().listCharsJp
      # seteo las letras normales
      for i in range(0x80, 0x100):
        self.dict[i] = listCharsJp[i-0x80]

      # cargo el banco 0
      bank0 = RomSplitter.instance().banks[0x00]
      dic = []
      string = ''
      vaPorAddr = Address.instance().addrDictionary
      cont = 0x20
      # entre 0x20 y 0x40 seteo las palabras comprimidas
      while(cont < 0x40):
        val = bank0[vaPorAddr]
        vaPorAddr += 1
        if(val == 0x00):
          self.dict[cont] = string
#          print('dictu {:02x} '.format(cont) + string)
          cont +=1
          string = ''
        else:
          chary = Dictionary.instance().decodeByte(val)
          string += chary


  def decodeByte(self, byte):
    char = '·'

    if(byte in self.dict.keys()):
      char = self.dict[byte]

    return char


  def decodeArray(self, array):
    string = ''
    for hexa in array:
      char = self.decodeByte(hexa)
      string += char
    return string

  def keys(self):

    keys = self.dict.keys()
    return keys

  def chars(self):
    """ retorna lista de los chars disponibles en el dicconario """
    # invierto el diccionario
    invDict = {v: k for k, v in self.dict.items()}
    # los chars son las keys del diccionario invertido
    chars = invDict.keys()
    # los retorno
    return chars
 

  def encodeChars(self, chars):
    """ codifica un char, o un par de chars """
    # invierto el diccionario
    invDict = {v: k for k, v in self.dict.items()}
    # busco en el diccionario invertido
    hexy = invDict[chars]
    # retorno lo encontrado
    return hexy


##########################################################
@Singleton
class Cosas:
  """ representa la colección de items, weapons, y magias """

  def __init__(self):
    self.items = []
    self.weapons = []
    self.magics = []

  def addItem(self, item):
    self.items.append(item)
  def getItem(self, nroItem):
    for item in self.items:
      if(item.nro == nroItem):
        return item

  def addWeapon(self, weapon):
    self.weapons.append(weapon)
  def getWeapon(self, nroWeapon):
    for weap in self.weapons:
      if(weap.nro == nroWeapon):
        return weap

  def addMagic(self, magic):
    self.magics.append(magic)
  def getMagic(self, nroMagic):
    for magic in self.magics:
      if(magic.nro == nroMagic):
        return magic


##########################################################
class Personaje:
  """ representa un personaje """

  def __init__(self, nroPersonaje):

    self.nroPersonaje = nroPersonaje

    # el tipo
    # 0x81 = amigo (si lo tocás habla)
    # 0x87 = se cuelga todo?
    # 0x91 = enemigo (si lo tocás lastima)
    # 0x93 = enemigo (si lo tocás lastima, el puede atravezar paredes)
    # 0x95 = se cuelga todo?
    # 0xa9 = muñeco (si lo tocás lo empujás)
    # 0xd9 = transparente (si lo tocás lo atravezás)
    self.amistad = 0x00

    # la velocidad de caminar, tipos de ataque, fuerza
    self.tipo = 0x00

    # la forma de caminar (20,40,50,58,60,6e,74,78,7c) (algunas requieren mas sprites)
    self.cantSprites = 0x00

    # (01,02,04,06,08,0c,0a)
    self.nose1 = 0x00
    # (00,40,80,c0)
    self.nose2 = 0x00

    self.nroSprite = 0x00
#    self.nose3 = 0x00
#    self.nose4 = 0x00
    # suele apuntar a 3:3b5a de donde lee 16 bytes
    self.addrRaro = 0x0000
# nose5
#(02,
# 22,26,
#          3e,
# 42,46,4a,
# 62,66,6a,6e,
# 72,
#    86,8a,8e,
#    96,
#          ae,
#    b6,ba,
# d2,   da,de,
#    f6,fa,fe 
#    self.nose5 = 0x00
#    self.nose6 = 0x00
    self.addrDosTiles = 0x0000

    self.patasSepa  = 0x00
    self.muevePatas = 0x00

    self.nose7 = 0x00
    self.nose8 = 0x00
    self.nose9 = 0x00
    self.nose10 = 0x00

    self.nose11 = 0x00
    self.nose12 = 0x00
    self.nose13 = 0x00
    self.nose14 = 0x00

    self.nroScript  = 0x0000
    self.itemTesoro = 0x0000


  def decodeRom(self, subArray):

    self.amistad   = subArray[0] # 0x81
    self.tipo      = subArray[1] # 0x0b
    self.cantSprites  = subArray[2] # 0x40   
    self.nose1        = subArray[3] # 0x08   (01,02,04,06,08,0c,0a)
    self.nose2        = subArray[4] # 0x00   (00,40,80,c0)

    self.nroSprite = subArray[5] # 5f  (cuando camina para los costados)
    addrRaro1     = subArray[6]
    addrRaro2     = subArray[7]
    # 0x7b5a (salvo que 0x7b56) (desde 3:7b5a lee 16 bytes)
    self.addrRaro = addrRaro2*0x100 + addrRaro1

    addrDosTiles1 = subArray[8] # 0xb6 (gira,permuta sus sprites?)
    addrDosTiles2 = subArray[9] # 0x7c (2c,7b,7c,7d,7e,7f)
    self.addrDosTiles = addrDosTiles2*0x100 + addrDosTiles1  # apunta en el dic de 3:3b72

    self.patasSepa    = subArray[10] # 0x00   0 ó 1 (patas sólo separadas)
    self.muevePatas   = subArray[11] # 0x01   0,1,2 (patas juntas)
    self.nose7        = subArray[12] # 0x01   0,1,2
    self.nose8        = subArray[13] # 0x00   0,1,2
    self.nose9        = subArray[14] # 0x00   0,1,2
    self.nose10       = subArray[15] # 0x00   0,1,2

    self.nose11       = subArray[16] # 0x04   02=suelo, 10=salta 12=fantasma bajo suelo 15=teleport
    self.nose12       = subArray[17] # 0x04  
    self.nose13       = subArray[18] # 0x04  
    self.nose14       = subArray[19] # 0x04  

    self.nroScript    = subArray[20] + subArray[21]*0x100 # 0x0267
    self.itemTesoro   = subArray[22] + subArray[23]*0x100 # 0x0000  

  def encodeRom(self):
    array = []

    array.append(self.amistad)
    array.append(self.tipo)
    array.append(self.cantSprites)
    array.append(self.nose1)
    array.append(self.nose2)

    array.append(self.nroSprite)
    array.append(self.addrRaro%0x100)
    array.append(self.addrRaro//0x100)

    array.append(self.addrDosTiles%0x100)
    array.append(self.addrDosTiles//0x100)

    array.append(self.patasSepa)
    array.append(self.muevePatas)
    array.append(self.nose7)
    array.append(self.nose8)
    array.append(self.nose9)
    array.append(self.nose10)

    array.append(self.nose11)
    array.append(self.nose12)
    array.append(self.nose13)
    array.append(self.nose14)

    array.append(self.nroScript%0x100)
    array.append(self.nroScript//0x100)
    array.append(self.itemTesoro%0x100)
    array.append(self.itemTesoro//0x100)

    return array

  def encodeTxt(self):
    lines = []

    lines.append('\n------------ personaje ')
    lines.append('nroPersonaje: {:02x}'.format(self.nroPersonaje))
    lines.append('amistad:      {:02x}'.format(self.amistad))

    lines.append('tipo:         {:02x}'.format(self.tipo))
    lines.append('cantSprites:  {:02x}'.format(self.cantSprites))
    lines.append('nose1:        {:02x}'.format(self.nose1))
    lines.append('nose2:        {:02x}'.format(self.nose2))
    lines.append('nroSprite:    {:02x}'.format(self.nroSprite))
    lines.append('addrRaro:     {:04x}'.format(self.addrRaro))
    lines.append('addrDosTiles: {:04x}'.format(self.addrDosTiles))

    lines.append('patasSepa:    {:02x}'.format(self.patasSepa))
    lines.append('muevePatas:   {:02x}'.format(self.muevePatas))
    lines.append('nose7:        {:02x}'.format(self.nose7))
    lines.append('nose8:        {:02x}'.format(self.nose8))
    lines.append('nose9:        {:02x}'.format(self.nose9))
    lines.append('nose10:       {:02x}'.format(self.nose10))

    lines.append('nose11:       {:02x}'.format(self.nose11))
    lines.append('nose12:       {:02x}'.format(self.nose12))
    lines.append('nose13:       {:02x}'.format(self.nose13))
    lines.append('nose14:       {:02x}'.format(self.nose14))

    lines.append('nroScript:    {:04x}'.format(self.nroScript))
    lines.append('itemTesoro:   {:04x}'.format(self.itemTesoro))

    return lines

  def decodeTxt(self, lines):
    for line in lines:
#      print('lineee: ' + line)
      if(line.startswith('nroPersonaje:')):
        strNroPersonaje = line[13:].strip()
        self.nroPersonaje = int(strNroPersonaje,16)
      elif(line.startswith('amistad:')):
        strAmistad = line[8:].strip()
        self.amistad = int(strAmistad,16)
      elif(line.startswith('tipo:')):
        strTipo = line[5:].strip()
        self.tipo = int(strTipo,16)
      elif(line.startswith('cantSprites:')):
        strCantSprites = line[12:].strip()
        self.cantSprites = int(strCantSprites,16)
      elif(line.startswith('nose1:')):
        strNose1 = line[6:].strip()
        self.nose1 = int(strNose1,16)
      elif(line.startswith('nose2:')):
        strNose2 = line[6:].strip()
        self.nose2 = int(strNose2,16)
      elif(line.startswith('nroSprite:')):
        strNroSprite = line[10:].strip()
        self.nroSprite = int(strNroSprite,16)
      elif(line.startswith('addrRaro:')):
        strAddrRaro = line[9:].strip()
        self.addrRaro = int(strAddrRaro,16)
      elif(line.startswith('addrDosTiles:')):
        strAddrDosTiles = line[13:].strip()
        self.addrDosTiles = int(strAddrDosTiles,16)
      elif(line.startswith('patasSepa:')):
        strPatasSepa = line[10:].strip()
        self.patasSepa = int(strPatasSepa,16)
      elif(line.startswith('muevePatas:')):
        strMuevePatas = line[11:].strip()
        self.muevePatas = int(strMuevePatas,16)
      elif(line.startswith('nose7:')):
        strNose7 = line[6:].strip()
        self.nose7 = int(strNose7,16)
      elif(line.startswith('nose8:')):
        strNose8 = line[6:].strip()
        self.nose8 = int(strNose8,16)
      elif(line.startswith('nose9:')):
        strNose9 = line[6:].strip()
        self.nose9 = int(strNose9,16)
      elif(line.startswith('nose10:')):
        strNose10 = line[7:].strip()
        self.nose10 = int(strNose10,16)
      elif(line.startswith('nose11:')):
        strNose11 = line[7:].strip()
        self.nose11 = int(strNose11,16)
      elif(line.startswith('nose12:')):
        strNose12 = line[7:].strip()
        self.nose12 = int(strNose12,16)
      elif(line.startswith('nose13:')):
        strNose13 = line[7:].strip()
        self.nose13 = int(strNose13,16)
      elif(line.startswith('nose14:')):
        strNose14 = line[7:].strip()
        self.nose14 = int(strNose14,16)
      elif(line.startswith('nroScript:')):
        strNroScript = line[10:].strip()
        self.nroScript = int(strNroScript,16)
      elif(line.startswith('itemTesoro:')):
        strItemTesoro = line[11:].strip()
        self.itemTesoro = int(strItemTesoro,16)
 
 
  def __str__(self):

    string = 'amist={:02x} tipo={:02x} cantSp={:02x}  {:02x} {:02x}  spri={:02x} {:04x} addrDosTiles={:04x} patas={:02x},{:02x} {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}  script={:04x} item={:04x}'.format(self.amistad, self.tipo, self.cantSprites, self.nose1, self.nose2, self.nroSprite, self.addrRaro, self.addrDosTiles, self.patasSepa, self.muevePatas, self.nose7, self.nose8, self.nose9, self.nose10, self.nose11, self.nose12, self.nose13, self.nose14, self.nroScript, self.itemTesoro)

    return string


##########################################################
class GruposPersonajes:
  """ representa el listado de grupos de 3 personajes? """

  def __init__(self, addr):
    self.addr = addr

    self.grupos = []
    self.apariciones = []

  def decodeRom(self, array):

    vaPorAddr = self.addr

    self.grupos = []
    # cargo los grupos
    for i in range(0,109):
      grupo = GrupoPersonaje(i)
      grupo.decodeRom(array[6*i:6*(i+1)])
      self.grupos.append(grupo)
      vaPorAddr += 6

    length = 6*len(self.grupos)

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    RomStats.instance().appendDato(0x03, 0x3142, vaPorAddr, (rr, gg, bb), 'grupos personajes')

    # me quedo con la segunda parte (0x33d0 ?)
    array = array[length:]
    addr = vaPorAddr + 0x4000

    self.apariciones = []
    # y cargo las apariciones
    for i in range(0,215):

      apa = AparicionPersonaje(i)
      apa.addr = addr
      apa.decodeRom(array)
      self.apariciones.append(apa)

      arru = apa.encodeRom()
      array = array[len(arru):]
      addr += len(arru)

    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    RomStats.instance().appendDato(0x03, vaPorAddr, addr - 0x4000, (rr, gg, bb), 'aparición personajes')

    addrsApas = [apa.addr for apa in self.apariciones]
    # vuelvo a recorrer los grupos
    for grupo in self.grupos:
      addrA = grupo.addrA
      idxA = addrsApas.index(addrA)
      # y refresco sus labels
      grupo.labelA = 'nro{:03}'.format(idxA)

      addrB = grupo.addrB
      idxB = addrsApas.index(addrB)
      grupo.labelB = 'nro{:03}'.format(idxB)

      addrC = grupo.addrC
      idxC = addrsApas.index(addrC)
      grupo.labelC = 'nro{:03}'.format(idxC)

  def decodeTxt(self, lines):
    idx = 0 
    # busco el índice donde comienzan las apariciones
    for line in lines:
      if('------ aparicion personaje' in line):
        break
      idx += 1

    linesGrupos = lines[:idx]
    linesApas = lines[idx:]

    vaPorAddr = self.addr

    i = 0
    self.grupos = []
    # por cada renglón
    for line in linesGrupos:
      line = line.strip()
      # si no está vacío ni es comentario
      if(len(line) > 0 and not line.startswith('#')):
#        print(line)
        grupo = GrupoPersonaje(i)
        grupo.decodeTxt(line)
        self.grupos.append(grupo)
        i += 1

    vaPorAddr += 6*len(self.grupos)
    addr = vaPorAddr + 0x4000

    i = 0
    self.apariciones = []
    primero = True
    subLines = []
    for line in linesApas:
#      print('line: ' + line)
      if('aparicion personaje' in line):
        if(not primero):
          apa = AparicionPersonaje(i)
          apa.decodeTxt(subLines)
          apa.addr = addr
          self.apariciones.append(apa)
          i += 1
          subLines = []

          arru = apa.encodeRom()
          addr += len(arru)
        else:
          primero = False
      subLines.append(line)
    apa = AparicionPersonaje(i)
    apa.decodeTxt(subLines)
    apa.addr = addr
    self.apariciones.append(apa)
    i += 1
    arru = apa.encodeRom()
    addr += len(arru)
    
    # vuelvo a recorrer los grupos
    for grupo in self.grupos:
      labelA = grupo.labelA
      nro = int(labelA[3:6])
      apa = self.apariciones[nro]
      # y refesco sus addr
      grupo.addrA = apa.addr

      labelB = grupo.labelB
      nro = int(labelB[3:6])
      apa = self.apariciones[nro]
      grupo.addrB = apa.addr

      labelC = grupo.labelC
      nro = int(labelC[3:6])
      apa = self.apariciones[nro]
      grupo.addrC = apa.addr

#      print('grupo: ' + str(grupo))

  def encodeTxt(self):

    lines = []

    for grupo in self.grupos:
      strGrupo = grupo.encodeTxt()
      lines.append('group: {:02x} | '.format(grupo.nro) + strGrupo)

    for apa in self.apariciones:
      subLines = apa.encodeTxt()
      lines.extend(subLines)

    return lines

  def encodeRom(self):

    array = []

    for grupo in self.grupos:
      subArray = grupo.encodeRom()
      array.extend(subArray)

    for apa in self.apariciones:
      subArray = apa.encodeRom()
      array.extend(subArray)

    return array


##########################################################
class GrupoPersonaje:
  """ representa un grupo de 3 personajes? """

  def __init__(self, nro):
    self.nro = nro

    self.addrA = 0x0000
    self.addrB = 0x0000
    self.addrC = 0x0000

    self.labelA = 'nro000'
    self.labelB = 'nro000'
    self.labelC = 'nro000'

  def decodeRom(self, array):

    addr1 = array[0]
    addr2 = array[1]
    self.addrA = addr2*0x100 + addr1

    addr1 = array[2]
    addr2 = array[3]
    self.addrB = addr2*0x100 + addr1

    addr1 = array[4]
    addr2 = array[5]
    self.addrC = addr2*0x100 + addr1

  def encodeTxt(self):
    return self.labelA + ', ' + self.labelB + ', ' + self.labelC

  def decodeTxt(self, string):
    idx = string.find('|')
    subString = string[idx+1:].strip()
    nros = subString.split(',')
    self.labelA = nros[0].strip()
    self.labelB = nros[1].strip()
    self.labelC = nros[2].strip()

  def encodeRom(self):
    array = []

    array.extend( [ self.addrA%0x100, self.addrA//0x100 ] )
    array.extend( [ self.addrB%0x100, self.addrB//0x100 ] )
    array.extend( [ self.addrC%0x100, self.addrC//0x100 ] )

    return array

  def __str__(self):
    addrs = [self.addrA, self.addrB, self.addrC]
    strHex = Util.instance().strHexa(addrs)
    return 'nro: {:02x} | '.format(self.nro) + strHex + ' | ' + self.labelA + ', ' + self.labelB + ', ' + self.labelC

##########################################################
class AparicionPersonaje:
  """ representa una aparición personaje """

  def __init__(self, nro):
    self.nro = nro
    self.addr = 0x0000

    self.valMin = 0x00
    self.valMax = 0x00
    self.values = [0x00, 0x00, 0x00, 0x00]
    # una cantidad par entre 0 y 8 de bytes?
    self.extras = []
    self.cierre = [0x80, 0x80]

  def decodeRom(self, array):

    self.valMin = array[0]
    self.valMax = array[1]

    self.values = [array[2], array[3], array[4], array[5]]

    subArray = array[6:]
    idx = subArray.index(0x80)
#    print('idx: ' + str(idx))

    self.extras = array[6:6+idx]

    self.cierre = array[6+idx:6+idx+2]


  def encodeRom(self):
    array = []

    array.append(self.valMin)
    array.append(self.valMax)
    array.extend(self.values)
    array.extend(self.extras)
    array.extend(self.cierre)

    return array

  def encodeTxt(self):
    lines = []

    lines.append('\n------ aparicion personaje')
    lines.append('nro{:03}'.format(self.nro))
    lines.append('valMin: {:02x}'.format(self.valMin))
    lines.append('valMax: {:02x}'.format(self.valMax))
    lines.append('values: {:02x} {:02x} {:02x} {:02x}'.format(self.values[0], self.values[1], self.values[2], self.values[3]))
    lines.append('extras: ' + Util.instance().strHexa(self.extras))
    lines.append('cierre: {:02x} {:02x}'.format(self.cierre[0], self.cierre[1]))

    return lines

  def decodeTxt(self, lines):

    for line in lines:
      if(line.startswith('nro')):
        strNro = line[3:].strip()
#        print('strNro: ' + strNro)
        self.nro = int(strNro, 16)
      elif(line.startswith('valMin:')):
        strMin = line[7:].strip()
#        print('strMin: ' + strMin)
        self.valMin = int(strMin, 16)
      elif(line.startswith('valMax:')):
        strMax = line[7:].strip()
#        print('strMax: ' + strMax)
        self.valMax = int(strMax, 16)
      elif(line.startswith('values:')):
        strVals = line[7:].strip()
#        print('strVals: ' + strVals)
        strVals = strVals.split()
        vals = [int(strVal,16) for strVal in strVals]
        self.values = vals
      elif(line.startswith('extras:')):
        strExts = line[7:].strip()
#        print('strExts: ' + strExts)
        strExts = strExts.split()
        exts = [int(strExt,16) for strExt in strExts]
        self.extras = exts
      elif(line.startswith('cierre:')):
        strCierre = line[7:].strip()
#        print('strCierre: ' + strCierre)
        strCierre = strCierre.split()
        cierre = [int(strCierre,16) for strCierre in strCierre]
        self.cierre = cierre

  def __str__(self):
    strExtras = Util.instance().strHexa(self.extras)
    string = 'nro{:03} addr {:04x} | minmax: {:02x} {:02x} values: {:02x} {:02x} {:02x} {:02x} extras: '.format(self.nro, self.addr, self.valMin, self.valMax, self.values[0], self.values[1], self.values[2], self.values[3]) + strExtras + ' cierre: {:02x} {:02x}'.format(self.cierre[0], self.cierre[1])
    return string

##########################################################
class Magic:
  """ representa una magia """

  def __init__(self):
    self.nro = -1
    self.name = ''
    self.nose = []

  def decodeRom(self, data):
    """ decodifica la magia a partir del array de 16 bytes """
    # el id de magia
    self.nro = data[0]

    name = ''
    for hexa in data[1:1+8]:
      if(hexa != 0x00):
        chary = Dictionary.instance().decodeByte(hexa)
        name += chary
      else:
        break
    self.name = name

    self.nose = data[9:9+7]

  def encodeTxt(self):
    lines = []
    lines.append('\n--- magic: ' + self.name)
    lines.append('nro: {:02x}'.format(self.nro))
    strHex = Util.instance().strHexa(self.nose)
    lines.append('nose: ' + strHex)
    return lines

  def decodeTxt(self, lines):

    for line in lines:
      if('magic:' in line):
        idx0 = line.index('magic:')
        self.name = line[idx0+6:].strip()
      elif('nro:' in line):
        idx0 = line.index('nro:')
        self.nro = int(line[idx0+4:].strip(),16)
      elif('nose:' in line):
        idx0 = line.index('nose:')
        nose = line[idx0+5:].strip()
        nose = nose.split()
        nose = [int(nosy,16) for nosy in nose]
        self.nose = nose

  def encodeRom(self):
    array = []

    array.append(self.nro)
    for chary in self.name:
      hexy = Dictionary.instance().encodeChars(chary)
      array.append(hexy)

    faltan = 9-len(array)
    extras = [0x00]*faltan
    array.extend(extras)

    array.extend(self.nose)

    return array

  def __str__(self):
    return self.name


##########################################################
class Item:
  """ representa un item """

  def __init__(self, tipo):

    # el tipo puede ser uno de ['magic', 'item', 'weapon']
    self.tipo = tipo

    self.nro = -1
    self.name = ''
    self.nose = []
    self.enabled = False
    # los bytes del item disabled
    self.disabledBytes = []

  def decodeRom(self, data):
    """ decodifica el item a partir del array de 16 bytes """
    # el id de item
    self.nro = data[0]


#    strHex = Util.instance().strHexa(data[1:1+8])
#    print('llego nombre = ' + strHex)

    lang = Address.instance().language
    icon = data[1]
    firstLetter = data[2]

#    print('hexName: ' + Util.instance().strHexa(data[0:9]))

    # si es del tipo magia ó es rom 'jp' ó el nombre comienza con un ícono y continúa una letra mayúscula
    if(self.tipo == 'magic' or lang == JAPAN or (icon in range(0xa0,0xb0) and firstLetter in range(0xb0,0xd4))):
#    if(True):
      name = ''
      for hexa in data[1:1+8]:
        if(hexa != 0x00):
          chary = Dictionary.instance().decodeByte(hexa)
          name += chary
        else:
          break
#      print('nombre: ' + name)
      # el nombre del item
      self.name = name

#      print('name: ' + name)

      self.nose = data[9:9+7]
      self.enabled = True
    # sino, el nombre no comienza con un ícono
    else:
      # lo considero desactivo
      self.enabled = False
      self.disabledBytes = data[0:16]

  def encodeTxt(self):
    lines = []
    lines.append('\n--- nro: {:02x}'.format(self.nro))
    lines.append('tipo: ' + self.tipo)
    if(self.enabled):
      lines.append('name: ' + self.name)
      strHex = Util.instance().strHexa(self.nose)
      lines.append('nose: ' + strHex)
    else:
      strHex = Util.instance().strHexa(self.disabledBytes)
      lines.append('disabledBytes: ' + strHex)
    return lines

  def decodeTxt(self, lines):

    for line in lines:
      if('nro:' in line):
        idx0 = line.index('nro:')
        self.nro = int(line[idx0+4:].strip(),16)
      elif('name:' in line):
        idx0 = line.index('name:')
        self.name = line[idx0+5:].strip()
        self.enabled = True
      elif('nose:' in line):
        idx0 = line.index('nose:')
        nose = line[idx0+5:].strip()
        nose = nose.split()
        nose = [int(nosy,16) for nosy in nose]
        self.nose = nose
      elif('disabledBytes:' in line):
        idx0 = line.index('disabledBytes:')
        diss = line[idx0+14:].strip()
        diss = diss.split()
        diss = [int(dissy,16) for dissy in diss]
        self.disabledBytes = diss
        self.enabled = False

  def encodeRom(self):
    array = []

    if(self.enabled):

      array.append(self.nro)

      for chary in self.name:
#        print('chary: ' + chary)
        hexy = Dictionary.instance().encodeChars(chary)
        array.append(hexy)

      faltan = 9-len(array)
      extras = [0x00]*faltan
      array.extend(extras)

      array.extend(self.nose)

    # sino, no está enabled
    else:
      array.extend(self.disabledBytes)

    return array

  def __str__(self):
    return self.name

##########################################################
class Weapon:
  """ representa un weapon """

  def __init__(self):
    pass

  def decodeRom(self, data):
    """ decodifica el weapon a partir del array de 16 bytes """
    # el id de weapon
    self.nro = data[0]

    strName = Dictionary.instance().decodeArray(data[2:2+7])
    # el nombre del weapon
    self.name = strName

  def __str__(self):
    return '{:02x}'.format(self.nro) + ' - ' + self.name




##########################################################
class Canciones:
  """ representa la lista de canciones """

  def __init__(self):
    self.canciones = []

  def decodeRom(self, bank):
    self.canciones = []

    # para cada canción
    for i in range(0,30):

      cancion = Cancion(i)
      # la decodifico
      cancion.decodeRom(bank)

      print('--- ' + str(i) + ' i: {:02x} | cancion: '.format(i) + str(cancion))

      # y la agrego a la lista
      self.canciones.append(cancion)

  def encodeTxt(self):

    lines = []

    basePath = Address.instance().basePath
    path = basePath + '/audio'

    # para cada canción
    for i in range(0,30):

      # agarro la canción
      cancion = self.canciones[i]
      subLines = cancion.encodeTxt()
      lines.extend(subLines)

    return lines
    
  def decodeTxt(self, lines):
    """ decodifica la lista de canciones del txt """

    self.canciones = []

    i=0
    songLines = []

    # por cada renglón
    for line in lines:

      # si es una nueva canción
      if('song' in line):
        # y es la primera
        if(i==0): 
          # vamos agregando renglones
          songLines.append(line)
        # sino
        else:
          cancion = Cancion(i-1)
          cancion.decodeTxt(songLines)
          self.canciones.append(cancion)
          songLines = []
          songLines.append(line)
        i += 1

      # sino, el renglón no tiene song
      else:
        # lo voy agregando
        songLines.append(line)
 
    # terminó el archivo, ya esta lista la ultima canción
    cancion = Cancion(i-1)
    cancion.decodeTxt(songLines)
    self.canciones.append(cancion)
    songLines = []
    songLines.append(line)



##########################################################
class Cancion:
  """ representa una cancion """

  def __init__(self, nro):
    self.nro = nro

    # si la canción puede terminar en repeat en lugar de loop
    # solo la cancion 2, que se le permite terminar en repeat por un bug en la rom
    self.repeatTermina = (nro == 2)

    self.addrCh2 = None
    self.addrCh1 = None
    self.addrCh3 = None

    self.melody2 = None
    self.melody1 = None
    self.melody3 = None

  def decodeRom(self, bank):
    """ decodifica una cancion """

    base = 0x0a12 + 6*self.nro

    self.addrCh2 = bank[base + 1]*0x100 + bank[base + 0]
    self.addrCh1 = bank[base + 3]*0x100 + bank[base + 2]
    self.addrCh3 = bank[base + 5]*0x100 + bank[base + 4]

    melody2 = Melody(nroChannel=2, addr=self.addrCh2, repeatTermina=self.repeatTermina)
    melody2.decodeRom(bank)
    self.melody2 = melody2
    melody1 = Melody(nroChannel=1, addr=self.addrCh1, repeatTermina=self.repeatTermina)
    melody1.decodeRom(bank)
    self.melody1 = melody1
    melody3 = Melody(nroChannel=3, addr=self.addrCh3, repeatTermina=self.repeatTermina)
    melody3.decodeRom(bank)
    self.melody3 = melody3

  def encodeTxt(self):
    lines = []

    lines.append('\n--------- song {:02} ---------'.format(self.nro))
    lines.extend(self.melody2.encodeTxt())
    lines.extend(self.melody1.encodeTxt())
    lines.extend(self.melody3.encodeTxt())

    return lines

  def decodeTxt(self, lines):
    """ decodifica una cancion del txt """

    currAddr = 0x0000
    channels = [2,1,3]
    i=0
    chLines = []

    # por cada renglón
    for line in lines:

      # si es un nuevo channel
      if('CHANNEL' in line):
        # y es el primero
        if(i==0): 
          # vamos agregando renglones
          chLines.append(line)
        # si es la segunda vez que aparece
        elif(i==1):
          # ya esta listo el CHANNEL 2
          self.addrCh2 = currAddr
          melody2 = Melody(nroChannel=2, addr=self.addrCh2, repeatTermina=self.repeatTermina)
          melody2.decodeTxt(chLines)
          self.melody2 = melody2
          chLines = []
          chLines.append(line)
        # si es la tercera vez que aparece
        elif(i==2):
          # ya esta listo el CHANNEL 1
          self.addrCh1 = currAddr
          melody1 = Melody(nroChannel=1, addr=self.addrCh1, repeatTermina=self.repeatTermina)
          melody1.decodeTxt(chLines)
          self.melody1 = melody1
          chLines = []
          chLines.append(line)

        idx0 = line.rfind(':')+1
        strAddr=line[idx0:].strip()
        currAddr = int(strAddr,16) 
        i += 1

      # sino, el renglón no tiene CHANNEL
      else:
        # lo voy agregando
        chLines.append(line)
 
    # terminó el archivo, ya esta listo el CHANNEL 3
    self.addrCh3 = currAddr
    melody3 = Melody(nroChannel=3, addr=self.addrCh3, repeatTermina=self.repeatTermina)
    melody3.decodeTxt(chLines)
    self.melody3 = melody3
    chLines = []



#    strHexa = Util.instance().strHexa(array)
#    print(strHexa)

#    for note in self.melody2.notas:
#      print('notu: ' + note.longString())


  def encodeLilypond(self):
    lines = []

    # los canales a exportar
    canales = [1,2,3]
#    canales = [2,3]

#    tempo = 60
    tempo = 120

    time = '4/4'
#    time = '3/4'

    lines.append('\\version "2.20.0"')
    if(2 in canales):
      lines.append('ch_two = {')
      lines.append('  \\clef treble')
      lines.append('  \\key c \\major')
      lines.append('  \\time ' + time)
#      lines.append('  \\tempo 4 = ' + str(tempo))
      lines.append('  ' + self.melody2.encodeLilypond())
      lines.append('}')

    if(1 in canales):
      lines.append('ch_one = {')
      lines.append('  \\clef treble')
      lines.append('  \\key c \\major')
      lines.append('  \\time ' + time)
#      lines.append('  \\tempo 4 = ' + str(tempo))
      lines.append('  ' + self.melody1.encodeLilypond())
      lines.append('}')

    if(3 in canales):
      lines.append('ch_three = {')
      lines.append('%  \\clef bass')
      lines.append('  \\clef treble')
      lines.append('  \\key c \\major')
      lines.append('  \\time ' + time)
#      lines.append('  \\tempo 4 = ' + str(tempo))
      lines.append('  ' + self.melody3.encodeLilypond())
      lines.append('}')

    lines.append('\\score {')
    lines.append('  <<')

    if(2 in canales):
      lines.append('    \\new Staff {')
      lines.append('      \set Staff.midiInstrument = "violin"')   # "string ensemble 1"  "violin"  "flute" "harmonica"
      lines.append('      \\new Voice = "ch2" \\ch_two')
      lines.append('    }')

    if(1 in canales):
      lines.append('    \\new Staff {')
      lines.append('      \set Staff.midiInstrument = "piano"')  # "bass section"   "electric guitar (steel)"
      lines.append('      \\new Voice = "ch1" \\ch_one')
      lines.append('    }')

    if(3 in canales):
      lines.append('    \\new Staff {')
      lines.append('      \set Staff.midiInstrument = "cello"')
      lines.append('      \\new Voice = "ch3" \\ch_three')
      lines.append('    }')

    lines.append('  >>')
    lines.append('  \\layout { }')
    lines.append('  \\midi { }')
    lines.append('}')

    return lines

  def exportLilypond(self):

    basePath = Address.instance().basePath
    path = basePath + '/audio'
 
    fileTxt = 'song_{:02}.txt'.format(self.nro)
    fileLily = 'song_{:02}_lily.txt'.format(self.nro)
    fileMidi = 'song_{:02}_lily.midi'.format(self.nro)
    fileMp3 = 'song_{:02}_lily.mp3'.format(self.nro)

    lines = self.encodeTxt()
    strTxt = '\n'.join(lines)
    f = open(path + '/' + fileTxt, 'w')
    f.write(strTxt)
    f.close()

#    exportaLily = False
    exportaLily = True
    # si quiero exportar al lilypond
    if(exportaLily):
      
      lines = self.encodeLilypond()
      strLily = '\n'.join(lines)

      f = open(path + '/' + fileLily, 'w')
      f.write(strLily)
      f.close()

      compilarLily = False
#      compilarLily = True
      # si además quiero compilarlo
      if(compilarLily):
        os.chdir(path)
        os.system('lilypond ./' + fileLily)
        os.system('timidity -Ow -o - ' + fileMidi + ' | lame - ' + fileMp3)
        os.chdir('../..')



  def __str__(self):
    string = 'addrCh2: {:04x} | addrCh1: {:04x} | addrCh3: {:04x}'.format(self.addrCh2, self.addrCh1, self.addrCh3)
    return string

##########################################################
class Melody:
  """ representa una melodía de un canal de una canción """

  def __init__(self, nroChannel=None, addr=None, repeatTermina=False):
    # si es pulso (ch2 y ch1) o wave (ch3)  (cambia el comando 0xe0)
    self.nroChannel = nroChannel
    # el address donde se quema
    self.addr = addr
    # si puede terminar con repeat en vez de loop (por el bug en la rom)
    self.repeatTermina = repeatTermina

    # las notas (comandos) de la melodía
    self.notas = []
 
  def decodeRom(self, bank):
    """ decodifica una melodía """

#    strHexa = Util.instance().strHexa(array[0:16])
#    print('melody: ' + strHexa)

    array = bank[self.addr - 0x4000:]

    currAddr = self.addr

    while(True):

      cmd = array[0]

      # si es el comando 0xe0
      if(cmd == 0xe0):
        # si estamos en el wave channel (ch3)
        if(self.nroChannel == 3):
          arg = array[1]
          nota = NotaMusical(currAddr, 2, cmd, arg)
          array = array[2:]
          currAddr += nota.length
        # sino, estamos en un ch2 ó ch1
        else:
          arg1 = array[1]
          arg2 = array[2]
          arg = arg2*0x100 + arg1
          nota = NotaMusical(currAddr, 3, cmd, arg)
          array = array[3:]
          currAddr += nota.length

      elif(cmd in [0xe3, 0xe5, 0xe6, 0xe7]):
        arg = array[1]
        nota = NotaMusical(currAddr, 2, cmd, arg)
        array = array[2:]
        currAddr += nota.length

      #0xe1 AAAA (LOOP AAAA) (loop infinito)
      #0xe2 AAAA (REPEAT AAAA) (repite una vez)
      elif(cmd in [0xe1, 0xe2, 0xe4, 0xe8]):
        arg1 = array[1]
        arg2 = array[2]
        arg = arg2*0x100 + arg1
        nota = NotaMusical(currAddr, 3, cmd, arg)
        array = array[3:]
        currAddr += nota.length

      # eb 01 xxyy    (repetir una vez y saltar al addr yyxx ?) 
      elif(cmd in [0xeb]):
        arg = array[1]
        arg21 = array[2]
        arg22 = array[3]

        arg2 = arg22*0x100 + arg21

        nota = NotaMusical(currAddr, 4, cmd, arg, arg2)
        array = array[4:]
        currAddr += nota.length

      else:
        arg = None
        nota = NotaMusical(currAddr, 1, cmd, arg)
        array = array[1:]
        currAddr += nota.length

#      print('nota: ' + str(nota))
      self.notas.append(nota)

      # si el comando es loop o 0xff
      if(cmd in [0xff, 0xe1]):
        # termino la melodía
        break
      # si permito terminar con repeat (por el bug en la rom) y es el comando repeat
      elif(self.repeatTermina and cmd == 0xe2):
        # termino la melodía
        break


    # inicio el contador de labels
    lblCount = 1
    # por cada nota
    for nota in self.notas:
#      print('notaa: ' + str(nota))
      # si es un jump
      if(nota.cmd in [0xe1, 0xe2, 0xeb]):
        addr = nota.arg
        # en el caso del jumpif
        if(nota.cmd == 0xeb):
          # el addr está indicado en el argumento 2
          addr = nota.arg2

#        print('es un e1 {:4x} '.format(arg))
        # busco la nota a la cual saltar
        for noty in self.notas:
          if(noty.addr == addr):
#            print('encontre: ' + str(noty))
            # y le agrego el label
            nota.jumpLabel = 'label{:}'.format(lblCount)
            noty.labels.append('label{:}'.format(lblCount))
            # incremento contador de labels
            lblCount += 1

#    print('----')
          

  def encodeTxt(self):

    string = ''


    string += '\n--- CHANNEL: {:02x} addr: {:4x}\n'.format(self.nroChannel, self.addr)

    # si el comando anterior fue una nota musical
    anteriorFueNota = False
    # por cada nota
    for nota in self.notas:

      # si tiene labels
      if(len(nota.labels) > 0):
        # si estaba imprimiendo notas musicales
        if(anteriorFueNota):
          # dejo un renglón
          string += '\n'
        # ya no estoy imprimiendo notas musicales
        anteriorFueNota = False
        # imprimo los labels
        for label in nota.labels:
          string += label + ':\n'

#      print('notaa: ' + str(nota))
      # si es un comando (salvo subir o bajar escala)
      if(nota.cmd1 in [0xd, 0xe] and nota.cmd not in [0xd8, 0xdc]):
        # si estaba imprimiendo notas musicales
        if(anteriorFueNota):
          # dejo un enter
          string += '\n'
        # muestro el comando
        string += str(nota) + '\n'
        # ya no estoy imprimiendo notas musicales
        anteriorFueNota = False
      # sino, es una nota musical
      else:
        # si ya estaba imprimiendo notas musicales
        if(anteriorFueNota):
          # sigo al lado
          string += ' ' + str(nota)
        # sino
        else:
          # es un nuevo comando play
          string += 'PLAY ' + str(nota)
        # indico que estoy imprimiendo notas musicales
        anteriorFueNota = True

    lines = string.splitlines()
    return lines

  def decodeTxt(self, lines):
    """ decodifica el canal a partir de un txt """

    # reinicio el listado de notas
    self.notas = []

    # el addr de la nota actual
    vaPorAddr = 0
    # los labels de la nota actual
    currentLabels = []

    for line in lines:
      line = line.strip()
#      print('line: ' + line)

      # si es un comentario
      if(line.startswith('#') or len(line) == 0):
        # no hago nada
        pass
      # sino, no es un comentario
      else:
        if('CHANNEL' in line):

          idx0 = line.find(':')+2
          strCh = line[idx0:idx0+2]
          nroChannel = int(strCh)
          self.nroChannel = nroChannel

          idx1 = line.rfind(':')+2
          strAddr = line[idx1:idx1+4]
          addr = int(strAddr,16)
          self.addr = addr

          # indico por que addr va la instrucción actual
          vaPorAddr = addr

        elif('TEMPO' in line):

#          print('line: ' + line)
          args = line.split()
          tempo = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 2, 0xe7, tempo)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('INSTR_e4' in line):
 
#          print('line: ' + line)
          args = line.split()
          e4Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 3, 0xe4, e4Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('INSTR_e8' in line):
 
#          print('line: ' + line)
          args = line.split()
          e8Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 3, 0xe8, e8Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('INSTR_e0' in line):
 
#          print('line: ' + line)
          cantBytes = 3
          if(self.nroChannel==3):
            cantBytes=2

          args = line.split()
          e0Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, cantBytes, 0xe0, e0Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('INSTR_e5' in line):
 
#          print('line: ' + line)
          args = line.split()
          e5Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 2, 0xe5, e5Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('INSTR_e6' in line):
 
#          print('line: ' + line)
          args = line.split()
          e6Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 2, 0xe6, e6Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        # si es un label (termina en ':')
        elif(':' in line):
          # le quito el ':'
          label = line[:len(line)-1]
#          print('label: ' + label)
          currentLabels.append(label)
 
        elif('COUNTER' in line):
 
#          print('line: ' + line)
          args = line.split()
          counterArg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 2, 0xe3, counterArg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('OCTAVE' in line):
 
#          print('line: ' + line)
          idx0 = line.find('OCTAVE')+7
          strOctave = line[idx0:idx0+2]
          octave = int(strOctave,16)

          nota = NotaMusical(vaPorAddr, 1, octave, None)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('JUMPIF' in line):
 
#          print('line: ' + line)
          args = line.split()
          arg = int(args[1])
          label = args[2]

          nota = NotaMusical(vaPorAddr, 4, 0xeb, arg)
          nota.labels = currentLabels
          nota.jumpLabel = label
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('REPEAT' in line):
 
#          print('line: ' + line)
          args = line.split()
          label = args[1]
          nota = NotaMusical(vaPorAddr, 3, 0xe2, None)
          nota.labels = currentLabels
          nota.jumpLabel = label
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('JUMP' in line and 'JUMPIF' not in line):
 
#          print('line: ' + line)
          args = line.split()
          label = args[1]
          nota = NotaMusical(vaPorAddr, 3, 0xe1, None)
          nota.labels = currentLabels
          nota.jumpLabel = label
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('PLAY' in line):
#          print('line: ' + line)

          idx0 = line.find('PLAY')+5
          strNotas = line[idx0:]

          # diccionario para armar el cmd2 (la segunda parte del byte nota musical)
          valCmd2 = { 'c':0x0, 'd':0x2, 'e':0x4, 'f':0x5, 'g':0x7, 'a':0x9, 'b':0xb, 'r':0xf}

          cmd = 0
          currentNote = ''
          currentAccident = ''
          currentTilde = ''
          currentLength = ''

          # por cada caracter del string con todas las notas
          for chara in strNotas:

            # si es una nota musical
            if(chara in ['c','d','e','f','g','a','b','r','<','>']):

              # si hay una nota anterior
              if(currentNote != ''):

                # la nota anterior está terminada
                if(currentNote == '<'):
                  cmd = 0xdc
                elif(currentNote == '>'):
                  cmd = 0xd8
                else:
                  cmd2 = valCmd2[currentNote]
                  if(currentTilde == "'"):
                    cmd2 += 12
                  if(currentAccident == "#"):
                    cmd2 += 1

                  # pongo un length default
                  if(currentLength == ''):
                    cmd1 = 0x8
                  else:
                    cmd1 = int(currentLength, 10)

#                  print('cnd1: ' + str(cmd1))
                  cmd = cmd1*0x10 + cmd2
                # la creo
                nota = NotaMusical(vaPorAddr, 1, cmd, None)
                nota.labels = currentLabels
                # y agrego al listado de notas
                self.notas.append(nota)
                vaPorAddr += nota.length
                currentLabels = []


              currentNote = chara
              currentAccident = ''
              currentTilde = ''
              currentLength = ''

            # si es un tilde
            elif(chara == "'"):
              currentTilde = "'" 
            # si es un accidente
            elif(chara in ['#', '+']):
              currentAccident = '#'

            elif(chara in ['0','1','2','3','4','5','6','7','8','9']):
              currentLength += chara

          # la nota anterior está terminada
          if(currentNote == '<'):
            cmd = 0xdc
          elif(currentNote == '>'):
            cmd = 0xd8
          else:
            cmd2 = valCmd2[currentNote]
            if(currentTilde == "'"):
              cmd2 += 12
            if(currentAccident == "#"):
              cmd2 += 1

            # pongo un length default
            if(currentLength == ''):
              cmd1 = 0x8
            else:
              cmd1 = int(currentLength, 10)

            cmd = cmd1*0x10 + cmd2
          # la creo
          nota = NotaMusical(vaPorAddr, 1, cmd, None)
          nota.labels = currentLabels
          # y agrego al listado de notas
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []

    # calculo los addr de los labels !!!
    self.refreshLabels()

  def refreshLabels(self):
    """ setea los addrs de los labels """

    # la primer nota está en addr del canal
    vaPorAddr = self.addr

    # segunda pasada (para setear addr fisico de los labels)
    for nota in self.notas:

      nota.addr = vaPorAddr
      vaPorAddr += nota.length

      # si es una instrucción de salto (JUMP, REPEAT, JUMPIF)
      if(nota.cmd in [0xe1, 0xe2, 0xeb]):
#        print('note: ' + str(nota))
        jumpLabel = nota.jumpLabel
        for noty in self.notas:
          if(jumpLabel in noty.labels):
#            print('lo encontré: {:4x}'.format(noty.addr))
            if(nota.cmd in [0xe1, 0xe2]):
              nota.arg = noty.addr
            else:
              nota.arg2 = noty.addr

#    for nota in self.notas:
#      print('nota: ' + str(nota))


  def encodeRom(self):
    array = []

    for nota in self.notas:
      array.extend(nota.toBytes())

    return array


  def encodeLilypond(self):

    string = ''

    dicLong = {
                0x0 : '1',   # 0x60 (96)
                0x1 : '2.',  # 0x48 (72)
                0x2 : '2',   # 0x30 (48)
                0x4 : '4.',  # 0x24 (36)
                0x5 : '4',   # 0x18 (24)
                0x7 : '8.',  # 0x12 (18)
                0x8 : '8',   # 0x0c (12)
                0xa : '16',  # 0x06 (06)
                0xb : '16.', # 0x04 (04)  # se usar para triplets
                0xc : '32',  # 0x03 (03)

                0xf : '1',   # 0xc1?      # 0xff se usa para indicar el final de la canción ?

                0x3 : '2',   # 0x20 (32)  # no se usa
                0x6 : '4',   # 0x10 (16)  # no se usa
                0x9 : '8'    # 0x08 (08)
              }

    dicNotas = { 0x0 : 'c',
                 0x1 : 'cis',
                 0x2 : 'd', 
                 0x3 : 'dis',
                 0x4 : 'e',
                 0x5 : 'f',
                 0x6 : 'fis',
                 0x7 : 'g',
                 0x8 : 'gis',
                 0x9 : 'a',
                 0xa : 'ais',
                 0xb : 'b',
                 0xc : 'c',
                 0xd : 'cis',
                 0xe : 'd',
                 0xf : 'r'
               }

    # índice del último label visto
    lastLabelIndex = 0

    # eligo valores de mano y octava default
    mano = 0x3
    octava = 1
    # para cada nota
    for i in range(0, len(self.notas)):
      # la agarro
      nota = self.notas[i]

      # si tiene labels
      if(len(nota.labels)>0):
        # voy indicando que es la última vista con labels
        lastLabelIndex = i

      # si es REPEAT
      if(nota.cmd == 0xe2):
        # indico en el último label que hay repeat
        self.notas[lastLabelIndex].repeatsTo = True



    # el contador de repeticiones
    counter = 0
    # si el repeat actual tiene jumpif
    tieneJumpif = False

    # vuelvo a iterar sobre las notas
    for nota in self.notas:

      # si es COUNTER
      if(nota.cmd == 0xe3):
        counter = nota.arg

      # si tiene label que inicia un repeat
      if(nota.repeatsTo):
#        string += "  \\repeat volta " + str(counter) + " {\n"
        string += "  \\repeat unfold " + str(counter) + " {\n"

      # si es JUMPIF
      if(nota.cmd == 0xeb):
        string += "\n  | }\\alternative {{ \n"
        # indico que tieneJumpif
        tieneJumpif = True

      # si es REPEAT
      if(nota.cmd == 0xe2):
        if(tieneJumpif):
          string += "\n    }{}}\n"
        else:
          string += "\n    | }\n"
        # reseteo tieneJumpif para la próxima
        tieneJumpif = False


      # si cambia donde va la mano
      if(nota.cmd1 == 0xd):
        mano = nota.cmd2
#        print('mano: {:x} '.format(mano))

        # eligo la octava default actual
#        if(mano in [0x3, 0x8]):
        if(mano in [0x3]):
          octava = 1
        elif(mano in [0x2]):
          octava = 1
        elif(mano in [0x8]):
          octava += 1
        elif(mano in [0xc]):
          octava -= 1

#      print('comando: {:x}'.format(nota.cmd))

      # tempo
      if(nota.cmd == 0xe7):
        # trato de emular el tempo correcto (no se cual es el valor exacto)
        string += '\n  \\tempo 4 = ' + str(int((100*nota.arg/84))) + '\n  '
#        string += '\n  \\tempo 4 = ' + str(int(nota.arg)) + '\n  '
        pass

      # si es un comando de octava
      if(nota.cmd1 == 0xd):
        # no muestro nada
        pass
      # si es un comando normal
      elif(nota.cmd1 == 0xe):
        pass

      # sino, es una nota musical
      else:

        lilyNota = dicNotas[nota.cmd2]

        saltaOctava = 0
        # si la nota es 0xc o mas alta (salvo 0xe que creo que es vibrato)
        if(nota.cmd2 in [0xc, 0xd]):
          # es de la octava siguiente
          saltaOctava = 1

        # si es la nota de longitud rara
        if(nota.cmd1 == 0xb):
          string += '\\tuplet 3/2 {' + lilyNota
          if(lilyNota != 'r'):
            string += '\''*(octava + saltaOctava)
          string += '16}'

        # sino, es de longitud normal
        else:
          string += lilyNota

          if(lilyNota != 'r'):
            string += '\''*(octava + saltaOctava)

          if(nota.cmd1 in dicLong):
            lilyLength = dicLong[nota.cmd1]
            string += lilyLength


        string += ' '


    return string


  def __str__(self):

    string = '\n'
    for nota in self.notas:
      string += str(nota) + '\n'

    return string



##########################################################
class NotaMusical:
  """ representa una nota o comando musical de una melodía """

  def __init__(self, addr, length, cmd, arg, arg2=None):
    # la dirección física dentro del bank de la rom
    self.addr = addr
    # la longitud en bytes de la nota
    self.length = length
    # el comando de la nota
    self.cmd = cmd
    # sus posibles argumentos
    self.arg = arg
    self.arg2 = arg2

    # guardo el primer y segundo char hexa del comando por separados
    self.cmd1 = (cmd & 0xf0)//0x10
    self.cmd2 = (cmd & 0x0f)

    # label al cual hace jump esta nota 
    self.jumpLabel = ''
    # lista de labels que se usan para saltar a esta nota
    self.labels = []
    # se usa para indicar si tiene algún label que proviene de un REPEAT
    self.repeatsTo = False

    self.dicNotas = {
                 0x0 : "c",
                 0x1 : "c#",
                 0x2 : "d", 
                 0x3 : "d#",
                 0x4 : "e",
                 0x5 : "f",
                 0x6 : "f#",
                 0x7 : "g",
                 0x8 : "g#",
                 0x9 : "a",
                 0xa : "a#",
                 0xb : "b",
                 0xc : "c'",
                 0xd : "c'#",
                 0xe : "d'",
                 0xf : "r"
               }

  def toBytes(self):
    array = []

    array.append(self.cmd)

    # si tiene un primer argumento
    if(self.arg != None):
      # si ocupa un solo byte
      if(self.arg <= 0xff):

        # lo agrego
        array.append(self.arg)

      # sino, ocupa dos bytes
      else:
        # los separo
        argu1 = self.arg // 0x100
        argu2 = self.arg % 0x100
        # y los agrego
        array.append(argu2)
        array.append(argu1)

    # si tiene un segundo argumento (siempre es de 2 bytes)
    if(self.arg2 != None):
      # los separo
      argu1 = self.arg2 // 0x100
      argu2 = self.arg2 % 0x100
      # y los agrego
      array.append(argu2)
      array.append(argu1)

    return array

  def longString(self):

    string = ''

    string += '{:04x} | '.format(self.addr)

#    string += '{:04x} | {:02x} '.format(self.addr, self.cmd)
#    if(self.arg != None):
#      string += '{:04x} '.format(self.arg)

    # imprimo los labels
    for label in self.labels:
#      string += label + ':\n'
      string += label + ' '

    string += str(self)
    return string

 
  def __str__(self):
    string = ''

#    string += '{:04x} | '.format(self.addr)

#    string += '{:04x} | {:02x} '.format(self.addr, self.cmd)
#    if(self.arg != None):
#      string += '{:04x} '.format(self.arg)

    # imprimo los labels
#    for label in self.labels:
#      string += label + ':\n'
#      string += label + ' '

    # si es un comando de octava
    if(self.cmd1 == 0xd):
      if(self.cmd2 == 0x8):
        string += '>' 
      elif(self.cmd2 == 0xc):
        string += '<'
      else:
        string += 'OCTAVE_{:02x}'.format(self.cmd)

    # sino, si es un comando general
    elif(self.cmd1 == 0xe):

      # instr e0
      if(self.cmd2 == 0x0):
        string += 'INSTR_e0 {:x}'.format(self.arg)
      # jump
      elif(self.cmd2 == 0x1):
        string += 'JUMP ' + self.jumpLabel
      # repeat
      elif(self.cmd2 == 0x2):
        string += 'REPEAT ' + self.jumpLabel
      # contador
      elif(self.cmd2 == 0x3):
        string += 'COUNTER {:x}'.format(self.arg)
      # instr e4
      elif(self.cmd2 == 0x4):
        string += 'INSTR_e4 {:x}'.format(self.arg)
      # instrumento?
      elif(self.cmd2 == 0x5):
        string += 'INSTR_e5 {:x}'.format(self.arg)
      # instr e6
      elif(self.cmd2 == 0x6):
        string += 'INSTR_e6 {:x}'.format(self.arg)
      # tempo
      elif(self.cmd2 == 0x7):
        string += 'TEMPO {:x}'.format(self.arg)
      # instr e8
      elif(self.cmd2 == 0x8):
        string += 'INSTR_e8 {:x}'.format(self.arg)
      # jumpif
      elif(self.cmd2 == 0xb):
        string += 'JUMPIF {:x} '.format(self.arg) + self.jumpLabel
      else:
        string += '{:02x} '.format(self.cmd, self.arg)
        if(self.arg != None):
          string += '{:x} '.format(self.arg)
        if(self.arg2 != None):
          string += '{:x} '.format(self.arg2)

    # sino, es una nota musical
    else:
      lilyNota = self.dicNotas[self.cmd2]
      lilyLength = str(self.cmd1)
#      if(self.cmd1 == 0xb):
#        lilyLength = 'coco'
      string += lilyNota + lilyLength



    return string



##########################################################
class Slot:
  """ representa un slot de guardado """

  def __init__(self, array):
    self.array = array

  def get(self, idx):
    """ retorna el byte del array indicado """
    return self.array[idx]

  def setChecksum(self, check):
    """ setea el checksum """

#    print('seteando checksum {:04x}'.format(check))
    check1 = check % 0x100
    check2 = check // 0x100
    self.array[1] = check1
    self.array[2] = check2

  def fixChecksum(self):
    """ corrige el checksum """
    check = self.calculateChecksum()
    self.setChecksum(check)

  def getChecksum(self):
    """ retorna el checksum guardado en el .sav """

    checkArray = self.array[1:3]
    check = checkArray[1]*0x100 + checkArray[0]
    return check

  def calculateChecksum(self):
    """ calcula el checksum correspondiente al .sav """
    suma = 0x00
    for i in range(3, 8*15+3):
      val = self.array[i]
      suma += val
#      print('valor {:02x}'.format(val))
   
    return suma

  def getHeros(self):
    """ retorna los nombres de los heroes guardado en el slot """

    heroArray = self.array[3:7]
    heroinArray = self.array[7:11]

    strHero = Dictionary.instance().decodeArray(heroArray)
    strHeroin = Dictionary.instance().decodeArray(heroinArray)

    return strHero, strHeroin

  def getHP(self):
    """ retorna hp y hpTotal """

    hpArray = self.array[11:13]
    hp = hpArray[1]*0x100 + hpArray[0]

    hpTotalArray = self.array[13:15]
    hpTotal = hpTotalArray[1]*0x100 + hpTotalArray[0]

    return hp, hpTotal

  def getMP(self):
    """ retorna mp y mpTotal """

    mpArray = self.array[15:17]
    mp = mpArray[1]*0x100 + mpArray[0]

    mpTotalArray = self.array[17:19]
    mpTotal = mpTotalArray[1]*0x100 + mpTotalArray[0]

    return mp, mpTotal

  def getLevel(self):
    """ retorna level """

    level = self.array[19]
    return level

  def getExp(self):
    """ retorna experiencia """

    expArray = self.array[20:23]
    exp = expArray[2]*(0x10000) + expArray[1]*0x100 + expArray[0]
    return exp

  def getNextLevelExp(self):
    """ retorna la experiencia necesaria para pasar de nivel """

    nextExp = 0

    # f(1) = 16
    # f(2) = 44
    # f(3) = 90

    level = self.getLevel()
#    print('level: ' + str(level))

    nextExp = 2**3 * 2**(level)

    return nextExp


  def getGP(self):
    """ retorna gp """

    gpArray = self.array[23:25]
    gp = gpArray[1]*0x100 + gpArray[0]
    return gp

  def setGP(self, gp):
    """ setea gp """
    gp1 = gp % 0x100
    gp2 = gp // 0x100
    self.array[23] = gp1
    self.array[24] = gp2

  def getStatus(self):
    """ retorna status """

    status = self.array[25]
    return status

  def getStamnPowerWisdmWill(self):
    """ retorna stamina, power, wisdom, will """

    stamn = self.array[26]
    power = self.array[27]
    wisdm = self.array[28]
    will  = self.array[29]

    return stamn, power, wisdm, will

  def getFlags(self):
    """ retorna los flags (variables de estado según avance del juego) """

    # flag[11] = acompaña (0x40 = jofy, 0x08 = bogard, ...)
#    flags = self.array[30:30+19]
    flags = self.array[31:46]
    return flags

  def getFlag(self, nroFlag):
    idx = nroFlag // 8
    idx2 = nroFlag % 8

    # agarro el byte donde está el flag
    val = self.getFlags()[idx] 
    # me quedo con el bit del flag
    val = val & 2**(7-idx2)

    # es True si no quedó en cero
    ret = (val != 0) 
    return ret

  def setFlag(self, nroFlag, val):
    idx = nroFlag // 8
    idx2 = nroFlag % 8

    # agarro el byte donde está el flag
    preval = self.getFlags()[idx]

#    print('prevalA: {:08b}'.format(preval))
    if(val):
      preval = preval | 2**(7-idx2)
    else:
      preval = preval & (0xff - 2**(7-idx2))
#    print('prevalB: {:08b}'.format(preval))

    self.array[31+idx] = preval

  def setFlagByLabel(self, label, val):
    # busco el nro de flag correspondiente al label
    nroFlag = Variables.instance().getVal(label)
    self.setFlag(nroFlag, val)
 
  def getFlagByLabel(self, label):
    # busco el nro de flag correspondiente al label
    nroFlag = Variables.instance().getVal(label)
    val = self.getFlag(nroFlag)
    return val
 

  def printFlags(self):
    flags = self.getFlags()
    i = 0
    string = ''
    for flag in flags:
#      string += str(i).zfill(2) + '|'
      i += 1
#    string += '\n'
    for flag in flags:
      string += '{:02x}'.format(flag) + '|'
    print(string)

#  def setFlag(self, i, val):
#    """ setea el valor indicado al flag indicado """
#    self.array[30+i] = val


  def getApVp(self):
    """ retorna puntos de ataque y defensa según el equip """

    ap = self.array[51]
    dp = self.array[53]

    return ap, dp

  def getInventario(self):
    """ retorna el inventario """

    # array de códigos de item
    invArray = self.array[55:71]
    # array paralelo de cantidades de cada item
    cantArray = self.array[99:115]

    for i in range(0,16):
      val = invArray[i]
      cant = cantArray[i]
#      print('inv: {:02x}'.format(val) + ' dec: ' + str(val))

      idx = val // 8
      idx2 = val % 8

      val0 = 1 if val & 2**(7-0) != 0 else 0
      val1 = 1 if val & 2**(7-1) != 0 else 0
      val2 = 1 if val & 2**(7-2) != 0 else 0
      val3 = 1 if val & 2**(7-3) != 0 else 0
      val4 = 1 if val & 2**(7-4) != 0 else 0
      val5 = 1 if val & 2**(7-5) != 0 else 0
      val6 = 1 if val & 2**(7-6) != 0 else 0
      val7 = 1 if val & 2**(7-7) != 0 else 0
#      print('--> ' + str(val0) + ',' + str(val1) + ',' + str(val2)  + ',' + str(val3) + ','  + str(val4) + ','  + str(val5) + ','  + str(val6) + ','  + str(val7))

      # el primer bit indica si puede haber mas de uno
      varios = val0*2**0
      comodin = '*' if varios != 0 else ' '
      # el nro es el código de item
      nro = val1*2**6 + val2*2**5 + val3*2**4 + val4*2**3 + val5*2**2 + val6*2**1 + val7*2**0
      # obtengo la descripción del item
      descr = Variables.instance().items[nro-1]
      print('item: ' + str(cant) + ' ' + comodin + descr)


  def getMagia(self):

    # array de códigos de magia
    magArray = self.array[71:79]
#    magArray = self.array[72:80]

    for i in range(0,8):
      val = magArray[i]
#      print('mag: {:02x}'.format(val))

      val0 = 1 if val & 2**(7-0) != 0 else 0
      val1 = 1 if val & 2**(7-1) != 0 else 0
      val2 = 1 if val & 2**(7-2) != 0 else 0
      val3 = 1 if val & 2**(7-3) != 0 else 0
      val4 = 1 if val & 2**(7-4) != 0 else 0
      val5 = 1 if val & 2**(7-5) != 0 else 0
      val6 = 1 if val & 2**(7-6) != 0 else 0
      val7 = 1 if val & 2**(7-7) != 0 else 0

      # el primer bit indica si puede haber mas de uno
      varios = val0*2**0
      comodin = '*' if varios != 0 else ' '
      # el nro es el código de item
      nro = val1*2**6 + val2*2**5 + val3*2**4 + val4*2**3 + val5*2**2 + val6*2**1 + val7*2**0
      # obtengo la descripción del item
      descr = Variables.instance().items[nro-1]
      print('mag: ' + comodin + str(nro))


  def getArmas(self):

    # array de códigos de weapon
    weapArray = self.array[79:91]

    for i in range(0,12):
      val = weapArray[i]
      descr = Variables.instance().armas[val-1]
      print('arma: {:02x}'.format(val) + ' - ' + descr)



    weaponMano = self.array[91]
    descr = Variables.instance().armas[weaponMano-1]
    print('arma en mano: {:02x}'.format(val) + ' - ' + descr)

    sombreroMano = self.array[92]
    descr = Variables.instance().armas[sombreroMano-1]
    print('sombrero en mano: {:02x}'.format(val) + ' - ' + descr)

    ropaMano = self.array[94]
    descr = Variables.instance().armas[ropaMano-1]
    print('ropa en mano: {:02x}'.format(val) + ' - ' + descr)

    escudoMano = self.array[96]
    descr = Variables.instance().armas[escudoMano-1]
    print('escudo en mano: {:02x}'.format(val) + ' - ' + descr)


   

  def getCoords(self):
    """ retorna las coordenadas del mapa """
    mm = self.array[115]
    xy = self.array[116]
    uu = self.array[117]
    vv = self.array[118]

#    print('mm {:02x}'.format(mm))
    return mm,xy,uu,vv
 
  def setCoords(self, mm, xy, uu, vv):
    """ setea las coordenadas del mapa """
    self.array[115] = mm
    self.array[116] = xy
    self.array[117] = uu
    self.array[118] = vv

  def printFull(self):

    print(' ----- ')

    hero, heroin = self.getHeros()
    print('hero: ' + hero + ' | heroin: ' + heroin)

    hp, hpTotal = self.getHP()
    print('hp: ' + str(hp) + ' | hpTotal: ' + str(hpTotal))

    mp, mpTotal = self.getMP()
    print('mp: ' + str(mp) + ' | mpTotal: ' + str(mpTotal))

    level = self.getLevel()
    print('level: ' + str(level))
    exp = self.getExp()
    print('exp: ' + str(exp))
    nextExp = self.getNextLevelExp()
    print('nextExp: ' + str(nextExp))
    gp = self.getGP()
    print('GP: ' + str(gp))

    status = self.getStatus()
    print('status: ' + str(status))
    stamn,power,wisdm,will = self.getStamnPowerWisdmWill()
    print('stamn: ' + str(stamn) + ' | power: ' + str(power) + ' | wisdm: ' + str(wisdm) + ' | will: ' + str(will))
    ap,vp = self.getApVp()
    print('ap: ' + str(ap) + ' | vp: ' + str(vp))

    mm,xy,uu,vv = self.getCoords()
    print('mm xy uu vv: {:02x} {:02x} {:02x} {:02x}'.format(mm,xy,uu,vv))

    flags = self.getFlags()
    for flag in flags:
      print('flagarray: {:08b}'.format(flag))

    for i in range(0,8*15):
      label = Variables.instance().getLabel(i)
      flag = self.getFlag(i)
      val = 0
      if(flag):
        val = 1
      print('flag: ' + str(val) + ' = ' + label)

    inv = self.getInventario()
    mag = self.getMagia()
    equip = self.getArmas()

class Saves:

  def __init__(self):
    self.saves = []

    saveFile = './roms/savegames/save_01_first_cave.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_02_ketts_place.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_03_marsh_cave.sav'
    self.save = Save(saveFile)
    saves.append(save)
    saveFile = './roms/savegames/save_04_ketts_place_revisited.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_05_wendel.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_06_silver_mine.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_07_gaia.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_08_airship.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_09_menos.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_10_medusas_cave.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_11_davias_mansion.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_12_cave_at_mt_rocks.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_13_mt_rocks.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_14_glaive_castle.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_15_cave_of_snowfields.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_16_floatrocks.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_17_cave_in_floatrocks.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_18_undersea_volcano.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_19_lichs_cave.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_20_cave_of_ruins.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_21_dime_tower.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_22_temple_of_mana.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_23_final_battle_ground.sav'
    save = Save(saveFile)
    self.saves.append(save)



##########################################################
class Save:
  """ analiza el savestate .sav """

  def __init__(self, filepath):
    self.filepath = filepath

    array = Util.instance().fileToArray(self.filepath)

    # el array con los 2 slots para grabar
    self.slot = []

    array1 = []
    array2 = []
    iArr = 0
    # para cada uno de los 16 renglones
    for j in range(0x10):
      # para cada una de las 8 columnas
      for i in range(8):

        byte2 = array[j*0x10 + 2*i+1]
        byte1 = array[j*0x10 + 2*i]
        strByte2 = '{:02x}'.format(byte2)[1]
        strByte1 = '{:02x}'.format(byte1)[1]
#        print('strByte2, strByte1: ' + strByte2 + ', ' + strByte1)
        strNum1 = strByte2 + strByte1
        val1 = int(strNum1, 16)
        # agrego el valor al slot1
        array1.append(val1)

        byte2 = array[(j+0x10)*0x10 + 2*i+1]
        byte1 = array[(j+0x10)*0x10 + 2*i]
        strByte2 = '{:02x}'.format(byte2)[1]
        strByte1 = '{:02x}'.format(byte1)[1]
        strNum2 = strByte2 + strByte1
        val2 = int(strNum2, 16)
        # agrego el valor al slot2
        array2.append(val2)

    # la primer pos de guardado
    self.slot.append(Slot(array1))
    # la segunda pos de guardado
    self.slot.append(Slot(array2))

  def saveFile(self):
    """ reescribe el archivo .sav !! """

#    f = open(self.filepath + '.new', 'bw')
    f = open(self.filepath, 'bw')

    for i in range(0,2):

      # corrijo el checksum
      self.slot[i].fixChecksum()

      slotArray = self.slot[i].array
#      print('slotArray[' + str(i) + '] = ' + str(slotArray))

#      for byte in slotArray:
      for k in range(0,0x80 - 4):
        byte = slotArray[k]
        strByte = '{:02x}'.format(byte)
#        print('strByte: ' + strByte)

#        rellenoConF = True
        rellenoConF = False
        if(rellenoConF):
          strByte1 = 'F' + strByte[0]
          strByte2 = 'F' + strByte[1]
        else:
          strByte1 = '0' + strByte[0]
          strByte2 = '0' + strByte[1]

#        print('strByte1: ' + strByte1)
#        print('strByte2: ' + strByte2)

        byte1 = int(strByte1, 16)
        byte2 = int(strByte2, 16)

#        print('byte1: {:02x}'.format(byte1))
#        print('byte2: {:02x}'.format(byte2))


        f.write(bytes([byte2, byte1]))

      f.write(bytes([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))

    f.close()

  def printBatt(self):
    """ muestro la info de los slots """

    # para cada uno de los 16 renglones
    for j in range(0x10):
      renglon1 = ''
      renglon2 = ''
      # para cada una de las 8 columnas
      for i in range(8):
        val1 = self.slot[0].get(8*j + i)
        val2 = self.slot[1].get(8*j + i)
        renglon1 += '{:02x}'.format(val1) + ' '
        renglon2 += '{:02x}'.format(val2) + ' '
   
      print(renglon1 + ' | ' + renglon2)


  def printLindo(self):

    for i in range(0,2):

      print('--- slot ' + str(i+1) + ' ---')
      hero, heroin = self.slot[i].getHeros()
      print(hero + ', ' + heroin)
      hp, hpTotal = self.slot[i].getHP()
      print('HP: ' + str(hp) + '/' + str(hpTotal))
      mp, mpTotal = self.slot[i].getMP()
      print('MP: ' + str(mp) + '/' + str(mpTotal))
      level = self.slot[i].getLevel()
      print('L' + str(level))
      exp = self.slot[i].getExp()
      print('E ' + str(exp))
      gp = self.slot[i].getGP()
      print('GP ' + str(gp))
      status = self.slot[i].getStatus()
      print('status: ' + str(status))
      stamn, power, wisdm, will = self.slot[i].getStamnPowerWisdmWill()
      print('stamn ' + str(stamn) + ' power ' + str(power) + ' wisdm ' + str(wisdm) + ' will ' + str(will))

      ap, vp = self.slot[i].getApVp()
      print('AP: ' + str(ap) + ' VP: ' + str(vp))

      print('--------------')



#################################
def main(argv):
  print('Welcome to mystic-editor')

  # hago copia de seguridad de las roms stock que encuentre en el directorio actual
  RomSplitter.instance().protectStockRoms()

  romPath = './stockRoms/en.gb'
#  romPath = './stockRoms/fr.gb'
#  romPath = './stockRoms/de.gb'
#  romPath = './stockRoms/jp.gb'
#  romPath = './game.gb'
  Address.instance().detectRomLanguage(romPath)
  RomSplitter.instance().configure()
  # decodifico el diccionario (compress)
  Dictionary.instance().decodeRom()

#  for i in range(0,0x100):
#    chary = Dictionary.instance().decodeByte(i)
#    print('{:02x} '.format(i) + chary)
#  sys.exit(0)

  basePath = Address.instance().basePath

  print('basePath: ' + basePath)

  # si tiene la cantidad correcta de parámetros
  if(len(argv) == 1):
    command = argv[0]

    if(command in ['-d', '--decode']):
      print('decoding ' + romPath + '...')

      # limpio el banks/
      RomSplitter.instance().clean()
      # creo el banks/
      RomSplitter.instance().split()

      # exporto lo gráficos (cada .bin en cuatro .png)
      RomSplitter.instance().exportGfx()
      # exporto los tilesets
      RomSplitter.instance().exportTilesets()
      RomSplitter.instance().exportFont()
      # exporto los cuatro spriteSheets 
      RomSplitter.instance().exportSpriteSheets()
      # exporto los spriteSheet de personajes
      RomSplitter.instance().exportSpriteSheetPersonajes()
      print('exportando sprite sheet del heroe')
      RomSplitter.instance().exportSpriteSheetHero()
      print('exportando spriteSheet de monstruos')
      RomSplitter.instance().exportSpriteSheetMonster()

      # exporto los personajes
      RomSplitter.instance().exportPersonajes()
      # exporto grupos de aparición de personajes
      RomSplitter.instance().exportGrupos3Personajes()


      # exporto el texto
      RomSplitter.instance().exportTexto()

      # exporto intro.txt
      RomSplitter.instance().exportIntro()
      # exporto la magia, items y weapons
      RomSplitter.instance().exportItems()


      print('exportando scripts...')
      RomSplitter.instance().exportScripts()

      # exporto todos los mapas
      RomSplitter.instance().exportMapas(exportPngFile=True)
#      RomSplitter.instance().exportMapas(exportPngFile=False)



      # exporto la música
#      RomSplitter.instance().exportSongs(exportLilypond=False)
      RomSplitter.instance().exportSongs(exportLilypond=True)

      # exporto las estadísticas del rom
      RomStats.instance().exportPng()

      # termino el script
      sys.exit(0)


    elif(command in ['-e', '--encode']):
      print('encoding ' + romPath + '...')


      # quemo el nroScript inicial (default 0x0003)
#      entraTopple = 0x0271
#      RomSplitter.instance().burnInitialScript(entraTopple)

      RomSplitter.instance().burnIntro()
      # quemando la magia
      RomSplitter.instance().burnItems('magic', basePath+'/magic.txt')
      # items
      RomSplitter.instance().burnItems('item', basePath+'/items.txt')
      # y weapons
      RomSplitter.instance().burnItems('weapon', basePath+'/weapons.txt')


      RomSplitter.instance().burnFont()
      RomSplitter.instance().burnTilesets()
      RomSplitter.instance().burnSpriteSheetPersonajes()

      print('quemando personajes...')
      # quemo los personajes en la rom
      RomSplitter.instance().burnPersonajes(basePath + '/personajes/personajes.txt')
      # quemo los grupos de aparición de personajes
      RomSplitter.instance().burnGrupos3Personajes(basePath + '/personajes/grupos3Personajes.txt')

      print('quemando mapas...')
#      RomSplitter.instance().burnMapas(basePath + '/mapas/mapas.txt')
      RomSplitter.instance().burnMapasTiled()


      print('quemando scripts...')
      RomSplitter.instance().burnScripts(basePath + '/scripts/scripts.txt')

      print('quemando songs...')
      # trata de mantener compatibilidad binaria con la rom original
#      RomSplitter.instance().burnSongs(filepath=basePath+'/audio/songs.txt', ignoreAddrs=False)
      # concatena todas las canciones, default para roms nuevas (no compatible con la original)
#      RomSplitter.instance().burnSongs(filepath=basePath+'/audio/songs.txt', ignoreAddrs=True)
      # compatible con la original (agrega los headers misteriosos sin uso)
      RomSplitter.instance().burnSongsHeaders(filepath=basePath+'/audio/songs.txt')

      # exporto la gbs rom con música
      RomSplitter.instance().exportGbsRom(basePath+'/audio.gb')

      # exporto nueva rom
      RomSplitter.instance().exportRom(basePath + '/newRom.gb')

      lang = Address.instance().language
      strLang = stockRomsLang[lang]
      stockPath = './stockRoms/' + strLang + '.gb'
      newPath = basePath + '/newRom.gb'
      print('comparando ' + stockPath + ' con ' + newPath)
      iguales = Util.instance().compareFiles(stockPath, newPath, 0x0000, 0x40000)
      print('roms iguales = ' + str(iguales))

      # la juego
#      RomSplitter.instance().testRom(basePath + '/newRom.gb', 'vba')
#      RomSplitter.instance().testRom(basePath + '/newRom.gb', 'mgba')

#      shutil.copyfile(basePath + '/newRom.gb', '/home/arathron/RetroPie/roms/gb/newRom.gb')
#      RomSplitter.instance().testRom('/home/arathron/RetroPie/roms/gb/newRom.gb', 'vba-m')


      # termino el script
      sys.exit(0)

    else:
      printHelp()
  else:
    printHelp()


  # limpio el banks/
#  RomSplitter.instance().clean()
  # creo el banks/
#  RomSplitter.instance().split()

  # decodifico el diccionario (compress)
#  Dictionary.instance().decodeRom()



  # exporto los tilesets
#  RomSplitter.instance().exportTilesets()

  # exporto los cuatro spriteSheets 
#  RomSplitter.instance().exportSpriteSheets()


  # exporto lo gráficos (cada .bin en cuatro .png)
#  RomSplitter.instance().exportGfx()
#  RomSplitter.instance().exportFont()
#  RomSplitter.instance().burnFont()
#  RomSplitter.instance().burnTilesets()

#  print('exportando sprite sheet del heroe')
  # exporto los spriteSheet de personajes
#  RomSplitter.instance().exportSpriteSheetPersonajes()
#  RomSplitter.instance().exportSpriteSheetHero()
#  RomSplitter.instance().exportSpriteSheetMonster()
#  RomSplitter.instance().burnSpriteSheetPersonajes()





  # exporto el texto
#  RomSplitter.instance().exportTexto()

  # para buscar patterns en la rom
#  RomSplitter.instance().pattern()
#  RomSplitter.instance().pattern2()

  # exporto la magia, items y weapons
#  RomSplitter.instance().exportItems()

#  RomSplitter.instance().burnItems('magic','./game/magic.txt')
#  RomSplitter.instance().burnItems('item','./game/items.txt')
#  RomSplitter.instance().burnItems('weapon','./game/weapons.txt')

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

#  script = RomSplitter.instance().scriptDecode(addr)
#  string, calls = script.iterarRecursivoRom(depth=0)
#  print('string: ' + string)


#  print('exportando scripts...')
#  RomSplitter.instance().exportScripts()
#  print('importando scripts...')
#  RomSplitter.instance().burnScripts('./en/scripts/scripts.txt')

  # exporto intro.txt
#  RomSplitter.instance().exportIntro()
#  RomSplitter.instance().burnIntro()
  # quemo el nroScript inicial (default 0x0003)
#  entraTopple = 0x0271
#  RomSplitter.instance().burnInitialScript(entraTopple)



#  bank06 = RomSplitter.instance().banks[0x06]
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

#  sheet = RomSplitter.instance().spriteSheets[1]
#  bloque.exportPngFile('./game/bloqu.png', sheet)

#  f = open('./game/bloquy.txt', 'w')
#  f.write(strLines + '\n')
#  f.close()

#  f = open('./game/bloquy.txt', 'r')
#  lines = f.readlines()
#  f.close()

  
#  bloque2 = BloqueExterior()
#  bloque2.decodeTxt(lines)
#  bloque2.decodeTxtEvents(lines)


#  array = bloque2.encodeRom(compress=4, disabledSpriteBytes=8)
#  strArray = Util.instance().strHexa(array)
#  print('strArray: ' + strArray)

#  lines = lines[3:]

#  bloque2.decodeTxtSprites(lines)

#  array = bloque2.encodeRomSprites(compress=3)
#  print('array = ' + str(array))
#  strArray = Util.instance().strHexa(array)
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
#  bank07 = RomSplitter.instance().banks[0x07]
#  array = bank07[0x3ee5:]
#  bloque._decodeRomSprites(array, 4)


#  bank07 = RomSplitter.instance().banks[0x07]
#  array = bank07[0x09f2:]
#  bloque3 = BloqueInterior()
#  bloque3.decodeRom(array)
  
#  lines = bloque3.encodeTxt()
#  strLines = '\n'.join(lines)

#  sheet = RomSplitter.instance().spriteSheets[2]
#  bloque3.exportPngFile('./game/inte.png',sheet)

#  f = open('./de/bloquyint2.txt', 'w')
#  f.write(strLines + '\n')
#  f.close()

#  f = open('./de/bloquyint2.txt', 'r')
#  lines = f.readlines()
#  f.close()

#  bloque4 = BloqueInterior()
#  bloque4.decodeTxt(lines)

#  array = bloque4.encodeRom()
#  strArray = Util.instance().strHexa(array)
#  print('strArray4: ' + strArray)



#  nroSpriteSheet=2
  # agarro el spriteSheet del nroSpriteSheet indicado
#  spriteSheet = SpriteSheet(16,8)
#  spriteSheet.readBank(nroSpriteSheet)


  # exporto todos los mapas
#  RomSplitter.instance().exportMapas(exportPngFile=False)
#  RomSplitter.instance().exportMapas(exportPngFile=True)



#  mapa = MapaExterior()

#  bank05 = RomSplitter.instance().banks[0x05]
#  array = bank05
#  disabledSpriteBytes = 8
#  mapa.decodeRom(array, disabledSpriteBytes)
#  sheet = RomSplitter.instance().spriteSheets[0]
#  mapa.exportPngFile('./game/mapy.png', sheet)

#  mapa = MapaInterior()
#  bank07 = RomSplitter.instance().banks[0x07]
#  array = bank07[0x0871:]
#  mapa.decodeRom(array)
#  sheet = RomSplitter.instance().spriteSheets[2]
#  mapa.exportPngFile('./game/mapu.png', sheet)




  # exporto los personajes
#  RomSplitter.instance().exportPersonajes()
#  RomSplitter.instance().burnPersonajes('./game/personajes/personajes.txt')

  # exporto grupos de 3 personajes
#  RomSplitter.instance().exportGrupos3Personajes()
#  RomSplitter.instance().burnGrupos3Personajes('./game/personajes/grupos3Personajes.txt')
 
  # exporto cosas raras personajes tiles
#  RomSplitter.instance().exportCosasRarasPersonajes()

  # exporto las personajes dobleTiles
#  RomSplitter.instance().exportPersonajesDobleTile()

  # exporto golpes
#  RomSplitter.instance().exportGolpes()

  # exporto monstruo grande dobleTiles
#  RomSplitter.instance().exportMonstruoGrandeDobleTile()


  modificarBateria = False
#  modificarBateria = True
  if(modificarBateria):
#    saveFile = '/home/arathron/RetroPie/roms/gb/newRom.sav'
    saveFile = '/home/arathron/newRom.sav'
    save = Save(saveFile)
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
#  RomSplitter.instance().exportSongs(exportLilypond=False)
#  RomSplitter.instance().exportSongs(exportLilypond=True)


  # trata de mantener compatibilidad binaria con la rom original
#  RomSplitter.instance().burnSongs(filepath='./game/audio/songs.txt')
  # concatena todas las canciones, default para roms nuevas (no compatible con la original)
#  RomSplitter.instance().burnSongs(filepath='./de/audio/songs.txt', ignoreAddrs=True)
  # compatible con la original (agrega los headers misteriosos sin uso)
#  RomSplitter.instance().burnSongsHeaders(filepath='./de/audio/songs.txt')


  # exporto las estadísticas del rom
#  RomStats.instance().exportPng()

#  RomSplitter.instance().exportGbsRom('./de/gbs.gb')
#  RomSplitter.instance().exportGbsRom('./game/gbs.gb')


#  nroTileset = 0
#  banco12 = RomSplitter.instance().banks[12]
#  array = banco12[0x1000*nroTileset:0x1000*(nroTileset+1)]
#  tileset.decodeRom(array)
#  tile = Tile()
#  tile.decodeRom(array)
#  tile.exportPngFile('./game/tile.png')
#  tile.importPngFile('./game/tile.png')
#  lines = tile.encodeTxt()
#  string = '\n'.join(lines)
#  print(string)



#  iguales = Util.instance().compareFiles('./stockRoms/gbs_de.gb', './de/gbs.gb', 0x0000, 0x8000)
#  print('gbs iguales = ' + str(iguales))


#  mapas = Mapas()
#  mapas.decodeRom()
#  RomSplitter.instance().exportMapas(exportPngFile=False)
#  RomSplitter.instance().exportMapas(exportPngFile=True)
#  RomSplitter.instance().burnMapas('./game/mapas/mapas.txt')
#  RomSplitter.instance().burnMapasTiled()


#  RomSplitter.instance().gameGenieHacks()


  # exporto a solarus
#  RomSplitter.instance().exportSolarus()




  # exporto nueva rom
#  RomSplitter.instance().exportRom(basePath + '/newRom.gb')

#  lang = Address.instance().language
#  strLang = stockRomsLang[lang]
#  stockPath = './stockRoms/' + strLang + '.gb'
#  newPath = basePath + '/newRom.gb'
#  print('comparando ' + stockPath + ' con ' + newPath)
#  iguales = Util.instance().compareFiles(stockPath, newPath, 0x0000, 0x40000)
#  print('roms iguales = ' + str(iguales))

#  iguales = Util.instance().compareFiles('/home/arathron/newRomOrig.sav', '/home/arathron/newRom.sav', 0x0000, 0x40000)
#  print('save iguales = ' + str(iguales))





  # la juego
#  RomSplitter.instance().testRom(basePath + '/newRom.gb', 'vba')
#  shutil.copyfile(basePath + '/newRom.gb', '/home/arathron/RetroPie/roms/gb/newRom.gb')
#  RomSplitter.instance().testRom('/home/arathron/RetroPie/roms/gb/newRom.gb', 'vba-m')
#  RomSplitter.instance().testRom(basePath + '/newRom.gb', 'vba-m2')
#  RomSplitter.instance().testRom(basePath + '/newRom.gb', 'mgba')
#  RomSplitter.instance().testRom('/home/arathron/newRom.gb', 'vba-m')


#  iguales = Util.instance().compareFiles('./roms/gbs.gb', './game/banks/bank_15/bank_15.bin', 0x4000, 0x40000)
#  iguales = Util.instance().compareFiles('./en/banks/bank_15/bank_15.bin','./fr/banks/bank_15/bank_15.bin', 0x0000, 0x4000)
#  print('los gbs iguales = ' + str(iguales))

  # la escucho
#  RomSplitter.instance().testRom('./de/gbs.gb', 'vba')



if __name__ == "__main__":
  main(sys.argv[1:])

