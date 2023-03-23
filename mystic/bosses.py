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

def _signedIntoToStrHex(sInt):
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
 
  def decodeRom(self, bank, vaPorAddr, cantBosses):

#    vaPorAddr = 0x0739

    self.jsonBosses = {}
    self.jsonBosses['boss'] = []

    self.jsonBossesParallel = {}
    self.jsonBossesParallel['boss'] = []


    for i in range(0,cantBosses):
      boss = {}
      bossParallel = {}

      subArray = bank[vaPorAddr : vaPorAddr+24]
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
      vaPorAddr += 24

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

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
      vaPorAddr += 8*cantSpriteBlocks
      # and add the spritesDamage
      self.jsonBosses['spriteBlocks'].append(spritesDamage)
      i += 1

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

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


      behavBosses = [boss for boss in self.jsonBossesParallel['boss'] if boss['addrBehaviour'] == '{:04x}'.format(vaPorAddr+0x4000)]
      indices = [ self.jsonBossesParallel['boss'].index(bBoss) for bBoss in behavBosses  ]
      bossesNames = [ mystic.variables.bosses[k] for k in indices ]

      startBosses = [boss for boss in self.jsonBossesParallel['boss'] if boss['addrBehaviourStart'] == '{:04x}'.format(vaPorAddr+0x4000)]
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
        if(bank[vaPorAddr] == 0xff):
          vaPorAddr += 2
          # break the loop
          break

        subArray = bank[vaPorAddr : vaPorAddr + 10]

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

        vaPorAddr += 10 
#        strHexa = mystic.util.strHexa(subArray)
#        print('behav: ' + strHexa)


      self.jsonBosses['behaviours'].append({'idBehaviour': i, 'comment' : comment, 'actionGroups' : actionGroup})
      i += 1

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))


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
        if(bank[vaPorAddr] == 0xff):
          vaPorAddr += 2
          # break the loop
          break


        subArray = bank[vaPorAddr : vaPorAddr + 5]

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

        vaPorAddr += 5

      self.jsonBosses['deathAction'].append({'idDeathAction': i, 'comment' : str(bossesNames), 'actions' : actions})
      i += 1

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))


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
        dicLiveAction['{:04x}'.format(vaPorAddr + 0x4000)] = i
        actions = []
        actions.append( {'cant' : "02", 'idDirection' : "6917", 'idLayout' : "6d9c"} )
        vaPorAddr += 6
        self.jsonBosses['liveAction'].append({'idLiveAction': i, 'actions' : actions})
        i += 1

#      vaPorAddr = addr - 0x4000 
      # change the dictionary to reflect it's id
#      dicLiveAction[strAddr] = i
      dicLiveAction['{:04x}'.format(vaPorAddr + 0x4000)] = i



      actions = []
#      print('--- ' + str(i))
      while(True):
        # if it is the end of the list (it ends in 0xff)
        if(bank[vaPorAddr] == 0xff):
          vaPorAddr += 1
          # break the loop
          break


        subArray = bank[vaPorAddr : vaPorAddr + 5]

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

        vaPorAddr += 5

      self.jsonBosses['liveAction'].append({'idLiveAction': i, 'actions' : actions})
      i += 1

#    print('dicLiveAction: ' + str(dicLiveAction))

#    sortedDic = dict(sorted(dicLiveAction.items(), key=lambda item: item[1]))
#    print('sortedDic: ' + str(sortedDic))

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

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
        dicDirection['{:04x}'.format(vaPorAddr + 0x4000)] = i
        vaPorAddr += 3
        tipo, vram = _byteToVramDic(0x0c)
        self.jsonBosses['direction'].append({'idDirection': i, 'type' : tipo, 'vramSprite' : vram, '(dx,dy)':"(+0,+0)" } ) 
        i += 1
      elif(i == 96):
        dicDirection['{:04x}'.format(vaPorAddr + 0x4000)] = i
        vaPorAddr += 3
        tipo, vram = _byteToVramDic(0x19)
        self.jsonBosses['direction'].append({'idDirection': i, 'type' : tipo, 'vramSprite' : vram, '(dx,dy)':"(-4,+4)" } ) 
        i += 1
      elif(i == 106):
        dicDirection['{:04x}'.format(vaPorAddr + 0x4000)] = i
        vaPorAddr += 3
        tipo, vram = _byteToVramDic(0x02)
        self.jsonBosses['direction'].append({'idDirection': i, 'type' : tipo, 'vramSprite' : vram, '(dx,dy)':"(+4,+4)" } ) 
        i += 1

#      print('vaPorAddr: {:04x} addr {:04x}'.format(vaPorAddr, addr-0x4000))
#      subArray = bank[addr - 0x4000:]
      subArray = bank[vaPorAddr - 0x4000:]

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

      vaPorAddr += 3
