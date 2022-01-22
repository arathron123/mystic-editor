import mystic.variables

##########################################################
class Boss:
  """ representa un monstruo grande """

  def __init__(self, nroBoss):

    self.nroBoss = nroBoss

    self.nose1  = 0x00
    self.nose2  = 0x00
    self.nose3  = 0x00
    self.nose4  = 0x00
    self.nose5  = 0x00

    self.addr1  = 0x0000

    self.nose6  = 0x00
    self.vramTileOffset = 0x00
    self.cantDosTiles   = 0x00

    self.offsetBank8  = 0x0000
    self.addrRaro     = 0x0000
    self.addrDosTiles = 0x0000

    self.addr2  = 0x0000
    self.addr3  = 0x0000
    self.addr4  = 0x0000
    self.addr5  = 0x0000


  def decodeRom(self, subArray):

    self.nose1   = subArray[0]
    self.nose2   = subArray[1]
    self.nose3   = subArray[2]
    self.nose4   = subArray[3]
    self.nose5   = subArray[4]

    addr1_1 = subArray[5]
    addr1_2 = subArray[6]
    self.addr1 = addr1_2*0x100 + addr1_1

    self.nose6   = subArray[7]
    self.vramTileOffset = subArray[8]
    self.cantDosTiles   = subArray[9]

    offsetBank8_1 = subArray[10]
    offsetBank8_2 = subArray[11]
    self.offsetBank8 = offsetBank8_2*0x100 + offsetBank8_1

    addrRaro1     = subArray[12]
    addrRaro2     = subArray[13]
    self.addrRaro = addrRaro2*0x100 + addrRaro1

    addrDosTiles1 = subArray[14]
    addrDosTiles2 = subArray[15]
    self.addrDosTiles = addrDosTiles2*0x100 + addrDosTiles1

    addr2_1  = subArray[16]
    addr2_2  = subArray[17]
    self.addr2 = addr2_2*0x100 + addr2_1

    addr3_1  = subArray[18]
    addr3_2  = subArray[19]
    self.addr3 = addr3_2*0x100 + addr3_1

    addr4_1  = subArray[20]
    addr4_2  = subArray[21]
    self.addr4 = addr4_2*0x100 + addr4_1

    addr5_1  = subArray[22]
    addr5_2  = subArray[23]
    self.addr5 = addr5_2*0x100 + addr5_1

  def encodeRom(self):
    array = []

    array.append(self.nose1)
    array.append(self.nose2)
    array.append(self.nose3)
    array.append(self.nose4)
    array.append(self.nose5)

    array.append(self.addr1%0x100)
    array.append(self.addr1//0x100)

    array.append(self.nose6)
    array.append(self.vramTileOffset)
    array.append(self.cantDosTiles)

    array.append(self.offsetBank8%0x100)
    array.append(self.offsetBank8//0x100)

    array.append(self.addrRaro%0x100)
    array.append(self.addrRaro//0x100)

    array.append(self.addrDosTiles%0x100)
    array.append(self.addrDosTiles//0x100)

    array.append(self.addr2%0x100)
    array.append(self.addr2//0x100)
    array.append(self.addr3%0x100)
    array.append(self.addr3//0x100)
    array.append(self.addr4%0x100)
    array.append(self.addr4//0x100)
    array.append(self.addr5%0x100)
    array.append(self.addr5//0x100)

    return array

  def encodeTxt(self):
    lines = []

    lines.append('\n------------ boss: ' + mystic.variables.bosses[self.nroBoss] )
    lines.append('nroBoss:        {:02x}'.format(self.nroBoss))
    lines.append('nose1:          {:02x}'.format(self.nose1))
    lines.append('nose2:          {:02x}'.format(self.nose2))
    lines.append('nose3:          {:02x}'.format(self.nose3))
    lines.append('nose4:          {:02x}'.format(self.nose4))
    lines.append('nose5:          {:02x}'.format(self.nose5))
    lines.append('addr1:          {:04x}'.format(self.addr1))
    lines.append('nose6:          {:02x}'.format(self.nose6))
    lines.append('vramTileOffset: {:02x}'.format(self.vramTileOffset))
    lines.append('cantDosTiles:   {:02x}'.format(self.cantDosTiles))
    lines.append('offsetBank8:    {:04x}'.format(self.offsetBank8))
    lines.append('addrRaro:       {:04x}'.format(self.addrRaro))
    lines.append('addrDosTiles:   {:04x}'.format(self.addrDosTiles))
    lines.append('addr2:          {:04x}'.format(self.addr2))
    lines.append('addr3:          {:04x}'.format(self.addr3))
    lines.append('addr4:          {:04x}'.format(self.addr4))
    lines.append('addr5:          {:04x}'.format(self.addr5))

    return lines

  def decodeTxt(self, lines):
    for line in lines:
#      print('lineee: ' + line)
      if(line.startswith('nroBoss:')):
        strNroBoss = line[len('nroBoss:'):].strip()
        self.nroBoss = int(strNroBoss,16)

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
      elif(line.startswith('nose5:')):
        strNose5 = line[len('nose5:'):].strip()
        self.nose5 = int(strNose5,16)

      elif(line.startswith('addr1:')):
        strAddr1 = line[len('addr1:'):].strip()
        self.addr1 = int(strAddr1,16)

      elif(line.startswith('nose6:')):
        strNose6 = line[len('nose6:'):].strip()
        self.nose6 = int(strNose6,16)

      elif(line.startswith('vramTileOffset:')):
        strVramTileOffset = line[len('vramTileOffset:'):].strip()
        self.vramTileOffset = int(strVramTileOffset,16)
      elif(line.startswith('cantDosTiles:')):
        strCantDosTiles = line[len('cantDosTiles:'):].strip()
        self.cantDosTiles = int(strCantDosTiles,16)
      elif(line.startswith('offsetBank8:')):
        strOffsetBank8 = line[len('offsetBank8:'):].strip()
        self.offsetBank8 = int(strOffsetBank8,16)
      elif(line.startswith('addrRaro:')):
        strAddrRaro = line[len('addrRaro:'):].strip()
        self.addrRaro = int(strAddrRaro,16)
      elif(line.startswith('addrDosTiles:')):
        strAddrDosTiles = line[len('addrDosTiles:'):].strip()
        self.addrDosTiles = int(strAddrDosTiles,16)

      elif(line.startswith('addr2:')):
        strAddr2 = line[len('addr2:'):].strip()
        self.addr2 = int(strAddr2,16)
      elif(line.startswith('addr3:')):
        strAddr3 = line[len('addr3:'):].strip()
        self.addr3 = int(strAddr3,16)
      elif(line.startswith('addr4:')):
        strAddr4 = line[len('addr4:'):].strip()
        self.addr4 = int(strAddr4,16)
      elif(line.startswith('addr5:')):
        strAddr5 = line[len('addr5:'):].strip()
        self.addr5 = int(strAddr5,16)

  def __str__(self):

    string = ' {:02x} {:02x} {:02x} {:02x} {:02x} {:04x} {:02x} vramTileOffset={:02x} cantDosTiles={:02x} offsetBank8={:04x} addrRaro={:04x} addrDosTiles={:04x} {:04x} {:04x} {:04x} {:04x} '.format(self.nose1, self.nose2, self.nose3, self.nose4, self.nose5, self.addr1, self.nose6, self.vramTileOffset, self.cantDosTiles, self.offsetBank8, self.addrRaro, self.addrDosTiles, self.addr2, self.addr3, self.addr4, self.addr5)

    return string


