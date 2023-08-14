
import mystic.variables


##########################################################
class Windows:
  """ represents the windows data """

  def __init__(self):
    self.jsonWindows = {}

  def decodeRom(self):

#    print('--- 2:1baa')

    lang = mystic.address.language
    strLang = mystic.language.stockRomsLang[lang]
#    print('strLang: ' + strLang)

    nroBank,addr = mystic.address.addrWindows
    bank = mystic.romSplitter.banks[nroBank]
    # the total number of windows
    numWindows = 34

#    currentAddr = 0x1baa
    currentAddr = addr
#    print('currentAddr: {:04x}'.format(currentAddr))

    self.jsonWindows = {}


    self.jsonWindows['windows'] = []

    for i in range(0,numWindows):

      window = {}
      window['idWindow'] = i
      window['comment'] = mystic.variables.windows[i]

      subArray = bank[currentAddr: currentAddr+10]
      strArray = mystic.util.strHexa(subArray)
#      print('window: ' + strArray)

      window['x'] = subArray[0]
      window['y'] = subArray[1]
      window['w'] = subArray[2]
      window['h'] = subArray[3]
      # amount of rows to draw with labels
      window['labelRows'] = subArray[4]
      # length of each label
      window['labelWidth'] = subArray[5]
      # amount of cursor positions
      window['handPositions'] = subArray[6]
      # type of window (can select horizontally? has garbage bin? can swap items?)
      window['type'] = '{:08b}'.format(subArray[7])
      # amount of cursor columns
      window['columns'] = subArray[8]
      # horizontal cursor shift for columns
      window['horizontalShift'] = subArray[9]

      self.jsonWindows['windows'].append(window)
      currentAddr += 10

    nroBank,levelUpAddr = mystic.address.addrLevelUp
    bank = mystic.romSplitter.banks[nroBank]
    currentAddr = levelUpAddr 

    # labels of the level up choices
    levelUpChoiceLabel = ['Power', 'Wisdom', 'Stamina', 'Will']

    self.jsonWindows['levelUpChoices'] = []
    # for the 4 level up choices
    for i in range(0,4):

      levelUp = {}
      levelUp['idLevelUpChoice'] = i
      levelUp['comment'] = levelUpChoiceLabel[i]

      subArray = bank[currentAddr: currentAddr+4]
      strArray = mystic.util.strHexa(subArray)
#      print('levelUp: ' + strArray)
      levelUp['Stamn_Power_Wisdm_Will'] = strArray

      self.jsonWindows['levelUpChoices'].append(levelUp)
      currentAddr += 4


    nroBank,addrWindowsAddr = mystic.address.addrWindowsAddr
    bank = mystic.romSplitter.banks[nroBank]
    currentAddr = addrWindowsAddr

#    print('addrWindowsAddr: {:04x}'.format(addrWindowsAddr))

    addr1 = []
    for i in range(0,numWindows):
      addr = bank[currentAddr+1]*0x100 + bank[currentAddr]
#      print('addr1: {:04x}'.format(addr))
      addr1.append(addr)
      currentAddr += 2

    addr2 = []
    for i in range(0,numWindows):
      addr = bank[currentAddr+1]*0x100 + bank[currentAddr]
#      print('addr2: {:04x}'.format(addr))
      addr2.append(addr)
      currentAddr += 2

    addr3 = []
    for i in range(0,numWindows):
      addr = bank[currentAddr+1]*0x100 + bank[currentAddr]
#      print('addr3: {:04x}'.format(addr))
      addr3.append(addr)
      currentAddr += 2

    # recorro las 34 ventanas
    for i in range(0,numWindows):
      self.jsonWindows['windows'][i]['addr1'] = '{:04x}'.format(addr1[i])
      self.jsonWindows['windows'][i]['addr2'] = '{:04x}'.format(addr2[i])
      self.jsonWindows['windows'][i]['addr3'] = '{:04x}'.format(addr3[i])

#    print('currentAddr: {:04x}'.format(currentAddr))
  

#    if(True):
#    for i in range(0,37):
    i = 0
#    for window in self.jsonWindows['windows']:
    if(False):
