import mystic.tileset

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
      tile = mystic.tileset.Tile()
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
      tile = mystic.tileset.Tile()
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
