import os

import mystic.variables



def _byteToVramDic(byteVal):
  """ returns vram dictionary version of byte value """

#  print('byteVal: {:02x} {:08b}'.format(byteVal, byteVal))

  strBinary = '{:08b}'.format(byteVal)
  tipo = int(strBinary[0:2],2)
  vram = int(strBinary[2:8],2)

#  print('tipo ' + str(tipo) + ' + vram ' + str(vram) + ' = byteVal {:02x}'.format(byteVal))

  return (tipo, vram)


def _vramDicToByte(dic):
  """ returns byte version of the vram dictionary """

  tipo = dic[0]
  vram = dic[1]

  strTipo = '{:02b}'.format(tipo)
  strVram = '{:06b}'.format(vram)

  strByte = strTipo + strVram
  byteVal = int(strByte,2)

#  print('tipo ' + str(tipo) + ' + vram ' + str(vram) + ' = byteVal {:02x}'.format(byteVal))

  return byteVal


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
class Bosses:
  """ representa la colección de los monstruos grandes """

  def __init__(self):
    self.jsonBosses = {}
    # parallel structure for data that ends up redundant
    self.jsonBossesParallel = {}
 
  def decodeRom(self, bank, currentAddr, numberBoss):

#    currentAddr = 0x0739

    self.jsonBosses = {}
    self.jsonBosses['boss'] = []

    self.jsonBossesParallel = {}
    self.jsonBossesParallel['boss'] = []


    for i in range(0,numberBoss):
      boss = {}
      bossParallel = {}

      subArray = bank[currentAddr : currentAddr+24]
      strHexa = mystic.util.strHexa(subArray)
#      print('boss: {:02x} - '.format(i) + strHexa)

      boss['idBoss'] = i #'{:02x}'.format(i)
      bossParallel['idBoss'] = i 
      boss['comment'] = mystic.variables.bosses[i]
      boss['speedSleep'] = '{:02x}'.format(subArray[0])
      boss['hp'] = '{:02x}'.format(subArray[1])
      boss['exp'] = '{:02x}'.format(subArray[2])
      boss['gp'] = '{:02x}'.format(subArray[3])

      bossParallel['cantSpriteBlocks'] = '{:02x}'.format(subArray[4])

      boss['projectile'] = '{:02x}'.format(subArray[5])

      scri_1 = subArray[6]
      scri_2 = subArray[7]
      boss['scriptDefeated'] = '{:04x}'.format(scri_2*0x100 + scri_1)

      boss['vramTileOffset'] = '{:02x}'.format(subArray[8])
      boss['cantDosTiles']   = '{:02x}'.format(subArray[9])

      offsetBank8_1 = subArray[10]
      offsetBank8_2 = subArray[11]
      boss['offsetBank8'] = '{:04x}'.format(offsetBank8_2*0x100 + offsetBank8_1)

      addrTile1     = subArray[12]
      addrTile2     = subArray[13]
#      boss['addrSortTiles'] = '{:04x}'.format(addrTile2*0x100 + addrTile1)
      boss['idSortTiles'] = '{:04x}'.format(addrTile2*0x100 + addrTile1)

      addrSpriteGrp1 = subArray[14]
      addrSpriteGrp2 = subArray[15]
#      boss['addrSpriteGroup'] = '{:04x}'.format(addrSpriteGrp2*0x100 + addrSpriteGrp1)
      boss['idSpriteGroup'] = '{:04x}'.format(addrSpriteGrp2*0x100 + addrSpriteGrp1)

      addrDam1  = subArray[16]
      addrDam2  = subArray[17]
      addrSpritesDamage = addrDam2*0x100 + addrDam1
#      print('addrSpritesDamage: ' + addrSpritesDamage)
      bossParallel['addrSpritesDamage'] = '{:04x}'.format(addrSpritesDamage)

      addrBeh_1  = subArray[18]
      addrBeh_2  = subArray[19]
#      boss['addrBehaviour'] = '{:04x}'.format(addrBeh_2*0x100 + addrBeh_1)
      bossParallel['addrBehaviour'] = '{:04x}'.format(addrBeh_2*0x100 + addrBeh_1)

      addrBeh_1  = subArray[20]
      addrBeh_2  = subArray[21]
#      boss['addrBehaviourStart'] = '{:04x}'.format(addrBeh_2*0x100 + addrBeh_1)
      bossParallel['addrBehaviourStart'] = '{:04x}'.format(addrBeh_2*0x100 + addrBeh_1)

      addrDeath_1  = subArray[22]
      addrDeath_2  = subArray[23]
#      boss['addrDeathAction'] = '{:04x}'.format(addrDeath_2*0x100 + addrDeath_1)
      bossParallel['addrDeathAction'] = '{:04x}'.format(addrDeath_2*0x100 + addrDeath_1)

#      print('boss: {:02x} - '.format(i) + str(boss))

      self.jsonBosses['boss'].append(boss)
      self.jsonBossesParallel['boss'].append(bossParallel)
      currentAddr += 24

#    print('currentAddr: {:04x}'.format(currentAddr))

    # the bosses spritesDamage dict without repetition
    bossSprites = {}

    for bossParallel in self.jsonBossesParallel['boss']:

      cantSpriteBlocks = int(bossParallel['cantSpriteBlocks'],16)
      addrSpritesDamage = int(bossParallel['addrSpritesDamage'],16)

      # set the entry in the spriteDamage dictionary
      bossSprites[addrSpritesDamage - 0x4000] = cantSpriteBlocks


#    print('bossSprites: ' + str(bossSprites))
    # sort the sprites according to their addr
    sortSprites = sorted(bossSprites.items())
#    print('sortSprites: ' + str(sortSprites))

    self.jsonBosses['spriteBlocks'] = []

    i = 0
    # for each spriteDamage sorted
    for addr, cantSprites in sortSprites:
      spritesDamage = {}

      spriteBosses = [boss for boss in self.jsonBossesParallel['boss'] if boss['addrSpritesDamage'] == '{:04x}'.format(addr+0x4000)]
      indices = [ self.jsonBossesParallel['boss'].index(sprBoss) for sprBoss in spriteBosses  ]
      bossesNames = [ mystic.variables.bosses[k] for k in indices ]

#      print('indices: ' + str(indices))

      # set the bosses spriteDamage
      for idx in indices:
        self.jsonBosses['boss'][idx]['idSpriteBlocks'] = i

      spritesDamage['idSpriteBlocks'] = i # '{:02}'.format(i)
      spritesDamage['comment'] = str(bossesNames)
