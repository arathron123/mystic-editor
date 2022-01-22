import mystic.tileset

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

    tileset = mystic.romSplitter.tilesets[self.nroTileset]
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
    dibu = mystic.tileset.Tileset(2*w,2*h)

    # agarro el tileset para colorear
    tileset = mystic.romSplitter.tilesets[self.nroTileset]

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

    f = open(filepath, 'w', encoding="utf-8")
    f.write(strTxt)
    f.close()



