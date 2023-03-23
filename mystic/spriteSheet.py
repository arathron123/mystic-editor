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
#    tileset = mystic.romSplitter.tilesets[self.nroTileset]
    tileset = mystic.romSplitter.tilesets
    baseTile = mystic.address.baseSubtile[self.nroTileset]

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
          tiles[2*w*v + u] = tileset.tiles[baseTile + sprite.tiles[k]]


    # seteo los tiles en el orden adecuado    
    dibu.tiles = tiles

    # y exporto el .png
    dibu.exportPngFile(filepath)

  def exportTiledOld(self, filepath):
    """ deprecated, see exportTiledXmlTsx """
    lines = []

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<tileset version="1.9" tiledversion="1.9.0" name="' + self.name + '" tilewidth="16" tileheight="16" tilecount="128" columns="16">')
    lines.append(' <image source="sheet_{:02x}.png" width="256" height="128"/>'.format(self.nroSpriteSheet))
#    lines.append(' <tile id="125" type="Otracosa"/>')
#    lines.append(' <tile id="126" type="Evento"/>')
    lines.append('</tileset>')

    strTxt = '\n'.join(lines)

    f = open(filepath, 'w', encoding="utf-8")
    f.write(strTxt)
    f.close()


  def exportTiledXmlTsxOld(self, filepath):
    """ deprecated, now it is exported as a metatile map, see exportTiledXml """

    import xml.etree.cElementTree as ET

    root = ET.Element("tileset", version='1.9', tiledversion="1.9.0", name=self.name, tilewidth="16", tileheight="16", tilecount="128", columns="16")

    img = ET.SubElement(root, "image", source="sheet_{:02x}.png".format(self.nroSpriteSheet), width="256", height="128")


    tree = ET.ElementTree(root)
    ET.indent(root, space=" ", level=0)
    tree.write(filepath, xml_declaration=True, encoding='utf-8')
#    print('ET: ' + str(ET.tostring(root, encoding='UTF-8')))




  def exportTiledXml(self, filepath):

    width = self.w*2
    height = self.h*2
    # el id a ir incrementando
    iidd = 1

    import xml.etree.cElementTree as ET

    root = ET.Element("map", version='1.9', tiledversion="1.9.0", orientation="orthogonal", renderorder="right-down", width=str(width), height=str(height), tilewidth="8", tileheight="8", infinite="0", nextlayerid="3", nextobjectid="14")

#    tileset = ET.SubElement(root, "tileset", firstgid="1", source='../tilesets/tilesets.tsx')
    tileset = ET.SubElement(root, "tileset", firstgid="1", source='../tilesets/sub_tileset_{:02x}.tsx'.format(self.nroTileset))

    layer1 = ET.SubElement(root, "layer", id=str(iidd), name="Tile Layer 1", width=str(width), height=str(height))
    iidd += 1
    data = ET.SubElement(layer1, "data", encoding="csv")

    # where the subtilesets begin respective to the big tileset      xxxxxx
    baseTile = mystic.address.baseSubtile[self.nroTileset]

    renglones = []
    renglones.append("")
    for j in range(0,height):
      renglon = ''
      for i in range(0,width):
#        renglon += '0'
        spritex = i//2
        spritey = j//2

        if(spritey*self.w + spritex < len(self.sprites)):
          sprite = self.sprites[spritey*self.w + spritex]