#      print(strAddr + ' vramSprite: ' + '{:02x}'.format(vramSprite) + ' direc: (dx,dy)=(' + strDx + ',' + strDy + ')')
#      self.jsonBosses['direction'].append({'idDirection': i, 'vramSprite': '{:02x}'.format(vramSprite), '(dx,dy)':"("+strDx+","+strDy+")" })

      self.jsonBosses['direction'].append({'idDirection': i, 'type' : tipo, 'vramSprite' : vram, '(dx,dy)':"("+strDx+","+strDy+")" })



      i += 1


#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

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
        dicLayout['{:04x}'.format(vaPorAddr + 0x4000)] = i

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

        vaPorAddr += 3*len(lays) + 1
        self.jsonBosses['layout'].append({'idLayout': i, 'lays': lays})
        i += 1
      elif(i == 86):
        dicLayout['{:04x}'.format(vaPorAddr + 0x4000)] = i

        lays = []

        for k in range(0, 9):
          tipo, vram = _byteToVramDic(0x13)
          lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f0'), 'y' : _strHexToSignedInt('00')} )
        vaPorAddr += 3*len(lays) + 1
        self.jsonBosses['layout'].append({'idLayout': i, 'lays': lays})
        i += 1
      elif(i == 88):
        dicLayout['{:04x}'.format(vaPorAddr + 0x4000)] = i

        lays = []

        tipo, vram = _byteToVramDic(0x11)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f0'), 'y' : _strHexToSignedInt('f0')} )
        tipo, vram = _byteToVramDic(0x10)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('00'), 'y' : _strHexToSignedInt('f0')} )
        for k in range(0, 7):
          tipo, vram = _byteToVramDic(0x12)
          lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt('f0'), 'y' : _strHexToSignedInt('00')} )
        vaPorAddr += 3*len(lays) + 1
        self.jsonBosses['layout'].append({'idLayout': i, 'lays': lays})
        i += 1

#      print('strAddr: ' + strAddr + ' addr ' + str(addr) + ' vaPorAddr {:04x}'.format(vaPorAddr) + ' ' + str(i))
      dicLayout['{:04x}'.format(vaPorAddr + 0x4000)] = i

      lays = []
#      print('--- ' + str(i))
      while(True):
        # if it is the end of the list (it ends in 0xff)
        if(bank[vaPorAddr] == 0xff):
          vaPorAddr += 1
          # break the loop
          break

        subArray = bank[vaPorAddr : vaPorAddr + 3]

        vramByte = subArray[0]
        x = subArray[1]
        y = subArray[2]

        tipo, vram = _byteToVramDic(vramByte)
        strX = '{:02x}'.format(x)
        strY = '{:02x}'.format(y)
        lays.append( {'type' : tipo, 'vramSprite' : vram, 'x' : _strHexToSignedInt(strX), 'y' : _strHexToSignedInt(strY)} )
        vaPorAddr += 3

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

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

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
    addrSortTilesEnd = vaPorAddr + sizeSortTiles + 0x4000
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


    vaPorAddr += sizeSortTiles
#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

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
        subArray = bank[vaPorAddr:vaPorAddr+3]
#        print('subArray: ' + mystic.util.strHexa(subArray))

        attrib = subArray[0]
        tile1 = subArray[1]
        tile2 = subArray[2]

        strAttrib = '{:02x}'.format(attrib)
        strTile1 = '{:02x}'.format(tile1)
        strTile2 = '{:02x}'.format(tile2)

        sprites.append({'idSprite' : j, 'attrib' : strAttrib, 'tile1' : strTile1, 'tile2' : strTile2})
        vaPorAddr += 3

      # for hydra
      if(i == 1):
        # we hardcode the unused sprite
        sprites.append({'idSprite' : j+1, 'attrib' : '10', 'tile1' : '3c', 'tile2' : '3e'})
        vaPorAddr += 3

      self.jsonBosses['spriteGroups'].append( {'idSpriteGroup' : i, 'comment' : str(bossesNames), 'sprites' : sprites} )


#    print('vaPorAddr: {:04x}'.format(vaPorAddr))




  def encodeRom(self, addrBosses):

    array = []

    vaPorAddr = addrBosses

    for boss in self.jsonBosses['boss']:
#      print('boss: ' + str(boss))
#      print('vaPorAddr: {:04x}'.format(vaPorAddr))

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
      vaPorAddr += len(subArray)


#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    # dictionary for labels of spriteDamages
    spritesAddrDic = {}

    i = 0
    for spriteBlock in self.jsonBosses['spriteBlocks']:
      # set the address of each spriteDamage
      spritesAddrDic[i] = vaPorAddr

      blocks = spriteBlock['blocks']
#      print('sprites: ' + str(sprites))
#      print('vaPorAddr: {:04x}'.format(vaPorAddr))

      subArray = []
      for strBlock in blocks:
        block = mystic.util.hexaStr(strBlock.strip())
#        print('block: ' + str(block))
        subArray.extend(block)

      array.extend(subArray)
      vaPorAddr += len(subArray)
      i += 1

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    # dictionary for labels of behaviours
    behavAddrDic = {}

    i = 0
    for behav in self.jsonBosses['behaviours']:
#      print(' --- behav: ')
      # set the address of each behaviour
      behavAddrDic[i] = vaPorAddr

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
      vaPorAddr += len(subArray)
      i += 1


#    print('vaPorAddr: {:04x}'.format(vaPorAddr))


    # dictionary for labels of deathActions
    deathAddrDic = {}

    i = 0
    for death in self.jsonBosses['deathAction']:
#      print(' --- death: ')
      # set the address of each deathAction
      deathAddrDic[i] = vaPorAddr

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
      vaPorAddr += len(subArray)

      i += 1


#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    # dictionary for labels of liveActions
    liveAddrDic = {}

    i = 0
    for live in self.jsonBosses['liveAction']:
#      print(' --- live: ' + str(i) + ' {:04x}'.format(vaPorAddr))
      # set the address of each deathAction
      liveAddrDic[i] = vaPorAddr

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
      vaPorAddr += len(subArray)

      i += 1


#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    # dictionary of directions
    dicDirection = {}

    i = 0
    for direc in self.jsonBosses['direction']:
#      print(' --- direc: ' + str(direc) + ' {:04x} '.format(vaPorAddr) + str(i))

      dicDirection[i] = vaPorAddr

      subArray = []
      tipo = direc['type']
      vram = direc['vramSprite']
      vramVal = _vramDicToByte( (tipo, vram) )
      subArray.append(vramVal)

      dx = int(direc['(dx,dy)'][1:3],16)
      dy = int(direc['(dx,dy)'][4:6],16)

#      print('{:04x} vramSprite: {:02x}'.format(vaPorAddr, vramVal) + ' ' + str(dx) + ', ' + str(dy))

      dig1 = dx if dx >= 0 else 0x10 + dx
      dig2 = dy if dy >= 0 else 0x10 + dy
      ddir = dig1*0x10 + dig2

#      print('ddir: ' + str(ddir))

      subArray.append(ddir)
      subArray.append(0xff)

      array.extend(subArray)
      vaPorAddr += len(subArray)
      i += 1

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))


    # dictionary of layouts
    dicLayout = {}

    i = 0
    for layout in self.jsonBosses['layout']:
#      print(' --- layout {:04x} '.format(vaPorAddr) + str(i))

      dicLayout[i] = vaPorAddr

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
        strX = _signedIntoToStrHex(intX)
        x = int(strX,16)

        intY = lay['y']
        strY = _signedIntoToStrHex(intY)
        y = int(strY,16)

        subArray.append(x)
        subArray.append(y)

      subArray.append(0xff)
      array.extend(subArray)
      vaPorAddr += len(subArray)

      i += 1

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    # dictionary of sortTiles
    dicSortTiles = {}

    i = 0
    for sortTile in self.jsonBosses['sortTiles']:
#      print(' --- sortTile: ' + str(sortTile))

      dicSortTiles[i] = vaPorAddr

      strSortT = sortTile['sorting']
      subArray = mystic.util.hexaStr(strSortT.strip())
#      print('subArray: ' + mystic.util.strHexa(subArray))

      array.extend(subArray)
      vaPorAddr += len(subArray)

      i += 1

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    # dictionary of spriteGroups
    dicSpriteGrp = {}

    i = 0
    for group in self.jsonBosses['spriteGroups']:
#      print(' --- group: {:04x}'.format(vaPorAddr)) # + str(group))

      dicSpriteGrp[i] = vaPorAddr

      for sprite in group['sprites']:
#        print('sprite: ' + str(sprite))

        attrib = int(sprite['attrib'],16)
        tile1 = int(sprite['tile1'],16)
        tile2 = int(sprite['tile2'],16)
        subArray = [attrib, tile1, tile2]

        array.extend(subArray)
        vaPorAddr += len(subArray)


      i += 1

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))


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


##########################################################
# @deprecated, can/should be deleted
class BossesOld:
  """ representa la colección de los monstruos grandes """

  def __init__(self):
    self.bosses = []
    self.bossesDamage = []
    self.bossesBehaviours = []
    self.bossesActions = []
    self.bossesMiniActions = []
    self.bossesPositions = []
    self.bossesSortTiles = []
    self.dosTiles = []

  def decodeRom(self):

    basePath = mystic.address.basePath
    path = basePath + '/bosses'

    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    nroBank,addrBosses = mystic.address.addrBosses
    bank = mystic.romSplitter.banks[nroBank]

    vaPorAddr = addrBosses
    bossesAddr = vaPorAddr

    f = open(path + '/01_bosses.txt', 'w', encoding="utf-8")

    self.bosses = []
    for i in range(0,21):
      subArray = bank[vaPorAddr : vaPorAddr+24]
      strHexa = mystic.util.strHexa(subArray)
#      print('boss: {:02x} - '.format(i) + strHexa)

      boss = mystic.bosses.Boss(i)
      boss.decodeRom(subArray)
      self.bosses.append(boss)
