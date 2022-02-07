
import mystic.address
import mystic.dictionary


##########################################################
class Window:
  """ representa una ventana/panel """

  def __init__(self, nroWin):

    self.nroWin = nroWin

    self.x = 0x00
    self.y = 0x00
    self.w = 0x00
    self.h = 0x00
    # number of label rows
    self.labelRows = 0x00
    # the text width of the label of each option/item
    self.labelWidth = 0x00
    # how many options can fit in the window, counting scrolling
    self.cantHandOptions = 0x00
    # type of window (can select horizontally? has garbage bin? can swap items?)
    self.type = 0x00
    # number of columns selectable with hand cursor
    self.handCols = 0x00
    # horizontal hand displacement
    self.horizHandDisplacement = 0x00

  def decodeRom(self, data):
    """ decodifica la ventana a partir del array de 10 bytes """

    self.x = data[0]
    self.y = data[1]
    self.w = data[2]
    self.h = data[3]
    self.labelRows = data[4]
    self.labelWidth = data[5]
    self.cantHandOptions = data[6]
    self.type = data[7]
    self.handCols = data[8]
    self.horizHandDisplacement = data[9]

  def encodeTxt(self):
    lines = []

    lines.append('\n------------ window: ' + mystic.variables.windows[self.nroWin])
    lines.append('x:                     {:02x}'.format(self.x))
    lines.append('y:                     {:02x}'.format(self.y))
    lines.append('w:                     {:02x}'.format(self.w))
    lines.append('h:                     {:02x}'.format(self.h))
    lines.append('labelRows:             {:02x}'.format(self.labelRows))
    lines.append('labelWidth:            {:02x}'.format(self.labelWidth))
    lines.append('cantHandOptions:       {:02x}'.format(self.cantHandOptions))
    lines.append('type:                  {:02x}'.format(self.type))
    lines.append('handCols:              {:02x}'.format(self.handCols))
    lines.append('horizHandDisplacement: {:02x}'.format(self.horizHandDisplacement))

    return lines


  def decodeTxt(self, lines):

    for line in lines:

      if(line.startswith('x:')):
        self.x = int(line[len('x:'):].strip(),16)
      elif(line.startswith('y:')):
        self.y = int(line[len('y:'):].strip(),16)
      elif(line.startswith('w:')):
        self.w = int(line[len('w:'):].strip(),16)
      elif(line.startswith('h:')):
        self.h = int(line[len('h:'):].strip(),16)
      elif(line.startswith('labelRows:')):
        self.labelRows = int(line[len('labelRows:'):].strip(),16)
      elif(line.startswith('labelWidth:')):
        self.labelWidth = int(line[len('labelWidth:'):].strip(),16)
      elif(line.startswith('cantHandOptions:')):
        self.cantHandOptions = int(line[len('cantHandOptions:'):].strip(),16)
      elif(line.startswith('type:')):
        self.type = int(line[len('type:'):].strip(),16)
      elif(line.startswith('handCols:')):
        self.handCols = int(line[len('handCols:'):].strip(),16)
      elif(line.startswith('horizHandDisplacement:')):
        self.horizHandDisplacement = int(line[len('horizHandDisplacement:'):].strip(),16)


  def encodeRom(self):
    array = []

    array.append(self.x)
    array.append(self.y)
    array.append(self.w)
    array.append(self.h)
    array.append(self.labelRows)
    array.append(self.labelWidth)
    array.append(self.cantHandOptions)
    array.append(self.type)
    array.append(self.handCols)
    array.append(self.horizHandDisplacement)

    return array

  def __str__(self):
    return 'nroWin: {:02x} x: {:02x}, y: {:02x} w: {:02x} h: {:02x} rows: {:02x} labelW: {:02x} cantHand: {:02x} type: {:02x} cols: {:02x} horizHand: {:02x}'.format(self.nroWin, self.x, self.y, self.w, self.h, self.labelRows, self.labelWidth, self.cantHandOptions, self.type, self.handCols, self.horizHandDisplacement)