#      window = self.jsonWindows['windows'][i]
#      print('win: ' + str(window))
      strAddr1 = window['addr1']
      strAddr2 = window['addr2']
      strAddr3 = window['addr3']

      strAddrs = [strAddr1, strAddr2, strAddr3]

      for strAddr in strAddrs:
     
        addr = int(strAddr,16)
        print('----i: ' + str(i) + ' addr: {:04x} '.format(addr) + mystic.variables.windows[i])
        if(addr >= 0x4000 and addr < 0x8000):
          addr -= 0x4000
          nroBank = 2
        elif(addr < 0x4000 and addr > 0x0000):
          nroBank = 0
        else:
          # working ram
          nroBank = -1


        if(nroBank >= 0):
          currentAddr = addr

          bank = mystic.romSplitter.banks[nroBank]
          labelRows = window['labelRows']
          handPositions = window['handPositions']
          labelWidth = window['labelWidth']
#          print('labelWidth: ' + str(labelWidth))

          tipo = int(window['type'],2)
#          if(tipo in [1,3]):
#            labelWidth = 16

#          for j in range(0,labelRows):
          for j in range(0,handPositions):
            subArray = bank[currentAddr : currentAddr + labelWidth]
            subArray = self._truncateSpecial(subArray)
#            print('subArray: ' + mystic.util.strHexa(subArray))
#            currentAddr += labelWidth
            currentAddr += len(subArray)

            label = ''
            for hexy in subArray:
              chars = mystic.dictionary.decodeByte(hexy)
              label += chars

            print('label: ' + label)
        
      i += 1


    nroBank = 2
    bank = mystic.romSplitter.banks[nroBank]

     
    addrMagic = self.jsonWindows['windows'][2]['addr1']
    addrMagic = int(addrMagic,16) - 0x4000
#    print('addrMagic: {:04x}'.format(addrMagic))
    currentAddr = addrMagic

#    labelRows = window['labelRows']
#    handPositions = window['handPositions']
#    labelWidth = window['labelWidth']
#    tipo = int(window['type'],2)

    self.jsonWindows['magic'] = []
    for i in range(0,8):
      subArray = bank[currentAddr : currentAddr+16]
      row = {}
      # pongo esto primero para que el comentario quede segundo
      row['id'] = 0
      row['comment'] = mystic.variables.magic[i]
      # decodifico la fila
      row = self._decodeRow(subArray, row)
      row['comment'] = mystic.variables.magic[i]
      self.jsonWindows['magic'].append(row)
      currentAddr += 16

    addrItems = self.jsonWindows['windows'][1]['addr1']
    addrItems = int(addrItems,16) - 0x4000
#    print('addrItems: {:04x}'.format(addrItems))
    currentAddr = addrItems
 
    self.jsonWindows['items'] = []
    for i in range(0,57):
      subArray = bank[currentAddr : currentAddr+16]
      row = {}
      # pongo esto primero para que el comentario quede segundo
      row['id'] = 0
      row['comment'] = mystic.variables.item[i]
      # decodifico la fila
      row = self._decodeRow(subArray, row)
      self.jsonWindows['items'].append(row)
      currentAddr += 16


    addrEquip = self.jsonWindows['windows'][3]['addr1']
    addrEquip = int(addrEquip,16) - 0x4000
#    print('addrEquip: {:04x}'.format(addrEquip))
    currentAddr = addrEquip
 
    self.jsonWindows['equip'] = []
    for i in range(0,48):
#    for i in range(0,46): 
      subArray = bank[currentAddr : currentAddr+16]
      row = {}
      # pongo esto primero para que el comentario quede segundo
      row['id'] = 0
      row['comment'] = mystic.variables.equip[i]
      # decodifico la fila
      row = self._decodeRow(subArray, row)

      self.jsonWindows['equip'].append(row)
      currentAddr += 16


#    addrApdp = self.jsonWindows['windows'][26]['addr1']
#    addrApdp = int(addrApdp,16) - 0x4000
#    print('addrApdp: {:04x}'.format(addrApdp))
#    currentAddr = addrApdp
 
