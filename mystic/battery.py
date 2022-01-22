
import mystic.util
import mystic.variables
import mystic.dictionary

##########################################################
class Slot:
  """ representa un slot de guardado """

  def __init__(self, array):
    self.array = array

  def get(self, idx):
    """ retorna el byte del array indicado """
    return self.array[idx]

  def setChecksum(self, check):
    """ setea el checksum """

#    print('seteando checksum {:04x}'.format(check))
    check1 = check % 0x100
    check2 = check // 0x100
    self.array[1] = check1
    self.array[2] = check2

  def fixChecksum(self):
    """ corrige el checksum """
    check = self.calculateChecksum()
    self.setChecksum(check)

  def getChecksum(self):
    """ retorna el checksum guardado en el .sav """

    checkArray = self.array[1:3]
    check = checkArray[1]*0x100 + checkArray[0]
    return check

  def calculateChecksum(self):
    """ calcula el checksum correspondiente al .sav """
    suma = 0x00
    for i in range(3, 8*15+3):
      val = self.array[i]
      suma += val
#      print('valor {:02x}'.format(val))
   
    return suma

  def getHeros(self):
    """ retorna los nombres de los heroes guardado en el slot """

    heroArray = self.array[3:7]
    heroinArray = self.array[7:11]

    strHero = mystic.dictionary.decodeArray(heroArray)
    strHeroin = mystic.dictionary.decodeArray(heroinArray)

    return strHero, strHeroin

  def getHP(self):
    """ retorna hp y hpTotal """

    hpArray = self.array[11:13]
    hp = hpArray[1]*0x100 + hpArray[0]

    hpTotalArray = self.array[13:15]
    hpTotal = hpTotalArray[1]*0x100 + hpTotalArray[0]

    return hp, hpTotal

  def getMP(self):
    """ retorna mp y mpTotal """

    mpArray = self.array[15:17]
    mp = mpArray[1]*0x100 + mpArray[0]

    mpTotalArray = self.array[17:19]
    mpTotal = mpTotalArray[1]*0x100 + mpTotalArray[0]

    return mp, mpTotal

  def getLevel(self):
    """ retorna level """

    level = self.array[19]
    return level

  def getExp(self):
    """ retorna experiencia """

    expArray = self.array[20:23]
    exp = expArray[2]*(0x10000) + expArray[1]*0x100 + expArray[0]
    return exp

  def getNextLevelExp(self):
    """ retorna la experiencia necesaria para pasar de nivel """

    nextExp = 0

    # f(1) = 16
    # f(2) = 44
    # f(3) = 90

    level = self.getLevel()
#    print('level: ' + str(level))

    nextExp = 2**3 * 2**(level)

    return nextExp


  def getGP(self):
    """ retorna gp """

    gpArray = self.array[23:25]
    gp = gpArray[1]*0x100 + gpArray[0]
    return gp

  def setGP(self, gp):
    """ setea gp """
    gp1 = gp % 0x100
    gp2 = gp // 0x100
    self.array[23] = gp1
    self.array[24] = gp2

  def getStatus(self):
    """ retorna status """

    status = self.array[25]
    return status

  def getStamnPowerWisdmWill(self):
    """ retorna stamina, power, wisdom, will """

    stamn = self.array[26]
    power = self.array[27]
    wisdm = self.array[28]
    will  = self.array[29]

    return stamn, power, wisdm, will

  def getFlags(self):
    """ retorna los flags (variables de estado según avance del juego) """

    # flag[11] = acompaña (0x40 = jofy, 0x08 = bogard, ...)
#    flags = self.array[30:30+19]
    flags = self.array[31:46]
    return flags

  def getFlag(self, nroFlag):
    idx = nroFlag // 8
    idx2 = nroFlag % 8

    # agarro el byte donde está el flag
    val = self.getFlags()[idx] 
    # me quedo con el bit del flag
    val = val & 2**(7-idx2)

    # es True si no quedó en cero
    ret = (val != 0) 
    return ret

  def setFlag(self, nroFlag, val):
    idx = nroFlag // 8
    idx2 = nroFlag % 8

    # agarro el byte donde está el flag
    preval = self.getFlags()[idx]