#      print('boss: {:02x} - '.format(i) + str(boss))

      lines = boss.encodeTxt(vaPorAddr)
      strBoss = '\n'.join(lines)

      f.write(strBoss)
      vaPorAddr += 24
    f.close()

    length = 24*len(self.bosses)
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x04, bossesAddr, bossesAddr+length, (rr, gg, bb), 'bosses')

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))
    addressesDamage = [boss.addrDamage for boss in self.bosses]

    f = open(path + '/02_bossesDamage.txt', 'w', encoding="utf-8")
    bossesDamageAddr = vaPorAddr

    self.bossesDamage = []
    # decodificamos los daños
    for i in range(0,152):
      subArray = bank[vaPorAddr: vaPorAddr+8]
#      strHexa = mystic.util.strHexa(subArray)


      stringDamage = ''
      if(vaPorAddr+0x4000 in addressesDamage):
        idx = addressesDamage.index(vaPorAddr+0x4000)
        stringDamage = mystic.variables.bosses[idx] + ' damage\n'
        f.write('---- ' + stringDamage)

      damage = BossDamage()
      damage.decodeRom(subArray)
      lines = damage.encodeTxt()
      strDamage = '\n'.join(lines)
      f.write('damage: ' + strDamage + '\n')

      vaPorAddr += 8
    f.close()

    length = 152*8 
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x04, bossesDamageAddr, bossesDamageAddr+length, (rr, gg, bb), 'bosses damage')



#    print('vaPorAddr: {:04x}'.format(vaPorAddr))
    addressesStart = [boss.addrBehaviourStart for boss in self.bosses]
    addressesBeh = [boss.addrBehaviour for boss in self.bosses]

    f = open(path + '/03_bossesBehaviour.txt', 'w', encoding="utf-8")

    bossesBehaviourAddr = vaPorAddr

    self.bossesBehaviours = []
    for i in range(0,44):

      stringStart = ''
      if(vaPorAddr+0x4000 in addressesStart):
        idx = addressesStart.index(vaPorAddr+0x4000)
        stringStart = mystic.variables.bosses[idx] + ' start'

      stringBeh = ''
      if(vaPorAddr+0x4000 in addressesBeh):
        idx = addressesBeh.index(vaPorAddr+0x4000)
        stringBeh = mystic.variables.bosses[idx] + ' beh'

#      if(True):
      if(stringStart != '' or stringBeh != ''):
        f.write('---- addr: {:04x}'.format(vaPorAddr+0x4000) + ' ' + stringStart + ' ' + stringBeh + '\n')

      while(True):
        subArray = bank[vaPorAddr : vaPorAddr + 10]
        # if it is the end of the list (it ends in 0xffff)
        if(subArray[0] == 0xff):
          vaPorAddr += 1
          f.write('END\n')
          break

#        strHexa = mystic.util.strHexa(subArray)
#        print('start: ' + strHexa)
        behaviour = BossBehaviour()
        behaviour.decodeRom(subArray)
        lines = behaviour.encodeTxt()
        string = '\n'.join(lines)
        f.write(string)

        vaPorAddr += 10 
    f.close()

    length = vaPorAddr - bossesBehaviourAddr
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x04, bossesBehaviourAddr, bossesBehaviourAddr+length, (rr, gg, bb), 'bosses behaviour')

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))
    addressesStart = [boss.addrBehaviourStart for boss in self.bosses]
    addressesDeath = [boss.addrDeathExplosion for boss in self.bosses]

    addressesInnBeh = []
    for boss in self.bosses:
      addr = boss.addrBehaviour - 0x4000
#      print('addrBehaviour: {:04x}'.format(addr))

      addr1 = bank[addr]
      addr2 = bank[addr+1]
      addrInnBeh = addr2*0x100 + addr1 #- 0x4000