#    self.jsonWindows['APDP'] = []
#    for i in range(0,2):
#      subArray = bank[currentAddr : currentAddr+16]
#      row = self._decodeRow(subArray)
#      self.jsonWindows['APDP'].append(row)
#      currentAddr += 16

#    print('currentAddr: {:04x}'.format(currentAddr))


    self.jsonWindows['vendorInventories'] = []
    for i in range(0,17):
      vendor = {}

      subArray = bank[currentAddr : currentAddr+16]

      vendor['idVendor'] = subArray[0]
      idid = subArray[0]*0x100 + subArray[1]
#      print('idid: {:04x}'.format(idid))

      items = []
      for j in range(0,7):
        idItem = subArray[2+2*j]
        if(idItem >= 128):
          idItem = idItem - 256
        ctrl = subArray[2+2*j+1]
#        print('item: ' + str(item) + ' ctrl: ' + str(ctrl))
        if(ctrl != 0):

#          print('idItem: ' + str(idItem))
          if(idItem <= 56):
            itemNameOld = self.jsonWindows['items'][idItem]['name']
            itemName = mystic.variables.item[idItem]
          else:
            itemNameOld = self.jsonWindows['equip'][idItem-57]['name']
            itemName = mystic.variables.equip[idItem-57]
#          print('itemName: ' + itemName)
          items.append({'idItem' : idItem, 'comment': itemName})
 
      vendor['items'] = items
      currentAddr += 16

      self.jsonWindows['vendorInventories'].append(vendor)


    nroBank,addr = mystic.address.addrInitialWeapons
    bank = mystic.romSplitter.banks[nroBank]

    self.jsonWindows['initialWeapons'] = {}

    idWeapon = bank[addr+0]-1
    idHelmet = bank[addr+1]-1

    ap     = bank[addr+2]
    strAp = '{:08b}'.format(ap)
    apHighBit = int(strAp[0])
    idAp = int('0' + strAp[1:],2)-1

    idArmor  = bank[addr+3]-1

#    idDp     = bank[addr+4]-1
    dp     = bank[addr+4]
    strDp = '{:08b}'.format(dp)
    dpHighBit = int(strDp[0])
    idDp = int('0' + strDp[1:],2)-1

    idShield = bank[addr+5]-1

#    strWeapon = self.jsonWindows['equip'][idWeapon]['name']
#    strHelmet = self.jsonWindows['equip'][idHelmet]['name']
#    strAp = self.jsonWindows['equip'][idAp]['name']
#    strArmor = self.jsonWindows['equip'][idArmor]['name']
#    strDp = self.jsonWindows['equip'][idDp]['name']
#    strShield = self.jsonWindows['equip'][idShield]['name']

    strWeapon = mystic.variables.equip[idWeapon]
    strHelmet = mystic.variables.equip[idHelmet]
    strAp = mystic.variables.equip[idAp]
    strArmor = mystic.variables.equip[idArmor]
    strDp = mystic.variables.equip[idDp]
    strShield = mystic.variables.equip[idShield]

    self.jsonWindows['initialWeapons']['weapon'] = {'idWeapon' : idWeapon, 'comment' : strWeapon}
    self.jsonWindows['initialWeapons']['helmet'] = {'idHelmet' : idHelmet, 'comment' : strHelmet}
#    self.jsonWindows['initialWeapons']['idAp'] = idAp
    self.jsonWindows['initialWeapons']['ap'] = {'idAp' : idAp, 'highBit' : apHighBit, 'comment' : strAp}
    self.jsonWindows['initialWeapons']['armor'] = {'idArmor' : idArmor, 'comment' : strArmor}
#    self.jsonWindows['initialWeapons']['idDp'] = idDp
    self.jsonWindows['initialWeapons']['dp'] = {'idDp' : idDp, 'highBit' : dpHighBit, 'comment' : strDp}
    self.jsonWindows['initialWeapons']['shield'] = {'idShield' : idShield, 'comment' : strShield}


    nroBank,addr = mystic.address.addrDoorTileLocations
    bank = mystic.romSplitter.banks[nroBank]

    currentAddr = addr
