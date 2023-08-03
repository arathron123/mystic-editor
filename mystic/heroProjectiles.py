import os

import mystic.variables



##########################################################
class HeroProjectiles:
  """ represents the list of hero-projectiles """

  def __init__(self):
    self.jsonHeroProjs = {}

  def decodeRom(self, bank, currentAddr):

    # currentAddr = 0x1dcd
    weaponAnimationsAddr = currentAddr
#    print('currentAddr: {:04x}'.format(currentAddr))
#    print('weaponAnimationsAddr: {:04x}'.format(weaponAnimationsAddr))

    self.jsonHeroProjs = {}

    self.jsonHeroProjs['weaponAnimations'] = []
    for i in range(0,16):
      weaponAnim = {}
#      weaponAnim['comment'] = mystic.variables.armas[i].encode('ascii', 'ignore').decode()
      weaponAnim['comment'] = mystic.variables.armas[i]
      data = bank[currentAddr]
      frame = data//0x10
      idAnimation = data%0x10
      weaponAnim['frame'] = frame
      weaponAnim['idAnimation'] = idAnimation
      self.jsonHeroProjs['weaponAnimations'].append(weaponAnim)
      currentAddr += 1

    itemAnimationsAddr = currentAddr
#    print('currentAddr: {:04x}'.format(currentAddr))
#    print('itemAnimationsAddr: {:04x}'.format(itemAnimationsAddr))

    self.jsonHeroProjs['itemAnimations'] = []
    for i in range(0,8*8):
      itemAnim = {}

      if(i < 8):
        label = mystic.variables.magias[i].encode('ascii', 'ignore').decode()
      else:
        label = mystic.variables.items[i-8].encode('ascii', 'ignore').decode()

      itemAnim['comment'] = label
      data = bank[currentAddr]
      frame = data//0x10
      idAnimation = data%0x10
      itemAnim['frame'] = frame
      itemAnim['idAnimation'] = idAnimation
      self.jsonHeroProjs['itemAnimations'].append(itemAnim)
      currentAddr += 1

    # we store the addrAnimations for later
#    addrAnimations = 0x1e1d
    addrAnimations = currentAddr
#    print('currentAddr: {:04x}'.format(currentAddr))
#    print('addrAnimations: {:04x}'.format(addrAnimations))


    # we jump the animations table for now
    currentAddr += 16*6*2

#    addrFire = 0x1edd
    addrFire = currentAddr
#    print('currentAddr: {:04x}'.format(currentAddr))
#    print('addrFire: {:04x}'.format(addrFire))


    fireListAddr = []
    for i in range(0,16):
      addr = bank[currentAddr+1]*0x100 + bank[currentAddr]
      strAddr = '{:04x}'.format(addr)
      fireListAddr.append(strAddr)
#      print('addr: ' + strAddr )
      currentAddr += 2


#    print('currentAddr: {:04x}'.format(currentAddr))
#    addrFireList = 0x1efd
    addrFireList = currentAddr

    self.jsonHeroProjs['fire_animations'] = []

    for i in range(0,16):
      dxdy = 0xffff
#      print('----')
      fireDxdy = {}
      fireDxdy['idFireAnim'] = i
      fireDxdy['currentAddr'] = '{:02x}'.format(currentAddr)
      incrementsDxDy = []
      while(dxdy != 0x0000):


        dx = bank[currentAddr + 0]
        dy = bank[currentAddr + 1]
        incrementsDxDy.append(['{:02x}'.format(dx), '{:02x}'.format(dy)])
        dxdy = dx*0x100+dy

        strDxdy = '{:02x} {:02x}'.format(dx,dy)
#        print('dxdy: ' + strDxdy)
        currentAddr += 2

      fireDxdy['incrementsDxDy'] = str(incrementsDxDy)
      self.jsonHeroProjs['fire_animations'].append(fireDxdy)


    # we rewind to the addrAnimations
    currentAddr = addrAnimations
    animationsAddr = []

    # for each of the 6 frames
    for j in range(0,6):
#      print('----')
      row = []
      # for each of the 16 animations
      for i in range(0,16):
        addr = bank[currentAddr+1]*0x100 + bank[currentAddr]
        strAddr = '{:04x}'.format(addr)