#      print('addrInnBeh: {:04x}'.format(addrInnBeh))
      addressesInnBeh.append(addrInnBeh)

    f = open(path + '/04_bossesAction.txt', 'w', encoding="utf-8")
    bossesActionAddr = vaPorAddr

    self.bossesActions = []
    for i in range(0,107):
      stringInnBehaviour = ''
      if(vaPorAddr+0x4000 in addressesInnBeh):
        idx = addressesInnBeh.index(vaPorAddr+0x4000)
        stringInnBehaviour = mystic.variables.bosses[idx] + ' inn_behaviour'

      stringStart = ''
      if(vaPorAddr+0x4000 in addressesStart):
        idx = addressesStart.index(vaPorAddr+0x4000)
        stringStart = mystic.variables.bosses[idx] + ' start'

      stringDeath = ''
      if(vaPorAddr+0x4000 in addressesDeath):
        idx = addressesDeath.index(vaPorAddr+0x4000)
        stringDeath = mystic.variables.bosses[idx] + ' death'

      if(stringInnBehaviour != '' or stringStart != '' or stringDeath != ''):
        f.write('---- addr: {:04x}'.format(vaPorAddr+0x4000) + ' ' + stringStart + ' ' + stringDeath + ' ' + stringInnBehaviour + '\n')

      while(True):
        subArray = bank[vaPorAddr : vaPorAddr + 5]
        if(subArray[0] == 0xff):
          vaPorAddr += 1
          f.write('END\n')
          break

        action = BossAction()
        action.decodeRom(subArray)
        lines = action.encodeTxt()
        string = '\n'.join(lines)
        f.write(string)

        vaPorAddr += 5
    f.close()

    length = vaPorAddr - bossesActionAddr
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x04, bossesActionAddr, bossesActionAddr+length, (rr, gg, bb), 'bosses action')

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    f = open(path + '/05_bossesMiniAction.txt', 'w', encoding="utf-8")
    bossesMiniActionAddr = vaPorAddr

    for i in range(0,193):
      subArray = bank[vaPorAddr : vaPorAddr+3]
      mini = BossMiniAction()
      mini.decodeRom(subArray)
      lines = mini.encodeTxt(vaPorAddr)
      string = '\n'.join(lines)
      f.write(string)

      vaPorAddr += 3
    f.close()

    length = vaPorAddr - bossesMiniActionAddr
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x04, bossesMiniActionAddr, bossesMiniActionAddr+length, (rr, gg, bb), 'bosses mini-action')


#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    f = open(path + '/06_bossesSpritesPos.txt', 'w', encoding="utf-8")
    bossesPositionAddr = vaPorAddr

    for i in range(0,159):

      f.write('---- sprites position: {:04x}\n'.format(vaPorAddr+0x4000))
      while(True):
        subArray = bank[vaPorAddr:vaPorAddr+3]
#        strHexa = mystic.util.strHexa(subArray)
#        print('subArray: ' + strHexa)

        if(subArray[0] == 0xff):
          vaPorAddr += 1
          f.write('END\n')
          break

        pos = BossSpritePos()
        pos.decodeRom(subArray)
        lines = pos.encodeTxt()
        string = '\n'.join(lines)
        f.write(string)

        vaPorAddr += 3

    f.close()

    length = vaPorAddr - bossesPositionAddr
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x04, bossesPositionAddr, bossesPositionAddr+length, (rr, gg, bb), 'bosses position')

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    f = open(path + '/07_bossesSortTiles.txt', 'w', encoding="utf-8")
    addressesSortTiles = [boss.addrSortTiles for boss in self.bosses]

    bossesSortTilesAddr = vaPorAddr

    prevAddrSortTile = vaPorAddr
    arrayTiles = []
    primero = True
    for i in range(0,618):

      if(vaPorAddr+0x4000 in addressesSortTiles):
        if(primero):
          primero = False
        else:

          stringTile = ''
          if(vaPorAddr+0x4000 in addressesSortTiles):
            idx = addressesSortTiles.index(prevAddrSortTile+0x4000)
            stringTile = mystic.variables.bosses[idx] + ' sort-tiles'
          strHexa = mystic.util.strHexa(arrayTiles)
          self.bossesSortTiles.append(arrayTiles)
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
    self.bossesSortTiles.append(arrayTiles)
    f.write('--- sortTiles: {:04x} '.format(prevAddrSortTile) + stringTile + '\n' + strHexa + '\n')

    f.close()

    length = vaPorAddr - bossesSortTilesAddr
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x04, bossesSortTilesAddr, bossesSortTilesAddr+length, (rr, gg, bb), 'bosses sort-tiles')

#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

    # creo la lista de addresses de animaciones
    animAddrs = []
    # recorro los bosses
    for boss in self.bosses:
      anim = boss.addrDosTiles
      # y agrego su animación a la lista
      animAddrs.append(anim)

    # remuevo duplicados y ordeno
    animAddrs = sorted(set(animAddrs))

    f = open(path + '/08_bossesAnimations.txt', 'w', encoding="utf-8")

    bossesAnimationsAddr = vaPorAddr

    animCounter = 1
    self.dosTiles = []

    subDosTiles = []
    for i in range(0,326):

      if(vaPorAddr + 0x4000 in animAddrs):
#        print('---animation' + str(animCounter))
        f.write('---animation' + str(animCounter) + '\n')
        animCounter += 1
        self.dosTiles.append(subDosTiles)
        subDosTiles = []

      subArray = bank[vaPorAddr : vaPorAddr + 3]
      dosTiles = mystic.tileset.DosTiles(vaPorAddr)
      dosTiles.decodeRom(subArray)
#      print('dosTiles: ' + str(dosTiles))
      subDosTiles.append(dosTiles)
      lines = dosTiles.encodeTxt()
      strDosTiles = '\n'.join(lines)
      f.write(strDosTiles + '\n')
      vaPorAddr += 3

    self.dosTiles.pop(0)
    f.close()

    length = 3*len(self.dosTiles)
    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(0x04, bossesAnimationsAddr, bossesAnimationsAddr+length, (rr, gg, bb), 'bosses animations dosTiles')



  def decodeTxt(self, lines):

    i = 0
    self.bosses = []
    primero = True
    subLines = []
    for line in lines:
#      print('line: ' + line)
      if('------------ boss' in line):
        if(not primero):
          b = mystic.bosses.Boss(i)
          b.decodeTxt(subLines)
          self.bosses.append(b)
          i += 1
          subLines = []
        else:
          primero = False

      subLines.append(line)

    b = mystic.bosses.Boss(i)
    b.decodeTxt(subLines)
    self.bosses.append(b)

  def decodeDamageTxt(self, lines):

    self.bossesDamage = []

    for line in lines:
      # if it is not a comment
      if(not line.startswith('-')):
        line = line[7:].strip()
        damage = BossDamage()
        damage.decodeTxt([line])
#        print('damage: ' + str(damage))
        self.bossesDamage.append(damage)

  def decodeBehaviourTxt(self, lines):

    self.bossesBehaviours = []

    for line in lines:
#      print('line: ' + line)
      if(line.startswith('END')):
        self.bossesBehaviours.append('END')
      elif(line.startswith('actionBehaviour')):
        behaviour = BossBehaviour()
        behaviour.decodeTxt([line])
        self.bossesBehaviours.append(behaviour)

  def decodeActionsTxt(self, lines):

    self.bossesActions = []

    for line in lines:
#      print('line: ' + line)
      if(line.startswith('END')):
        self.bossesActions.append('END')
      elif(line.startswith('action')):
        action = BossAction()
        action.decodeTxt([line])
        self.bossesActions.append(action)

  def decodeMiniActionsTxt(self, lines):

    self.bossesMiniActions = []

    for line in lines:
      mini = BossMiniAction()
      mini.decodeTxt([line])
      self.bossesMiniActions.append(mini)
 
  def decodePositionsTxt(self, lines):

    self.bossesPositions = []

    grupo = []
    for line in lines:
      if(line.startswith('spritePos')):
#        print('linee: ' + line)
        pos = BossSpritePos()
        pos.decodeTxt([line])
        grupo.append(pos)
      elif(line.startswith('END')):
        self.bossesPositions.append(grupo)
        grupo = []

  def decodeSortTilesTxt(self, lines):

    self.bossesSortTiles = []

    for line in lines:
      # if it is not a comment
      if(not line.startswith('-')):
        line = line.strip()
        sortTiles = mystic.util.hexaStr(line)
        self.bossesSortTiles.append(sortTiles)


  def decodeAnimationsTxt(self, lines):

    self.dosTiles = []
    for line in lines:
#      print('line: ' + line)
      if('(attr,tile1,tile2)' in line):
         dosTiles = mystic.tileset.DosTiles(0x0000)
         dosTiles.decodeTxt([line])
         self.dosTiles.append(dosTiles)



 
  def encodeRom(self):

    array = []
    for b in self.bosses:
#      print('b: ' + str(b))
      subArray = b.encodeRom()
      array.extend(subArray)

    for d in self.bossesDamage:
#      print('d: ' + str(d))
      subArray = d.encodeRom()
      array.extend(subArray)

    for b in self.bossesBehaviours:
#      print('b: ' + str(b))
      if(b == 'END'):
        array.append(0xff)
      else:
        subArray = b.encodeRom()
        array.extend(subArray)

    for a in self.bossesActions:
#      print('a: ' + str(a))
      if(a == 'END'):
        array.append(0xff)
      else:
        subArray = a.encodeRom()
        array.extend(subArray)

    for m in self.bossesMiniActions:
#      print('m: ' + str(m))
      subArray = m.encodeRom()
      array.extend(subArray)


    for grupo in self.bossesPositions:
      for p in grupo:
        subArray = p.encodeRom()
        array.extend(subArray)
      array.append(0xff)

    for s in self.bossesSortTiles:
      array.extend(s)

    for d in self.dosTiles:
      subArray = d.encodeRom()
      array.extend(subArray)

    return array



##########################################################
# @deprecated, can/should be deleted
class BossSpritePos:

  def __init__(self):
    self.nroSprite = 0x00
    self.x = 0x00
    self.y = 0x00

  def decodeRom(self, subArray):
    self.nroSprite = subArray[0]
    self.x = subArray[1]
    self.y = subArray[2]

  def encodeTxt(self):
    lines = []
#    subArray = [self.nroSprite, self.x, self.y]
#    strHexa = mystic.util.strHexa(subArray)
    lines.append('spritePos: {:02x} (x,y) = ({:02x},{:02x})\n'.format(self.nroSprite, self.x, self.y))
    return lines

  def decodeTxt(self, lines):
    line = lines[0]
    line = line[10:].strip()
#    print('linecocu: ' + line)
    strNroSprite = line[0:2]
    self.nroSprite = int(strNroSprite,16)
    strX = line[12:14]
    self.x = int(strX,16)
    strY = line[15:17]
    self.y = int(strY,16)

  def encodeRom(self):
    array = []
    array.append(self.nroSprite)
    array.append(self.x)
    array.append(self.y)
    return array
 