##########################################################
class Item:
  """ representa un item """

  def __init__(self, tipo):

    # el tipo puede ser uno de ['magic', 'item', 'weapon']
    self.tipo = tipo

    self.nro = -1
    self.name = ''

    # the 7 bytes that encodes the behaviour of the item
#    self.nose = []

    # ---byte0
    # si el item se puede usar varias veces antes de consumirse (0 ó 1)
    self.multiuse = 0
    # si el item no lo podemos vender (0 ó 1)
    self.unsellable = 0
    self.bit_unknown_1 = 0
    self.bit_unknown_2 = 0
    self.bit_unknown_3 = 0
    self.bit_unknown_4 = 0
    # MP cost (between 0 and 3)
    self.magic_cost = 0

    # ---byte1
    self.bit_unknown_5 = 0
    # original quantity of consumable multi-use item (between 0 and 7)
    self.quantity = 0
    # if it is a shield, helmet, armor or weapon (0 or 1)
    self.shield = 0
    self.helmet = 0
    self.armor = 0
    self.weapon = 0

    # ---byte2: not sure, seems to be how much HP recover in some items
    self.hp = 0x00
    # ---byte3: not sure, seems to be how much MP recover in some items
    self.mp = 0x00
    # ---byte4: the attack or defense points, whatever corresponds
    self.attack_defense_points = 0x00
    # ---byte5 and byte6: the value of the item when you want to buy it
    self.gold_value = 0x0000

    self.enabled = False
    # los bytes del item disabled
    self.disabledBytes = []


  def decodeRom(self, data):
    """ decodifica el item a partir del array de 16 bytes """
    # el id de item
    self.nro = data[0]


#    strHex = mystic.util.strHexa(data[1:1+8])
#    print('llego nombre = ' + strHex)

    lang = mystic.address.language
    icon = data[1]
    firstLetter = data[2]
    secondLetter = data[3]

#    print('hexName: ' + mystic.util.strHexa(data[0:9]))

    # si es del tipo magia ó es rom 'jp' ó el nombre comienza con un ícono y continúa una letra mayúscula ó es el Mirror (firstLetter == 'M' and secondLetter == 'i')
    if(self.tipo == 'magic' or lang == mystic.language.JAPAN or (icon in range(0xa0,0xb0) and firstLetter in range(0xb0,0xd4)) or (firstLetter == 198 and secondLetter == 220)):
#    if(True):
      name = ''
      for hexa in data[1:1+8]:
        if(hexa != 0x00):
          chary = mystic.dictionary.decodeByte(hexa)
          name += chary
        else:
          break
#      print('nombre: ' + name)
#      print('firstLetter: ' + str(firstLetter))
#      print('secondLetter: ' + str(secondLetter))
      # el nombre del item
      self.name = name

#      print('------ name: ' + name)

#      self.nose = data[9:9+7]

      byte0 = data[9]
#      print('byte0: {:02x}'.format(byte0))

      # el primer bit establece si se consume en un solo uso (por contra de varias veces)
      self.multiuse = 1 if (byte0 & 2**7 != 0) else 0
#      print('multiuse: ' + str(self.multiuse))
 
      # el segundo bit establece si es vendible
      self.unsellable = 1 if (byte0 & 2**6 != 0) else 0
#      print('unsellable: ' + str(self.unsellable))

      # bits desconocidos (todos cero?)
      self.bit_unknown_1 = 1 if (byte0 & 2**5 != 0) else 0
#      print('bit_unknown_1: ' + str(self.bit_unknown_1))
      self.bit_unknown_2 = 1 if (byte0 & 2**4 != 0) else 0
#      print('bit_unknown_2: ' + str(self.bit_unknown_2))
      self.bit_unknown_3 = 1 if (byte0 & 2**3 != 0) else 0
#      print('bit_unknown_3: ' + str(self.bit_unknown_3))
      self.bit_unknown_4 = 1 if (byte0 & 2**2 != 0) else 0
#      print('bit_unknown_4: ' + str(self.bit_unknown_4))

      mpCost1 = 1 if (byte0 & 2**1 != 0) else 0
      mpCost0 = 1 if (byte0 & 2**0 != 0) else 0
      self.magic_cost = mpCost1*2+mpCost0
