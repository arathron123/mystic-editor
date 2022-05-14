
import mystic.variables

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

    # indice en la tabla de estadísticas del personaje (velocidad de caminar, tipos de ataque, fuerza, etc)
    self.stats = 0x00

    # el offset a partir del cual se cargan los tiles en la vram
    self.vramTileOffset = 0x00

    # quantity of two vertical tiles (if it is invisible it shows 01, otherwise how many sprites for the personaje)
    self.cantDosTiles = 0x00
    # offset to where the tiles are located (global address 0x20000 + offsetBank8) (mod 0x4000 to find the bank number)
    self.offsetBank8 = 0x0000

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

    # the animation dictionary
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
    self.stats     = subArray[1] # 0x0b
    self.vramTileOffset = subArray[2] # 0x40   

    self.cantDosTiles = subArray[3] # 0x08   (01,02,04,06,08,0c,0a)
    offsetBank8_1 = subArray[4] 
    offsetBank8_2 = subArray[5]
    self.offsetBank8 = offsetBank8_2*0x100 + offsetBank8_1

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
    array.append(self.stats)
    array.append(self.vramTileOffset)

    array.append(self.cantDosTiles)
    array.append(self.offsetBank8%0x100)
    array.append(self.offsetBank8//0x100)

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

    lines.append('\n------------ personaje: ' + mystic.variables.personajes[self.nroPersonaje] )
    lines.append('nroPersonaje:   {:02x}'.format(self.nroPersonaje))
    lines.append('amistad:        {:02x}'.format(self.amistad))

    lines.append('stats:          {:02x}'.format(self.stats))
    lines.append('vramTileOffset: {:02x}'.format(self.vramTileOffset))

    lines.append('cantDosTiles:   {:02x}'.format(self.cantDosTiles))
    lines.append('offsetBank8:    {:04x}'.format(self.offsetBank8))

    lines.append('addrRaro:       {:04x}'.format(self.addrRaro))
    lines.append('addrDosTiles:   {:04x}'.format(self.addrDosTiles))

    lines.append('patasSepa:      {:02x}'.format(self.patasSepa))
    lines.append('muevePatas:     {:02x}'.format(self.muevePatas))
    lines.append('nose7:          {:02x}'.format(self.nose7))
    lines.append('nose8:          {:02x}'.format(self.nose8))
    lines.append('nose9:          {:02x}'.format(self.nose9))
    lines.append('nose10:         {:02x}'.format(self.nose10))

    lines.append('nose11:         {:02x}'.format(self.nose11))
    lines.append('nose12:         {:02x}'.format(self.nose12))
    lines.append('nose13:         {:02x}'.format(self.nose13))
    lines.append('nose14:         {:02x}'.format(self.nose14))

    lines.append('nroScript:      {:04x}'.format(self.nroScript))
    lines.append('itemTesoro:     {:04x}'.format(self.itemTesoro))

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
      elif(line.startswith('stats:')):
        strStats = line[6:].strip()
        self.stats = int(strStats,16)
      elif(line.startswith('vramTileOffset:')):
        strVramTileOffset = line[15:].strip()
        self.vramTileOffset = int(strVramTileOffset,16)
      elif(line.startswith('cantDosTiles:')):
        strCantDosTiles = line[13:].strip()
        self.cantDosTiles = int(strCantDosTiles,16)
      elif(line.startswith('offsetBank8:')):
        strOffsetBank8 = line[12:].strip()
        self.offsetBank8 = int(strOffsetBank8,16)
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

    string = 'amist={:02x} stats={:02x} vramTileOffset={:02x} cantTiles={:02x} offsetBank8={:04x} {:04x} addrDosTiles={:04x} patas={:02x},{:02x} {:02x} {:02x} {:02x} {:02x}  {:02x} {:02x} {:02x} {:02x}  script={:04x} item={:04x}'.format(self.amistad, self.stats, self.vramTileOffset, self.cantDosTiles, self.offsetBank8, self.addrRaro, self.addrDosTiles, self.patasSepa, self.muevePatas, self.nose7, self.nose8, self.nose9, self.nose10, self.nose11, self.nose12, self.nose13, self.nose14, self.nroScript, self.itemTesoro)

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
    mystic.romStats.appendDato(0x03, 0x3142, vaPorAddr, (rr, gg, bb), 'grupos personajes')

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
    mystic.romStats.appendDato(0x03, vaPorAddr, addr - 0x4000, (rr, gg, bb), 'aparición personajes')

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
    strHex = mystic.util.strHexa(addrs)
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
    lines.append('position_xy: ' + mystic.util.strHexa(self.extras))
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
      elif(line.startswith('position_xy:')):
        strExts = line[12:].strip()
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
    strExtras = mystic.util.strHexa(self.extras)
    string = 'nro{:03} addr {:04x} | minmax: {:02x} {:02x} values: {:02x} {:02x} {:02x} {:02x} position_xy: '.format(self.nro, self.addr, self.valMin, self.valMax, self.values[0], self.values[1], self.values[2], self.values[3]) + strExtras + ' cierre: {:02x} {:02x}'.format(self.cierre[0], self.cierre[1])
    return string

##########################################################
class PersonajeStats:
  """ representa los stats de un personaje """

  def __init__(self, nroStats):
    self.nroStats = nroStats

    # the speed (0x01 is the faster, the higher the slower)
    self.speedSleep = 0x00

    self.nose1    = 0x00
    self.nose2    = 0x00
    self.nose3    = 0x00
    self.nose4    = 0x00
    self.maybeDP  = 0x00
    self.maybeAP  = 0x00
    self.nose5    = 0x00
    self.nose6    = 0x00
    self.projectile = 0x00
    self.nose7    = 0x00
    self.nose8    = 0x00
    self.maybeExp = 0x00
    self.maybeGP  = 0x00

  def decodeRom(self, subArray):

    self.speedSleep = subArray[0] 
    self.nose1    = subArray[1]
    self.nose2    = subArray[2]
    self.nose3    = subArray[3]
    self.nose4    = subArray[4]
    self.maybeDP  = subArray[5]
    self.maybeAP  = subArray[6]
    self.nose5    = subArray[7]
    self.nose6    = subArray[8]
    self.projectile = subArray[9]
    self.nose7    = subArray[10]
    self.nose8    = subArray[11]
    self.maybeExp = subArray[12]
    self.maybeGP  = subArray[13]

  def encodeRom(self):
    array = []

    array.append(self.speedSleep)
    array.append(self.nose1)
    array.append(self.nose2)
    array.append(self.nose3)
    array.append(self.nose4)
    array.append(self.maybeDP)
    array.append(self.maybeAP)
    array.append(self.nose5)
    array.append(self.nose6)
    array.append(self.projectile)
    array.append(self.nose7)
    array.append(self.nose8)
    array.append(self.maybeExp)
    array.append(self.maybeGP)

    return array
 
  def encodeTxt(self, personajes):
    lines = []

    # for all the personajes that use this stat
    pers = [per for per in personajes if per.stats == self.nroStats]
    # get all their names
    names = []
    for per in pers:
      name = mystic.variables.personajes[per.nroPersonaje]
      names.append(name)

#    lines.append('\n------------ stats: ' + mystic.variables.personajes[self.nroStats] + '?' )
    lines.append('\n------------ stats: ' + str(names) )

    lines.append('nroStats:     {:02x}'.format(self.nroStats))
    lines.append('speedSleep:   {:02x}'.format(self.speedSleep))
    lines.append('nose1:        {:02x}'.format(self.nose1))
    lines.append('nose2:        {:02x}'.format(self.nose2))
    lines.append('nose3:        {:02x}'.format(self.nose3))
    lines.append('nose4:        {:02x}'.format(self.nose4))
    lines.append('maybeDP:      {:02x}'.format(self.maybeDP))
    lines.append('maybeAP:      {:02x}'.format(self.maybeAP))
    lines.append('nose5:        {:02x}'.format(self.nose5))
    lines.append('nose6:        {:02x}'.format(self.nose6))
    lines.append('projectile:   {:02x}'.format(self.projectile))
    lines.append('nose7:        {:02x}'.format(self.nose7))
    lines.append('nose8:        {:02x}'.format(self.nose8))
    lines.append('maybeExp:     {:02x}'.format(self.maybeExp))
    lines.append('maybeGP:      {:02x}'.format(self.maybeGP))

    return lines

  def decodeTxt(self, lines):
    for line in lines:
#      print('lineee: ' + line)
      if(line.startswith('nroStats:')):
        strNroStats = line[len('nroStats:'):].strip()
        self.nroStats = int(strNroStats,16)
      elif(line.startswith('speedSleep:')):
        strSpeed = line[len('speedSleep:'):].strip()
        self.speedSleep = int(strSpeed,16)
      elif(line.startswith('nose1:')):
        strNose1 = line[len('nose1:'):].strip()
        self.nose1 = int(strNose1,16)
      elif(line.startswith('nose2:')):
        strNose2 = line[len('nose2:'):].strip()
        self.nose2 = int(strNose2,16)
      elif(line.startswith('nose3:')):
        strNose3 = line[len('nose3:'):].strip()
        self.nose3 = int(strNose3,16)
      elif(line.startswith('nose4:')):
        strNose4 = line[len('nose4:'):].strip()
        self.nose4 = int(strNose4,16)
      elif(line.startswith('maybeDP:')):
        strMaybeDP = line[len('maybeDP:'):].strip()
        self.maybeDP = int(strMaybeDP,16)
      elif(line.startswith('maybeAP:')):
        strMaybeAP = line[len('maybeAP:'):].strip()
        self.maybeAP = int(strMaybeAP,16)
      elif(line.startswith('nose5:')):
        strNose5 = line[len('nose5:'):].strip()
        self.nose5 = int(strNose5,16)
      elif(line.startswith('nose6:')):
        strNose6 = line[len('nose6:'):].strip()
        self.nose6 = int(strNose6,16)
      elif(line.startswith('projectile:')):
        strProjectile = line[len('projectile:'):].strip()
        self.projectile = int(strProjectile,16)
      elif(line.startswith('nose7:')):
        strNose7 = line[len('nose7:'):].strip()
        self.nose7 = int(strNose7,16)
      elif(line.startswith('nose8:')):
        strNose8 = line[len('nose8:'):].strip()
        self.nose8 = int(strNose8,16)
      elif(line.startswith('maybeExp:')):
        strMaybeExp = line[len('maybeExp:'):].strip()
        self.maybeExp = int(strMaybeExp,16)
      elif(line.startswith('maybeGP:')):
        strMaybeGP = line[len('maybeGP:'):].strip()
        self.maybeGP = int(strMaybeGP,16)

  def __str__(self):
    string = ' speed={:02x} {:02x} {:02x} {:02x} {:02x} DP?={:02x} AP?={:02x} {:02x} {:02x} {:02x} {:02x} {:02x} Exp?={:02x} GP?={:02x}'.format(self.speedSleep, self.nose1, self.nose2, self.nose3, self.nose4, self.maybeDP, self.maybeAP, self.nose5, self.nose6, self.projectile, self.nose7, self.nose8, self.maybeExp, self.maybeGP)

    return string + ' ' + mystic.variables.personajes[self.nroStats] + '?'



