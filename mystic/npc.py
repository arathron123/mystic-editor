
import mystic.variables

def _strHexToStrCoord(strHex):
  """ converts a pair of hex string into a coordinate string, example "0a 0b" = "(10,11)" """

  strHex = strHex.strip()
  strHexs = strHex.split(' ')
  strHex1 = strHexs[0]
  strHex2 = strHexs[1]

  strCoord = str( (_strHexToSignedInt(strHex1), _strHexToSignedInt(strHex2)) )
  return strCoord


def _strCoordToStrHex(strCoord):
  """ converts a coordinate string into a pair of hex string, example "(10,11)" = "0a 0b" """

  strCoord = strCoord.strip('(')
  strCoord = strCoord.strip(')')
  strCoords = strCoord.split(',')
  coords = []
  strHex = ""
  for strCoord in strCoords:
    strCoord = strCoord.strip()
    coord = int(strCoord)
    strHex += _signedIntToStrHex(coord) + ' '

  strHex = strHex.strip()
  return strHex


def _strHexToSignedInt(strHex):
  """ converts an hex string into a signed integer, example "FF" = -1, "02" = 2 """
  val = int(strHex,16)
  if(val >= 128):
    val = val - 256
  return val

def _signedIntToStrHex(sInt):
  """ converts a signed integer into an hex string, example -1 = "FF", 2 = "02" """
  if(sInt < 0):
    sInt += 256
  strHex = '{:02x}'.format(sInt)
  return strHex


##########################################################
class Npcs:
  """ represents the list of npcs """

  def __init__(self):
    self.jsonNpcs = {}

  def decodeRom(self, bank, currentAddr, numberNpcStats, numberNpc, numberNpcGroups):

#    currentAddr = 0x19fe
#    print('currentAddr: {:04x}'.format(currentAddr))

    self.jsonNpcs = {}


    self.jsonNpcs['npcStat'] = []

    for i in range(0,numberNpcStats):
      npcStat = {}

      subArray = bank[currentAddr : currentAddr+14]

      npcStat['idNpcStat'] = i
      npcStat['comment'] = ''
      npcStat['speedSleep'] = '{:02x}'.format(subArray[0])
      npcStat['hp'] = '{:02x}'.format(subArray[1])
      npcStat['nose2'] = '{:02x}'.format(subArray[2])
      npcStat['nose3'] = '{:02x}'.format(subArray[3])
      npcStat['nose4'] = '{:02x}'.format(subArray[4])
      npcStat['maybeDP'] = '{:02x}'.format(subArray[5])
      npcStat['maybeAP'] = '{:02x}'.format(subArray[6])
      npcStat['vulnerability'] = '{:02x}'.format(subArray[7])
      npcStat['nose6'] = '{:02x}'.format(subArray[8])
      npcStat['projectile'] = '{:02x}'.format(subArray[9])
      npcStat['nose7'] = '{:02x}'.format(subArray[10])
      npcStat['statusInflicting'] = '{:02x}'.format(subArray[11])
      npcStat['maybeExp'] = '{:02x}'.format(subArray[12])
      npcStat['maybeGp'] = '{:02x}'.format(subArray[13])
 
      self.jsonNpcs['npcStat'].append(npcStat)
      currentAddr += 14

#    currentAddr += numberNpcStats*14
#    print('currentAddr: {:04x}'.format(currentAddr))

    self.jsonNpcs['npc'] = []

    for i in range(0,numberNpc):
      npc = {}

      subArray = bank[currentAddr : currentAddr+24]

#      strSubarray = mystic.util.strHexa(subArray)
#      print('subArray: ' + strSubarray)

      npc['idNpc'] = i
      npc['comment'] = mystic.variables.npc[i]
      npc['collisionFlags'] = '{:02x}'.format(subArray[0])
      npc['idNpcStat'] = subArray[1]
      npc['vramTileOffset'] = '{:02x}'.format(subArray[2])
      npc['cantDosTiles'] = '{:02x}'.format(subArray[3])

      offsetBank8_1 = subArray[4]
      offsetBank8_2 = subArray[5]
      npc['offsetBank8'] = '{:04x}'.format(offsetBank8_2*0x100 + offsetBank8_1)

      addrTile1     = subArray[6]
      addrTile2     = subArray[7]