#      print('addr: {:04x}'.format(addr + 0x4000))

      # the cantSprites is taken from the first boss to use it
      cantSpriteBlocks = int(self.jsonBossesParallel['boss'][indices[0]]['cantSpriteBlocks'],16)
#      print('cantSpriteBlocks: ' + str(cantSpriteBlocks))

      sprites = []
      for j in range(0, cantSpriteBlocks):
        damage = bank[addr + j*8:addr + (j+1)*8]
        spriteDamage = mystic.util.strHexa(damage)
#        print('spriteDamage: ' + spriteDamage)
        sprites.append(spriteDamage)

      spritesDamage['blocks'] = sprites
      currentAddr += 8*cantSpriteBlocks
      # and add the spritesDamage
      self.jsonBosses['spriteBlocks'].append(spritesDamage)
      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))

    # the bosses behaviours dict without repetition
    bossBehavs = {}

    for bossParallel in self.jsonBossesParallel['boss']:

      addrBehaviour = int(bossParallel['addrBehaviour'],16)
      addrBehaviourStart = int(bossParallel['addrBehaviourStart'],16)

      # set the entry in the dictionary
      bossBehavs[addrBehaviour - 0x4000] = bossParallel['addrBehaviour']
      bossBehavs[addrBehaviourStart - 0x4000] = bossParallel['addrBehaviourStart']


#    print('bossBehavs: ' + str(bossBehavs))
    # sort the sprites according to their addr
    sortBehavs = sorted(bossBehavs.items())
#    print('sortBehavs: ' + str(sortBehavs))

    self.jsonBosses['behaviours'] = []

    # dictionary of liveActions without repetition
    dicLiveAction = {}

    i = 0
    # for each behaviour sorted
    for addr, strAddr in sortBehavs:


      behavBosses = [boss for boss in self.jsonBossesParallel['boss'] if boss['addrBehaviour'] == '{:04x}'.format(currentAddr+0x4000)]
      indices = [ self.jsonBossesParallel['boss'].index(bBoss) for bBoss in behavBosses  ]
      bossesNames = [ mystic.variables.bosses[k] for k in indices ]

      startBosses = [boss for boss in self.jsonBossesParallel['boss'] if boss['addrBehaviourStart'] == '{:04x}'.format(currentAddr+0x4000)]
      indicesStart = [ self.jsonBossesParallel['boss'].index(bBoss) for bBoss in startBosses  ]
      bossesNamesStart = [ mystic.variables.bosses[k] for k in indicesStart ]

#      print('indicesBehav: ' + str(indices) + ' indicesBehavStart: ' + str(indicesStart) )
      comment = 'start: ' + str(bossesNamesStart) + ' behav: ' + str(bossesNames)

      # set the bosses behaviours
      for idx in indices:
        self.jsonBosses['boss'][idx]['idBehaviour'] = i
      for idx in indicesStart:
        self.jsonBosses['boss'][idx]['idBehaviourStart'] = i


      actionGroup = []
#      print('--- ' + str(i))
      while(True):
        # if it is the end of the list (it ends in 0xffff)
        if(bank[currentAddr] == 0xff):
          currentAddr += 2
          # break the loop
          break

        subArray = bank[currentAddr : currentAddr + 10]

        actionGrp = {}

        addr1 = subArray[1]*0x100 + subArray[0]
        addr2 = subArray[3]*0x100 + subArray[2]
        addr3 = subArray[5]*0x100 + subArray[4]
        addr4 = subArray[7]*0x100 + subArray[6]
        strAddr1 = '{:04x}'.format(addr1)
        strAddr2 = '{:04x}'.format(addr2)
        strAddr3 = '{:04x}'.format(addr3)
        strAddr4 = '{:04x}'.format(addr4)

        dicLiveAction[strAddr1] = addr1
        dicLiveAction[strAddr2] = addr2
        dicLiveAction[strAddr3] = addr3
        dicLiveAction[strAddr4] = addr4

        addrs = [addr1, addr2, addr3, addr4]
        strAddrs = ['{:04x}'.format(addr) for addr in addrs]
#        action['liveActions'] = ' '.join(strAddrs) #strAddrs
        actionGrp['idLiveAction'] = ' '.join(strAddrs) #strAddrs
        x = subArray[8]
        y = subArray[9]
        pos = [x,y]
        strPos = ['{:02x}'.format(coord) for coord in pos]
        actionGrp['position'] = ' '.join(strPos) #strPos
        actionGroup.append(actionGrp)

        currentAddr += 10 
#        strHexa = mystic.util.strHexa(subArray)
#        print('behav: ' + strHexa)


      self.jsonBosses['behaviours'].append({'idBehaviour': i, 'comment' : comment, 'actionGroups' : actionGroup})
      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))


    # the bosses death action dict without repetition
    bossDeathAction = {}

    for bossParallel in self.jsonBossesParallel['boss']:

      addrDeathAction = int(bossParallel['addrDeathAction'],16)

      # set the entry in the spriteDamage dictionary
      bossDeathAction[addrDeathAction - 0x4000] = bossParallel['addrDeathAction']




#    print('bossDeathAction: ' + str(bossDeathAction))
    # sort the deathActions according to their addr
    sortDeathAction = sorted(bossDeathAction.items())
#    print('sortDeathAction: ' + str(sortDeathAction))

    self.jsonBosses['deathAction'] = []

    # dictionary of directions
    dicDirection = {}
    # dictionary of boss layout
    dicLayout = {}

    i = 0
    # for each deathAction sorted
    for addr, strAddr in sortDeathAction:
#      print('strAddr: ' + strAddr)

      deathBosses = [boss for boss in self.jsonBossesParallel['boss'] if boss['addrDeathAction'] == '{:04x}'.format(addr+0x4000)]
      indices = [ self.jsonBossesParallel['boss'].index(dBoss) for dBoss in deathBosses  ]
      bossesNames = [ mystic.variables.bosses[k] for k in indices ]
#      print('bossesNames: ' + str(bossesNames))

      for idx in indices:
        self.jsonBosses['boss'][idx]['idDeathAction'] = i

      actions = []
#      print('--- ' + str(i))
      while(True):
        # if it is the end of the list (it ends in 0xffff)
        if(bank[currentAddr] == 0xff):
          currentAddr += 2
          # break the loop
          break


        subArray = bank[currentAddr : currentAddr + 5]

        cant = subArray[0]
        addrDirection = subArray[2]*0x100 + subArray[1]
        addrLayout = subArray[4]*0x100 + subArray[3]
 
        strCant = '{:02x}'.format(cant)
        strAddrDirection = '{:04x}'.format(addrDirection)
        strAddrLayout = '{:04x}'.format(addrLayout)

        dicDirection[strAddrDirection] = addrDirection
        dicLayout[strAddrLayout] = addrLayout

