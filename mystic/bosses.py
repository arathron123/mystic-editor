import os

import mystic.variables


##########################################################
class Bosses:
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

  def decodeRom(self, bank):

    basePath = mystic.address.basePath
    path = basePath + '/bosses'

    # si el directorio no existía
    if not os.path.exists(path):
      # lo creo
      os.makedirs(path)

    vaPorAddr = 0x0739
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

    # how many lines starting from addrDamage
    self.cantDamages = 0x00
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

    self.cantDamages = subArray[4]

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

    array.append(self.cantDamages)

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
    lines.append('cantDamages:        {:02x}'.format(self.cantDamages))
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
      elif(line.startswith('cantDamages:')):
        strCantDamages = line[len('cantDamages:'):].strip()
        self.cantDamages = int(strCantDamages,16)

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

    string = ' speed={:02x} hp={:02x} exp={:02x} GP={:02x} cantDam={:02x} {:04x} {:02x} vramTileOffset={:02x} cantDosTiles={:02x} offsetBank8={:04x} addrSortTiles={:04x} addrDosTiles={:04x} {:04x} {:04x} {:04x} {:04x} '.format(self.speedSleep, self.hp, self.exp, self.gp, self.cantDamages, self.projectile, self.scriptDefeated, self.vramTileOffset, self.cantDosTiles, self.offsetBank8, self.addrSortTiles, self.addrDosTiles, self.addrDamage, self.addrBehaviour, self.addrBehaviourStart, self.addrDeathExplosion)

    return string