#          nroTile = baseTile + sprite.tiles[(j%2)*2+(i%2)]
          # don't use the baseTile for using subtiles in tiled
          nroTile = sprite.tiles[(j%2)*2+(i%2)]
          renglon += str(nroTile+1)
        else:
          sprite = None
          nroTile = None
          renglon += ''


        if(i != width-1 or j != height-1):
          renglon += ','
      renglones.append(renglon)

    renglones.append("")
    textData = '\n'.join(renglones)
    data.text = textData


    objgroup1 = ET.SubElement(root, "objectgroup", color="#550000", id=str(iidd), name="Properties Layer", visible="0")
    iidd += 1

    for j in range(0,self.h):
      for i in range(0,self.w):
        if(j*self.w+i < len(self.sprites)):
          sprite = self.sprites[j*self.w + i]
          bloqueo = '{:02x}'.format(sprite.bloqueo)
          tipo = '{:02x}'.format(sprite.tipo)

          obj = ET.SubElement(objgroup1, "object", {'id':str(iidd), 'class':"Prop", 'x':str(i*2*8), 'y':str(j*2*8), 'width':"16", 'height':"16"})
          iidd += 1

          props = ET.SubElement(obj, "properties")
          prop = ET.SubElement(props, "property", name="bloqueo", value=bloqueo)
          prop = ET.SubElement(props, "property", name="tipo", value=tipo)


    tree = ET.ElementTree(root)
    ET.indent(root, space=" ", level=0)
    tree.write(filepath + '.tmx', xml_declaration=True, encoding='utf-8')
#    print('ET: ' + str(ET.tostring(root, encoding='UTF-8')))




    # y ahora exporto el .tsx para utilizarlo como tileset de los mapas
    root = ET.Element("tileset", version='1.9', tiledversion="1.9.0", name=self.name, tilewidth="16", tileheight="16", tilecount="128", columns="16")

    img = ET.SubElement(root, "image", source="sheet_{:02x}.tmx".format(self.nroSpriteSheet), width="256", height="128")


    tree = ET.ElementTree(root)
    ET.indent(root, space=" ", level=0)
    tree.write(filepath + '.tsx', xml_declaration=True, encoding='utf-8')
