
import mystic.romSplitter
import mystic.romStats
import mystic.util
import mystic.spriteSheet

##########################################################
class Mapas:
  """ representa el listado de mapas """

  def __init__(self):
    # el listado de mapas
    self.mapas = []

  def decodeRom(self):

    bank08 = mystic.romSplitter.banks[0x08]

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x08, 0x0000, 0x0000 + 16*11 , (rr, gg, bb), 'header de los mapas')

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


      array = mystic.romSplitter.banks[mapBank]
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

#    array = mystic.romSplitter.banks[self.mapBank]
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

#    basePath = mystic.address.basePath
#    filepath = basePath + '/mapas/mapa_{:02}_{:02x}.png'.format(self.nroMapa, self.nroMapa)

    # agarro el spriteSheet del nroSpriteSheet indicado
    sheet = mystic.romSplitter.spriteSheets[self.nroSpriteSheet]

    self.mapa.exportPngFile(filepath, sheet)



  def exportJs(self, filepath):
#    print('export json: ' + filepath)

    # tipo de mapa
    TIPO_EXTERIOR = 0
    TIPO_INTERIOR = 1

    # la data del json
    data = {}

    data['property'] = {}
    data['property']['nroMapa'] = '{:02x}'.format(self.nroMapa)
    data['property']['nroSpriteSheet'] = '{:02x}'.format(self.nroSpriteSheet)
    data['property']['nose'] = '{:02x}'.format(self.nose)
    data['property']['spriteAddr'] = '{:04x}'.format(self.spriteAddr)
    data['property']['cantSprites'] = '{:02x}'.format(self.cantSprites)
    data['property']['mapBank'] = '{:02x}'.format(self.mapBank)
    data['property']['mapAddr'] = '{:04x}'.format(self.mapAddr)
    data['property']['noseAddr'] = '{:04x}'.format(self.noseAddr)

    data['property']['tipo'] = '{:02x}'.format(self.mapa.tipo)
    data['property']['compress'] = '{:02x}'.format(self.mapa.compress)
    data['property']['sizeY'] = '{:02x}'.format(self.mapa.sizeY)
    data['property']['sizeX'] = '{:02x}'.format(self.mapa.sizeX)

    # si el mapa es interior
    if(self.mapa.tipo == TIPO_INTERIOR):
      # exporto el headerLoco
      headerLoco = self.mapa.headerLoco
      strHeaderLoco = mystic.util.strHexa(headerLoco)
      data['property']['headerLoco'] = strHeaderLoco

    data['rooms'] = []

    idxX = 0
    idxY = 0
#    if(True):
    for bloque in self.mapa.bloques:
#      bloque = self.mapa.bloques[0]
      room = {}

      room['xy'] = ['{:02x}'.format(idxX), '{:02x}'.format(idxY)]
      idxX += 1
      if(idxX == self.mapa.sizeX):
        idxX = 0
        idxY += 1
      room['enabled'] = bloque.enabled 
      room['eventoEntrada'] = '{:04x}'.format(bloque.eventoEntrada)
      room['eventos'] = []
      for pos, nroScript in bloque.listEvents:
        evt = [ '{:02x}'.format(pos), '{:04x}'.format(nroScript) ]
        room['eventos'].append(evt)
      if(self.mapa.tipo == TIPO_INTERIOR):
        room['right_left_north_south'] = [ '{:02x}'.format(door) for door in [bloque.doorRight, bloque.doorLeft, bloque.doorNorth, bloque.doorSouth]]

      room['data'] = []

      for j in range(0, 8):
        renglon = []
        for i in range(0, 10):
          if(self.mapa.tipo == TIPO_EXTERIOR):
            spr = bloque.sprites[j][i]
          else:
            spr = bloque.getSprites()[j][i]

          renglon.append('{:02x}'.format(spr))
        room['data'].append(renglon)

      data['rooms'].append(room)

    import json
#    strMapa = json.dumps(data, indent=2)
#    strMapa = json.dumps(data)
#    print('strMapa: \n' + strMapa)

#    f = open(filepath, 'w', encoding="utf-8")
#    f.write(strMapa)
#    f.close()

    strMapa = json.dumps(data, indent=2)