#        print('addr: ' + strAddr )
        row.append(strAddr)
        currentAddr += 2
      animationsAddr.append(row)


    dicAnimationFrame = {}
    # for each of the 16 animations
    for i in range(0,16):
      animLabel = mystic.variables.hero_projs_animation[i]
#      print('animation: ' + animLabel)
      # for each of the 6 frames
      for j in range(0,6):
        addr = animationsAddr[j][i]
#        print('addr: ' + addr)
        dicAnimationFrame[addr] = addr


#    print('dicAnimationFrame: ' + str(dicAnimationFrame))
    # sort the animations according to their addr
    sortAnimationFrames = sorted(dicAnimationFrame.items())
#    print('sortAnimationFrame: ' + str(sortAnimationFrames))


    # the sorted addresses of the sortAnimations
    sortedAddrs = [sort[1] for sort in sortAnimationFrames]
#    print('sortedAddrs: ' + str(sortedAddrs))

    # if it has a NULL address
    if(sortedAddrs[0] == '0000'):
      # we delete it from the list of real animation addrs
      sortedAddrs = sortedAddrs[1:]

    dicBehaviours = {}
    dicSortTiles = {}

    self.jsonHeroProjs['animations'] = []
    self.jsonHeroProjs['animationFrames'] = []
    for i in range(0, len(sortedAddrs)):
      animationFrame = {}
      animationFrame['idAnimationFrame'] = i
      animationFrame['comment'] = mystic.variables.hero_projectile_frame[i]
 
      strAddr = sortedAddrs[i]
      dicAnimationFrame[strAddr] = i
      addr = int(strAddr,16)-0x4000
#      print('addr: {:04x}'.format(addr))

      animationFrame['speedSleep'] = '{:02x}'.format(bank[addr+0])

      animationFrame['collisionFlags'] = '{:02x}'.format(bank[addr+1])
      animationFrame['vramSlot'] = '{:02x}'.format(bank[addr+2])

      animationFrame['noseBytes'] = mystic.util.strHexa(bank[addr+3:addr+6])

      offsetBank7 = bank[addr+7]*0x100 + bank[addr+6]
#      print('offsetBank7: {:04x}'.format(offsetBank7))
      animationFrame['offsetBank7'] = '{:04x}'.format(offsetBank7)

      addrSortTiles = bank[addr+9]*0x100 + bank[addr+8]
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
      dicSortTiles[strAddrSortTiles] = addrSortTiles
#      animation['addrSortTiles'] = strAddrSortTiles
      animationFrame['idSortTiles'] = strAddrSortTiles


      addrs = []
      for j in range(0,4):
        addrBeh = bank[addr+11+j*2]*0x100 + bank[addr+11+j*2-1]
        strAddrBeh = '{:04x}'.format(addrBeh)
        dicBehaviours[strAddrBeh] = strAddrBeh
        addrs.append(strAddrBeh)
      # straight attack east,west,north,south
      animationFrame['idBehaviourStraightAttackEastWestNorthSouth'] = addrs

      addrs = []
      for j in range(4,8):
        addrBeh = bank[addr+11+j*2]*0x100 + bank[addr+11+j*2-1]
        strAddrBeh = '{:04x}'.format(addrBeh)
        dicBehaviours[strAddrBeh] = strAddrBeh
        addrs.append(strAddrBeh)
      # straight attack east,west,north,south
      animationFrame['idBehaviourSlideAttackEastWestNorthSouth'] = addrs

      addrs = []
      for j in range(8,12):
        addrBeh = bank[addr+11+j*2]*0x100 + bank[addr+11+j*2-1]
        strAddrBeh = '{:04x}'.format(addrBeh)
        dicBehaviours[strAddrBeh] = strAddrBeh
        addrs.append(strAddrBeh)
      # straight attack east,west,north,south
      animationFrame['idBehaviourSpecialStraightAttackEastWestNorthSouth'] = addrs

      addrs = []
      for j in range(12,16):
        addrBeh = bank[addr+11+j*2]*0x100 + bank[addr+11+j*2-1]
        strAddrBeh = '{:04x}'.format(addrBeh)
        dicBehaviours[strAddrBeh] = strAddrBeh
        addrs.append(strAddrBeh)
      # straight attack east,west,north,south
      animationFrame['idBehaviourSpecialSlideAttackEastWestNorthSouth'] = addrs

      self.jsonHeroProjs['animationFrames'].append(animationFrame)




    currentAddr = addr+42