#      npc['addrSortTiles'] = '{:04x}'.format(addrTile2*0x100 + addrTile1)
      npc['idSortTiles'] = '{:04x}'.format(addrTile2*0x100 + addrTile1)

      addrSpriteGrp1 = subArray[8]
      addrSpriteGrp2 = subArray[9]
#      npc['addrSpriteGroup'] = '{:04x}'.format(addrSpriteGrp2*0x100 + addrSpriteGrp1)
      npc['idSpriteGroup'] = '{:04x}'.format(addrSpriteGrp2*0x100 + addrSpriteGrp1)

      npc['patasSepa'] = '{:02x}'.format(subArray[10]) # 0x00   0 ó 1 (patas sólo separadas)
      npc['muevePatas'] = '{:02x}'.format(subArray[11]) # 0x01   0,1,2 (patas juntas)
      npc['nose7'] = '{:02x}'.format(subArray[12]) # 0x01   0,1,2
      npc['nose8'] = '{:02x}'.format(subArray[13]) # 0x00   0,1,2
      npc['nose9'] = '{:02x}'.format(subArray[14]) # 0x00   0,1,2
      npc['nose10'] = '{:02x}'.format(subArray[15]) # 0x00   0,1,2


      npc['behaviourOnHeroWalk1'] = '{:02x}'.format(subArray[16]) # 0x04   02=suelo, 10=salta 12=fantasma bajo suelo 15=teleport
      npc['behaviourOnHeroWalk2'] = '{:02x}'.format(subArray[17]) # 0x04  
      npc['behaviourOnVerticalSight'] = '{:02x}'.format(subArray[18]) # 0x04  
      npc['behaviourOnHorizontalSight'] = '{:02x}'.format(subArray[19]) # 0x04  

      talkScript_1  = subArray[20]
      talkScript_2  = subArray[21]
      npc['talkScript'] = '{:04x}'.format(talkScript_2*0x100 + talkScript_1)

      chestScript_1  = subArray[22]
      chestScript_2  = subArray[23]
      npc['chestScript'] = '{:04x}'.format(chestScript_2*0x100 + chestScript_1)

      self.jsonNpcs['npc'].append(npc)
      currentAddr += 24

#    print('currentAddr: {:04x}'.format(currentAddr))


    # we update each npcStats comment with the npc names that use it
    for k in range(0, numberNpcStats):
      npcStatComments = [npc['comment'] for npc in self.jsonNpcs['npc'] if npc['idNpcStat'] == k]
      comment = '[' + ', '.join(npcStatComments) + ']'
      self.jsonNpcs['npcStat'][k]['comment'] = comment


    self.jsonNpcs['npcGroups'] = []

    dicApparition = {}

    for i in range(0,numberNpcGroups):
      npcGroup = {}

      subArray = bank[currentAddr : currentAddr+6]

      strSubarray = mystic.util.strHexa(subArray)
#      print('subArray: ' + strSubarray)

      npcGroup['idGroup'] = i
      npcGroup['comment'] = ""

      addrAppa1_1 = subArray[0]
      addrAppa1_2 = subArray[1]
      addrApparition1 = addrAppa1_2*0x100 + addrAppa1_1
#      npcGroup['idApparition1'] = '{:04x}'.format(addrApparition1)

      addrAppa2_1 = subArray[2]
      addrAppa2_2 = subArray[3]
      addrApparition2 = addrAppa2_2*0x100 + addrAppa2_1
#      npcGroup['idApparition2'] = '{:04x}'.format(addrApparition2)

      addrAppa3_1 = subArray[4]
      addrAppa3_2 = subArray[5]
      addrApparition3 = addrAppa3_2*0x100 + addrAppa3_1
#      npcGroup['idApparition3'] = '{:04x}'.format(addrApparition3)

      npcGroup['idApparitions'] = [addrApparition1, addrApparition2, addrApparition3]

      dicApparition[addrApparition1] = addrApparition1
      dicApparition[addrApparition2] = addrApparition2
      dicApparition[addrApparition3] = addrApparition3

      self.jsonNpcs['npcGroups'].append(npcGroup)
      currentAddr += 6

