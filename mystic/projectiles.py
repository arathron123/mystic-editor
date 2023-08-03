import os

import mystic.variables



##########################################################
class Projectiles:
  """ represents the list of projectiles """

  def __init__(self):
    self.jsonProjectiles = {}

  def decodeRom(self, bank, currentAddr, numberProjectiles):

    # currentAddr = 0x0479
#    print('currentAddr: {:04x}'.format(currentAddr))

    self.jsonProjectiles = {}


    self.jsonProjectiles['projectiles'] = []

    for i in range(0,numberProjectiles):
      proj = {}

      subArray = bank[currentAddr : currentAddr+16]

      proj['idProjectile'] = i
      proj['comment'] = mystic.variables.projectiles[i]
      # it seems to change the movement style (straight, rotating, etc)
      proj['nose1'] = '{:02x}'.format(subArray[0])
      proj['speedSleep'] = '{:02x}'.format(subArray[1])
      proj['nose3'] = '{:02x}'.format(subArray[2])
      proj['nose4'] = '{:02x}'.format(subArray[3])
      proj['nose5'] = '{:02x}'.format(subArray[4])
      proj['nose6'] = '{:02x}'.format(subArray[5])
      proj['vramTileOffset'] = '{:02x}'.format(subArray[6])
      proj['cantDosTiles'] = '{:02x}'.format(subArray[7])

      off_1 = subArray[8]
      off_2 = subArray[9]
      proj['offsetBank8'] = '{:04x}'.format(off_2*0x100 + off_1)

      addr_1 = subArray[10]
      addr_2 = subArray[11]
#      proj['addrSortTiles'] = '{:04x}'.format(addr_2*0x100 + addr_1)
      proj['idSortTiles'] = '{:04x}'.format(addr_2*0x100 + addr_1)

      addr2_1 = subArray[12]
      addr2_2 = subArray[13]
      proj['idSpriteGroup'] = '{:04x}'.format(addr2_2*0x100 + addr2_1)

      addr3_1 = subArray[14]
      addr3_2 = subArray[15]
      proj['idPattern'] = '{:04x}'.format(addr3_2*0x100 + addr3_1)

      self.jsonProjectiles['projectiles'].append(proj)
      currentAddr += 16

#    print('currentAddr: {:04x}'.format(currentAddr))



    # dictionary of sortTiles and patterns
    dicSortTiles = {}
    dicPattern = {}

    # en la primer iteración creo el dicSortTiles
    for proj in self.jsonProjectiles['projectiles']:
#      print('proj: ' + str(proj))
      addrSortTiles = int(proj['idSortTiles'],16)
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addrSortTiles: ' + strAddrSortTiles)
      dicSortTiles[strAddrSortTiles] = addrSortTiles #0x00

      addrPattern = int(proj['idPattern'],16)
      strAddrPattern = '{:04x}'.format(addrPattern)
#      print('addrPattern: ' + strAddrPattern)
      dicPattern[strAddrPattern] = addrPattern


#    print('dicSortTiles: ' + str(dicSortTiles))
    # sort the sortTiles according to their addr
    sortSortTiles = sorted(dicSortTiles.items())
#    print('sortSortTiles: ' + str(sortSortTiles))

#    print('dicPattern: ' + str(dicPattern))
    # sort the patterns according to their addr
    sortPattern = sorted(dicPattern.items())
#    print('sortPattern: ' + str(sortPattern))



    # size of the sortTiles table (in bytes)
    sizeSortTiles = 120
    # addr where the sortTiles table end
    addrSortTilesEnd = currentAddr + sizeSortTiles + 0x4000
#    print('addrSortTilesEnd: {:04x}'.format(addrSortTilesEnd))

    # the sorted addresses of the sortTiles
    sortedAddrs = [sort[1] for sort in sortSortTiles]
    # we add the last addr
    sortedAddrs.append(addrSortTilesEnd)
#    print('sortedAddrs: ' + str(sortedAddrs))


    self.jsonProjectiles['sortTiles'] = []
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

      self.jsonProjectiles['sortTiles'].append( {'idSortTiles': i, 'sorting' : strSortTiles } )


    # change the addr's of sortTiles to it's index number
    for proj in self.jsonProjectiles['projectiles']:
#      print('proj: ' + str(proj))
      addrSortTiles = int(proj['idSortTiles'],16)
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addrSortTiles: ' + strAddrSortTiles)
      idSortTiles = dicSortTiles[strAddrSortTiles]
#      print('addr: ' + strAddrSortTiles + ' id: ' + str(idSortTiles))
      proj['idSortTiles'] = idSortTiles

    currentAddr += sizeSortTiles
#    print('currentAddr: {:04x}'.format(currentAddr))


    dicSpriteGroup = {}
    # el dicSpriteGroup
    for proj in self.jsonProjectiles['projectiles']:
#      print('proj: ' + str(proj))
      addrSpriteGroup = int(proj['idSpriteGroup'],16)
      strAddrSpriteGroup = '{:04x}'.format(addrSpriteGroup)
#      print('addrSpriteGroup: ' + strAddrSpriteGroup)
      dicSpriteGroup[strAddrSpriteGroup] = addrSpriteGroup #0x00


#    print('dicSpriteGroup: ' + str(dicSpriteGroup))
    # sort according to their addr
    sortSpriteGroup = sorted(dicSpriteGroup.items())
#    print('sortSpriteGroup: ' + str(sortSpriteGroup))



    self.jsonProjectiles['spriteGroups'] = []

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

      projs = [proj for proj in self.jsonProjectiles['projectiles'] if proj['idSpriteGroup'] == strAddrSpriteGroup]
      comments = [proj['comment'] for proj in projs]
      spriteGroup['comment'] = str(comments)

      # update the idSpriteGroup of npcs
      for proj in projs:
        proj['idSpriteGroup'] = i


      sprites = []

      currentAddr = addrSpriteGroup-0x4000

      for j in range(0,4*2):
        subArray = bank[currentAddr:currentAddr+3]

        attrib = subArray[0]
        tile1 = subArray[1]
        tile2 = subArray[2]

        strAttrib = '{:02x}'.format(attrib)
        strTile1 = '{:02x}'.format(tile1)
        strTile2 = '{:02x}'.format(tile2)

        sprite = {'idSprite' : j, 'attrib' : strAttrib, 'tile1' : strTile1, 'tile2' : strTile2}
#        print('sprite: ' + str(sprite))
        sprites.append(sprite)
        currentAddr += 3
       
      spriteGroup['sprites'] = sprites
      self.jsonProjectiles['spriteGroups'].append(spriteGroup)
      i += 1


#    print('currentAddr: {:04x}'.format(currentAddr))


    # size of the patterns table (in bytes)
    sizePatterns = 87
    # addr where the patterns table end
    addrPatternEnd = currentAddr + sizePatterns + 0x4000
#    print('addrPatternEnd: {:04x}'.format(addrPatternEnd))

    # the sorted addresses of the patterns
    sortedPatterns = [sort[1] for sort in sortPattern]
    # we add the last addr
    sortedPatterns.append(addrPatternEnd)
#    print('sortedPatterns: ' + str(sortedPatterns))




    self.jsonProjectiles['patterns'] = []
    # and calculate the size of each pattern (as a difference between two consecutive addr)
    for i in range(0, len(sortedPatterns)-1):
      delta = sortedPatterns[i+1] - sortedPatterns[i]
      addrPattern = sortedPatterns[i]
      strAddrPattern = '{:04x}'.format(addrPattern)
#      print('addr ' + strAddrPattern + ' delta: ' + str(delta))

      dicPattern[strAddrPattern] = i

      pattern = bank[addrPattern-0x4000:addrPattern-0x4000+delta]
      strPattern = mystic.util.strHexa(pattern)
#      print('pattern: ' + strPattern)

      self.jsonProjectiles['patterns'].append( {'idPattern': i, 'pattern' : strPattern } )



    # change the addr's of patterns to it's index number
    for proj in self.jsonProjectiles['projectiles']:
#      print('proj: ' + str(proj))
      addrPattern = int(proj['idPattern'],16)
      strAddrPattern = '{:04x}'.format(addrPattern)
#      print('addrPattern: ' + strAddrPattern)
      idPattern = dicPattern[strAddrPattern]
#      print('addr: ' + strAddrPattern + ' id: ' + str(idPattern))
      proj['idPattern'] = idPattern


    currentAddr += sizePatterns
#    print('currentAddr: {:04x}'.format(currentAddr))




  def encodeRom(self, addrProjectiles):
    array = []