#    strMapa = json.dumps(data)
    f = open(filepath, 'w', encoding="utf-8")
    f.write('mapa_{:02x} = \n'.format(self.nroMapa) + strMapa)
    f.close()



  def importJs(self, filepath):
#    print('import json: ' + filepath)

    # --- tipod de mapa
    TIPO_EXTERIOR = 0
    TIPO_INTERIOR = 1

    f = open(filepath, 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()
    # elimino el primer renglón (no es json)
    lines.pop(0)
    data = '\n'.join(lines)

    import json
    jsonMapa = json.loads(data)

    tipo = int(jsonMapa['property']['tipo'],16)
    if(tipo == TIPO_EXTERIOR):
      mapa = MapaExterior(self.nroMapa)
    else:
      mapa = MapaInterior(self.nroMapa)
      headerLoco = jsonMapa['property']['headerLoco']
      headerLoco = headerLoco.split()
      headerLoco = [int(num,16) for num in headerLoco]

    compress = int(jsonMapa['property']['compress'],16)
    sizeY = int(jsonMapa['property']['sizeY'],16)
    sizeX = int(jsonMapa['property']['sizeX'],16)



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
      lastRoom = jsonMapa['rooms'][sizeX*sizeY-1]
      listStrSprites = lastRoom['data']
      # recorro los sprites interiores del primer bloque
      for v in range(0,8):
        for u in range(0,10):
          nroSprite = int(listStrSprites[v][u],16)
          # si está dentro del bloque
          if(u>0 and v>0 and u<9 and v<7):
            # lo limpio
            nroSprite = 0x00
          spritesFondo[v][u] = nroSprite
      mapa.spritesFondo = spritesFondo


    k = 0
    for j in range(0, sizeY):
      for i in range(0, sizeX):
#        print('va por bloque: ' + str(i) + ', ' + str(j))
        bloque = bloques[j][i]
        bloque.mapa = mapa

        jsonRoom = jsonMapa['rooms'][k]

        # si es mapa exterior
        if(tipo == TIPO_EXTERIOR):

          bloque.enabled = jsonRoom['enabled']
          bloque.eventoEntrada = int(jsonRoom['eventoEntrada'], 16)

          subSprites = [ [0x00 for i in range(0,10)] for j in range(0,8) ]
          for v in range(0,8):
            for u in range(0,10):
#              subSprites[v][u] = listSprites[j*sizeX*10+i*10 + u]
              subSprites[v][u] = int(jsonRoom['data'][v][u],16)
          bloque.sprites = subSprites

        # sino, es tipo interior
        else:

          bloque.enabled = jsonRoom['enabled']
          bloque.eventoEntrada = int(jsonRoom['eventoEntrada'], 16)
          bloque.doorRight = int(jsonRoom['right_left_north_south'][0],16)
          bloque.doorLeft = int(jsonRoom['right_left_north_south'][1],16)
          bloque.doorNorth = int(jsonRoom['right_left_north_south'][2],16)
          bloque.doorSouth = int(jsonRoom['right_left_north_south'][3],16)


          subListSprites = []
          # recorro los sprites
          for v in range(0,8):
            for u in range(0,10):
              nroSprite = int(jsonRoom['data'][v][u],16)
              nroSpriteFondo = spritesFondo[v][u]
              # si cambió respecto al fondo
              if(nroSprite != nroSpriteFondo):
                pos = v*0x10 + u
                # lo agrego a la lista con su posición
                subListSprites.append( [pos, nroSprite] )
          # seteo la lista de sprites
          bloque.listSprites = subListSprites

        strEventos = jsonRoom['eventos']
#        print('strEventos: ' + str(strEventos))

        for pos, nroScript in jsonRoom['eventos']:
          # y lo agrego a la lista de sus eventos
          bloque.listEvents.append( [int(pos,16), int(nroScript,16)] )


        k += 1


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
      mystic.util.arrayToFile(array, './en/mapu_{:02x}.bin'.format(self.nroMapa))

      iguales = mystic.util.compareFiles('./en/banks/bank_{:02x}/bank_{:02x}.bin'.format(self.mapBank, self.mapBank), './en/mapu_{:02x}.bin'.format(self.nroMapa), self.mapAddr, len(array))
      print('mapa iguales = ' + str(iguales))



#      sheet = mystic.romSplitter.spriteSheets[2]
#      mapa.exportPngFile('./game/mapu.png', sheet)
#      bloque.exportPngFile('./game/mapu.png', sheet)
#      primerBloque.exportPngFile('./game/mapu.png', sheet)
      lines = mapa.encodeTxt()
      strTxt = '\n'.join(lines)

      f = open('./en/mapu_{:02x}.txt'.format(mapa.nroMapa), 'w', encoding="utf-8")
      f.write(strTxt)
      f.close()

    self.mapa = mapa


  def exportTiledXml(self, filepath):

    lines = []

    # --- tipod de mapa
    TIPO_EXTERIOR = 0
    TIPO_INTERIOR = 1

    tipo = self.mapa.tipo

    width  = self.mapa.sizeX*10
    height = self.mapa.sizeY*8

    # el id a ir incrementando
    iidd = 1

    import xml.etree.cElementTree as ET

    root = ET.Element("map", version='1.9', tiledversion="1.9.0", orientation="orthogonal", renderorder="right-down", width=str(width), height=str(height), tilewidth="16", tileheight="16", infinite="0", nextlayerid="4", nextobjectid="13")

    props = ET.SubElement(root, "properties")

    ET.SubElement(props, "property", name="nroMapa", value='{:02x}'.format(self.nroMapa))
    ET.SubElement(props, "property", name="nroSpriteSheet", value='{:02x}'.format(self.nroSpriteSheet))
    ET.SubElement(props, "property", name="nose", value='{:02x}'.format(self.nose))
    ET.SubElement(props, "property", name="spriteAddr", value='{:04x}'.format(self.spriteAddr))
    ET.SubElement(props, "property", name="cantSprites", value='{:02x}'.format(self.cantSprites))
    ET.SubElement(props, "property", name="mapBank", value='{:02x}'.format(self.mapBank))
    ET.SubElement(props, "property", name="mapAddr", value='{:04x}'.format(self.mapAddr))
    ET.SubElement(props, "property", name="noseAddr", value='{:04x}'.format(self.noseAddr))

    ET.SubElement(props, "property", name="tipo", value='{:02x}'.format(self.mapa.tipo))
    ET.SubElement(props, "property", name="compress", value='{:02x}'.format(self.mapa.compress))
    ET.SubElement(props, "property", name="sizeY", value='{:02x}'.format(self.mapa.sizeY))
    ET.SubElement(props, "property", name="sizeX", value='{:02x}'.format(self.mapa.sizeX))

    # si el mapa es interior
    if(self.mapa.tipo == TIPO_INTERIOR):
      # exporto el headerLoco
      headerLoco = self.mapa.headerLoco
      strHeaderLoco = mystic.util.strHexa(headerLoco)
      ET.SubElement(props, "property", name="headerLoco", value=strHeaderLoco)

    tileset = ET.SubElement(root, "tileset", firstgid="1", source='../spriteSheets/sheet_{:02x}.tsx'.format(self.nroSpriteSheet))
    layer1 = ET.SubElement(root, "layer", id=str(iidd), name="Tile Layer 1", width=str(width), height=str(height))
    iidd += 1
    data = ET.SubElement(layer1, "data", encoding="csv")

    renglones = []
    renglones.append("")
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
      renglones.append(renglon)

    renglones.append("")
    textData = '\n'.join(renglones)
    data.text = textData


    objgroup1 = ET.SubElement(root, "objectgroup", color="#005500", id=str(iidd), name="Rooms Layer")
    iidd += 1

    for j in range(0,self.mapa.sizeY):
      for i in range(0,self.mapa.sizeX):
        bloque = self.mapa.bloques[j*self.mapa.sizeX + i]
        enabled = 'true'
        if(bloque.enabled == False):
          enabled = 'false'
        eventoEntrada = '{:04x}'.format(bloque.eventoEntrada)


        obj = ET.SubElement(objgroup1, "object", {'id':str(iidd), 'class':"Room", 'x':str(i*10*16), 'y':str(j*8*16), 'width':"160", 'height':"127"})
        iidd += 1

        props = ET.SubElement(obj, "properties")
        prop = ET.SubElement(props, "property", name="enabled", type="bool", value=enabled)
        prop = ET.SubElement(props, "property", name="eventoEntrada", value=eventoEntrada)

        if(self.mapa.tipo == TIPO_INTERIOR):
          prop = ET.SubElement(props, "property", name="right,left,north,south", value="{:02x},{:02x},{:02x},{:02x}".format(bloque.doorRight,bloque.doorLeft,bloque.doorNorth,bloque.doorSouth))

    objgroup2 = ET.SubElement(root, "objectgroup", color="#ffaaff", id=str(iidd), name="Events Layer")
    iidd += 1

    for j in range(0,self.mapa.sizeY):
      for i in range(0,self.mapa.sizeX):
        bloque = self.mapa.bloques[j*self.mapa.sizeX + i]

        for evt in bloque.listEvents:
          pos = evt[0]
          nroScript = evt[1]

          posx = pos%0x10
          posy = pos//0x10

          evtx = i*10*16 + posx*16
          evty = j*8*16 + posy*16


          obj = ET.SubElement(objgroup2, "object", {'id':str(iidd), 'class':"Event", 'x':str(evtx), 'y':str(evty), 'width':"16", 'height':"16"})
          iidd += 1

          props = ET.SubElement(obj, "properties")
          prop = ET.SubElement(props, "property", name="nroScript", value='{:04x}'.format(nroScript))


    tree = ET.ElementTree(root)
#    printed_xml = tree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True)
    ET.indent(root, space=" ", level=0)
    tree.write(filepath, xml_declaration=True, encoding='utf-8')
#    print('ET: ' + str(ET.tostring(root, encoding='UTF-8')))



  def importTiledXml(self, filepath):

    # --- obtengo el mapa
    TIPO_EXTERIOR = 0
    TIPO_INTERIOR = 1

    f = open(filepath, 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()
    data = '\n'.join(lines)

    import xml.etree.ElementTree as ET
    myroot = ET.fromstring(data)

    for prop in myroot[0]:
      if(prop.attrib['name'] == 'tipo'):
        tipo = int(prop.attrib['value'],16)

    if(tipo == TIPO_EXTERIOR):
      mapa = MapaExterior(self.nroMapa)
    else:
      mapa = MapaInterior(self.nroMapa)

    for prop in myroot[0]:
      if(prop.attrib['name'] == 'tipo'):
        tipo = int(prop.attrib['value'],16)
      elif(prop.attrib['name'] == 'compress'):
        compress = int(prop.attrib['value'],16)
      elif(prop.attrib['name'] == 'sizeY'):
        sizeY = int(prop.attrib['value'],16)
      elif(prop.attrib['name'] == 'sizeX'):
        sizeX = int(prop.attrib['value'],16)
      elif(prop.attrib['name'] == 'headerLoco'):
        headerLoco = prop.attrib['value'].split()
        headerLoco = [int(num,16) for num in headerLoco]
#        print('headerLoco: ' + str(headerLoco))

    listSprites = []
    tiles = myroot[2][0].text
#    print('tiles: ' + tiles)
    tiles = tiles.strip().split(',')
#    print('tiles1: ' + str(tiles))
    tiles = [tile for tile in tiles if len(tile) > 0]
#    print('tiles2: ' + str(tiles))
    tiles = [int(tile)-1 for tile in tiles]
#    print('tiles3: ' + str(tiles))
    listSprites.extend(tiles)

    listBloques = []
    objectgroup = myroot[3]
#    print('objectgroup = ' + str(objectgroup))
    for obj in objectgroup:
      # obtengo sus coordenadas 
      bloqueX = int(obj.attrib['x'])//(16*10)
      bloqueY = int(obj.attrib['y'])//(16*8)
      # parseo sus propiedades
      for prop in obj[0]:
        if(prop.attrib['name'] == 'enabled'):
          enabled = prop.attrib['value']
#          print('enabled: ' + enabled)
          enabled = (enabled == "true")
        elif(prop.attrib['name'] == 'eventoEntrada'):
          eventoEntrada = prop.attrib['value']
#          print('eventoEntrada: ' + eventoEntrada)
          eventoEntrada = int(eventoEntrada, 16)
        elif(prop.attrib['name'] == 'right,left,north,south'):
          doors = prop.attrib['value']
          doors = doors.split(',')
          doors = [int(door,16) for door in doors]
#          print('doors: ' + str(doors))
      # lo agrego al listado de bloques según el tipo de mapa
      if(tipo == TIPO_EXTERIOR):
        listBloques.append( [enabled, eventoEntrada, bloqueX, bloqueY] )
      else:
        listBloques.append( [enabled, eventoEntrada, bloqueX, bloqueY, doors] )


    listEventos = []
    objectgroup = myroot[4]
#    print('objectgroup = ' + str(objectgroup))
    for obj in objectgroup:
      # obtengo sus coordenadas 
      evtX = int(obj.attrib['x'])//16
      evtY = int(obj.attrib['y'])//16
      nroScript = obj[0][0].attrib['value']
#      print('nroScript: ' + nroScript)
      nroScript = int(nroScript, 16)
      listEventos.append( [nroScript, evtX, evtY] )


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

          for enabled, eventoEntrada, bloqueX, bloqueY in listBloques:
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

          for enabled, eventoEntrada, bloqueX, bloqueY, doors in listBloques:
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

#        strHex = mystic.util.strHexa(subArray)
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
      mystic.util.arrayToFile(array, './en/mapu_{:02x}.bin'.format(self.nroMapa))

      iguales = mystic.util.compareFiles('./en/banks/bank_{:02x}/bank_{:02x}.bin'.format(self.mapBank, self.mapBank), './en/mapu_{:02x}.bin'.format(self.nroMapa), self.mapAddr, len(array))
      print('mapa iguales = ' + str(iguales))



#      sheet = mystic.romSplitter.spriteSheets[2]
#      mapa.exportPngFile('./game/mapu.png', sheet)
#      bloque.exportPngFile('./game/mapu.png', sheet)
#      primerBloque.exportPngFile('./game/mapu.png', sheet)
      lines = mapa.encodeTxt()
      strTxt = '\n'.join(lines)

      f = open('./en/mapu_{:02x}.txt'.format(mapa.nroMapa), 'w', encoding="utf-8")
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

      bloque = BloqueExterior()
      bloque.mapa = self
      bloque.decodeRom(array, compress)

      subArray = bloque.encodeRom(compress, disabledSpriteBytes)

      strArray = mystic.util.strHexa(subArray)
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
    """ el idx0 es el addr donde comienza el mapa en el banco (para armar los índices) """

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

    dibu = mystic.spriteSheet.SpriteSheet(10*self.sizeX,8*self.sizeY, sheet.nroSpriteSheet, 'png')
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
    dibu = mystic.spriteSheet.SpriteSheet(w,h,sheet.nroSpriteSheet, 'png')

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
    strHeaderLoco = mystic.util.strHexa(headerLoco)
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
    strSprites = mystic.util.strHexa(subArray)

    # salteo el bloque de sprites para la habitación
    array = array[len(subArray):]

    # para cada bloque
    for i in range(0, sizeX*sizeY):

#      print('----- bloque: ' + str(i))

      bloque = BloqueInterior()
      bloque.mapa = self
      bloque.decodeRom(array)

      subArray = bloque.encodeRom()

#      strArray = mystic.util.strHexa(subArray)
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

    strHeaderLoco = mystic.util.strHexa(self.headerLoco)
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
    headerLoco = mystic.util.hexaStr(strHeaderLoco)
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


    dibu = mystic.spriteSheet.SpriteSheet(10*self.sizeX,8*self.sizeY, sheet.nroSpriteSheet, 'png')
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
#    print('eventoEntrada: {:04x}'.format(self.eventoEntrada))

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
    dibu = mystic.spriteSheet.SpriteSheet(w,h,sheet.nroSpriteSheet, 'png')

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