#    print('currentAddr: {:04x}'.format(currentAddr))


#    print('dicApparition: ' + str(dicApparition))

    # sort the apparitions dictionary
    sortAppas = sorted(dicApparition.items())
#    print('sortAppas: ' + str(sortAppas))
#    print('len: ' + str(len(sortAppas)))

    self.jsonNpcs['apparitions'] = []

#    for i in range(0,215):
    i = 0
    for sortAppa in sortAppas:

      # we hardcode-add the unused apparition
      if(i == 197):

        appa = {}
        appa['idApparition'] = i
        appa['comment'] = mystic.variables.npc[175]
        appa['minVal'] = 1
        appa['maxVal'] = 1
        appa['idNpcs'] = [175, 175, 175, 175]
        appa['position_xy'] = [ str( (int("09",16), int("0c",16)) ) ]
        appa['closing'] = "80 80"

        dicApparition[currentAddr+0x4000] = i
        self.jsonNpcs['apparitions'].append(appa)

        currentAddr += 10
        i += 1


      appa = {}
      appa['idApparition'] = i
      appa['comment'] = mystic.variables.npc[bank[currentAddr+2]]
      appa['minVal'] = bank[currentAddr+0]
      appa['maxVal'] = bank[currentAddr+1]
      appa['idNpcs'] = [bank[currentAddr+2], bank[currentAddr+3], bank[currentAddr+4], bank[currentAddr+5]]

      subArray = bank[currentAddr+6:]
      idx = subArray.index(0x80)
#      print('idx: ' + str(idx))

      subArray = bank[currentAddr+6:currentAddr+6+idx]