#    print('prevalA: {:08b}'.format(preval))
    if(val):
      preval = preval | 2**(7-idx2)
    else:
      preval = preval & (0xff - 2**(7-idx2))
#    print('prevalB: {:08b}'.format(preval))

    self.array[31+idx] = preval

  def setFlagByLabel(self, label, val):
    # busco el nro de flag correspondiente al label
    nroFlag = mystic.variables.getVal(label)
    self.setFlag(nroFlag, val)
 
  def getFlagByLabel(self, label):
    # busco el nro de flag correspondiente al label
    nroFlag = mystic.variables.getVal(label)
    val = self.getFlag(nroFlag)
    return val
 

  def printFlags(self):
    flags = self.getFlags()
    i = 0
    string = ''
    for flag in flags:
#      string += str(i).zfill(2) + '|'
      i += 1
#    string += '\n'
    for flag in flags:
      string += '{:02x}'.format(flag) + '|'
    print(string)

#  def setFlag(self, i, val):
#    """ setea el valor indicado al flag indicado """
#    self.array[30+i] = val


  def getApVp(self):
    """ retorna puntos de ataque y defensa según el equip """

    ap = self.array[51]
    dp = self.array[53]

    return ap, dp

  def getInventario(self):
    """ retorna el inventario """

    # array de códigos de item
    invArray = self.array[55:71]
    # array paralelo de cantidades de cada item
    cantArray = self.array[99:115]

    for i in range(0,16):
      val = invArray[i]
      cant = cantArray[i]
#      print('inv: {:02x}'.format(val) + ' dec: ' + str(val))

      idx = val // 8
      idx2 = val % 8

      val0 = 1 if val & 2**(7-0) != 0 else 0
      val1 = 1 if val & 2**(7-1) != 0 else 0
      val2 = 1 if val & 2**(7-2) != 0 else 0
      val3 = 1 if val & 2**(7-3) != 0 else 0
      val4 = 1 if val & 2**(7-4) != 0 else 0
      val5 = 1 if val & 2**(7-5) != 0 else 0
      val6 = 1 if val & 2**(7-6) != 0 else 0
      val7 = 1 if val & 2**(7-7) != 0 else 0
#      print('--> ' + str(val0) + ',' + str(val1) + ',' + str(val2)  + ',' + str(val3) + ','  + str(val4) + ','  + str(val5) + ','  + str(val6) + ','  + str(val7))

      # el primer bit indica si puede haber mas de uno
      varios = val0*2**0
      comodin = '*' if varios != 0 else ' '
      # el nro es el código de item
      nro = val1*2**6 + val2*2**5 + val3*2**4 + val4*2**3 + val5*2**2 + val6*2**1 + val7*2**0
      # obtengo la descripción del item
      descr = mystic.variables.items[nro-1]
      print('item: ' + str(cant) + ' ' + comodin + descr)


  def getMagia(self):

    # array de códigos de magia
    magArray = self.array[71:79]
#    magArray = self.array[72:80]

    for i in range(0,8):
      val = magArray[i]
#      print('mag: {:02x}'.format(val))

      val0 = 1 if val & 2**(7-0) != 0 else 0
      val1 = 1 if val & 2**(7-1) != 0 else 0
      val2 = 1 if val & 2**(7-2) != 0 else 0
      val3 = 1 if val & 2**(7-3) != 0 else 0
      val4 = 1 if val & 2**(7-4) != 0 else 0
      val5 = 1 if val & 2**(7-5) != 0 else 0
      val6 = 1 if val & 2**(7-6) != 0 else 0
      val7 = 1 if val & 2**(7-7) != 0 else 0

      # el primer bit indica si puede haber mas de uno
      varios = val0*2**0
      comodin = '*' if varios != 0 else ' '
      # el nro es el código de item
      nro = val1*2**6 + val2*2**5 + val3*2**4 + val4*2**3 + val5*2**2 + val6*2**1 + val7*2**0
      # obtengo la descripción del item
      descr = mystic.variables.items[nro-1]
      print('mag: ' + comodin + str(nro))


  def getArmas(self):

    # array de códigos de weapon
    weapArray = self.array[79:91]

    for i in range(0,12):
      val = weapArray[i]
      descr = mystic.variables.armas[val-1]
      print('arma: {:02x}'.format(val) + ' - ' + descr)



    weaponMano = self.array[91]
    descr = mystic.variables.armas[weaponMano-1]
    print('arma en mano: {:02x}'.format(val) + ' - ' + descr)

    sombreroMano = self.array[92]
    descr = mystic.variables.armas[sombreroMano-1]
    print('sombrero en mano: {:02x}'.format(val) + ' - ' + descr)

    ropaMano = self.array[94]
    descr = mystic.variables.armas[ropaMano-1]
    print('ropa en mano: {:02x}'.format(val) + ' - ' + descr)

    escudoMano = self.array[96]
    descr = mystic.variables.armas[escudoMano-1]
    print('escudo en mano: {:02x}'.format(val) + ' - ' + descr)


   

  def getCoords(self):
    """ retorna las coordenadas del mapa """
    mm = self.array[115]
    xy = self.array[116]
    uu = self.array[117]
    vv = self.array[118]