#    print('currentAddr: {:04x}'.format(currentAddr))

    # this are used on load state so that if the hero is standing on a doorway, it opens that door
    self.jsonWindows['doorTileLocations'] = []

    doors = ['north', 'south', 'east', 'west']
    for i in range(0,4):
      door = {}
      door['comment'] = doors[i]
      doorLocations = []
      x = bank[currentAddr]
      y = bank[currentAddr+1]
#      print('x: {:02x} y: {:02x}'.format(x,y))
      while(x != 0x00 or y != 0x00):
        x = bank[currentAddr]
        x = x if x < 128 else x-256
        y = bank[currentAddr+1]
        y = y if y < 128 else y-256
#        print('x: {:02x} y: {:02x}'.format(x,y))
        doorLocations.append( (x,y) )
        currentAddr += 2

      door['xy'] = str(doorLocations)
      self.jsonWindows['doorTileLocations'].append(door)

#    print('currentAddr: {:04x}'.format(currentAddr))

 
    self.jsonWindows['specialItems'] = []
    specialItems = ['itemsListCure', 'itemsListHeal', 'itemsListLevelup', 'itemsListSleep', 'itemsListMute', 'itemsListLights', 'itemsListCrystal', 'itemsListDamage' ]

    for i in range(0,8):

      itemList = {}
      itemList['comment'] = specialItems[i]
      items = []
 
      idItem = 0xff
      while(idItem != 0x00):
        idItem = bank[currentAddr]
#        print('idItem: {:02x}'.format(idItem))
        currentAddr += 1

        # if it is not the terminator 0x00
        if(idItem != 0x00):

          if(idItem <= 8):
            itemNameOld = self.jsonWindows['magic'][idItem-1]['name']
            itemName = mystic.variables.magic[idItem-1]
          else:
            itemNameOld = self.jsonWindows['items'][idItem-9]['name']
            itemName = mystic.variables.item[idItem-9]

#          items.append( {'idItem' : idItem, 'comment' : itemName, 'commentOld' : itemNameOld } )
          items.append( {'idItem' : idItem, 'comment' : itemName} )

      itemList['items'] = items

      self.jsonWindows['specialItems'].append(itemList)

#    print('currentAddr: {:04x}'.format(currentAddr))



    window = self.jsonWindows['windows'][0]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']
    currentAddr = self._appendItems('win_START_MENU', currentAddr, labelRows, labelWidth, bank)
    

    window = self.jsonWindows['windows'][17]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']    
    currentAddr = self._appendItems('win_SELECT_MENU', currentAddr, labelRows, labelWidth, bank)
    
    window = self.jsonWindows['windows'][24]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']    
    currentAddr = self._appendItems('win_LEVEL_UP_STATS_OPTIONS', currentAddr, labelRows, labelWidth, bank)
    
    window = self.jsonWindows['windows'][25]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']    
    currentAddr = self._appendItems('win_YES_NO', currentAddr, labelRows, labelWidth, bank)
    
    window = self.jsonWindows['windows'][33]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']    
    currentAddr = self._appendItems('win_LEVEL_UP', currentAddr, labelRows, labelWidth, bank)

    labelRows = 1
    labelWidth = 7
    if(strLang == 'de'):
      labelRows = 2
      labelWidth = 19
    elif(strLang == 'fr'):
      labelRows = 2
      labelWidth = 7
    elif(strLang == 'jp'):
      labelRows = 1
      labelWidth = 10


    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('bought', currentAddr, labelRows, labelWidth, bank)
    
    window = self.jsonWindows['windows'][15]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']
    currentAddr = self._appendItems('win_VENDOR_TEXT_TOP', currentAddr, labelRows, labelWidth, bank)

    labelRows = 2
    labelWidth = 15
    if(strLang == 'de'):
      labelRows = 3
      labelWidth = 18
    elif(strLang == 'jp'):
      # it has only one row, but I decode here the next (unused?) 'jp' text
      labelRows = 5

    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('notEnoughGp', currentAddr, labelRows, labelWidth, bank)

    window = self.jsonWindows['windows'][16]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']
    currentAddr = self._appendItems('win_VENDOR_SELL_NO', currentAddr, labelRows, labelWidth, bank)

    window = self.jsonWindows['windows'][11]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']
    currentAddr = self._appendItems('win_VENDOR_BUY_SELL', currentAddr, labelRows, labelWidth, bank)

    labelRows = 1
    labelWidth = 2
    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('statusScreenGoldLabel', currentAddr, labelRows, labelWidth, bank)

    window = self.jsonWindows['windows'][18]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']
    currentAddr = self._appendItems('win_STATUS_RIGHT', currentAddr, labelRows, labelWidth, bank)

    window = self.jsonWindows['windows'][20]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']
    currentAddr = self._appendItems('win_STATUS_HP_MP', currentAddr, labelRows, labelWidth, bank)


    window = self.jsonWindows['windows'][23]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']
    currentAddr = self._appendItems('win_LEVEL_UP_STATS', currentAddr, labelRows, labelWidth, bank)