#        print('--- ' + strCant + ', ' + strAddrDirection + ', ' + strAddrLayout)
        actions.append( {'cant' : strCant, 'idDirection' : strAddrDirection, 'idLayout' : strAddrLayout} )

        currentAddr += 5

      self.jsonBosses['deathAction'].append({'idDeathAction': i, 'comment' : str(bossesNames), 'actions' : actions})
      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))


#    print('dicLiveAction: ' + str(dicLiveAction))
    # sort the liveActions according to their addr
    sortLiveAction = sorted(dicLiveAction.items())
#    print('sortLiveAction: ' + str(sortLiveAction))

    self.jsonBosses['liveAction'] = []

    i = 0
    # for each liveAction sorted
    for strAddr, addr in sortLiveAction:
#      print('strAddr: ' + strAddr + ' addr ' + str(addr))

      # we add the unused action 27
      if(i == 27):
        dicLiveAction['{:04x}'.format(currentAddr + 0x4000)] = i
        actions = []
        actions.append( {'cant' : "02", 'idDirection' : "6917", 'idLayout' : "6d9c"} )
        currentAddr += 6
        self.jsonBosses['liveAction'].append({'idLiveAction': i, 'actions' : actions})
        i += 1

#      currentAddr = addr - 0x4000 
      # change the dictionary to reflect it's id
#      dicLiveAction[strAddr] = i
      dicLiveAction['{:04x}'.format(currentAddr + 0x4000)] = i



      actions = []
#      print('--- ' + str(i))
      while(True):
        # if it is the end of the list (it ends in 0xff)
        if(bank[currentAddr] == 0xff):
          currentAddr += 1
          # break the loop
          break


        subArray = bank[currentAddr : currentAddr + 5]

        cant = subArray[0]
        addrDirection = subArray[2]*0x100 + subArray[1]
        addrLayout = subArray[4]*0x100 + subArray[3]
 
        strCant = '{:02x}'.format(cant)
        strAddrDirection = '{:04x}'.format(addrDirection)
        strAddrLayout = '{:04x}'.format(addrLayout)

        dicDirection[strAddrDirection] = addrDirection
        dicLayout[strAddrLayout] = addrLayout

#        print('--- ' + strCant + ', ' + strAddrDirection + ', ' + strAddrLayout)
        actions.append( {'cant' : strCant, 'idDirection' : strAddrDirection, 'idLayout' : strAddrLayout} )

        currentAddr += 5

      self.jsonBosses['liveAction'].append({'idLiveAction': i, 'actions' : actions})
      i += 1

#    print('dicLiveAction: ' + str(dicLiveAction))

#    sortedDic = dict(sorted(dicLiveAction.items(), key=lambda item: item[1]))
#    print('sortedDic: ' + str(sortedDic))

#    print('currentAddr: {:04x}'.format(currentAddr))

    i = 0
    for behav in self.jsonBosses['behaviours']:
#      print(' --- behav: ' + str(behav))
      for actionGrp in behav['actionGroups']:
#        print('actionGrp: ' + str(actionGrp))
        strLiveActionsAddr = actionGrp['idLiveAction']
#        print('strLiveActionsAddr: ' + strLiveActionsAddr)
#        liveActionsAddr = mystic.util.hexaStr(strLiveActionsAddr)
        liveActionsAddr = strLiveActionsAddr.split(' ')

#        print('liveActionsAddr: ' + str(liveActionsAddr))
        liveActions = [ dicLiveAction[addr] for addr in liveActionsAddr ]
#        print('liveActions: ' + str(liveActions))
        actionGrp['idLiveAction'] = ','.join( [ str(act) for act in liveActions  ]  )

 
#    print('dicDirection: ' + str(dicDirection))
    # sort the directions according to their addr
    sortDirection = sorted(dicDirection.items())
#    print('sortDirection: ' + str(sortDirection))

    self.jsonBosses['direction'] = []

    i = 0
    # for each direction sorted
    for strAddr, addr in sortDirection:
#      print('strAddr: ' + strAddr + ' addr ' + str(addr))

      # we add the unused direction 0
      if(i == 0):
        dicDirection['{:04x}'.format(currentAddr + 0x4000)] = i
        currentAddr += 3
        tipo, vram = _byteToVramDic(0x0c)
        self.jsonBosses['direction'].append({'idDirection': i, 'type' : tipo, 'vramSprite' : vram, '(dx,dy)':"(+0,+0)" } ) 
        i += 1
      elif(i == 96):
        dicDirection['{:04x}'.format(currentAddr + 0x4000)] = i
        currentAddr += 3
        tipo, vram = _byteToVramDic(0x19)
        self.jsonBosses['direction'].append({'idDirection': i, 'type' : tipo, 'vramSprite' : vram, '(dx,dy)':"(-4,+4)" } ) 
        i += 1
      elif(i == 106):
        dicDirection['{:04x}'.format(currentAddr + 0x4000)] = i
        currentAddr += 3
        tipo, vram = _byteToVramDic(0x02)
        self.jsonBosses['direction'].append({'idDirection': i, 'type' : tipo, 'vramSprite' : vram, '(dx,dy)':"(+4,+4)" } ) 
        i += 1

#      print('currentAddr: {:04x} addr {:04x}'.format(currentAddr, addr-0x4000))
#      subArray = bank[addr - 0x4000:]
      subArray = bank[currentAddr - 0x4000:]

      dicDirection[strAddr] = i

      vramSprite = subArray[0]
      tipo, vram = _byteToVramDic(vramSprite)
      direc = subArray[1]
      dx = direc // 0x10
      dy = direc % 0x10
      direc = (dx,dy)
      strDx = '+' + str(dx) if (dx < 7) else '-' + str(0x10 - dx)
      strDy = '+' + str(dy) if (dy < 7) else '-' + str(0x10 - dy)
      nose3 = subArray[2]

      currentAddr += 3
#      print(strAddr + ' vramSprite: ' + '{:02x}'.format(vramSprite) + ' direc: (dx,dy)=(' + strDx + ',' + strDy + ')')
#      self.jsonBosses['direction'].append({'idDirection': i, 'vramSprite': '{:02x}'.format(vramSprite), '(dx,dy)':"("+strDx+","+strDy+")" })

      self.jsonBosses['direction'].append({'idDirection': i, 'type' : tipo, 'vramSprite' : vram, '(dx,dy)':"("+strDx+","+strDy+")" })



      i += 1