#    print('ET: ' + str(ET.tostring(root, encoding='UTF-8')))

  def importTiledXml(self, filepath):

    f = open(filepath, 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()
    data = '\n'.join(lines)

    import xml.etree.ElementTree as ET
    myroot = ET.fromstring(data)

    tileData = []

    # where the subtilesets begin respective to the big tileset
    baseTile = mystic.address.baseSubtile[self.nroTileset]

    tiles = myroot[1][0].text
#    print('tiles: ' + tiles)
#    tiles = tiles.strip().split(',')
    lines = tiles.strip().split('\n\n')
    for line in lines:
      tiles = line.strip().split(',')
#      print('tiles: ' + str(tiles))

      renglon = []

      for tile in tiles:
        numTile = -1
        if(len(tile)>0):
#          numTile = int(tile,10)-1 - baseTile
          # don't use the baseTile for using subtiles in tiled
          numTile = int(tile,10)-1 
        renglon.append(numTile)

      tileData.append(renglon)

       
    k = 0
    objectgroup = myroot[2]
    for obj in objectgroup:

#      print('obj: ' + str(obj))

      # parseo sus propiedades
      for prop in obj[0]:
#        print('prop: ' + str(prop))
        if(prop.attrib['name'] == 'bloqueo'):
          bloqueo = prop.attrib['value']
          bloqueo = int(bloqueo,16)
        elif(prop.attrib['name'] == 'tipo'):
          tipo = prop.attrib['value']
          tipo = int(tipo,16)
 

      sprite = mystic.spriteSheet.Sprite(self.nroTileset)

      x = k%16
      y = k//16

      tile1 = tileData[2*y][2*x]
      tile2 = tileData[2*y][2*x+1]
      tile3 = tileData[2*y+1][2*x]
      tile4 = tileData[2*y+1][2*x+1]
      sprite.tiles = [tile1,tile2,tile3,tile4]

      sprite.bloqueo = bloqueo
      sprite.tipo = tipo

      self.sprites.append(sprite)

      k += 1


  def exportJs(self, filepath):

    # la data del json
    data = {}

    data['nroSpriteSheet'] = '{:02x}'.format(self.nroSpriteSheet)
    data['nroTileset'] = '{:02x}'.format(self.nroTileset)

    data['sprites'] = []

    for sprite in self.sprites:
      jsonSprite = {}
      jsonSprite['tiles'] = ['{:02x}'.format(sprite.tiles[0]), '{:02x}'.format(sprite.tiles[1]), '{:02x}'.format(sprite.tiles[2]), '{:02x}'.format(sprite.tiles[3])]
      jsonSprite['bloqueo'] = '{:02x}'.format(sprite.bloqueo)
      jsonSprite['tipo'] = '{:02x}'.format(sprite.tipo)

      data['sprites'].append(jsonSprite)


    import json
    strSheet = json.dumps(data, indent=2)
#    strSheet = json.dumps(data)
#    print('strSheet: \n' + strMapa)

#    f = open(filepath, 'w', encoding="utf-8")
#    f.write(strSheet)
#    f.close()

    strSheet = json.dumps(data, indent=2)
#    strSheet = json.dumps(data)
    f = open(filepath, 'w', encoding="utf-8")
    f.write('sheet_{:02x} = \n'.format(self.nroSpriteSheet) + strSheet)
    f.close()

  def exportPyxelEdit(self, filepath):

    import os
    # si el directorio no existía
    if not os.path.exists(filepath):
      # lo creo
      os.makedirs(filepath)

    tileset = mystic.romSplitter.tilesets
 
    nroTileset = 0
    baseTile = mystic.address.baseSubtile[nroTileset]
    for i in range(0,8*8):
      tile = tileset.tiles[baseTile + i]
      tile.exportPngFile(filepath + '/tile{:1}.png'.format(i))

    docData = {}

    docData['tileset'] = { 'tileWidth' : 8, 'tileHeight' : 8, 'tilesWide' : 8, 'numTiles' : 16 }
    docData['palette'] = {}
    docData['palette']['numColors'] = 32
    docData['palette']['colors'] = {"0":"ff1e2936",
"1":"ff0e354b",
"2":"ff004c73",
"3":"ff1279ae",
"4":"ff31a2ee",
"5":"ff88c7ea",
"6":"ff1b342b",
"7":"ff1e5537",
"8":"ff45911a",
"9":"ff79bf1d",
"10":"ffbede2c",
"11":"ff451212",
"12":"ff711f1f",
"13":"ffb82535",
"14":"ffdc5173",
"15":"ffff9fb6",
"16":"ff271443",
"17":"ff691c63",
"18":"ffad51b9",
"19":"ffb898d0",
"20":"ff353024",
"21":"ff594228",
"22":"ff8c5c4d",
"23":"ffd08070",
"24":"ffe59131",
"25":"fff7b072",
"26":"fffcd78e",
"27":"ff000000",
#"27":"000000",
"28":"ff212121",
"29":"ff4f4f4f",
"30":"ffb3b3b3",
"31":"ffffffff"
#"31":"ffffff"
}

    docData['canvas'] = {}
    docData['canvas']['tileWidth'] = 8
    docData['canvas']['tileHeight'] = 8
    docData['canvas']['width'] = 48
    docData['canvas']['height'] = 32
    docData['canvas']['numLayers'] = 1
    docData['canvas']['layers'] = {}
    docData['canvas']['layers']['0'] = {"name":"Layer 0","hidden":False,"tileRefs":{"0":{"index":0,"flipX":False,"rot":0},"1":{"index":1,"flipX":False,"rot":0},"2":{"index":2,"flipX":False,"rot":0},"4":{"index":0,"flipX":False,"rot":0},"5":{"index":1,"flipX":True,"rot":3},"22":{"index":0,"flipX":False,"rot":0},"18":{"index":0,"flipX":False,"rot":0},"11":{"index":1,"flipX":False,"rot":0},"20":{"index":13,"flipX":False,"rot":0},"13":{"index":14,"flipX":False,"rot":0},"15":{"index":15,"flipX":False,"rot":0}}}

    import json
    strSheet = json.dumps(docData, indent=2)
    f = open(filepath + '/docData.json', 'w', encoding="utf-8")
#    f.write('sheet_{:02x} = \n'.format(self.nroSpriteSheet) + strSheet)
    f.write(strSheet)
    f.close()