#    labelRows = 2
#    labelWidth = 17
#    strAddr = '{:04x}'.format(currentAddr)
#    currentAddr = self._appendItems('levelUpText2', currentAddr, labelRows, labelWidth, bank)

#    if(strLang in ['en', 'fr', 'jp']):
    if(strLang != 'de'):
      # skip the unused '[00]' char in the 'en' version
      currentAddr += 1

    labelRows = 5
    labelWidth = 4
    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('statusEffectLabels', currentAddr, labelRows, labelWidth, bank)

    # we hardcode the addr for the 'jp' rom
    if(strLang == 'jp'):
      currentAddr = 0x1dc4

    labelRows = 1
    labelWidth = 4
    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('boyLabel', currentAddr, labelRows, labelWidth, bank)

    labelRows = 1
    labelWidth = 4
    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('girlLabel', currentAddr, labelRows, labelWidth, bank)

#    window = self.jsonWindows['windows'][30]
#    strAddr = window['addr3']
#    currentAddr = int(strAddr,16) - 0x4000
#    labelRows = window['labelRows']
#    labelWidth = window['labelWidth']
#    currentAddr = self._appendItems('win_NAMING_BOTTOM', currentAddr, labelRows, labelWidth, bank)

    labelRows = 9
    labelWidth = 9

    # we hardcode the addr for the 'jp' rom
    if(strLang == 'jp'):
      labelRows = 20

    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('nameEntryInputOptions', currentAddr, labelRows, labelWidth, bank)

    window = self.jsonWindows['windows'][31]
    strAddr = window['addr3']
    currentAddr = int(strAddr,16) - 0x4000
    labelRows = window['labelRows']
    labelWidth = window['labelWidth']
    currentAddr = self._appendItems('win_NEW_GAME_CONTINUE', currentAddr, labelRows, labelWidth, bank)

    labelRows = 2
    labelWidth = 21

    if(strLang == 'jp'):
      labelRows = 1

    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('titleScreenLicenseText', currentAddr, labelRows, labelWidth, bank)


    labelRows = 37
    labelWidth = 19
    if(strLang == 'de'):
      labelRows = 34
    elif(strLang == 'fr'):
      labelRows = 32
    elif(strLang == 'jp'):
      currentAddr = 0x3e48
      labelRows = 30
    strAddr = '{:04x}'.format(currentAddr)
    currentAddr = self._appendItems('introScrollText', currentAddr, labelRows, labelWidth, bank)


  def _appendItems(self, windowLabel, currentAddr, labelRows, labelWidth, bank):

    self.jsonWindows[windowLabel] = {}

    strAddr = '{:04x}'.format(currentAddr)
    self.jsonWindows[windowLabel]['comment'] = strAddr

    self.jsonWindows[windowLabel]['items'] = []
    for j in range(0,labelRows):
#    for j in range(0,handPositions):
      subArray = bank[currentAddr : currentAddr + labelWidth]
      subArray = self._truncateSpecial(subArray)
#      print('subArray: ' + mystic.util.strHexa(subArray))
#      currentAddr += labelWidth
      currentAddr += len(subArray)

#      label = ''
#      for hexy in subArray:
#        chars = mystic.dictionary.decodeByte(hexy, False)
#        label += chars

      label = mystic.dictionary.decodeArray(subArray, False)