#    print('currentAddr: {:04x}'.format(currentAddr))

#    print('dicDirection: ' + str(dicDirection))

    # we change the address of directions with it's index number
    for death in self.jsonBosses['deathAction']:
#      print(' --- death: ')
      for action in death['actions']:
#        print('action: ' + str(action))
        addrDirection = action['idDirection']
#        print('addrDirection: ' + addrDirection)
        idDirection = dicDirection[addrDirection]
#        print('idDirection: ' + str(idDirection))
        action['idDirection'] = idDirection
    for liveAction in self.jsonBosses['liveAction']:
#      print(' --- live: ')
      for action in liveAction['actions']:
#        print('action: ' + str(action))
        addrDirection = action['idDirection']
#        print('addrDirection: ' + addrDirection)
        idDirection = dicDirection[addrDirection]
#        print('idDirection: ' + str(idDirection))
        action['idDirection'] = idDirection
 

#    print('dicLayout: ' + str(dicLayout))
    # sort the layouts according to their addr
    sortLayout = sorted(dicLayout.items())
#    print('sortLayout: ' + str(sortLayout))

    self.jsonBosses['layout'] = []

    i = 0
    # for each layout sorted
    for strAddr, addr in sortLayout:

      # we add the unused layout 22
      if(i == 22):
        dicLayout['{:04x}'.format(currentAddr + 0x4000)] = i

        lays = []
        
        tipo, vram = _byteToVramDic(0x03)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f0'), 'y' : _strHexToSignedInt('f0')} )
        tipo, vram = _byteToVramDic(0x04)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('00'), 'y' : _strHexToSignedInt('f0')} )
        tipo, vram = _byteToVramDic(0x01)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f0'), 'y' : _strHexToSignedInt('00')} )
        tipo, vram = _byteToVramDic(0x0e)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f8'), 'y' : _strHexToSignedInt('d0')} )
        tipo, vram = _byteToVramDic(0x0e)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f8'), 'y' : _strHexToSignedInt('20')} )
        tipo, vram = _byteToVramDic(0x0f)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('20'), 'y' : _strHexToSignedInt('f8')} )
        tipo, vram = _byteToVramDic(0x0f)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('d0'), 'y' : _strHexToSignedInt('f8')} )

        currentAddr += 3*len(lays) + 1
        self.jsonBosses['layout'].append({'idLayout': i, 'lays': lays})
        i += 1
      elif(i == 86):
        dicLayout['{:04x}'.format(currentAddr + 0x4000)] = i

        lays = []

        for k in range(0, 9):
          tipo, vram = _byteToVramDic(0x13)
          lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f0'), 'y' : _strHexToSignedInt('00')} )
        currentAddr += 3*len(lays) + 1
        self.jsonBosses['layout'].append({'idLayout': i, 'lays': lays})
        i += 1
      elif(i == 88):
        dicLayout['{:04x}'.format(currentAddr + 0x4000)] = i

        lays = []

        tipo, vram = _byteToVramDic(0x11)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f0'), 'y' : _strHexToSignedInt('f0')} )
        tipo, vram = _byteToVramDic(0x10)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('00'), 'y' : _strHexToSignedInt('f0')} )
        for k in range(0, 7):
          tipo, vram = _byteToVramDic(0x12)
          lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f0'), 'y' : _strHexToSignedInt('00')} )
        currentAddr += 3*len(lays) + 1
        self.jsonBosses['layout'].append({'idLayout': i, 'lays': lays})
        i += 1

#      print('strAddr: ' + strAddr + ' addr ' + str(addr) + ' currentAddr {:04x}'.format(currentAddr) + ' ' + str(i))
      dicLayout['{:04x}'.format(currentAddr + 0x4000)] = i

      lays = []
#      print('--- ' + str(i))
      while(True):
        # if it is the end of the list (it ends in 0xff)
        if(bank[currentAddr] == 0xff):
          currentAddr += 1
          # break the loop
          break

        subArray = bank[currentAddr : currentAddr + 3]

        vramByte = subArray[0]
        x = subArray[1]
        y = subArray[2]

        tipo, vram = _byteToVramDic(vramByte)
        strX = '{:02x}'.format(x)
        strY = '{:02x}'.format(y)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt(strX), 'y' : _strHexToSignedInt(strY)} )
        currentAddr += 3

      self.jsonBosses['layout'].append({'idLayout': i, 'lays' : lays})
      i += 1


#    print('dicLayout: \n' + str(dicLayout))

    # we change the address of layouts with it's index number
    for death in self.jsonBosses['deathAction']:
#      print(' --- death: ')
      for action in death['actions']:
#        print('action: ' + str(action))
        addrLayout = action['idLayout']
#        print('addrLayout: ' + addrLayout)
        idLayout = dicLayout[addrLayout]
#        print('idLayout: ' + str(idLayout))
        action['idLayout'] = idLayout

    for liveAction in self.jsonBosses['liveAction']:
#      print(' --- live: ')
      for action in liveAction['actions']:
#        print('action: ' + str(action))
        addrLayout = action['idLayout']
#        print('addrLayout: ' + addrLayout)
        idLayout = dicLayout[addrLayout]
#        print('idLayout: ' + str(idLayout))
        action['idLayout'] = idLayout

#    print('currentAddr: {:04x}'.format(currentAddr))

    # dictionary of sortTiles
    dicSortTiles = {}

    # en la primer iteración creo el dicSortTiles
    for boss in self.jsonBosses['boss']:
#      print('boss: ' + str(boss))
      addrSortTiles = int(boss['idSortTiles'],16)
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addrSortTiles: ' + strAddrSortTiles)
      cantDosTiles = int(boss['cantDosTiles'],16)
      dicSortTiles[strAddrSortTiles] = addrSortTiles #0x00

#    print('dicSortTiles: ' + str(dicSortTiles))

    # en la segunda le seteo al dicSortTiles el máximo cantDosTiles usado (algunos bosses usan mas tiles que otros)
#    for boss in self.jsonBosses['boss']:
#      print('boss: ' + str(boss))
#      addrSortTiles = int(boss['addrSortTiles'],16)
#      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addrSortTiles: ' + strAddrSortTiles)
#      cantDosTiles = int(boss['cantDosTiles'],16)
#      oldCantDosTiles = dicSortTiles[strAddrSortTiles]
#      print(strAddrSortTiles + ' comparando {:02x} con el anterior {:02x}'.format(cantDosTiles, oldCantDosTiles))
      # si supera el valor anterior