##########################################################
# @deprecated, can/should be deleted
class BossMiniAction:

  def __init__(self):
    self.nose1 = 0x00
    # the direction
    self.direc = (0,0)
    self.nose3 = 0x00

  def decodeRom(self, subArray):
    self.nose1 = subArray[0]
    direc = subArray[1]
    dx = direc // 0x10
    dy = direc % 0x10
    self.direc = (dx,dy)
    strDx = '+' + str(dx) if (dx < 7) else '-' + str(0x10 - dx)
    strDy = '+' + str(dy) if (dy < 7) else '-' + str(0x10 - dy)
#    print('direc: (dx,dy)=(' + strDx + ',' + strDy + ')')
    self.nose3 = subArray[2]

  def encodeTxt(self, vaPorAddr):
    lines = []

    dx = self.direc[0]
    dy = self.direc[1]

    strDx = '+' + str(dx) if (dx < 7) else '-' + str(0x10 - dx)
    strDy = '+' + str(dy) if (dy < 7) else '-' + str(0x10 - dy)

    lines.append('miniAction: nose1={:02x} '.format(self.nose1) + '(dx,dy)=(' + strDx + ',' + strDy + ')' + ' {:02x} '.format(self.nose3) + '   # {:04x}\n'.format(vaPorAddr+0x4000))
    return lines

  def decodeTxt(self, lines):
    line = lines[0]
    line = line[11:].strip()
    noses = line.split()
    strNose1 = noses[0]
    strNose1 = strNose1[6:8]
#    print('strNose1: ' + strNose1)
    self.nose1 = int(strNose1, 16)

    strDirec = noses[1]
#    print('strDirec: ' + strDirec)
    strDx = strDirec[9:11]
    strDy = strDirec[12:14]
    dx = int(strDx)
    dy = int(strDy)
    self.direc = (dx,dy)

    strNose3 = noses[2]
#    print('strNose3: ' + strNose3)
    self.nose3 = int(strNose3, 16)

  def encodeRom(self):
    array = []
    array.append(self.nose1)

    dx = self.direc[0]
    dy = self.direc[1]

    dig1 = dx if dx >= 0 else 0x10 + dx
    dig2 = dy if dy >= 0 else 0x10 + dy
    direc = dig1*0x10 + dig2

#    print('direc: ' + str(direc))

    array.append(direc)
    array.append(self.nose3)
    return array
 