#      print('magic_cost: ' + str(self.magic_cost))

      byte1 = data[10]
#      print('byte1: {:02x}'.format(byte1))

      self.bit_unknown_5 = 1 if (byte1 & 2**7 != 0) else 0
#      print('bit_unknown_5: ' + str(self.bit_unknown_5))

      cant2 = 1 if (byte1 & 2**6 != 0) else 0
      cant1 = 1 if (byte1 & 2**5 != 0) else 0
      cant0 = 1 if (byte1 & 2**4 != 0) else 0
      self.quantity = cant2*2**2 + cant1*2 + cant0
#      print('quantity: ' + str(self.quantity))

      self.shield = 1 if (byte1 & 2**3 != 0) else 0
#      print('shield: ' + str(self.shield))
      self.helmet = 1 if (byte1 & 2**2 != 0) else 0
#      print('helmet: ' + str(self.helmet))
      self.armor = 1 if (byte1 & 2**1 != 0) else 0
#      print('armor: ' + str(self.armor))
      self.weapon = 1 if (byte1 & 2**0 != 0) else 0
#      print('weapon: ' + str(self.weapon))

      byte2 = data[11]
      self.hp = byte2
#      print('hp: {:02x}'.format(self.hp))

      byte3 = data[12]
      self.mp = byte3
#      print('mp: {:02x}'.format(self.mp))

      byte4 = data[13]
      self.attack_defense_points = byte4
#      print('attack_defense_points: {:02x}'.format(self.attack_defense_points))

      byte5 = data[14]
      byte6 = data[15]
      self.gold_value = byte6*0x100 + byte5
#      print('gold_value: {:04x}'.format(self.gold_value))

      self.enabled = True
    # sino, el nombre no comienza con un ícono
    else:
      # lo considero desactivo
      self.enabled = False
      self.disabledBytes = data[0:16]

  def encodeTxt(self):
    lines = []
    lines.append('\n---------- nro: {:02x}'.format(self.nro))
    lines.append('tipo: ' + self.tipo)
    if(self.enabled):
      lines.append('name: ' + self.name)
#      strHex = mystic.util.strHexa(self.nose)
#      lines.append('nose: ' + strHex)

      # byte0
      lines.append('multiuse: ' + str(self.multiuse))
      lines.append('unsellable: ' + str(self.unsellable))
      lines.append('unknown_bits: {:1},{:1},{:1},{:1}'.format(self.bit_unknown_1, self.bit_unknown_2, self.bit_unknown_3, self.bit_unknown_4))
      lines.append('magic_cost: ' + str(self.magic_cost))

      # byte1
      lines.append('unknown_bit: {:1}'.format(self.bit_unknown_5))
      lines.append('quantity: {:1}'.format(self.quantity))
      lines.append('shield,helmet,armor,weapon: {:1},{:1},{:1},{:1}'.format(self.shield, self.helmet, self.armor, self.weapon))

      # byte2
      lines.append('hp: 0x{:02x}'.format(self.hp))
      # byte3
      lines.append('mp: 0x{:02x}'.format(self.mp))
      # byte4
      lines.append('attack_defense_points: 0x{:02x}'.format(self.attack_defense_points))

      # byte5 and byte6
      lines.append('gold_value: 0x{:04x}'.format(self.gold_value))

    else:
      strHex = mystic.util.strHexa(self.disabledBytes)
      lines.append('disabledBytes: ' + strHex)
    return lines

  def decodeTxt(self, lines):

    for line in lines:
      if('nro:' in line):
        idx0 = line.index('nro:')
        self.nro = int(line[idx0+4:].strip(),16)

      elif('name:' in line):
        idx0 = line.index('name:')
#        self.name = line[idx0+5:].strip()
        # es importante el espacio en blanco al final
        self.name = line[idx0+6:].rstrip('\n')
        self.enabled = True

