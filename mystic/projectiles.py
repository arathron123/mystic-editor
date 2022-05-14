import os

import mystic.variables


##########################################################
class Projectiles:
  """ representa la colección de projectiles y explosiones """

  def __init__(self):
    self.projectiles = []


  def decodeRom(self, bank):

    basePath = mystic.address.basePath
    path = basePath + '/projectiles'

    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    vaPorAddr = 0x0479
    projsAddr = vaPorAddr

    string = ''
    self.projectiles = []
    for i in range(0,40):
      subArray = bank[0x0479 + 16*i : 0x0479 + 16*(i+1)]
#      strHexa = mystic.util.strHexa(subArray)
#      print('addr: {:04x}'.format(0x0479+16*i))

      proj = mystic.projectiles.Projectile(i)
      # lo decodifico
      proj.decodeRom(subArray)

      self.projectiles.append(proj)

      lines = proj.encodeTxt()
      subString = '\n'.join(lines)
      string += subString

    f = open(path + '/01_projectiles.txt', 'w', encoding="utf-8")
    f.write(string)
    f.close()

    length = 16*len(self.projectiles)
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x09, projsAddr, projsAddr+length, (rr, gg, bb), 'projectiles')

    vaPorAddr += length

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    f = open(path + '/02_projsSortTiles.txt', 'w', encoding="utf-8")
    addressesSortTiles = [proj.addrSortTiles for proj in self.projectiles]

    projSortTilesAddr = vaPorAddr

    prevAddrSortTile = vaPorAddr
    arrayTiles = []
    primero = True
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
          f.write('--- sortTiles: {:04x} '.format(prevAddrSortTile) + stringTile + '\n' + strHexa + '\n')

          arrayTiles = []
        prevAddrSortTile = vaPorAddr

      arrayTiles.append(bank[vaPorAddr - 0x4000])
      vaPorAddr += 1

 
    stringTile = ''
    if(vaPorAddr+0x4000 in addressesSortTiles):
      idx = addressesSortTiles.index(prevAddrSortTiles+0x4000)
      stringTile = mystic.variables.bosses[idx] + ' sort-tiles'
    strHexa = mystic.util.strHexa(arrayTiles)
    f.write('--- sortTiles: {:04x} '.format(prevAddrSortTile) + stringTile + '\n' + strHexa + '\n')

    f.close()

    length = vaPorAddr - projSortTilesAddr
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x09, projSortTilesAddr, projSortTilesAddr+length, (rr, gg, bb), 'projectiles sort-tiles')



    # creo la lista de addresses de animaciones
    animAddrs = []
    # recorro los proyectiles
    for proj in self.projectiles:
      anim = proj.addrDosTiles
      # y agrego su animación a la lista
      animAddrs.append(anim)

    # remuevo duplicados y ordeno
    animAddrs = sorted(set(animAddrs))

    f = open(path + '/03_projsAnimations.txt', 'w', encoding="utf-8")

    projsAnimationsAddr = vaPorAddr

    animCounter = 1
    self.dosTiles = []
    for i in range(0,104):

      if(vaPorAddr + 0x4000 in animAddrs):
#        print('---animation' + str(animCounter))
        f.write('---animation' + str(animCounter) + '\n')
        animCounter += 1

      subArray = bank[vaPorAddr : vaPorAddr + 3]
      dosTiles = mystic.tileset.DosTiles(vaPorAddr)
      dosTiles.decodeRom(subArray)
#      print('dosTiles: ' + str(dosTiles))
      self.dosTiles.append(dosTiles)
      lines = dosTiles.encodeTxt()
      strDosTiles = '\n'.join(lines)
      f.write(strDosTiles + '\n')
      vaPorAddr += 3

    f.close()

    length = 3*len(self.dosTiles)
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x09, projsAnimationsAddr, projsAnimationsAddr+length, (rr, gg, bb), 'projectiles animations dosTiles')