##########################################################
# @deprecated, can/should be deleted
class BossAction:

  def __init__(self):
    self.cant = 0x00
    self.addrMini = 0x00
    self.addrSpritePos = 0x00
 
  def decodeRom(self, subArray):

    self.cant = subArray[0]
    self.addrMini = subArray[2]*0x100 + subArray[1]
    self.addrSpritePos = subArray[4]*0x100 + subArray[3]
 
  def encodeTxt(self):
    lines = []
    lines.append('action: cant={:02x} addrMini={:04x} addrSpritePos={:04x}\n'.format(self.cant, self.addrMini, self.addrSpritePos))
    return lines

  def decodeTxt(self, lines):
    line = lines[0]
    line = line[7:].strip()

    idx = line.index('=')
    line = line[idx+1:]
    strCant = line[0:2]
    self.cant = int(strCant,16)

    idx = line.index('=')
    line = line[idx+1:]
    strAddrMini = line[0:4]
    self.addrMini = int(strAddrMini,16)
 
    idx = line.index('=')
    line = line[idx+1:]
    strAddrSpritePos = line[0:4]
    self.addrSpritePos = int(strAddrSpritePos,16)

  def encodeRom(self):
    array = []

    array.append(self.cant)
    array.append(self.addrMini%0x100)
    array.append(self.addrMini//0x100)
    array.append(self.addrSpritePos%0x100)
    array.append(self.addrSpritePos//0x100)

    return array
 
 
##########################################################
# @deprecated, can/should be deleted
class BossBehaviour:

  def __init__(self):
    self.addr1 = 0x0000
    self.addr2 = 0x0000
    self.addr3 = 0x0000
    self.addr4 = 0x0000
    self.x = 0x00
    self.y = 0x00

  def decodeRom(self, subArray):

    self.addr1 = subArray[1]*0x100 + subArray[0]
    self.addr2 = subArray[3]*0x100 + subArray[2]
    self.addr3 = subArray[5]*0x100 + subArray[4]
    self.addr4 = subArray[7]*0x100 + subArray[6]
    self.x = subArray[8]
    self.y = subArray[9]

  def encodeTxt(self):
    lines = []
    lines.append('actionBehaviour: {:04x} {:04x} {:04x} {:04x} (x,y) = ({:02x},{:02x})\n'.format(self.addr1, self.addr2, self.addr3, self.addr4, self.x, self.y))
    return lines

  def decodeTxt(self, lines):
    line = lines[0]
    line = line[16:].strip()

    idx = line.index('(')
    strAddrs = line[:idx].strip().split(' ')

    strAddr1 = strAddrs[0]
    strAddr2 = strAddrs[1]
    strAddr3 = strAddrs[2]
    strAddr4 = strAddrs[3]
    self.addr1 = int(strAddr1, 16)
    self.addr2 = int(strAddr2, 16)
    self.addr3 = int(strAddr3, 16)
    self.addr4 = int(strAddr4, 16)

    strXy = line[idx:]
    idx = strXy.index('=')
    strXy = strXy[idx+1:]
    idx = strXy.index(',')
    strX = strXy[idx-2:idx]
    strY = strXy[idx+1:idx+3]
    self.x = int(strX,16)
    self.y = int(strY,16)

  def encodeRom(self):
    array = []

    array.append(self.addr1%0x100)
    array.append(self.addr1//0x100)
    array.append(self.addr2%0x100)
    array.append(self.addr2//0x100)
    array.append(self.addr3%0x100)
    array.append(self.addr3//0x100)
    array.append(self.addr4%0x100)
    array.append(self.addr4//0x100)
    array.append(self.x)
    array.append(self.y)

    return array



##########################################################
# @deprecated, can/should be deleted
class BossDamage:

  def __init__(self):
    self.nose1 = 0x00
    self.nose2 = 0x00
    self.nose3 = 0x00
    self.nose4 = 0x00
    self.nose5 = 0x00
    self.nose6 = 0x00
    self.nose7 = 0x00
    self.nose8 = 0x00

  def decodeRom(self, array):
    self.nose1 = array[0]
    self.nose2 = array[1]
    self.nose3 = array[2]
    self.nose4 = array[3]
    self.nose5 = array[4]
    self.nose6 = array[5]
    self.nose7 = array[6]
    self.nose8 = array[7]

  def encodeTxt(self):
    lines = []
    lines.append('{:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} '.format(self.nose1, self.nose2, self.nose3, self.nose4, self.nose5, self.nose6, self.nose7, self.nose8))
    return lines

  def decodeTxt(self, lines):

    line = lines[0]
    array = mystic.util.hexaStr(line)

    self.nose1 = array[0]
    self.nose2 = array[1]
    self.nose3 = array[2]
    self.nose4 = array[3]
    self.nose5 = array[4]
    self.nose6 = array[5]
    self.nose7 = array[6]
    self.nose8 = array[7]

  def encodeRom(self):
    array = []

    array.append(self.nose1)
    array.append(self.nose2)
    array.append(self.nose3)
    array.append(self.nose4)
    array.append(self.nose5)
    array.append(self.nose6)
    array.append(self.nose7)
    array.append(self.nose8)

    return array

  def __str__(self):
    string = '{:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} '.format(self.nose1, self.nose2, self.nose3, self.nose4, self.nose5, self.nose6, self.nose7, self.nose8)
    return string


##########################################################
# @deprecated, can/should be deleted
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

    # how many 16x16 sprites (and lines in addrDamage)
    self.cantSprites = 0x00
    self.projectile = 0x00
    self.scriptDefeated = 0x0000

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

    self.cantSprites = subArray[4]

    self.projectile = subArray[5]

    scri_1 = subArray[6]
    scri_2 = subArray[7]
    self.scriptDefeated = scri_2*0x100 + scri_1

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

    array.append(self.cantSprites)

    array.append(self.projectile)

    array.append(self.scriptDefeated%0x100)
    array.append(self.scriptDefeated//0x100)

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
    lines.append('cantSprites:        {:02x}'.format(self.cantSprites))
    lines.append('projectile:         {:02x}'.format(self.projectile))
    lines.append('scriptDefeated:     {:04x}'.format(self.scriptDefeated))
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
      elif(line.startswith('cantSprites:')):
        strCantSprites = line[len('cantSprites:'):].strip()
        self.cantSprites = int(strCantSprites,16)

      elif(line.startswith('projectile:')):
        strProj = line[len('projectile:'):].strip()
        self.projectile = int(strProj,16)

      elif(line.startswith('scriptDefeated:')):
        strScript = line[len('scriptDefeated:'):].strip()
        self.scriptDefeated = int(strScript,16)

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

    string = ' speed={:02x} hp={:02x} exp={:02x} GP={:02x} cantDam={:02x} {:04x} {:02x} vramTileOffset={:02x} cantDosTiles={:02x} offsetBank8={:04x} addrSortTiles={:04x} addrDosTiles={:04x} {:04x} {:04x} {:04x} {:04x} '.format(self.speedSleep, self.hp, self.exp, self.gp, self.cantSprites, self.projectile, self.scriptDefeated, self.vramTileOffset, self.cantDosTiles, self.offsetBank8, self.addrSortTiles, self.addrDosTiles, self.addrDamage, self.addrBehaviour, self.addrBehaviourStart, self.addrDeathExplosion)

    return string