#    print('mm {:02x}'.format(mm))
    return mm,xy,uu,vv
 
  def setCoords(self, mm, xy, uu, vv):
    """ setea las coordenadas del mapa """
    self.array[115] = mm
    self.array[116] = xy
    self.array[117] = uu
    self.array[118] = vv

  def printFull(self):

    print(' ----- ')

    hero, heroin = self.getHeros()
    print('hero: ' + hero + ' | heroin: ' + heroin)

    hp, hpTotal = self.getHP()
    print('hp: ' + str(hp) + ' | hpTotal: ' + str(hpTotal))

    mp, mpTotal = self.getMP()
    print('mp: ' + str(mp) + ' | mpTotal: ' + str(mpTotal))

    level = self.getLevel()
    print('level: ' + str(level))
    exp = self.getExp()
    print('exp: ' + str(exp))
    nextExp = self.getNextLevelExp()
    print('nextExp: ' + str(nextExp))
    gp = self.getGP()
    print('GP: ' + str(gp))

    status = self.getStatus()
    print('status: ' + str(status))
    stamn,power,wisdm,will = self.getStamnPowerWisdmWill()
    print('stamn: ' + str(stamn) + ' | power: ' + str(power) + ' | wisdm: ' + str(wisdm) + ' | will: ' + str(will))
    ap,vp = self.getApVp()
    print('ap: ' + str(ap) + ' | vp: ' + str(vp))

    mm,xy,uu,vv = self.getCoords()
    print('mm xy uu vv: {:02x} {:02x} {:02x} {:02x}'.format(mm,xy,uu,vv))

    flags = self.getFlags()
    for flag in flags:
      print('flagarray: {:08b}'.format(flag))

    for i in range(0,8*15):
      label = mystic.variables.getLabel(i)
      flag = self.getFlag(i)
      val = 0
      if(flag):
        val = 1
      print('flag: ' + str(val) + ' = ' + label)

    inv = self.getInventario()
    mag = self.getMagia()
    equip = self.getArmas()

class Saves:

  def __init__(self):
    self.saves = []

    saveFile = './roms/savegames/save_01_first_cave.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_02_ketts_place.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_03_marsh_cave.sav'
    self.save = Save(saveFile)
    saves.append(save)
    saveFile = './roms/savegames/save_04_ketts_place_revisited.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_05_wendel.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_06_silver_mine.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_07_gaia.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_08_airship.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_09_menos.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_10_medusas_cave.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_11_davias_mansion.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_12_cave_at_mt_rocks.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_13_mt_rocks.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_14_glaive_castle.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_15_cave_of_snowfields.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_16_floatrocks.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_17_cave_in_floatrocks.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_18_undersea_volcano.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_19_lichs_cave.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_20_cave_of_ruins.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_21_dime_tower.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_22_temple_of_mana.sav'
    save = Save(saveFile)
    self.saves.append(save)
    saveFile = './roms/savegames/save_23_final_battle_ground.sav'
    save = Save(saveFile)
    self.saves.append(save)