#      elif('nose:' in line):
#        idx0 = line.index('nose:')
#        nose = line[idx0+5:].strip()
#        nose = nose.split()
#        nose = [int(nosy,16) for nosy in nose]
#        self.nose = nose

      elif('multiuse:' in line):
        idx0 = line.index('multiuse:')
        self.multiuse = int(line[idx0+9:].strip(),2)
      elif('unsellable:' in line):
        idx0 = line.index('unsellable:')
        self.unsellable = int(line[idx0+11:].strip(),2)

      elif('unknown_bits:' in line):
        idx0 = line.index('unknown_bits:')
        strBits = line[idx0+13:].strip()
        strBitsList = strBits.split(',')
        self.bit_unknown_1 = int(strBitsList[0].strip(),2)
        self.bit_unknown_2 = int(strBitsList[1].strip(),2)
        self.bit_unknown_3 = int(strBitsList[2].strip(),2)
        self.bit_unknown_4 = int(strBitsList[3].strip(),2)

      elif('magic_cost:' in line):
        idx0 = line.index('magic_cost:')
        self.magic_cost = int(line[idx0+11:].strip())

      elif('unknown_bit:' in line):
        idx0 = line.index('unknown_bit:')
        self.bit_unknown_5 = int(line[idx0+12:].strip(),2)
 
      elif('quantity:' in line):
        idx0 = line.index('quantity:')
        self.quantity = int(line[idx0+9:].strip())

      elif('shield,helmet,armor,weapon:' in line):
        idx0 = line.index('shield,helmet,armor,weapon:')
        strBits = line[idx0+27:].strip()
        strBitsList = strBits.split(',')
        self.shield = int(strBitsList[0].strip(),2)
        self.helmet = int(strBitsList[1].strip(),2)
        self.armor = int(strBitsList[2].strip(),2)
        self.weapon = int(strBitsList[3].strip(),2)

      elif('hp:' in line):
        idx0 = line.index('hp:')
        self.hp = int(line[idx0+3:].strip(),16)

      elif('mp:' in line):
        idx0 = line.index('mp:')
        self.mp = int(line[idx0+3:].strip(),16)

      elif('attack_defense_points:' in line):
        idx0 = line.index('attack_defense_points:')
        self.attack_defense_points = int(line[idx0+22:].strip(),16)

      elif('gold_value:' in line):
        idx0 = line.index('gold_value:')
        self.gold_value = int(line[idx0+11:].strip(),16)
#        print('gold value {:04x}'.format(self.gold_value))

      elif('disabledBytes:' in line):
        idx0 = line.index('disabledBytes:')
        diss = line[idx0+14:].strip()
        diss = diss.split()
        diss = [int(dissy,16) for dissy in diss]
        self.disabledBytes = diss
        self.enabled = False

  def encodeRom(self):
    array = []

    if(self.enabled):

      array.append(self.nro)

      for chary in self.name:
#        print('chary: ' + chary)
        hexy = mystic.dictionary.encodeChars(chary)
        array.append(hexy)

      strHex = mystic.util.strHexa(array)

      faltan = 9-len(array)
      extras = [0x00]*faltan
      array.extend(extras)

      mpCost1 = self.magic_cost // 2
      mpCost0 = self.magic_cost % 2

      byte0 = self.multiuse*2**7 + self.unsellable*2**6 + self.bit_unknown_1*2**5 + self.bit_unknown_2*2**4 + self.bit_unknown_3*2**3 + self.bit_unknown_4*2**2 + mpCost1*2**1 + mpCost0*2**0
#      print('byte0: {:02x}'.format(byte0))

      cant2 = (self.quantity & 0b100) // 4
      cant1 = (self.quantity & 0b010) // 2
      cant0 = (self.quantity & 0b001) // 1

      byte1 = self.bit_unknown_5*2**7 + cant2*2**6 + cant1*2**5 + cant0*2**4 + self.shield*2**3 + self.helmet*2**2 + self.armor*2**1 + self.weapon*2**0