#      if(cantDosTiles > oldCantDosTiles):
        # lo reemplazo
#        dicSortTiles[strAddrSortTiles] = cantDosTiles
#        print('pusimos {:02x} en '.format(cantDosTiles) + strAddrSortTiles)


#    print('dicSortTiles: ' + str(dicSortTiles))
    # sort the sortTiles according to their addr
    sortSortTiles = sorted(dicSortTiles.items())
#    print('sortSortTiles: ' + str(sortSortTiles))

    # size of the sortTiles table (in bytes)
    sizeSortTiles = 618
    # addr where the sortTiles table end
    addrSortTilesEnd = currentAddr + sizeSortTiles + 0x4000
#    print('addrSortTilesEnd: {:04x}'.format(addrSortTilesEnd))

    # the sorted addresses of the sortTiles
    sortedAddrs = [sort[1] for sort in sortSortTiles]
    # we add the last addr
    sortedAddrs.append(addrSortTilesEnd)
#    print('sortedAddrs: ' + str(sortedAddrs))

    self.jsonBosses['sortTiles'] = []
    # and calculate the size of each sortTile (as a difference between two consecutive addr)
    for i in range(0, len(sortedAddrs)-1):
      delta = sortedAddrs[i+1] - sortedAddrs[i]
      addrSortTiles = sortedAddrs[i]
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addr ' + strAddrSortTiles + ' delta: ' + str(delta))


      sortBosses = [boss for boss in self.jsonBosses['boss'] if boss['idSortTiles'] == strAddrSortTiles]
      indices = [ self.jsonBosses['boss'].index(sBoss) for sBoss in sortBosses  ]
      bossesNames = [ mystic.variables.bosses[k] for k in indices ]
#      print('bossesNames: ' + str(bossesNames))

      dicSortTiles[strAddrSortTiles] = i

      sortTiles = bank[addrSortTiles-0x4000:addrSortTiles-0x4000+delta]
      strSortTiles = mystic.util.strHexa(sortTiles)
#      print('sortTiles: ' + strSortTiles)

      self.jsonBosses['sortTiles'].append( {'idSortTiles': i, 'comment' : str(bossesNames), 'sorting' : strSortTiles } )

#    print('dicSortTiles: ' + str(dicSortTiles))


    # change the addr's of sortTiles to it's index number
    for boss in self.jsonBosses['boss']:
#      print('boss: ' + str(boss))
      addrSortTiles = int(boss['idSortTiles'],16)
      strAddrSortTiles = '{:04x}'.format(addrSortTiles)
#      print('addrSortTiles: ' + strAddrSortTiles)
      idSortTiles = dicSortTiles[strAddrSortTiles]
#      print('addr: ' + strAddrSortTiles + ' id: ' + str(idSortTiles))
      boss['idSortTiles'] = idSortTiles


    currentAddr += sizeSortTiles
#    print('currentAddr: {:04x}'.format(currentAddr))

    # dictionary of the boss sprites
    dicSpriteGroupAddr = {}
    # dictionary of how many sprites does the boss use (counting unused sprites in the middle)
    dicBossCantSprites = {}

    i = 0
    # change the addr's of sortTiles to it's index number
    for boss in self.jsonBosses['boss']:
#      print('-------- boss: ' + boss['comment'])

      strAddrSpriteGroup = boss['idSpriteGroup']

      dicSpriteGroupAddr[strAddrSpriteGroup] = strAddrSpriteGroup
      
      vramDic = {}
      actions = []
      behaviourStart = self.jsonBosses['behaviours'][boss['idBehaviourStart']]
      # agrego todas las actions de start
      for actionGrp in behaviourStart['actionGroups']:
        idLiveActions = actionGrp['idLiveAction'].split(',')
        idLiveActions = [int(live) for live in idLiveActions]
#        print('idLiveActions: ' + str(idLiveActions))
        liveActions = [self.jsonBosses['liveAction'][idLive] for idLive in idLiveActions]

        for live in liveActions:
          actions.extend(live['actions'])

        for action in actions:
#          print('action: ' + str(action))
          idDirec = action['idDirection']
#          print('idDirection: ' + str(idDirec))
          direc = self.jsonBosses['direction'][idDirec]
          vramDic[direc['vramSprite']] = 0x00
#          print('vramStart: ' + str(direc['vramSprite']))
          idLayout = action['idLayout']
          layout = self.jsonBosses['layout'][idLayout]
          lays = layout['lays']
#          print('lays: ' + str(lays))
          vrams = [lay['vramSprite'] for lay in lays]
#          print('vramsStart: ' + str(vrams))
          for vram in vrams:
            vramDic[vram] = 0x00


#      print('vramDic: ' + str(vramDic))
      # sort the vramDic
      sortDic = sorted(vramDic.items())
      vramStart = [vram[0] for vram in sortDic]
#      print('---vramStart: ' + str(vramStart))


      vramDic = {}
      actions = []
      behaviour = self.jsonBosses['behaviours'][boss['idBehaviour']]
      # agrego todas las actions de behaviour
      for actionGrp in behaviour['actionGroups']:
        idLiveActions = actionGrp['idLiveAction'].split(',')
        idLiveActions = [int(live) for live in idLiveActions]
#        print('idLiveActions: ' + str(idLiveActions))
        liveActions = [self.jsonBosses['liveAction'][idLive] for idLive in idLiveActions]

        for live in liveActions:
          actions.extend(live['actions'])

        for action in actions:
#          print('action: ' + str(action))
          idDirec = action['idDirection']
#          print('idDirection: ' + str(idDirec))
          direc = self.jsonBosses['direction'][idDirec]
          vramDic[direc['vramSprite']] = 0x00
#          print('vramBeh: ' + str(direc['vramSprite']))
          idLayout = action['idLayout']
          layout = self.jsonBosses['layout'][idLayout]
          lays = layout['lays']
#          print('lays: ' + str(lays))
          vrams = [lay['vramSprite'] for lay in lays]
#          print('vramsBeh: ' + str(vrams))
          for vram in vrams:
            vramDic[vram] = 0x00

#      print('vramDic: ' + str(vramDic))
      # sort the vramDic
      sortDic = sorted(vramDic.items())
      vramBeh = [vram[0] for vram in sortDic]