#    print('addrProjectiles: {:04x}'.format(addrProjectiles))

    currentAddr = addrProjectiles

    arrayProjectile = []

    for projectile in self.jsonProjectiles['projectiles']:
#      print('projectile: ' + str(projectile)) 

      subArray = []

      nose1 = int(projectile['nose1'],16)
      subArray.append(nose1)
      speedSleep = int(projectile['speedSleep'],16)
      subArray.append(speedSleep)

      nose3 = int(projectile['nose3'],16)
      subArray.append(nose3)
      nose4 = int(projectile['nose4'],16)
      subArray.append(nose4)
      nose5 = int(projectile['nose5'],16)
      subArray.append(nose5)
      nose6 = int(projectile['nose6'],16)
      subArray.append(nose6)
      vramTileOffset = int(projectile['vramTileOffset'],16)
      subArray.append(vramTileOffset)
      cantDosTiles = int(projectile['cantDosTiles'],16)
      subArray.append(cantDosTiles)

      offsetBank8 = int(projectile['offsetBank8'],16)
      subArray.append(offsetBank8%0x100)
      subArray.append(offsetBank8//0x100)


      idSortTiles = projectile['idSortTiles']
#      subArray.extend( [0x00, 0x00] )
#      subArray.append(addrSortTiles%0x100)
#      subArray.append(addrSortTiles//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
      subArray.append('idSortTiles[' + str(idSortTiles) + ']')
      subArray.append('idSortTiles[' + str(idSortTiles) + ']')

      idSpriteGroup = projectile['idSpriteGroup']
#      subArray.extend( [0x00, 0x00] )
#      subArray.append(addrSpriteGroup%0x100)
#      subArray.append(addrSpriteGroup//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
      subArray.append('idSpriteGroup[' + str(idSpriteGroup) + ']')
      subArray.append('idSpriteGroup[' + str(idSpriteGroup) + ']')

      idPattern = projectile['idPattern']
#      subArray.extend( [0x00, 0x00] )
#      subArray.append(addrPattern%0x100)
#      subArray.append(addrPattern//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
      subArray.append('idPattern[' + str(idPattern) + ']')
      subArray.append('idPattern[' + str(idPattern) + ']')


      arrayProjectile.extend(subArray)
      currentAddr += len(subArray)


#    print('currentAddr: {:04x}'.format(currentAddr))

    addrSortTile = currentAddr


    arraySortTiles = []

    # dictionary of sortTiles
    dicSortTiles = {}
    i = 0
    for sortTile in self.jsonProjectiles['sortTiles']:
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

    arraySpriteGroup = []

    i = 0
    for spriteGroup in self.jsonProjectiles['spriteGroups']:
#      print('spriteGroup: ' + spriteGroup['comment'])


      dicSpriteGrp[i] = currentAddr + 0x4000
#      print('dicSpriteGrp[' + str(i) + '] = {:04x}'.format(currentAddr + 0x4000))

      # and we add the used spriteGroups
      for sprite in spriteGroup['sprites']:
        attrib = int(sprite['attrib'],16)
        tile1 = int(sprite['tile1'],16)
        tile2 = int(sprite['tile2'],16)
        subArray = [attrib, tile1, tile2]
        arraySpriteGroup.extend(subArray)
        currentAddr += len(subArray)

      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))
    addrPattern = currentAddr

    arrayPattern = []

    # dictionary of patterns
    dicPattern = {}
    i = 0
    for pattern in self.jsonProjectiles['patterns']:
#      print(' --- pattern: ' + str(pattern))
      dicPattern[i] = currentAddr
      strPattern = pattern['pattern']
      subArray = mystic.util.hexaStr(strPattern.strip())
#      print('subArray: ' + mystic.util.strHexa(subArray))
      arrayPattern.extend(subArray)
      currentAddr += len(subArray)
      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))

    array.extend(arrayProjectile)
    array.extend(arraySortTiles)
    array.extend(arraySpriteGroup)
    array.extend(arrayPattern)


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

        elif(cosa.startswith('idPattern[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idS = int(cosa[idx0:idx1])
#          print('idS: ' + str(idS))
          addr = dicPattern[idS] + 0x4000

#          print('translating ' + str(idS) + ' into {:04x}'.format(addr))

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2





    return array



