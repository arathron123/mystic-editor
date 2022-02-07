import mystic.variables

##########################################################
class Boss:
  """ representa un monstruo grande """

  def __init__(self, nroBoss):

    self.nroBoss = nroBoss

    # the speed (0x01 is the faster, the higher the slower)
    self.speedSleep = 0x00
    # the total hp of the boss is 0x10*self.hp
    self.hp     = 0x00
    # experience
    self.exp    = 0x00
    # gold
    self.gp     = 0x00

    self.nose1  = 0x00
    self.addr1  = 0x0000
    self.nose2  = 0x00

    self.vramTileOffset = 0x00
    self.cantDosTiles   = 0x00

    self.offsetBank8   = 0x0000
    self.addrSortTiles = 0x0000
    self.addrDosTiles  = 0x0000

    self.addrDamage  = 0x0000
    self.addrBehaviour  = 0x0000
    self.addrBehaviourStart  = 0x0000
    self.addrDeathExplosion  = 0x0000


  def decodeRom(self, subArray):

    self.speedSleep = subArray[0]
    self.hp      = subArray[1]
    self.exp     = subArray[2]
    self.gp      = subArray[3]

    self.nose1   = subArray[4]

    addr1_1 = subArray[5]
    addr1_2 = subArray[6]
    self.addr1 = addr1_2*0x100 + addr1_1

    self.nose2   = subArray[7]

    self.vramTileOffset = subArray[8]
    self.cantDosTiles   = subArray[9]

    offsetBank8_1 = subArray[10]
    offsetBank8_2 = subArray[11]
    self.offsetBank8 = offsetBank8_2*0x100 + offsetBank8_1

    addrTile1     = subArray[12]
    addrTile2     = subArray[13]
    self.addrSortTiles = addrTile2*0x100 + addrTile1

    addrDosTiles1 = subArray[14]
    addrDosTiles2 = subArray[15]
    self.addrDosTiles = addrDosTiles2*0x100 + addrDosTiles1

    addrDam1  = subArray[16]
    addrDam2  = subArray[17]
    self.addrDamage = addrDam2*0x100 + addrDam1

    addrBeh_1  = subArray[18]
    addrBeh_2  = subArray[19]
    self.addrBehaviour = addrBeh_2*0x100 + addrBeh_1

    addrBeh_1  = subArray[20]
    addrBeh_2  = subArray[21]
    self.addrBehaviourStart = addrBeh_2*0x100 + addrBeh_1

    addrDeath_1  = subArray[22]
    addrDeath_2  = subArray[23]
    self.addrDeathExplosion = addrDeath_2*0x100 + addrDeath_1

  def encodeRom(self):
    array = []

    array.append(self.speedSleep)
    array.append(self.hp)
    array.append(self.exp)
    array.append(self.gp)

    array.append(self.nose1)

    array.append(self.addr1%0x100)
    array.append(self.addr1//0x100)

    array.append(self.nose2)

    array.append(self.vramTileOffset)
    array.append(self.cantDosTiles)

    array.append(self.offsetBank8%0x100)
    array.append(self.offsetBank8//0x100)

    array.append(self.addrSortTiles%0x100)
    array.append(self.addrSortTiles//0x100)

    array.append(self.addrDosTiles%0x100)
    array.append(self.addrDosTiles//0x100)

    array.append(self.addrDamage%0x100)
    array.append(self.addrDamage//0x100)

    array.append(self.addrBehaviour%0x100)
    array.append(self.addrBehaviour//0x100)
    array.append(self.addrBehaviourStart%0x100)
    array.append(self.addrBehaviourStart//0x100)
    array.append(self.addrDeathExplosion%0x100)
    array.append(self.addrDeathExplosion//0x100)

    return array

  def encodeTxt(self, vaPorAddr):
    lines = []

    lines.append('\n------------ boss: {:04x} '.format(vaPorAddr) + mystic.variables.bosses[self.nroBoss] )
    lines.append('nroBoss:            {:02x}'.format(self.nroBoss))
    lines.append('speedSleep:         {:02x}'.format(self.speedSleep))
    lines.append('hp:                 {:02x}'.format(self.hp))
    lines.append('exp:                {:02x}'.format(self.exp))
    lines.append('gp:                 {:02x}'.format(self.gp))
    lines.append('nose1:              {:02x}'.format(self.nose1))
    lines.append('addr1:              {:04x}'.format(self.addr1))
    lines.append('nose2:              {:02x}'.format(self.nose2))
    lines.append('vramTileOffset:     {:02x}'.format(self.vramTileOffset))
    lines.append('cantDosTiles:       {:02x}'.format(self.cantDosTiles))
    lines.append('offsetBank8:        {:04x}'.format(self.offsetBank8))
    lines.append('addrSortTiles:      {:04x}'.format(self.addrSortTiles))
    lines.append('addrDosTiles:       {:04x}'.format(self.addrDosTiles))
    lines.append('addrDamage:         {:04x}'.format(self.addrDamage))
    lines.append('addrBehaviour:      {:04x}'.format(self.addrBehaviour))
    lines.append('addrBehaviourStart: {:04x}'.format(self.addrBehaviourStart))
    lines.append('addrDeathExplosion: {:04x}'.format(self.addrDeathExplosion))

    return lines

  def decodeTxt(self, lines):
    for line in lines:
#      print('lineee: ' + line)
      if(line.startswith('nroBoss:')):
        strNroBoss = line[len('nroBoss:'):].strip()
        self.nroBoss = int(strNroBoss,16)

      elif(line.startswith('speedSleep:')):
        strSpeedSleep = line[len('speedSleep:'):].strip()
        self.speedSleep = int(strSpeedSleep,16)
      elif(line.startswith('hp:')):
        strHp = line[len('hp:'):].strip()
        self.hp = int(strHp,16)
      elif(line.startswith('exp:')):
        strExp = line[len('exp:'):].strip()
        self.exp = int(strExp,16)
      elif(line.startswith('gp:')):
        strGp = line[len('gp:'):].strip()
        self.gp = int(strGp,16)
      elif(line.startswith('nose1:')):
        strNose1 = line[len('nose1:'):].strip()
        self.nose1 = int(strNose1,16)

      elif(line.startswith('addr1:')):
        strAddr1 = line[len('addr1:'):].strip()
        self.addr1 = int(strAddr1,16)

      elif(line.startswith('nose2:')):
        strNose2 = line[len('nose2:'):].strip()
        self.nose2 = int(strNose2,16)

      elif(line.startswith('vramTileOffset:')):
        strVramTileOffset = line[len('vramTileOffset:'):].strip()
        self.vramTileOffset = int(strVramTileOffset,16)
      elif(line.startswith('cantDosTiles:')):
        strCantDosTiles = line[len('cantDosTiles:'):].strip()
        self.cantDosTiles = int(strCantDosTiles,16)
      elif(line.startswith('offsetBank8:')):
        strOffsetBank8 = line[len('offsetBank8:'):].strip()
        self.offsetBank8 = int(strOffsetBank8,16)
      elif(line.startswith('addrSortTiles:')):
        strAddrSortTiles = line[len('addrSortTiles:'):].strip()
        self.addrSortTiles = int(strAddrSortTiles,16)
      elif(line.startswith('addrDosTiles:')):
        strAddrDosTiles = line[len('addrDosTiles:'):].strip()
        self.addrDosTiles = int(strAddrDosTiles,16)

      elif(line.startswith('addrDamage:')):
        strAddrDamage = line[len('addrDamage:'):].strip()
        self.addrDamage = int(strAddrDamage,16)
      elif(line.startswith('addrBehaviour:')):
        strBeh = line[len('addrBehaviour:'):].strip()
        self.addrBehaviour = int(strBeh,16)
      elif(line.startswith('addrBehaviourStart:')):
        strBeh = line[len('addrBehaviourStart:'):].strip()
        self.addrBehaviourStart = int(strBeh,16)
      elif(line.startswith('addrDeathExplosion:')):
        strDeath = line[len('addrDeathExplosion:'):].strip()
        self.addrDeathExplosion = int(strDeath,16)

  def __str__(self):

    string = ' speed={:02x} hp={:02x} exp={:02x} GP={:02x} {:02x} {:04x} {:02x} vramTileOffset={:02x} cantDosTiles={:02x} offsetBank8={:04x} addrSortTiles={:04x} addrDosTiles={:04x} {:04x} {:04x} {:04x} {:04x} '.format(self.speedSleep, self.hp, self.exp, self.gp, self.nose1, self.addr1, self.nose2, self.vramTileOffset, self.cantDosTiles, self.offsetBank8, self.addrSortTiles, self.addrDosTiles, self.addrDamage, self.addrBehaviour, self.addrBehaviourStart, self.addrDeathExplosion)

    return string