#      appa['position_xy'] = mystic.util.strHexa(bank[currentAddr+6:currentAddr+6+idx])
#      appa['position_xy'] = [ str( (subArray[2*j+0], subArray[2*j+1]) ) for j in range(0,idx//2)]

      positionsXy = []
      for k in range(0, idx//2):
        strHex = mystic.util.strHexa( [subArray[2*k+0], subArray[2*k+1]] )
        strCoord = _strHexToStrCoord(strHex)
        positionsXy.append(strCoord)

#        coords = _strCoordToStrHex(strCoord)
#        print('strHex: ' + strHex + ' coords: ' + strCoord + ' coords: ' + str(coords))

        
      appa['position_xy'] = positionsXy


      appa['closing'] = mystic.util.strHexa(bank[currentAddr+6+idx:currentAddr+6+idx+2]).strip()

      dicApparition[currentAddr+0x4000] = i
      self.jsonNpcs['apparitions'].append(appa)
      currentAddr += 6+idx+2
      i += 1

#      print('i: ' + str(i) + ' vaPorAddr: {:04x}'.format(currentAddr+0x4000) + ' sortAppas: ' + str(sortAppas[i][0]) )
#    print('dicApparition: ' + str(dicApparition))

#    print('currentAddr: {:04x}'.format(currentAddr))


    # change the addr's of sortTiles to it's index number
    for npcGroup in self.jsonNpcs['npcGroups']:
#      print('npcGroup: ' + str(npcGroup))

      npcComments = []

      for k in range(0,3):
        addrApparition = npcGroup['idApparitions'][k]
        strAddrApparition = '{:04x}'.format(addrApparition)
#        print('addrApparition: ' + strAddrApparition)
        idApparition = dicApparition[addrApparition]
#        print('addr: ' + strAddrApparition + ' id: ' + str(idApparition))

        npcGroup['idApparitions'][k] = idApparition

#        print('idApparition: ' + str(idApparition))
        appa = self.jsonNpcs['apparitions'][idApparition]
#        print('appa: ' + appa['comment'])
        npcComments.append(appa['comment'])

      npcGroup['comment'] = str(npcComments)



    # dictionary of sortTiles
    dicSortTiles = {}

    # en la primer iteración creo el dicSortTiles
    for npc in self.jsonNpcs['npc']:
#      print('npc: ' + str(npc))
      addrSortTiles = int(npc['idSortTiles'],16)
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addrSortTiles: ' + strAddrSortTiles)
      dicSortTiles[strAddrSortTiles] = addrSortTiles #0x00


#    print('dicSortTiles: ' + str(dicSortTiles))
    # sort the sortTiles according to their addr
    sortSortTiles = sorted(dicSortTiles.items())
#    print('sortSortTiles: ' + str(sortSortTiles))



    # size of the sortTiles table (in bytes)
    sizeSortTiles = 28
    # addr where the sortTiles table end
    addrSortTilesEnd = currentAddr + sizeSortTiles + 0x4000
#    print('addrSortTilesEnd: {:04x}'.format(addrSortTilesEnd))

    # the sorted addresses of the sortTiles
    sortedAddrs = [sort[1] for sort in sortSortTiles]
    # we add the last addr
    sortedAddrs.append(addrSortTilesEnd)
#    print('sortedAddrs: ' + str(sortedAddrs))

    self.jsonNpcs['sortTiles'] = []
    # and calculate the size of each sortTile (as a difference between two consecutive addr)
    for i in range(0, len(sortedAddrs)-1):
      delta = sortedAddrs[i+1] - sortedAddrs[i]
      addrSortTiles = sortedAddrs[i]
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addr ' + strAddrSortTiles + ' delta: ' + str(delta))

      dicSortTiles[strAddrSortTiles] = i

      sortTiles = bank[addrSortTiles-0x4000:addrSortTiles-0x4000+delta]
      strSortTiles = mystic.util.strHexa(sortTiles)
#      print('sortTiles: ' + strSortTiles)

      self.jsonNpcs['sortTiles'].append( {'idSortTiles': i, 'sorting' : strSortTiles } )


    # change the addr's of sortTiles to it's index number
    for npc in self.jsonNpcs['npc']:
#      print('npc: ' + str(npc))
      addrSortTiles = int(npc['idSortTiles'],16)
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addrSortTiles: ' + strAddrSortTiles)
      idSortTiles = dicSortTiles[strAddrSortTiles]
#      print('addr: ' + strAddrSortTiles + ' id: ' + str(idSortTiles))
      npc['idSortTiles'] = idSortTiles


    currentAddr += sizeSortTiles
#    print('currentAddr: {:04x}'.format(currentAddr))


    dicSpriteGroup = {}
    # el dicSpriteGroup
    for npc in self.jsonNpcs['npc']:
#      print('npc: ' + str(npc))
      addrSpriteGroup = int(npc['idSpriteGroup'],16)
      strAddrSpriteGroup = '{:04x}'.format(addrSpriteGroup)
#      print('addrSpriteGroup: ' + strAddrSpriteGroup)
      dicSpriteGroup[strAddrSpriteGroup] = addrSpriteGroup #0x00


#    print('dicSpriteGroup: ' + str(dicSpriteGroup))
    # sort according to their addr
    sortSpriteGroup = sorted(dicSpriteGroup.items())
#    print('sortSpriteGroup: ' + str(sortSpriteGroup))


    self.jsonNpcs['spriteGroups'] = []


#    prevAddr = 0
    i = 0
    for addrSpriteGroup in sortSpriteGroup:

      spriteGroup = {}
      spriteGroup['idSpriteGroup'] = i


      strAddrSpriteGroup = addrSpriteGroup[0]
      addrSpriteGroup = int(strAddrSpriteGroup,16)
#      diff = addrSpriteGroup - prevAddr
#      prevAddr = addrSpriteGroup
#      print('strAddrSpriteGroup: ' + strAddrSpriteGroup + ' diff: ' + str(diff))

      npcs = [npc for npc in self.jsonNpcs['npc'] if npc['idSpriteGroup'] == strAddrSpriteGroup]
      comments = [npc['comment'] for npc in npcs]
      spriteGroup['comment'] = str(comments)

      # update the idSpriteGroup of npcs
      for npc in npcs:
        npc['idSpriteGroup'] = i


      sprites = []
      if(addrSpriteGroup < 0x4000):

        bank0 = mystic.romSplitter.banks[0]
        currentAddr = addrSpriteGroup

        for j in range(0,4*2):
          subArray = bank0[currentAddr:currentAddr+3]

          attrib = subArray[0]
          tile1 = subArray[1]
          tile2 = subArray[2]

          strAttrib = '{:02x}'.format(attrib)
          strTile1 = '{:02x}'.format(tile1)
          strTile2 = '{:02x}'.format(tile2)

          sprite = {'idSprite' : j, 'attrib' : strAttrib, 'tile1' : strTile1, 'tile2' : strTile2}
#          print('sprite: ' + str(sprite))
          sprites.append(sprite)
          currentAddr += 3

      else:
        currentAddr = addrSpriteGroup-0x4000
        for j in range(0,4*3):
          subArray = bank[currentAddr:currentAddr+3]

          attrib = subArray[0]
          tile1 = subArray[1]
          tile2 = subArray[2]

          strAttrib = '{:02x}'.format(attrib)
          strTile1 = '{:02x}'.format(tile1)
          strTile2 = '{:02x}'.format(tile2)

          sprite = {'idSprite' : j, 'attrib' : strAttrib, 'tile1' : strTile1, 'tile2' : strTile2}
#          print('sprite: ' + str(sprite))
          sprites.append(sprite)
          currentAddr += 3
        
      spriteGroup['sprites'] = sprites
      self.jsonNpcs['spriteGroups'].append(spriteGroup)
      i += 1




  def encodeRom(self, addrNpcStats, addrSnowman):
    array = []

#    print('addrNpcStats: {:04x}'.format(addrNpcStats))

    currentAddr = addrNpcStats

    arrayNpcStat = []

    for npcStat in self.jsonNpcs['npcStat']:
#      print('npcStat: ' + str(npcStat)) 

      subArray = []

      speedSleep = int(npcStat['speedSleep'],16)
      subArray.append(speedSleep)
      hp = int(npcStat['hp'],16)
      subArray.append(hp)
      nose2 = int(npcStat['nose2'],16)
      subArray.append(nose2)
      nose3 = int(npcStat['nose3'],16)
      subArray.append(nose3)
      nose4 = int(npcStat['nose4'],16)
      subArray.append(nose4)
      maybeDP = int(npcStat['maybeDP'],16)
      subArray.append(maybeDP)
      maybeAP = int(npcStat['maybeAP'],16)
      subArray.append(maybeAP)
      vulnerability = int(npcStat['vulnerability'],16)
      subArray.append(vulnerability)
      nose6 = int(npcStat['nose6'],16)
      subArray.append(nose6)
      projectile = int(npcStat['projectile'],16)
      subArray.append(projectile)
      nose7 = int(npcStat['nose7'],16)
      subArray.append(nose7)
      statusInflicting = int(npcStat['statusInflicting'],16)
      subArray.append(statusInflicting)
      maybeExp = int(npcStat['maybeExp'],16)
      subArray.append(maybeExp)
      maybeGp = int(npcStat['maybeGp'],16)
      subArray.append(maybeGp)

      arrayNpcStat.extend(subArray)
      currentAddr += len(subArray)

#    currentAddr = addrNpc
    addrNpc = currentAddr
#    print('addrNpc: {:04x}'.format(addrNpc))

    arrayNpc = []

    for npc in self.jsonNpcs['npc']:
#      print('npc: ' + str(npc)) 
#      print('currentAddr: {:04x}'.format(currentAddr))

      subArray = []

      collisionFlags = int(npc['collisionFlags'],16)
      subArray.append(collisionFlags)
      stats = npc['idNpcStat']
      subArray.append(stats)
      vramTileOffset = int(npc['vramTileOffset'],16)
      subArray.append(vramTileOffset)
      cantDosTiles = int(npc['cantDosTiles'],16)
      subArray.append(cantDosTiles)

      offsetBank8 = int(npc['offsetBank8'],16)
      subArray.append(offsetBank8%0x100)
      subArray.append(offsetBank8//0x100)

#      addrSortTiles = int(npc['addrSortTiles'],16)
#      subArray.append(addrSortTiles%0x100)
#      subArray.append(addrSortTiles//0x100)

      idSortTiles = npc['idSortTiles']
#      subArray.extend( [0x00, 0x00] )
#      subArray.append(addrSortTiles%0x100)
#      subArray.append(addrSortTiles//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
      subArray.append('idSortTiles[' + str(idSortTiles) + ']')
      subArray.append('idSortTiles[' + str(idSortTiles) + ']')

      idSpriteGroup = npc['idSpriteGroup']
#      subArray.append(addrSpriteGroup%0x100)
#      subArray.append(addrSpriteGroup//0x100)
#      subArray.extend( [0x00, 0x00] )
      subArray.append('idSpriteGroup[' + str(idSpriteGroup) + ']')
      subArray.append('idSpriteGroup[' + str(idSpriteGroup) + ']')

      patasSepa = int(npc['patasSepa'],16)
      subArray.append(patasSepa)
      muevePatas = int(npc['muevePatas'],16)
      subArray.append(muevePatas)
      nose7 = int(npc['nose7'],16)
      subArray.append(nose7)
      nose8 = int(npc['nose8'],16)
      subArray.append(nose8)
      nose9 = int(npc['nose9'],16)
      subArray.append(nose9)
      nose10 = int(npc['nose10'],16)
      subArray.append(nose10)

      behaviourOnHeroWalk1 = int(npc['behaviourOnHeroWalk1'],16)
      subArray.append(behaviourOnHeroWalk1)
      behaviourOnHeroWalk2 = int(npc['behaviourOnHeroWalk2'],16)
      subArray.append(behaviourOnHeroWalk2)
      behaviourOnVerticalSight = int(npc['behaviourOnVerticalSight'],16)
      subArray.append(behaviourOnVerticalSight)
      behaviourOnHorizontalSight = int(npc['behaviourOnHorizontalSight'],16)
      subArray.append(behaviourOnHorizontalSight)

      talkScript = int(npc['talkScript'],16)
      subArray.append(talkScript%0x100)
      subArray.append(talkScript//0x100)

      chestScript = int(npc['chestScript'],16)
      subArray.append(chestScript%0x100)
      subArray.append(chestScript//0x100)

      arrayNpc.extend(subArray)
      currentAddr += len(subArray)


#    print('currentAddr: {:04x}'.format(currentAddr))

    addrNpcGroup = currentAddr
#    print('addrNpcGroup: {:04x}'.format(addrNpcGroup))

#    for npcGroup in self.jsonNpcs['npcGroups']:
#      array.extend([0x00, 0x00])
#      array.extend([0x00, 0x00])
#      array.extend([0x00, 0x00])
#      currentAddr += 6
#    addrApparitions = currentAddr

    addrApparitions = currentAddr + 6 * len(self.jsonNpcs['npcGroups'])
#    print('addrApparitions: {:04x}'.format(addrApparitions))

    arrayAppa = []

    dicApparition = {}
    currentAddr = addrApparitions

    i = 0
    for appa in self.jsonNpcs['apparitions']:

      dicApparition[i] = currentAddr

      subArray = []

      subArray.append(appa['minVal'])
      subArray.append(appa['maxVal'])
      subArray.extend(appa['idNpcs'])

#      print('appa: ' + appa['comment'])
      for strCoord in appa['position_xy']:
        strHex = _strCoordToStrHex(strCoord)
#        print('strCoord: ' + strCoord + ' strHex: ' + strHex)
        hexaCoords = mystic.util.hexaStr(strHex)
        subArray.extend(hexaCoords)
#        print('hexa coords: ' + mystic.util.strHexa(hexaCoords))

      closing = mystic.util.hexaStr(appa['closing'])
      subArray.extend(closing)
#      print('subArray: ' + mystic.util.strHexa(subArray))

      currentAddr += len(subArray)
      arrayAppa.extend(subArray)
      i += 1


    arrayGroups = []

    for npcGroup in self.jsonNpcs['npcGroups']:
      subArray = []

      idApparitions = npcGroup['idApparitions']
#      print('idApparitions: ' + str(idApparitions))

      addrApparition1 = dicApparition[idApparitions[0]] + 0x4000
#      print('addrApparition1: {:04x}'.format(addrApparition1))
      subArray.append(addrApparition1%0x100)
      subArray.append(addrApparition1//0x100)

      addrApparition2 = dicApparition[idApparitions[1]] + 0x4000
#      print('addrApparition2: {:04x}'.format(addrApparition2))
      subArray.append(addrApparition2%0x100)
      subArray.append(addrApparition2//0x100)

      addrApparition3 = dicApparition[idApparitions[2]] + 0x4000
#      print('addrApparition3: {:04x}'.format(addrApparition3))
      subArray.append(addrApparition3%0x100)
      subArray.append(addrApparition3//0x100)

      arrayGroups.extend(subArray)
#      currentAddr += len(subArray)

#    print('currentAddr: {:04x}'.format(currentAddr))

    arraySortTiles = []

    # dictionary of sortTiles
    dicSortTiles = {}
    i = 0
    for sortTile in self.jsonNpcs['sortTiles']:
#      print(' --- sortTile: ' + str(sortTile))
      dicSortTiles[i] = currentAddr
      strSortT = sortTile['sorting']
      subArray = mystic.util.hexaStr(strSortT.strip())
#      print('subArray: ' + mystic.util.strHexa(subArray))
      arraySortTiles.extend(subArray)
      currentAddr += len(subArray)
      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))
    addrSpriteGroup = currentAddr

    # dictionary of spriteGroups
    dicSpriteGrp = {}

    arraySpriteGroup1 = []
    arraySpriteGroup2 = []

    # the current addr from bank0
    currentAddr0 = addrSnowman

    i = 0
    for spriteGroup in self.jsonNpcs['spriteGroups']:
#      print('spriteGroup: ' + spriteGroup['comment'])

      # the first 3 spriteGroups are encoded into bank0
      if(i < 3):

        dicSpriteGrp[i] = currentAddr0
#        print('dicSpriteGrp[' + str(i) + '] = {:04x}'.format(currentAddr0))

        for sprite in spriteGroup['sprites']:
          attrib = int(sprite['attrib'],16)
          tile1 = int(sprite['tile1'],16)
          tile2 = int(sprite['tile2'],16)
          subArray = [attrib, tile1, tile2]
          arraySpriteGroup1.extend(subArray)
          currentAddr0 += len(subArray)


      # all the other spriteGroups are encoded into bank3
      else:

        # we add the unused spriteGroup
        if(i == 29):
          for k in range(0,4):
            subArray = [0x30, 0x46, 0x44]
            arraySpriteGroup2.extend(subArray)
            currentAddr += len(subArray)
          for k in range(0,8):
            subArray = [0x70, 0x46, 0x44]
            arraySpriteGroup2.extend(subArray)
            currentAddr += len(subArray)
#          i += 1


        dicSpriteGrp[i] = currentAddr + 0x4000
#        print('dicSpriteGrp[' + str(i) + '] = {:04x}'.format(currentAddr + 0x4000))

        # and we add the used spriteGroups
        for sprite in spriteGroup['sprites']:
          attrib = int(sprite['attrib'],16)
          tile1 = int(sprite['tile1'],16)
          tile2 = int(sprite['tile2'],16)
          subArray = [attrib, tile1, tile2]
          arraySpriteGroup2.extend(subArray)
          currentAddr += len(subArray)

      i += 1

#    print('arraySpriteGroup2: ' + mystic.util.strHexa(arraySpriteGroup2))
#    print('currentAddr: {:04x}'.format(currentAddr))

    array.extend(arrayNpcStat)
    array.extend(arrayNpc)
    array.extend(arrayGroups)
    array.extend(arrayAppa)
    array.extend(arraySortTiles)
    array.extend(arraySpriteGroup2)



    # translate the labels into addresses
    for i in range(0, len(array)):
      cosa = array[i]
      if( isinstance(cosa, str) ):
#        print('cosa: ' + cosa)

        if(cosa.startswith('idSortTiles[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idS = int(cosa[idx0:idx1])
#          print('idS: ' + str(idS))
          addr = dicSortTiles[idS] + 0x4000

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

        elif(cosa.startswith('idSpriteGroup[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idS = int(cosa[idx0:idx1])
#          print('idS: ' + str(idS))
          addr = dicSpriteGrp[idS]# + 0x4000

#          print('translating ' + str(idS) + ' into {:04x}'.format(addr))

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2




    return arraySpriteGroup1, array



