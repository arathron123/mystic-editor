# pip3 install pypng
import png


colorPaletteGrayscale = [ (0x00, 0x00, 0x00),(0x55, 0x55, 0x55),(0xaa, 0xaa, 0xaa),(0xff, 0xff, 0xff) ]
colorPalettePyxel = [ (0, 0, 0),(79, 79, 79),(179, 179, 179),(255, 255, 255) ]
colorPaletteYellow = [ (0x0f, 0x38, 0x0f),(0x30, 0x62, 0x30),(0x8b, 0xac, 0x0f),(0x9b, 0xbc, 0x0f) ]
colorPaletteGreen = [ (0x3e, 0x49, 0x43),(0x55, 0x5a, 0x56),(0x5e, 0x78, 0x5d),(0x84, 0xd0, 0x7d) ]
#colorPalette = colorPaletteGrayscale
colorPalette = colorPalettePyxel
#colorPalette = colorPaletteYellow
#colorPalette = colorPaletteGreen


##########################################################
class Tile:
  """ representa un tile de 8x8 """

  def __init__(self):

#    self.tileData = [ [0x03 for i in range(0,8) ] for j in range(0,8) ]
    self.tileData = [ 0x03 for i in range(0,8*8) ]


  def flipX(self):
    """ espeja el tile horizontalmente """

    newData = []
    # por cada renglón
    for j in range(0,8):

      # por cada columna
      for i in range(0,8):

        color =  self.tileData[(7-i) + 8*j]
        newData.append(color)

    self.tileData = newData

 
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

    tileData = self.encodePng()

    # creo el array
    s = []

    for j in range(8):
      row = []
      for i in range(8):
#        color = 255 - tileData[i+8*j]*255//3
        color = 3 - tileData[i+8*j]
#        print('color: ' + str(color))
        row.append(color)
      s.append(row)


    # convierto la imagen en RGB
    fullS = []
    for row in s:
      for color in row:

        fullCol = colorPalette[color]
#        fullCol = [color, color, color]
#        fullCol = [color, 0,0]
#        fullCol = [0, color,0]
        fullS.extend(fullCol)

#    w = png.Writer(8, 8, greyscale=True, bitdepth=2)
    w = png.Writer(8, 8, greyscale=False)
#    w = png.Writer(8, 8)
    f = open(filepath, 'wb')
#    w.write(f, s)
    w.write_array(f, fullS)
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

#          color = 255 - (2*b1 + b0)*255//3
          color = 3 - (2*b1 + b0)

#          print('(i,j) = ' + str(i) + ', ' + str(j))
#          print('color = ' + str(color))
#          s[j][i] = color

          s[8*v+j][8*u+i] = color

      k += 1


    # convierto la imagen en RGB
    fullS = []
    for row in s:
      for color in row:

        fullCol = colorPalette[color]
#        fullCol = [color, color, color]
#        fullCol = [color, 0,0]
#        fullCol = [0, color,0]
        fullS.extend(fullCol)


    f = open(filepath, 'wb')
#    w = png.Writer(8*self.w, 8*self.h, greyscale=True, bitdepth=2)
    w = png.Writer(8*self.w, 8*self.h, greyscale=False)
#    w = png.Writer(8*self.w, 8*self.h)
#    w.write(f, s)
    w.write_array(f, fullS)
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
      k = 0
      for val in row:
        # if it is the green info of RGB
        if( (k%3) == 1):
          # set the grayscale value to it
          s[j][i] = val
          i += 1
        k += 1
      j += 1
      i = 0

    # I use green to detect the grayscale level
    greens = [val[1] for val in colorPalette]

    for v in range(0, self.h):
      for u in range(0, self.w):

        tileData = []
        # para cada renglón
        for j in range(0,8):
          # para cada bit (columna)
          for i in range(0,8):

            val = 3 - greens.index(s[8*v+j][8*u+i])
#            print('val1: ' + str(val))
#            val = (255 - s[8*v+j][8*u+i])*3//255
#            print('val {:02x}'.format(val))

            tileData.append(val)
#          print('\n')

        tile = Tile()
        tile.tileData = tileData
        self.tiles.append(tile)

  def exportTiledXml(self, filepath):
    import xml.etree.cElementTree as ET

    paths = filepath.split('/')
    name = paths[len(paths)-1]
    name = name[:len(name)-4]

    tilecount = len(self.tiles)
    w = 0x10
    h = len(self.tiles) // 0x10

    root = ET.Element("tileset", version='1.9', tiledversion="1.9.0", name=name, tilewidth="8", tileheight="8", tilecount=str(tilecount), columns="16")
    img = ET.SubElement(root, "image", source=name+".png", width=str(w*8), height=str(h*8))

    tree = ET.ElementTree(root)
    ET.indent(root, space=" ", level=0)
    tree.write(filepath, xml_declaration=True, encoding='utf-8')


##########################################################
class DosTiles:
  """ representa una estructura de dosTiles """

  def __init__(self, addr):
    # el addr del dosTiles
    self.addr = addr

    # the attribute (10 = normal, 30 = espejo, ???)
    self.attr = None
    # the first tile
    self.tile1 = None
    # the second tile
    self.tile2 = None

  def decodeRom(self, subArray):
    self.attr  = subArray[0]
    self.tile1 = subArray[1]
    self.tile2 = subArray[2]


  def encodeRom(self):
    array = []

    array.append(self.attr)
    array.append(self.tile1)
    array.append(self.tile2)

    return array
 

  def encodeTxt(self):
    lines = []

    string = '(attr,tile1,tile2) = ({:02x}, {:02x}, {:02x})   # addr = {:04x}'.format(self.attr, self.tile1, self.tile2, self.addr)
    lines.append(string)

    return lines


  def decodeTxt(self, lines):
    line = lines[0]
   
    self.attr  = int(line[22:24],16)
    self.tile1 = int(line[26:28],16)
    self.tile2 = int(line[30:32],16)

  def __str__(self):
    string = '(attr,tile1,tile2) = ({:02x}, {:02x}, {:02x})   # addr = {:04x}'.format(self.attr, self.tile1, self.tile2, self.addr)
    return string