#      print('---vramBeh: ' + str(vramBeh))


      vramDic = {}
      actions = []
      # agrego todas las actions de death
      deathAction = self.jsonBosses['deathAction'][boss['idDeathAction']]
#      print('deathAction: ' + str(deathAction))
      actions.extend(deathAction['actions'])

      for action in actions:
#        print('action: ' + str(action))
        idDirec = action['idDirection']
#        print('idDirection: ' + str(idDirec))
        direc = self.jsonBosses['direction'][idDirec]
        vramDic[direc['vramSprite']] = 0x00
#        print('vramDeath: ' + str(direc['vramSprite']))
        idLayout = action['idLayout']
        layout = self.jsonBosses['layout'][idLayout]
        lays = layout['lays']
#        print('lays: ' + str(lays))
        vrams = [lay['vramSprite'] for lay in lays]
#        print('vramsDeath: ' + str(vrams))
        for vram in vrams:
          vramDic[vram] = 0x00

#      print('vramDic: ' + str(vramDic))
      # sort the vramDic
      sortDic = sorted(vramDic.items())
      vramDeath = [vram[0] for vram in sortDic]
#      print('---vramDeath: ' + str(vramDeath))


      vramBoss = {}
      for vram in vramStart:
        vramBoss[vram] = 0x00
      for vram in vramBeh:
        vramBoss[vram] = 0x00
      for vram in vramDeath:
        vramBoss[vram] = 0x00

      sortDic = sorted(vramBoss.items())
      vramBoss = [vram[0] for vram in sortDic]
#      print('-----vramBoss: ' + str(vramBoss))

      # the id of the last (higher id) sprite used by the boss
      lastSprite = vramBoss[len(vramBoss)-1]
#      print('lastSprite: ' + str(lastSprite))

      # set the last sprite of the boss
      dicBossCantSprites[i] = lastSprite+1

      i += 1


#    print('dicSpriteGroupAddr: ' + str(dicSpriteGroupAddr))
    sortSpriteGroup = sorted(dicSpriteGroupAddr.items())
    sortSpriteGroup = [sort[0] for sort in sortSpriteGroup]
#    print('sortSpriteGroup: ' + str(sortSpriteGroup))


    self.jsonBosses['spriteGroups'] = []
    for i in range(0, len(sortSpriteGroup)):

      strAddr = sortSpriteGroup[i]
#      print('strAddr: ' + strAddr)
      addr = int(strAddr,16)

      bosses = [boss for boss in self.jsonBosses['boss'] if boss['idSpriteGroup'] == strAddr]
      bossesNames = [boss['comment'] for boss in bosses]
#      print('bosses: ' + str(bossesNames))

      idBosses = [boss['idBoss'] for boss in bosses]
#      print('idBosses: ' + str(idBosses))

      # update the idSpriteGroup of the bosses
      for idBoss in idBosses:
        self.jsonBosses['boss'][idBoss]['idSpriteGroup'] = i

      # pick the first boss to read the quantity of sprites
#      boss = bosses[0]
      idBoss = idBosses[0] # boss['idBoss']
#      print('idBoss: ' + str(idBoss))
      cantSprites = dicBossCantSprites[idBoss]
#      print('cantSprites: ' + str(cantSprites))

      sprites = []
      for j in range(0, cantSprites):
        subArray = bank[currentAddr:currentAddr+3]
#        print('subArray: ' + mystic.util.strHexa(subArray))

        attrib = subArray[0]
        tile1 = subArray[1]
        tile2 = subArray[2]

        strAttrib = '{:02x}'.format(attrib)
        strTile1 = '{:02x}'.format(tile1)
        strTile2 = '{:02x}'.format(tile2)

        sprites.append({'idSprite' : j, 'attrib' : strAttrib, 'tile1' : strTile1, 'tile2' : strTile2})
        currentAddr += 3

      # for hydra
      if(i == 1):
        # we hardcode the unused sprite
        sprites.append({'idSprite' : j+1, 'attrib' : '10', 'tile1' : '3c', 'tile2' : '3e'})
        currentAddr += 3

      self.jsonBosses['spriteGroups'].append( {'idSpriteGroup' : i, 'comment' : str(bossesNames), 'sprites' : sprites} )


#    print('currentAddr: {:04x}'.format(currentAddr))




  def encodeRom(self, addrBosses):

    array = []

    currentAddr = addrBosses

    for boss in self.jsonBosses['boss']:
#      print('boss: ' + str(boss))
#      print('currentAddr: {:04x}'.format(currentAddr))

      subArray = []

      speedSleep = int(boss['speedSleep'],16)
      subArray.append(speedSleep)
      hp = int(boss['hp'],16)
      subArray.append(hp)
      exp = int(boss['exp'],16)
      subArray.append(exp)
      gp = int(boss['gp'],16)
      subArray.append(gp)

      idSpriteBlocks = boss['idSpriteBlocks']