#      print('label: ' + label)
      self.jsonWindows[windowLabel]['items'].append(label)
      
    return currentAddr



  def _decodeRow(self, array, row):
    row['id'] = array[0]

    subArray = array[1:8+1]
#    label = ''
#    for hexy in subArray:
#      chars = mystic.dictionary.decodeByte(hexy, False)
#      label += chars
    label = mystic.dictionary.decodeArray(subArray, False)
    row['name'] = label

    strAttrs = '{:08b}'.format(array[9])
#    row['strAtrs'] = strAttrs
    row['[0]multiuse [1]unsellable [2]unknown [3-7]mana_cost'] = strAttrs
#    row['multiuse'] = int(strAttrs[0])
#    row['unsellable'] = int(strAttrs[1])
#    row['unknown_bit'] = strAttrs[2]
#    row['mana_cost'] = int(strAttrs[3:8],2)

    strAttrs = '{:08b}'.format(array[10])
    row['[0]usable [1-3]quantity [4-7]shield_helmet_armor_weapon'] = strAttrs
#    row['usable'] = int(strAttrs[0])
#    row['quantity'] = int(strAttrs[1:1+3],2)
#    row['shield_helmet_armor_weapon'] = strAttrs[4:8]

    strAttrs = '{:08b}'.format(array[11])
    # helmets and armor: DP
    # weapons,spells, offsnsive items: [0]sleep [1]nuke [2]electric [3]ice [4]fire [5]star [6]silver [7]basic
    # player shield: [7]level_1_projectiles [6]level_2 [5]level_3 [4]level_4 [3]ice [2]fire [1]level_5 [0]always_1
    row['DP or [0]sleep [1]nuke [2]electric [3]ice [4]fire [5]star [6]silver [7]basic'] = strAttrs

    strAttrs = '{:02x}'.format(array[12])
    # element resistances/bonuses (MP?)
    row['resistances_bonuses'] = strAttrs

    strAttrs = '{:02x}'.format(array[13])
    # attack and defense points
    row['APDP'] = strAttrs

    # price to buy from a shop
    row['gold_value'] = '{:04x}'.format(array[15]*0x100 + array[14])
    price = array[15]*0x100 + array[14]
    if(price >= 32768):
      price = price - 65536
    row['int_gold_value'] = price

    return row


  def _truncateSpecial(self, array):
    """ truncates the array to the first special character """

    subArray = []

    for hexy in array:
      subArray.append(hexy)
      if(hexy <= 0x1f):
        break

    return subArray



  def _encodeRow(self, row):
    subArray = []

    subArray.append(row['id'])

    name = row['name']
#    print('------name: ' + name)
    values = mystic.dictionary.tryCompress(name, False)