#      print('byte1: {:02x}'.format(byte1))

      byte2 = self.hp
      byte3 = self.mp
      byte4 = self.attack_defense_points

      byte5 = self.gold_value % 0x100
      byte6 = self.gold_value // 0x100

      nose = [byte0, byte1, byte2, byte3, byte4, byte5, byte6]
#      strNoseOld = mystic.util.strHexa(self.nose)
#      print('strNoseOld: ' + strNoseOld)
#      strNoseNew = mystic.util.strHexa(nose)
#      print('strNoseNew: ' + strNoseNew)

      array.extend(nose)

    # sino, no está enabled
    else:
      array.extend(self.disabledBytes)

    return array

  def __str__(self):
    return self.name


##########################################################
class Apdp:

  def __init__(self):
    self.nose = 0x00
    self.apdp = ''
    self.noseArray = [0x00]*11

  def decodeRom(self, data):

    self.nose = data[0]

    array = data[1:5]
    string = ''
    # para cada byte del array
    for code in array:

      # lo decodifico
      if(code == 0xff):
        char = ' '
      else:
        char = mystic.dictionary.decodeByte(code)

      # y lo agrego al string
      string += char

    self.apdp = string

    for i in range(0,11):
      self.noseArray[i] = data[i+5]

  def encodeTxt(self):
    lines = []
    lines.append('nose: {:02x}'.format(self.nose))
    lines.append('apdp: ' + self.apdp)
    lines.append('noseArray: ' + mystic.util.strHexa(self.noseArray))
    return lines

  def decodeTxt(self, lines):

    strNose = lines[0][6:8]
    self.nose = int(strNose,16)

    strApdp = lines[1][6:10]
    self.apdp = strApdp

    strHexa = lines[2][11:].strip()
    self.noseArray = mystic.util.hexaStr(strHexa)


  def encodeRom(self):
    array = []

    array.append(self.nose)

    subArray = []
    for chary in self.apdp:
#      print('chary: ' + chary)
      hexy = mystic.dictionary.encodeChars(chary)
      subArray.append(hexy)

    array.extend(subArray)

    # por las dudas completo hasta formar 4 bytes el string
    faltan = 4-len(subArray)
    extras = [0xff]*faltan
    array.extend(extras)

    array.extend(self.noseArray)
    return array



  def __str__(self):
    return 'nose: {:02x}, apdp: '.format(self.nose) + self.apdp + ', noseArray: ' + mystic.util.strHexa(self.noseArray)




##########################################################
class Vendor:
  """ representa un vendedor """

  def __init__(self):
    self.nroVendor1 = 0x00
    self.nroVendor2 = 0x00

    self.items = []

  def decodeRom(self, data):
    self.nroVendor1 = data[0]
    self.nroVendor2 = data[1]

    for i in range(0,7):
      item = [ data[2*i+2], data[2*i+3] ]
      self.items.append(item)

  def encodeTxt(self):
    lines = []
    lines.append('\n--- vendor: {:02x} {:02x}'.format(self.nroVendor1, self.nroVendor2))
    for i in range(0,7):
      lines.append('item: {:02x} {:02x}'.format(self.items[i][0],self.items[i][1]))
 
    return lines

  def decodeTxt(self, lines):

    for line in lines:
      if('--- vendor:' in line):
        strVendor1 = line[12:14]
        self.nroVendor1 = int(strVendor1, 16)

        strVendor2 = line[15:17]
        self.nroVendor2 = int(strVendor2, 16)

      elif('item:' in line):
        strNroItem = line[6:8]
        nroItem = int(strNroItem, 16)

        strCodItem = line[9:11]
        codItem = int(strCodItem, 16)

        self.items.append( [nroItem, codItem] )


  def encodeRom(self):
    array = []

    array.append(self.nroVendor1)
    array.append(self.nroVendor2)

    for item in self.items:
      array.append(item[0])
      array.append(item[1])

    return array

  def __str__(self):
    string = 'vendor: {:02x} {:02x}\n'.format(self.nroVendor1, self.nroVendor2)
    for i in range(0,7):
 
      string += 'item: {:02x} {:02x}\n'.format(self.items[i][0],self.items[i][1])

    return string
 