#      cantSpriteBlocks = int(boss['cantSpriteBlocks'],16)
#      subArray.append(cantSpriteBlocks)
      subArray.append('cantSpriteBlocks[' + str(idSpriteBlocks) + ']')

      projectile = int(boss['projectile'],16)
      subArray.append(projectile)

      scriptDefeated = int(boss['scriptDefeated'],16)
      subArray.append(scriptDefeated%0x100)
      subArray.append(scriptDefeated//0x100)

      vramTileOffset = int(boss['vramTileOffset'],16)
      subArray.append(vramTileOffset)
      cantDosTiles = int(boss['cantDosTiles'],16)
      subArray.append(cantDosTiles)

      offsetBank8 = int(boss['offsetBank8'],16)
      subArray.append(offsetBank8%0x100)
      subArray.append(offsetBank8//0x100)

      idSortTiles = boss['idSortTiles']
#      subArray.extend( [0x00, 0x00] )
#      subArray.append(addrSortTiles%0x100)
#      subArray.append(addrSortTiles//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
      subArray.append('idSortTiles[' + str(idSortTiles) + ']')
      subArray.append('idSortTiles[' + str(idSortTiles) + ']')

      idSpriteGroup = boss['idSpriteGroup']
#      subArray.extend( [0x00, 0x00] )
#      addrSpriteGroup = int(boss['addrSpriteGroup'],16)
#      subArray.append(addrSpriteGroup%0x100)
#      subArray.append(addrSpriteGroup//0x100)
      subArray.append('idSpriteGroup[' + str(idSpriteGroup) + ']')
      subArray.append('idSpriteGroup[' + str(idSpriteGroup) + ']')

#      addrDamage = int(boss['addrSpritesDamage'],16)
#      subArray.append(addrDamage%0x100)
#      subArray.append(addrDamage//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
      subArray.append('idSpriteBlocks[' + str(idSpriteBlocks) + ']')
      subArray.append('idSpriteBlocks[' + str(idSpriteBlocks) + ']')

      idBehaviour = boss['idBehaviour']
#      addrBehaviour = int(boss['addrBehaviour'],16)
#      subArray.append(addrBehaviour%0x100)
#      subArray.append(addrBehaviour//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
#      subArray.extend([0x00, 0x00])
      subArray.append('idBehaviour[' + str(idBehaviour) + ']')
      subArray.append('idBehaviour[' + str(idBehaviour) + ']')

      idBehaviourStart = boss['idBehaviourStart']
#      addrBehaviourStart = int(boss['addrBehaviourStart'],16)
#      subArray.append(addrBehaviourStart%0x100)
#      subArray.append(addrBehaviourStart//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
#      subArray.extend([0x00, 0x00])
      subArray.append('idBehaviourStart[' + str(idBehaviourStart) + ']')
      subArray.append('idBehaviourStart[' + str(idBehaviourStart) + ']')


      idDeathAction = boss['idDeathAction']
#      addrDeath = int(boss['addrDeathAction'],16)
#      subArray.append(addrDeath%0x100)
#      subArray.append(addrDeath//0x100)
      # inserto dos veces porque debe ocupar 2 bytes
#      subArray.extend([0x00, 0x00])
      subArray.append('idDeathAction[' + str(idDeathAction) + ']')
      subArray.append('idDeathAction[' + str(idDeathAction) + ']')


      array.extend(subArray)
      currentAddr += len(subArray)


#    print('currentAddr: {:04x}'.format(currentAddr))

    # dictionary for labels of spriteDamages
    spritesAddrDic = {}

    i = 0
    for spriteBlock in self.jsonBosses['spriteBlocks']:
      # set the address of each spriteDamage
      spritesAddrDic[i] = currentAddr

      blocks = spriteBlock['blocks']
#      print('sprites: ' + str(sprites))
#      print('currentAddr: {:04x}'.format(currentAddr))

      subArray = []
      for strBlock in blocks:
        block = mystic.util.hexaStr(strBlock.strip())
#        print('block: ' + str(block))
        subArray.extend(block)

      array.extend(subArray)
      currentAddr += len(subArray)
      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))

    # dictionary for labels of behaviours
    behavAddrDic = {}

    i = 0
    for behav in self.jsonBosses['behaviours']:
#      print(' --- behav: ')
      # set the address of each behaviour
      behavAddrDic[i] = currentAddr

      subArray = []
      for actGrp in behav['actionGroups']:
        strAddrActions = actGrp['idLiveAction']
#        print('strAddrActions: ' + strAddrActions)
#        addrActions = mystic.util.hexaStr(strAddrActions)

        strActions = strAddrActions.split(',')
        idLiveActions = [int(action) for action in strActions]
#        print('strActions: ' + str(idLiveActions))


#        subArray.extend([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        subArray.append('idLiveAction[' + str(idLiveActions[0]) + ']')
        subArray.append('idLiveAction[' + str(idLiveActions[0]) + ']')

        subArray.append('idLiveAction[' + str(idLiveActions[1]) + ']')
        subArray.append('idLiveAction[' + str(idLiveActions[1]) + ']')

        subArray.append('idLiveAction[' + str(idLiveActions[2]) + ']')
        subArray.append('idLiveAction[' + str(idLiveActions[2]) + ']')

        subArray.append('idLiveAction[' + str(idLiveActions[3]) + ']')
        subArray.append('idLiveAction[' + str(idLiveActions[3]) + ']')

#        subArray.append(addrActions[0]%0x100)
#        subArray.append(addrActions[0]//0x100)
#        subArray.append(addrActions[1]%0x100)
#        subArray.append(addrActions[1]//0x100)
#        subArray.append(addrActions[2]%0x100)
#        subArray.append(addrActions[2]//0x100)
#        subArray.append(addrActions[3]%0x100)
#        subArray.append(addrActions[3]//0x100)

        strPos = actGrp['position']
        pos = mystic.util.hexaStr(strPos)
        subArray.append(pos[0])
        subArray.append(pos[1])

      # END of behaviours
      subArray.extend([0xff, 0xff])

      array.extend(subArray)
      currentAddr += len(subArray)
      i += 1


#    print('currentAddr: {:04x}'.format(currentAddr))


    # dictionary for labels of deathActions
    deathAddrDic = {}

    i = 0
    for death in self.jsonBosses['deathAction']:
#      print(' --- death: ')
      # set the address of each deathAction
      deathAddrDic[i] = currentAddr

      subArray = []
      for act in death['actions']:
#        print('act: ' + str(act))

        cant = int(act['cant'],16)
        idDirection = act['idDirection']
        idLayout = act['idLayout']

#        print('cant {:02x} idDirection {:04x} addrLayout {:04x}'.format(cant,idDirection,addrLayout))

        subArray.append(cant)

#        subArray.extend([0x00,0x00])
        subArray.append('idDirection[' + str(idDirection) + ']')
        subArray.append('idDirection[' + str(idDirection) + ']')
#        subArray.append(addrDirection%0x100)
#        subArray.append(addrDirection//0x100)

#        subArray.extend([0x00,0x00])
        subArray.append('idLayout[' + str(idLayout) + ']')
        subArray.append('idLayout[' + str(idLayout) + ']')
#        subArray.append(addrLayout%0x100)
#        subArray.append(addrLayout//0x100)

      # END of death
      subArray.extend([0xff, 0xff])

      array.extend(subArray)
      currentAddr += len(subArray)

      i += 1


#    print('currentAddr: {:04x}'.format(currentAddr))

    # dictionary for labels of liveActions
    liveAddrDic = {}

    i = 0
    for live in self.jsonBosses['liveAction']:
#      print(' --- live: ' + str(i) + ' {:04x}'.format(currentAddr))
      # set the address of each deathAction
      liveAddrDic[i] = currentAddr

      subArray = []
      for act in live['actions']:
#        print('act: ' + str(act))

        cant = int(act['cant'],16)
        idDirection = act['idDirection']
        idLayout = act['idLayout']

#        print('cant {:02x} addrDirection {:04x} addrLayout {:04x}'.format(cant,addrDirection,addrLayout))

        subArray.append(cant)

#        subArray.extend([0x00,0x00])
        subArray.append('idDirection[' + str(idDirection) + ']')
        subArray.append('idDirection[' + str(idDirection) + ']')