#    addrSortTiles = 0x28df
    addrSortTiles = currentAddr
#    print('addrSortTiles: {:04x}'.format(addrSortTiles))


#    print('dicAnimationFrame: ' + str(dicAnimationFrame))

    currentAddr = addrAnimations
    rows = []
    # for each of the 6 frames
    for j in range(0,6):
#      print('----')
      row = []
      # for each of the 16 animations
      for i in range(0,16):
        addr = bank[currentAddr+1]*0x100 + bank[currentAddr]
        strAddr = '{:04x}'.format(addr)
#        print('addr: ' + strAddr )
        if(addr == 0x0000):
          idAnimationFrame = -1
        else:
          idAnimationFrame = dicAnimationFrame[strAddr]
#        print('idAnimation: ' + str(idAnimation))
        row.append(idAnimationFrame)
        currentAddr += 2
      rows.append(row)

#    print('rows: ' + str(rows))

    # for each of the 16 animations
    for i in range(0,16):
      animation = {}
      animation['idAnimation'] = i
      animation['comment'] = mystic.variables.hero_projs_animation[i]
      animation['idAnimationFrames'] = []
#      print('----')
      # for each of the 6 frames
      for j in range(0,6):
        idAnimationFrame = rows[j][i]
#        print('idAnimationFrame: ' + str(idAnimationFrame))
        animation['idAnimationFrames'].append(idAnimationFrame)
      self.jsonHeroProjs['animations'].append(animation)


#    print('dicSortTiles: ' + str(dicSortTiles))
    # sort the sortTiles according to their addr
    sortSortTiles = sorted(dicSortTiles.items())
#    print('sortSortTiles: ' + str(sortSortTiles))



    currentAddr = addrSortTiles
    # size of the sortTiles table (in bytes)
    sizeSortTiles = 16*12
    # addr where the sortTiles table end
    addrSortTilesEnd = currentAddr + sizeSortTiles + 0x4000
#    print('addrSortTilesEnd: {:04x}'.format(addrSortTilesEnd))

    # the sorted addresses of the sortTiles
    sortedAddrs = [sort[1] for sort in sortSortTiles]
    # we add the last addr
    sortedAddrs.append(addrSortTilesEnd)
#    print('sortedAddrs: ' + str(sortedAddrs))


    self.jsonHeroProjs['sortTiles'] = []
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

      self.jsonHeroProjs['sortTiles'].append( {'idSortTiles': i, 'sorting' : strSortTiles } )


    # change the addr's of sortTiles to it's index number
    for h in self.jsonHeroProjs['animationFrames']:
#      print('h: ' + str(h))
      addrSortTiles = int(h['idSortTiles'],16)
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addrSortTiles: ' + strAddrSortTiles)
      idSortTiles = dicSortTiles[strAddrSortTiles]
#      print('addr: ' + strAddrSortTiles + ' id: ' + str(idSortTiles))
      h['idSortTiles'] = idSortTiles



#    print('dicBehaviours: ' + str(dicBehaviours))
    # sort the behaviours according to their addr
    sortBehaviours = sorted(dicBehaviours.items())
#    print('sortBehaviours: ' + str(sortBehaviours))


    # the sorted addresses of the sortBehaviours
    sortedAddrs = [sort[1] for sort in sortBehaviours]