##########################################################
class Projectile:
  """ representa un proyectil ó explosión de enemigo """

  def __init__(self, nroProjectile):

    self.nroProjectile = nroProjectile

    # it seems to change the movement style (straigt, rotating, etc)
    self.nose1 = 0x00

    self.speedSleep = 0x00
    self.nose3 = 0x00
    self.nose4 = 0x00
    self.nose5 = 0x00
    self.nose6 = 0x00
    self.vramTileOffset = 0x00
    self.cantDosTiles = 0x00
    self.offsetBank8 = 0x0000
    self.addrSortTiles = 0x0000
    self.addrDosTiles = 0x0000
    self.addr3 = 0x0000

  def decodeRom(self, subArray):

    self.nose1   = subArray[0]
    self.speedSleep = subArray[1]
    self.nose3   = subArray[2]
    self.nose4   = subArray[3]
    self.nose5   = subArray[4]
    self.nose6   = subArray[5]
    self.vramTileOffset = subArray[6]
    self.cantDosTiles = subArray[7]

    off_1 = subArray[8]
    off_2 = subArray[9]
    self.offsetBank8 = off_2*0x100 + off_1

    addr_1 = subArray[10]
    addr_2 = subArray[11]
    self.addrSortTiles = addr_2*0x100 + addr_1

    addr2_1 = subArray[12]
    addr2_2 = subArray[13]
    self.addrDosTiles = addr2_2*0x100 + addr2_1

    addr3_1 = subArray[14]
    addr3_2 = subArray[15]
    self.addr3 = addr3_2*0x100 + addr3_1

  def encodeRom(self):
    array = []

    array.append(self.nose1)
    array.append(self.speedSleep)
    array.append(self.nose3)
    array.append(self.nose4)
    array.append(self.nose5)
    array.append(self.nose6)
    array.append(self.vramTileOffset)
    array.append(self.cantDosTiles)

    array.append(self.offsetBank8%0x100)
    array.append(self.offsetBank8//0x100)

    array.append(self.addrSortTiles%0x100)
    array.append(self.addrSortTiles//0x100)

    array.append(self.addrDosTiles%0x100)
    array.append(self.addrDosTiles//0x100)

    array.append(self.addr3%0x100)
    array.append(self.addr3//0x100)

    return array

  def encodeTxt(self):
    lines = []

    lines.append('\n------------ projectile: ' + mystic.variables.projectiles[self.nroProjectile] )
    lines.append('nroProjectile:  {:02x}'.format(self.nroProjectile))
    lines.append('nose1:          {:02x}'.format(self.nose1))
    lines.append('speedSleep:     {:02x}'.format(self.speedSleep))
    lines.append('nose3:          {:02x}'.format(self.nose3))
    lines.append('nose4:          {:02x}'.format(self.nose4))
    lines.append('nose5:          {:02x}'.format(self.nose5))
    lines.append('nose6:          {:02x}'.format(self.nose6))
    lines.append('vramTileOffset: {:02x}'.format(self.vramTileOffset))
    lines.append('cantDosTiles:   {:02x}'.format(self.cantDosTiles))

    lines.append('offsetBank8:    {:04x}'.format(self.offsetBank8))
    lines.append('addrSortTiles:  {:04x}'.format(self.addrSortTiles))
    lines.append('addrDosTiles:   {:04x}'.format(self.addrDosTiles))
    lines.append('addr3:          {:04x}'.format(self.addr3))
 
    return lines


  def decodeTxt(self, lines):

    for line in lines:
#      print('lineee: ' + line)
      if(line.startswith('nroProjectile:')):
        strNroProjectile = line[len('nroProjectile:'):].strip()
        self.nroProjectile = int(strNroProjectile,16)

      elif(line.startswith('nose1:')):
        strNose1 = line[len('nose1:'):].strip()
        self.nose1 = int(strNose1,16)
      elif(line.startswith('speedSleep:')):
        strSpeed = line[len('speedSleep:'):].strip()
        self.speedSleep = int(strSpeed,16)
      elif(line.startswith('nose3:')):
        strNose3 = line[len('nose3:'):].strip()
        self.nose3 = int(strNose3,16)
      elif(line.startswith('nose4:')):
        strNose4 = line[len('nose4:'):].strip()
        self.nose4 = int(strNose4,16)
      elif(line.startswith('nose5:')):
        strNose5 = line[len('nose5:'):].strip()
        self.nose5 = int(strNose5,16)
      elif(line.startswith('nose6:')):
        strNose6 = line[len('nose6:'):].strip()
        self.nose6 = int(strNose6,16)
      elif(line.startswith('vramTileOffset:')):
        string = line[len('vramTileOffset:'):].strip()
        self.vramTileOffset = int(string,16)
      elif(line.startswith('cantDosTiles:')):
        string = line[len('cantDosTiles:'):].strip()
        self.cantDosTiles = int(string,16)

      elif(line.startswith('offsetBank8:')):
        string = line[len('offsetBank8:'):].strip()
        self.offsetBank8 = int(string,16)

      elif(line.startswith('addrSortTiles:')):
        string = line[len('addrSortTiles:'):].strip()
        self.addrSortTiles = int(string,16)
      elif(line.startswith('addrDosTiles:')):
        string = line[len('addrDosTiles:'):].strip()
        self.addrDosTiles = int(string,16)
      elif(line.startswith('addr3:')):
        string = line[len('addr3:'):].strip()
        self.addr3 = int(string,16)

  def __str__(self):

    string = '{:02x} speed={:02x} {:02x} {:02x} {:02x} {:02x} vram={:02x} cant={:02x} bank8={:04x} sort={:04x} dos={:04x} {:04x}'.format(self.nose1, self.speedSleep, self.nose3, self.nose4, self.nose5, self.nose6, self.vramTileOffset, self.cantDosTiles, self.offsetBank8, self.addrSortTiles, self.addrDosTiles, self.addr3)

    return string