#        subArray.append(addrDirection%0x100)
#        subArray.append(addrDirection//0x100)

#        subArray.extend([0x00,0x00])
        subArray.append('idLayout[' + str(idLayout) + ']')
        subArray.append('idLayout[' + str(idLayout) + ']')
#        subArray.append(addrLayout%0x100)
#        subArray.append(addrLayout//0x100)

      # END of liveAction
      subArray.extend([0xff])

      array.extend(subArray)
      currentAddr += len(subArray)

      i += 1


#    print('currentAddr: {:04x}'.format(currentAddr))

    # dictionary of directions
    dicDirection = {}

    i = 0
    for direc in self.jsonBosses['direction']:
#      print(' --- direc: ' + str(direc) + ' {:04x} '.format(currentAddr) + str(i))

      dicDirection[i] = currentAddr

      subArray = []
      tipo = direc['type']
      vram = direc['vramSprite']
      vramVal = _vramDicToByte( (tipo, vram) )
      subArray.append(vramVal)

      dx = int(direc['(dx,dy)'][1:3],16)
      dy = int(direc['(dx,dy)'][4:6],16)

#      print('{:04x} vramSprite: {:02x}'.format(currentAddr, vramVal) + ' ' + str(dx) + ', ' + str(dy))

      dig1 = dx if dx >= 0 else 0x10 + dx
      dig2 = dy if dy >= 0 else 0x10 + dy
      ddir = dig1*0x10 + dig2

#      print('ddir: ' + str(ddir))

      subArray.append(ddir)
      subArray.append(0xff)

      array.extend(subArray)
      currentAddr += len(subArray)
      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))


    # dictionary of layouts
    dicLayout = {}

    i = 0
    for layout in self.jsonBosses['layout']:
#      print(' --- layout {:04x} '.format(currentAddr) + str(i))

      dicLayout[i] = currentAddr

      subArray = []
      for lay in layout['lays']:
#        print('lay: ' + str(lay))

        tipo = lay['type']
        vram = lay['vramSprite']

        byteVal = _vramDicToByte( (tipo, vram) )
        subArray.append(byteVal)

#        x = int(lay['x'],16)
#        y = int(lay['y'],16)

        intX = lay['x']
        strX = _signedIntToStrHex(intX)
        x = int(strX,16)

        intY = lay['y']
        strY = _signedIntToStrHex(intY)
        y = int(strY,16)

        subArray.append(x)
        subArray.append(y)

      subArray.append(0xff)
      array.extend(subArray)
      currentAddr += len(subArray)

      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))

    # dictionary of sortTiles
    dicSortTiles = {}

    i = 0
    for sortTile in self.jsonBosses['sortTiles']:
#      print(' --- sortTile: ' + str(sortTile))

      dicSortTiles[i] = currentAddr

      strSortT = sortTile['sorting']
      subArray = mystic.util.hexaStr(strSortT.strip())
#      print('subArray: ' + mystic.util.strHexa(subArray))

      array.extend(subArray)
      currentAddr += len(subArray)

      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))

    # dictionary of spriteGroups
    dicSpriteGrp = {}

    i = 0
    for group in self.jsonBosses['spriteGroups']:
#      print(' --- group: {:04x}'.format(currentAddr)) # + str(group))

      dicSpriteGrp[i] = currentAddr

      for sprite in group['sprites']:
#        print('sprite: ' + str(sprite))

        attrib = int(sprite['attrib'],16)
        tile1 = int(sprite['tile1'],16)
        tile2 = int(sprite['tile2'],16)
        subArray = [attrib, tile1, tile2]

        array.extend(subArray)
        currentAddr += len(subArray)


      i += 1

#    print('currentAddr: {:04x}'.format(currentAddr))


    # translate the labels into addresses
    for i in range(0, len(array)):
      cosa = array[i]
      if( isinstance(cosa, str) ):
#        print('cosa: ' + cosa)

        if(cosa.startswith('idSpriteBlocks[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idSprite = int(cosa[idx0:idx1])
#          print('idSprite: ' + str(idSprite))
          addr = spritesAddrDic[idSprite] + 0x4000

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

        elif(cosa.startswith('cantSpriteBlocks[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idSprite = int(cosa[idx0:idx1])
#          print('idSprite: ' + str(idSprite))
          sprites = self.jsonBosses['spriteBlocks'][idSprite]['blocks']
#          print('sprites: ' + str(sprites))
          array[i] = len(sprites)

        elif(cosa.startswith('idBehaviour[') or cosa.startswith('idBehaviourStart[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idBehav = int(cosa[idx0:idx1])
#          print('idBehav: ' + str(idBehav))
          addr = behavAddrDic[idBehav] + 0x4000

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

        elif(cosa.startswith('idDeathAction[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idDeath = int(cosa[idx0:idx1])
#          print('idDeath: ' + str(idDeath))
          addr = deathAddrDic[idDeath] + 0x4000

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

        elif(cosa.startswith('idLiveAction[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idLive = int(cosa[idx0:idx1])
#          print('idLive: ' + str(idLive))
          addr = liveAddrDic[idLive] + 0x4000

#          print('translating ' + str(idLive) + ' into {:04x}'.format(addr))

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

        elif(cosa.startswith('idDirection[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idD = int(cosa[idx0:idx1])
#          print('idD: ' + str(idD))
          addr = dicDirection[idD] + 0x4000

#          print('translating ' + str(idD) + ' into {:04x}'.format(addr))

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

        elif(cosa.startswith('idLayout[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idL = int(cosa[idx0:idx1])
#          print('idL: ' + str(idL))
          addr = dicLayout[idL] + 0x4000

#          print('translating ' + str(idL) + ' into {:04x}'.format(addr))

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

        elif(cosa.startswith('idSortTiles[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idS = int(cosa[idx0:idx1])
#          print('idS: ' + str(idS))
          addr = dicSortTiles[idS] + 0x4000

#          print('translating ' + str(idS) + ' into {:04x}'.format(addr))

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

        elif(cosa.startswith('idSpriteGroup[')):
          idx0 = cosa.index('[')+1
          idx1 = cosa.index(']')
          idS = int(cosa[idx0:idx1])

#          print('idS: ' + str(idS))
          addr = dicSpriteGrp[idS] + 0x4000

#          print('translating ' + str(idS) + ' into {:04x}'.format(addr))

          addr1 = addr%0x100
          addr2 = addr//0x100

          array[i] = addr1
          array[i+1] = addr2

    return array 