#    print('values: ' + mystic.util.strHexa(values))
    subArray.extend(values)

    sMagicBits = row['[0]multiuse [1]unsellable [2]unknown [3-7]mana_cost']
    magicBits = int(sMagicBits, 2)
    subArray.append(magicBits)

    sWeaponBits = row['[0]usable [1-3]quantity [4-7]shield_helmet_armor_weapon']
    weaponBits = int(sWeaponBits, 2)
    subArray.append(weaponBits)

    sTypeBits = row['DP or [0]sleep [1]nuke [2]electric [3]ice [4]fire [5]star [6]silver [7]basic']
    typeBits = int(sTypeBits, 2)
    subArray.append(typeBits)

    sResistance = row['resistances_bonuses']
    resistance = int(sResistance, 16)
    subArray.append(resistance)

    sApdp = row['APDP']
    apdp = int(sApdp, 16)
    subArray.append(apdp)

    sGold = row['gold_value']
    gold = int(sGold, 16)
    subArray.extend( [gold%0x100, gold//0x100] )

    return subArray


  def _getArrayLevelUp(self):

    arrayLevelUp = []

    for levelUp in self.jsonWindows['levelUpChoices']:

      stamnPowerWisdmWill = levelUp['Stamn_Power_Wisdm_Will']
#      print('stamnPowerWisdmWill: ' + stamnPowerWisdmWill)
      subArray = mystic.util.hexaStr(stamnPowerWisdmWill)
      arrayLevelUp.extend(subArray)

    return arrayLevelUp

  def _getArrayWindowsAddr(self):

    arrayWindowsAddr = []

    for window in self.jsonWindows['windows']:
      strAddr1 = window['addr1']
#      print('strAddr1: ' + strAddr1)
      addr1 = int(strAddr1,16)
      arrayWindowsAddr.extend( [addr1%0x100, addr1//0x100] )

    for window in self.jsonWindows['windows']:
      strAddr2 = window['addr2']
#      print('strAddr2: ' + strAddr2)
      addr2 = int(strAddr2,16)
      arrayWindowsAddr.extend( [addr2%0x100, addr2//0x100] )

    for window in self.jsonWindows['windows']:
      strAddr3 = window['addr3']
#      print('strAddr3: ' + strAddr3)
      addr3 = int(strAddr3,16)
      arrayWindowsAddr.extend( [addr3%0x100, addr3//0x100] )

    return arrayWindowsAddr


  def _getArrayItems(self):
    arrayItems = []

    for magic in self.jsonWindows['magic']:
#      print('magic: ' + str(magic))
      subArray = self._encodeRow(magic)
#      print('subArray: ' + mystic.util.strHexa(subArray))
      arrayItems.extend(subArray)

    for item in self.jsonWindows['items']:
#      print('item: ' + str(item))
      subArray = self._encodeRow(item)
#      print('subArray: ' + mystic.util.strHexa(subArray))
      arrayItems.extend(subArray)

    for weap in self.jsonWindows['equip']:
#      print('weap: ' + str(weap))
      subArray = self._encodeRow(weap)
#      print('subArray: ' + mystic.util.strHexa(subArray))
      arrayItems.extend(subArray)

#    for apdp in self.jsonWindows['APDP']:
#      print('apdp: ' + str(apdp))
#      subArray = self._encodeRow(apdp)
#      print('subArray: ' + mystic.util.strHexa(subArray))
#      arrayItems.extend(subArray)

    for vendor in self.jsonWindows['vendorInventories']:
      subArray = []

      idVendor = vendor['idVendor']      
      subArray.append(idVendor)
      subArray.append(idVendor)

#      print('vendor: ' + str(vendor))
      for item in vendor['items']:
#        print('item: ' + str(item))
        idItem = item['idItem']
        subArray.append(idItem)
        subArray.append(0x0a)

      unusedCant = 7 - len(vendor['items'])
      unusedBytes = [0xff, 0x00]*unusedCant
#      print('unusedBytes: ' + mystic.util.strHexa(unusedBytes))
      subArray.extend(unusedBytes)

#      print('subArray: ' + mystic.util.strHexa(subArray))
      arrayItems.extend(subArray)

    return arrayItems


  def _getArrayLabels(self):

    arrayLabels = []

    for item in self.jsonWindows['win_START_MENU']['items']:
#      print('item: ' + item)
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['win_SELECT_MENU']['items']:
#      print('item: ' + item)
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['win_LEVEL_UP_STATS_OPTIONS']['items']:
#      print('item: ' + item)
      values = mystic.dictionary.tryCompress(item, False)
#      print('values: ' + mystic.util.strHexa(values))
      arrayLabels.extend(values)

    for item in self.jsonWindows['win_YES_NO']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    lang = mystic.address.language
    strLang = mystic.language.stockRomsLang[lang]
    if(strLang == 'fr'):
      arrayLabels.append(0x00)

    for item in self.jsonWindows['win_LEVEL_UP']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['bought']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['win_VENDOR_TEXT_TOP']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['notEnoughGp']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)


    if(strLang == 'fr'):
      values = mystic.dictionary.tryCompress('EST-CE[00]', False)
      arrayLabels.extend(values)


    for item in self.jsonWindows['win_VENDOR_SELL_NO']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['win_VENDOR_BUY_SELL']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['statusScreenGoldLabel']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['win_STATUS_RIGHT']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    if(strLang == 'fr'):
      arrayLabels.append(0x00)

    for item in self.jsonWindows['win_STATUS_HP_MP']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['win_LEVEL_UP_STATS']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

#    if(strLang in ['en', 'fr', 'jp']):
    if(strLang != 'de'):
      arrayLabels.append(0x00)

    for item in self.jsonWindows['statusEffectLabels']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    return arrayLabels


  def _getArrayLabels2(self):

    arrayLabels = []

    for item in self.jsonWindows['boyLabel']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['girlLabel']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['nameEntryInputOptions']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['win_NEW_GAME_CONTINUE']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    for item in self.jsonWindows['titleScreenLicenseText']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayLabels.extend(values)

    return arrayLabels


  def _getArrayIntro(self):
    arrayIntro = []

    for item in self.jsonWindows['introScrollText']['items']:
      values = mystic.dictionary.tryCompress(item, False)
      arrayIntro.extend(values)

    return arrayIntro


  def encodeRom(self):

    arrayWindows = []

    nroBank,addrWindows = mystic.address.addrWindows
    bank = mystic.romSplitter.banks[nroBank]

    currentAddr = addrWindows

    for window in self.jsonWindows['windows']:
#      print('win: ' + str(window))
      subArray = []
      subArray.append(window['x'])
      subArray.append(window['y'])
      subArray.append(window['w'])
      subArray.append(window['h'])
      subArray.append(window['labelRows'])
      subArray.append(window['labelWidth'])
      subArray.append(window['handPositions'])
      strType = window['type']
#      print('strType: ' + strType)
      intType = int(strType,2)
#      print('intType: ' + str(intType))
      subArray.append(intType)
      subArray.append(window['columns'])
      subArray.append(window['horizontalShift'])

#      print('window: ' + mystic.util.strHexa(subArray))

      arrayWindows.extend(subArray)
      currentAddr += len(subArray)

    arrayLevelUp = self._getArrayLevelUp()
    currentAddr += len(arrayLevelUp)

    arrayWindowsAddr = self._getArrayWindowsAddr()
    currentAddr += len(arrayWindowsAddr)

#    print('currentAddr: {:04x}'.format(currentAddr))

    arrayItems = self._getArrayItems()


    arrayInitialWeapons = []
    idWeapon = self.jsonWindows['initialWeapons']['weapon']['idWeapon']+1
    idHelmet = self.jsonWindows['initialWeapons']['helmet']['idHelmet']+1
    apHighBit = self.jsonWindows['initialWeapons']['ap']['highBit']
    idAp = apHighBit*2**7 + self.jsonWindows['initialWeapons']['ap']['idAp']+1
    idArmor = self.jsonWindows['initialWeapons']['armor']['idArmor']+1
    dpHighBit = self.jsonWindows['initialWeapons']['dp']['highBit']
    idDp = dpHighBit*2**7 + self.jsonWindows['initialWeapons']['dp']['idDp']+1
    idShield = self.jsonWindows['initialWeapons']['shield']['idShield']+1
    arrayInitialWeapons.extend( [idWeapon, idHelmet, idAp, idArmor, idDp, idShield] )


    arrayDoor = []

    for door in self.jsonWindows['doorTileLocations']:
#      print('door: ' + str(door))
      subArray = []

      sXy = door['xy']
#      print('sXy: ' + sXy)

      xys = sXy.replace('[','').replace(']','').replace('(','').replace(')','').replace(',','').split()
      for xy in xys:
        xy = int(xy)
#        print('xy: ' + str(xy))

        if(xy < 0):
          xy += 256

        subArray.append(xy)
      arrayDoor.extend(subArray)

    for items in self.jsonWindows['specialItems']:
      subArray = []
#      print('items: ' + str(items))
      for item in items['items']:
#        print('item: ' + str(item))
        subArray.append(item['idItem'])
      subArray.append(0x00)

      arrayDoor.extend(subArray)


    arrayLabels = self._getArrayLabels()
    arrayLabels2 = self._getArrayLabels2()
    arrayIntro = self._getArrayIntro()



#    strArray = mystic.util.strHexa(array)
#    print('array: ' + strArray)

    return arrayWindows, arrayLevelUp, arrayWindowsAddr, arrayItems, arrayInitialWeapons, arrayDoor, arrayLabels, arrayLabels2, arrayIntro