#    print('sortedAddrs: ' + str(sortedAddrs))

    currentAddr += sizeSortTiles

    self.jsonHeroProjs['behaviours'] = []
    i = 0
    for strAddr in sortedAddrs:

      # we add the unused behaviour 30
      if(i == 30):
        behaviour = {}
        behaviour['idBehaviour'] = i
        behaviour['currentAddr'] = '{:04x}'.format(currentAddr+2)
        cmds = []

        cmds.append('sound: {:02x}'.format(0x00))
        cmds.append('heroAction: {:02x}'.format(0x50))
        cmds.append('projSprite,yy,xx: ' + mystic.util.strHexa([0x11,0x00,0x00]))
        cmds.append('heroAction: {:02x}'.format(0x50))
        cmds.append('projSprite,yy,xx: ' + mystic.util.strHexa([0x11,0x00,0x00]))
        cmds.append('heroAction: {:02x}'.format(0x50))
        cmds.append('projSprite,yy,xx: ' + mystic.util.strHexa([0x12,0x00,0x00]))
        cmds.append('heroAction: {:02x}'.format(0x50))
        cmds.append('projSprite,yy,xx: ' + mystic.util.strHexa([0x12,0x00,0x00]))
        cmds.append('heroAction: {:02x}'.format(0x50))
        cmds.append('projSprite,yy,xx: ' + mystic.util.strHexa([0x11,0x00,0x00]))
        cmds.append('heroAction: {:02x}'.format(0x58))
        cmds.append('projSprite,yy,xx: ' + mystic.util.strHexa([0x11,0x00,0x00]))
        cmds.append('heroAction: {:02x}'.format(0x50))
        cmds.append('END')


        dicBehaviours['{:04x}'.format(currentAddr+0x4000)] = i
        behaviour['cmds'] = cmds
        self.jsonHeroProjs['behaviours'].append(behaviour)

        currentAddr += 27
        i += 1


      behaviour = {}
      behaviour['idBehaviour'] = i
      behaviour['currentAddr'] = '{:04x}'.format(currentAddr+2)
      cmds = []


      dicBehaviours['{:04x}'.format(currentAddr+2+0x4000)] = i
      
#      print('currentAddr: {:04x}'.format(currentAddr))

      sound = bank[currentAddr]
      cmds.append('sound: {:02x}'.format(sound))
      currentAddr += 1

      cmd = -1
      turnoHero = True
      thrownAxe = False
      ended = False
      while(not ended):
        cmd = bank[currentAddr]
        cmd1 = cmd//0x10
        cmd2 = cmd%0x10

        # if it is a heroAction command
        if(turnoHero and not thrownAxe):
          turnoHero = False
          heroAction = cmd
          cmds.append('heroAction: {:02x}'.format(heroAction))
          currentAddr += 1

          action = cmd2
          # if action is thrown axe
          if(action == 0x4):
            # we indicate it
            cmds.append('speed: {:02x}'.format(bank[currentAddr]))
            thrownAxe = True
            currentAddr += 1
        # else
        else:

          if(cmd == 0x00):
            cmds.append('END')
            currentAddr += 1
            ended = True
          # else, it is a projSprite command
          else:
            turnoHero = True
            projSprite = cmd
            yy = bank[currentAddr+1]
            xx = bank[currentAddr+2]
            cmds.append('projSprite,yy,xx: ' + mystic.util.strHexa([projSprite,yy,xx]))
            currentAddr += 3



      i += 1
      behaviour['cmds'] = cmds
#      behaviour['sound'] = '{:02x}'.format(bank[addr])

      self.jsonHeroProjs['behaviours'].append(behaviour)






    # change the addr's of behaviours to it's index number
    for h in self.jsonHeroProjs['animationFrames']:
#      print('h: ' + str(h))

      ids = []
      for strAddrBeh in h['idBehaviourStraightAttackEastWestNorthSouth']:
#        print('strAddrBeh: ' + strAddrBeh)
        idBeh = dicBehaviours[strAddrBeh]
        ids.append(idBeh)
      h['idBehaviourStraightAttackEastWestNorthSouth'] = ids

      ids = []
      for strAddrBeh in h['idBehaviourSlideAttackEastWestNorthSouth']:
#        print('strAddrBeh: ' + strAddrBeh)
        idBeh = dicBehaviours[strAddrBeh]
        ids.append(idBeh)
      h['idBehaviourSlideAttackEastWestNorthSouth'] = ids

      ids = []
      for strAddrBeh in h['idBehaviourSpecialStraightAttackEastWestNorthSouth']:
#        print('strAddrBeh: ' + strAddrBeh)
        idBeh = dicBehaviours[strAddrBeh]
        ids.append(idBeh)
      h['idBehaviourSpecialStraightAttackEastWestNorthSouth'] = ids

      ids = []
      for strAddrBeh in h['idBehaviourSpecialSlideAttackEastWestNorthSouth']:
#        print('strAddrBeh: ' + strAddrBeh)
        idBeh = dicBehaviours[strAddrBeh]
        ids.append(idBeh)
      h['idBehaviourSpecialSlideAttackEastWestNorthSouth'] = ids



  def encodeRom(self, addrHeroProjs):
    array = []

#    print('addrHeroProjs: {:04x}'.format(addrHeroProjs))
    currentAddr = addrHeroProjs


    arrayWeaponAnimations = []
    for w in self.jsonHeroProjs['weaponAnimations']:
#      print('w: ' + str(w)) 
      frame = w['frame']
      idAnimation = w['idAnimation']
      data = frame*0x10 + idAnimation
      arrayWeaponAnimations.append(data)
      currentAddr += 1

    arrayItemAnimations = []
    for it in self.jsonHeroProjs['itemAnimations']:
#      print('it: ' + str(it)) 
      frame = it['frame']
      idAnimation = it['idAnimation']
      data = frame*0x10 + idAnimation
      arrayItemAnimations.append(data)
      currentAddr += 1

    addrAnimations = currentAddr
#    print('currentAddr: {:04x}'.format(currentAddr))
#    print('addrAnimations: {:04x}'.format(addrAnimations))



    # we jump the animations table for now
    currentAddr += 16*6*2
#    print('currentAddr: {:04x}'.format(currentAddr))
#    addrFire = 0x1edd
    addrFire = currentAddr
#    print('addrFire: {:04x}'.format(addrFire))

    # we jump the fire addr table
    currentAddr += 2*len(self.jsonHeroProjs['fire_animations'])
#    print('currentAddr: {:04x}'.format(currentAddr))
#    addrFireList = 0x1efd
    addrFireList = currentAddr
#    print('addrFireList: {:04x}'.format(addrFireList))


    arrayFireAddr = []
    arrayFire = []
    for f in self.jsonHeroProjs['fire_animations']:
#      print('currentAddr: {:04x}'.format(currentAddr))
      fireAddr = currentAddr + 0x4000
      arrayFireAddr.extend([fireAddr%0x100, fireAddr//0x100])
      incrementsDxDy = f['incrementsDxDy']
#      print('inc: ' + incrementsDxDy)
      # we parse the list-string
      jInc = eval(incrementsDxDy)
#      print('jInc: ' + str(jInc))
      subArray = []
      for dxdy in jInc:
        dx = int(dxdy[0],16)
        dy = int(dxdy[1],16)
#        print('dx: ' + dxdy[0] + ' dy: ' + dxdy[1])
        subArray.extend([dx,dy])
      arrayFire.extend(subArray)
      currentAddr += len(subArray)


#    print('currentAddr: {:04x}'.format(currentAddr))
#    addrAnimationFrames = 0x20ff
    addrAnimationFrames = currentAddr
#    print('addrAnimationFrames: {:04x}'.format(addrAnimationFrames))

    # we create the dicAnimationFrame
    dicAnimationFrame = {}
    i = 0
    for animFrame in self.jsonHeroProjs['animationFrames']:
#      print('animFrame: ' + str(animFrame))
      strAddr = '{:04x}'.format(currentAddr+0x4000)
      dicAnimationFrame[i] = currentAddr
#      arrayAnimationsAddr.extend([currentAddr%0x100, currentAddr//0x100])
      currentAddr += 42
      i += 1
#    print('dicAnimationFrame: ' + str(dicAnimationFrame))


    # we encode the animations addr list
    arrayAnimationsAddr = []
    # for each of the 6 frames
    for j in range(0,6):
#      print('---')
      # for each of the 16 animations
      for i in range(0,16):
        anim = self.jsonHeroProjs['animations'][i]
        idFrame = anim['idAnimationFrames'][j]
#        print('idFrame: ' + str(idFrame))
        addrFrame = 0x0000
        if(idFrame != -1):
          addrFrame = dicAnimationFrame[idFrame] + 0x4000
#        print('addrFrame: {:04x}'.format(addrFrame)) 
        arrayAnimationsAddr.extend([addrFrame%0x100, addrFrame//0x100])


#    print('currentAddr: {:04x}'.format(currentAddr))
#    addrSortTiles = 0x28df
    addrSortTiles = currentAddr
#    print('addrSortTiles: {:04x}'.format(addrSortTiles))

    arraySortTiles = []
    dicSortTiles = {}
    i = 0
    for sortTile in self.jsonHeroProjs['sortTiles']:
      dicSortTiles[i] = currentAddr
      strSortT = sortTile['sorting']
      subArray = mystic.util.hexaStr(strSortT.strip())
#      print('subArray: ' + mystic.util.strHexa(subArray))
      arraySortTiles.extend(subArray)
      currentAddr += len(subArray)
      i += 1

#    print('dicSortTiles: ' + str(dicSortTiles))


#    currentAddr = addrAnimationFrames
#    currentAddr += 42*len(self.jsonHeroProjs['animationFrames'])


#    print('currentAddr: {:04x}'.format(currentAddr))
#    addrBehaviours = 0x299f
    addrBehaviours = currentAddr
#    print('addrBehaviours: {:04x}'.format(addrBehaviours))

    arrayBehaviours = []
    dicBehaviours = {}
    i = 0
    for beh in self.jsonHeroProjs['behaviours']:
#      print('beh: ' + str(beh))
      dicBehaviours[i] = '{:04x}'.format(currentAddr+2+0x4000)
      subArray = []
      for cmd in beh['cmds']:
        if(cmd == 'END'):
          subArray.append(0x00)
        else:
          idx0 = cmd.index(':')+1
          strCmd = cmd[idx0:].strip()
          cmdArray = mystic.util.hexaStr(strCmd)
#          print('cmd: ' + mystic.util.strHexa(cmdArray))
          subArray.extend(cmdArray)

      arrayBehaviours.extend(subArray)
      currentAddr += len(subArray)
      i += 1

#    print('dicBehaviours: ' + str(dicBehaviours))



    arrayFrames = []
    for f in self.jsonHeroProjs['animationFrames']:
#      print('f: ' + str(f))
      subArray = []

      speedSleep = int(f['speedSleep'],16)
      subArray.append(speedSleep)
      collisionFlags = int(f['collisionFlags'],16)
      subArray.append(collisionFlags)
      vramSlot = int(f['vramSlot'],16)
      subArray.append(vramSlot)
      noseBytes = mystic.util.hexaStr(f['noseBytes'])
      subArray.extend(noseBytes)
      offsetBank7 = int(f['offsetBank7'],16)
      subArray.append(offsetBank7%0x100)
      subArray.append(offsetBank7//0x100)

      idSortTiles = f['idSortTiles']
#      print('idSortTiles: ' + str(idSortTiles))
      addrSortTiles = dicSortTiles[idSortTiles]+0x4000
#      print('addrSortTiles: {:04x}'.format(addrSortTiles))
      subArray.append(addrSortTiles%0x100)
      subArray.append(addrSortTiles//0x100)

      for idB in f['idBehaviourStraightAttackEastWestNorthSouth']:
#        print('idB: ' + str(idB))
        addrB = dicBehaviours[idB]
#        print('addrB: ' + addrB)
        addrB = int(addrB,16)
#        print('addrB: {:04x}'.format(addrB))
        subArray.append(addrB%0x100)
        subArray.append(addrB//0x100)

      for idB in f['idBehaviourSlideAttackEastWestNorthSouth']:
        addrB = dicBehaviours[idB]
        addrB = int(addrB,16)
        subArray.append(addrB%0x100)
        subArray.append(addrB//0x100)

      for idB in f['idBehaviourSpecialStraightAttackEastWestNorthSouth']:
        addrB = dicBehaviours[idB]
        addrB = int(addrB,16)
        subArray.append(addrB%0x100)
        subArray.append(addrB//0x100)

      for idB in f['idBehaviourSpecialSlideAttackEastWestNorthSouth']:
        addrB = dicBehaviours[idB]
        addrB = int(addrB,16)
        subArray.append(addrB%0x100)
        subArray.append(addrB//0x100)

      arrayFrames.extend(subArray)


    array.extend(arrayWeaponAnimations)
    array.extend(arrayItemAnimations)
    array.extend(arrayAnimationsAddr)
    array.extend(arrayFireAddr)
    array.extend(arrayFire)
    array.extend(arrayFrames)
    array.extend(arraySortTiles)
    array.extend(arrayBehaviours)

    return array