##########################################################
class Save:
  """ analiza el savestate .sav """

  def __init__(self, filepath):
    self.filepath = filepath

    array = mystic.util.fileToArray(self.filepath)

    # el array con los 2 slots para grabar
    self.slot = []

    array1 = []
    array2 = []
    iArr = 0
    # para cada uno de los 16 renglones
    for j in range(0x10):
      # para cada una de las 8 columnas
      for i in range(8):

        byte2 = array[j*0x10 + 2*i+1]
        byte1 = array[j*0x10 + 2*i]
        strByte2 = '{:02x}'.format(byte2)[1]
        strByte1 = '{:02x}'.format(byte1)[1]
#        print('strByte2, strByte1: ' + strByte2 + ', ' + strByte1)
        strNum1 = strByte2 + strByte1
        val1 = int(strNum1, 16)
        # agrego el valor al slot1
        array1.append(val1)

        byte2 = array[(j+0x10)*0x10 + 2*i+1]
        byte1 = array[(j+0x10)*0x10 + 2*i]
        strByte2 = '{:02x}'.format(byte2)[1]
        strByte1 = '{:02x}'.format(byte1)[1]
        strNum2 = strByte2 + strByte1
        val2 = int(strNum2, 16)
        # agrego el valor al slot2
        array2.append(val2)

    # la primer pos de guardado
    self.slot.append(Slot(array1))
    # la segunda pos de guardado
    self.slot.append(Slot(array2))

  def saveFile(self):
    """ reescribe el archivo .sav !! """

#    f = open(self.filepath + '.new', 'bw')
    f = open(self.filepath, 'bw')

    for i in range(0,2):

      # corrijo el checksum
      self.slot[i].fixChecksum()

      slotArray = self.slot[i].array
#      print('slotArray[' + str(i) + '] = ' + str(slotArray))

#      for byte in slotArray:
      for k in range(0,0x80 - 4):
        byte = slotArray[k]
        strByte = '{:02x}'.format(byte)
#        print('strByte: ' + strByte)

#        rellenoConF = True
        rellenoConF = False
        if(rellenoConF):
          strByte1 = 'F' + strByte[0]
          strByte2 = 'F' + strByte[1]
        else:
          strByte1 = '0' + strByte[0]
          strByte2 = '0' + strByte[1]

#        print('strByte1: ' + strByte1)
#        print('strByte2: ' + strByte2)

        byte1 = int(strByte1, 16)
        byte2 = int(strByte2, 16)

#        print('byte1: {:02x}'.format(byte1))
#        print('byte2: {:02x}'.format(byte2))


        f.write(bytes([byte2, byte1]))

      f.write(bytes([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))

    f.close()

  def printBatt(self):
    """ muestro la info de los slots """

    # para cada uno de los 16 renglones
    for j in range(0x10):
      renglon1 = ''
      renglon2 = ''
      # para cada una de las 8 columnas
      for i in range(8):
        val1 = self.slot[0].get(8*j + i)
        val2 = self.slot[1].get(8*j + i)
        renglon1 += '{:02x}'.format(val1) + ' '
        renglon2 += '{:02x}'.format(val2) + ' '
   
      print(renglon1 + ' | ' + renglon2)


  def printLindo(self):

    for i in range(0,2):

      print('--- slot ' + str(i+1) + ' ---')
      hero, heroin = self.slot[i].getHeros()
      print(hero + ', ' + heroin)
      hp, hpTotal = self.slot[i].getHP()
      print('HP: ' + str(hp) + '/' + str(hpTotal))
      mp, mpTotal = self.slot[i].getMP()
      print('MP: ' + str(mp) + '/' + str(mpTotal))
      level = self.slot[i].getLevel()
      print('L' + str(level))
      exp = self.slot[i].getExp()
      print('E ' + str(exp))
      gp = self.slot[i].getGP()
      print('GP ' + str(gp))
      status = self.slot[i].getStatus()
      print('status: ' + str(status))
      stamn, power, wisdm, will = self.slot[i].getStamnPowerWisdmWill()
      print('stamn ' + str(stamn) + ' power ' + str(power) + ' wisdm ' + str(wisdm) + ' will ' + str(will))

      ap, vp = self.slot[i].getApVp()
      print('AP: ' + str(ap) + ' VP: ' + str(vp))

      print('--------------')


