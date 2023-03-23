
import mystic.address
import mystic.util

#Sounds can play on channel 1 and 4 (either or both).

#There is a table of pointers to channel 1 data at 0f:7b3c and channel 4 data at 0f:7b86. Each is 37 pointers.

#They point into data located at 0f:7bd0 and up (though there is nothing forcing them to).

#This data consists of four types of entries:
#1. 0xf0 to 0xff, the low nibble is loaded into a loop counter. I think 0xf0 is loop 255 and 0xf1 is loop zero?
#2. 0xef, if the loop counter is not one then the next two bytes are loaded into the current position pointer and the loop counter is decremented.
#3. 0x00 end of data.
#4. 0x01 to 0xee, this byte is a duration counter (in frames?) and the next bytes are fed to the channel. For channel 1 this would be followed by five bytes to be written into NR10 through NR14. For channel 4 it is followed by two bytes and NR44 is written with 0x80.

#An example from the airship sound (channel 4)

#7d8d:
#$f4		; load 4 into the counter (it is never going to allow this to hit zero)
#$03, $f8, $33	; durration=3, NR42=f8, NR43=33, NR44=80
#$02, $00, $00	; durration=2, NR42=00, NR43=00, NR44=80
#$03, $78, $43	; durration=3, NR42=78, NR43=43, NR44=80
#$02, $00, $00	; durration=2, NR42=00, NR43=00, NR44=80
#$ef, $8d, $7d	; jump 7d8d (back to start)
#$00 		; end (never reached)


##########################################################
class Sounds:
  """ represents the list of sounds """

  def __init__(self):
    self.sounds = []
    self.cantSFX = 37

  def decodeRom(self, bank, addrSounds):
    self.sounds = []

    addrs = []

    for i in range(0,self.cantSFX):

      baseCh1 = addrSounds + 2*i
      addr1 = bank[baseCh1+1]
      addr2 = bank[baseCh1]
      addrCh1 = addr1*0x100 + addr2 - 0x4000

      baseCh4 = addrSounds + 2*self.cantSFX + 2*i
      addr1 = bank[baseCh4+1]
      addr2 = bank[baseCh4]
      addrCh4 = addr1*0x100 + addr2 - 0x4000

      soundEffect = SoundEffect(i)
      soundEffect.decodeRom(bank, addrCh1, addrCh4)

      self.sounds.append(soundEffect)

  def encodeRom(self, addrSounds):
    addrsCh1 = []
    addrsCh4 = []
    dataArray = []

    vaPorAddr = addrSounds + 4*self.cantSFX

    # save the address of the empty channel
    emptyAddr = vaPorAddr
    # first add the empty channel
    dataArray.append(0x00)
    vaPorAddr += 1

#    for i in range(0,35):
    for i in range(0,len(self.sounds)):

      sound = self.sounds[i]
#      print('---encoding sfx: ' + str(sound.nro))

      sound.addrCh1 = vaPorAddr
      sound.refreshLabels()
      subArray = sound.encodeRomCh1()
      # add the "mystery header" (deleted sfx ch1)
      if(i == 33):
        subArray = [0x00,0x00,0x00,0x00,0x00,0x80,0x00]


      addrCh1 = vaPorAddr if len(subArray) > 0 else emptyAddr
      # we add the addr dictionary
      addrsCh1.append(addrCh1)
      # we add the sfx data to the array
      dataArray.extend(subArray)
      vaPorAddr += len(subArray)


      sound.addrCh4 = vaPorAddr
      sound.refreshLabels()
      subArray = sound.encodeRomCh4()
      # add the "mystery header" (deleted sfx ch4)
      if(i == 33): 
        subArray = [0x00,0x00,0x00,0x00]

      addrCh4 = vaPorAddr if len(subArray) > 0 else emptyAddr
      # we add the addr dictionary
      addrsCh4.append(addrCh4)
      # we add the sfx data to the array
      dataArray.extend(subArray)
      vaPorAddr += len(subArray)


    i = 0
    array1 = []
    for addr in addrsCh1:
#      print('{:02} {:04x} - addr1: {:04x}'.format(i, addrSounds + 2*i, addr))
      addr += 0x4000
      array1.append(addr % 0x100)
      array1.append(addr // 0x100)
      i += 1

    i = 0
    array4 = []
    for addr in addrsCh4:
#      print('{:02} {:04x} - addr1: {:04x}'.format(i, addrSounds + 2*i, addr))
      addr += 0x4000
      array4.append(addr % 0x100)
      array4.append(addr // 0x100)
      i += 1



    array = []
    array.extend(array1)
    array.extend(array4)
    array.extend(dataArray)

#    print('array: ' + mystic.util.strHexa(array))

    return array

  def encodeTxt(self):
    lines = []

    for i in range(0, self.cantSFX):
      soundEffect = self.sounds[i]

      lines.append('--------- sfx {:02} ---------'.format(i))

      subLines = soundEffect.encodeTxt()
      lines.extend(subLines)
      lines.append('')
      lines.append('')


    return lines

  def decodeTxt(self, lines):

    self.sounds = []

    i=0
    soundLines = []

    # por cada renglón
    for line in lines:
#      print('line: ' + line)

      # si es un nuevo efecto de sonido
      if('sfx' in line):
        # y es el primero
        if(i==0):
          # vamos agregando renglones
          soundLines.append(line)
        # sino
        else:
          sound = SoundEffect(i-1)
          sound.decodeTxt(soundLines)
          self.sounds.append(sound)
          soundLines = []
          soundLines.append(line)
        i += 1

      # sino, el renglón no tiene sfx
      else:
        # lo voy agregando
        soundLines.append(line)

    # terminó el archivo, ya esta listo el último sonido
    sound = SoundEffect(i-1)
    sound.decodeTxt(soundLines)
    self.sounds.append(sound)
    soundLines = []
    soundLines.append(line)




##########################################################
class SoundEffect:
  """ represents a sound effect """

  def __init__(self, nro):
    self.nro = nro
    self.addrCh1 = None
    self.addrCh4 = None

    self.soundCmds1 = []
    self.soundCmds4 = []

  def decodeRom(self, bank, addrCh1, addrCh4):
    self.addrCh1 = addrCh1
    self.addrCh4 = addrCh4


    self.soundCmds1 = []
    vaPorAddr = addrCh1
    self.soundCmds1 = self._decodeRom(bank, vaPorAddr, 1)

    self.soundCmds4 = []
    vaPorAddr = addrCh4
    self.soundCmds4 = self._decodeRom(bank, vaPorAddr, 4)


  def _decodeRom(self, bank, vaPorAddr, ch):

    soundCmds = []


    cmd = bank[vaPorAddr]
    soundCmd = SoundCmd(vaPorAddr, ch, cmd)
    soundCmd.decodeRom(bank[vaPorAddr:])

#    print('soundCmd: ' + str(soundCmd))
    soundCmds.append(soundCmd)

    i = 0
    while(soundCmd.cmd != 0x00):

      array = soundCmd.encodeRom()
      vaPorAddr += len(array)

      cmd = bank[vaPorAddr]
      soundCmd = SoundCmd(vaPorAddr, ch, cmd)
      soundCmd.decodeRom(bank[vaPorAddr:])

#      print('soundCmd: ' + str(soundCmd))
      soundCmds.append(soundCmd)

    # inicio el contador de labels
    lblCount = 1
    for soundCmd in soundCmds:
      # si es un JUMP
      if(soundCmd.cmd in [0xef]):
#        print('cmd: ' + str(soundCmd))
        addr = soundCmd.jumpAddr
#        print('cmd: ' + str(soundCmd) + ' addr: {:04x}'.format(addr))

        # busco el cmando al cual saltar
        for soundyCmd in soundCmds:
#          print('soundy addr {:04x}'.format(soundyCmd.addr))
          if(soundyCmd.addr == addr):
#            print('lo encontré: ' + str(soundyCmd))
            # y le agrego el label
            soundCmd.jumpLabel = 'label{:}'.format(lblCount)
            soundyCmd.labels.append('label{:}'.format(lblCount))
            # incremento el contador de labels
            lblCount += 1


    return soundCmds


  def encodeRomCh1(self):

    array = []

    # if it is not just an END (empty channel)
    if(len(self.soundCmds1) > 1):
      # we encode the channel 1
      for soundCmd1 in self.soundCmds1:
        subArray1 = soundCmd1.encodeRom()
#        print('subArray1: ' + mystic.util.strHexa(subArray1))
        array.extend(subArray1)

    return array

  def encodeRomCh4(self):

    array = []

    # if it is not just an END (empty channel)
    if(len(self.soundCmds4) > 1):
      # we encode the channel 4
      for soundCmd4 in self.soundCmds4:
        subArray4 = soundCmd4.encodeRom()
#        print('subArray4: ' + mystic.util.strHexa(subArray4))
        array.extend(subArray4)

    return array



  def encodeTxt(self):
    lines = []

    lines.append('--- CHANNEL: 01 addr: {:04x}'.format(self.addrCh1))

    for soundCmd in self.soundCmds1:
#      print('soundCmd: ' + str(soundCmd))

      # si tiene labels los imprimo
      for label in soundCmd.labels:
        lines.append(label + ':')

      subLines = soundCmd.encodeTxt()
      lines.extend(subLines)

    lines.append('--- CHANNEL: 04 addr: {:04x}'.format(self.addrCh4))
    for soundCmd in self.soundCmds4:
#      print('soundCmd: ' + str(soundCmd))

      # si tiene labels los imprimo
      for label in soundCmd.labels:
        lines.append(label + ':')

      subLines = soundCmd.encodeTxt()
      lines.extend(subLines)

    return lines


  def decodeTxt(self, lines):
    """ decoficina un efecto de sonido del txt """

    self.addrCh1 = None
    self.addrCh4 = None
    self.soundCmds1 = []
    self.soundCmds4 = []

    # el addr del comando actual
    vaPorAddr = 0
    # los labels del comando actual
    currentLabels = []

    # comienzo con un canal inválido
    ch = -1
    # y sin comandos
    cmds = []

    # saco el renglón del sfx
    lines.pop(0)

    # recorro los renglones
    for line in lines:
      line = line.strip()

      # si es un comentario
      if(line.startswith('#') or len(line) == 0):
        # no hago nada
        pass
      # sino, no es un comentario
      else:

        # si comienza un canal
        if('CHANNEL' in line):
          tag = 'CHANNEL: '
          idx0 = line.index(tag)
          strChannel = line[idx0+len(tag):idx0+len(tag)+2]
#          print('strChannel: ' + strChannel)
          ch = int(strChannel)
#          print('ch: ' + str(ch))
          strAddr = line[len(line)-4:len(line)]
#          print('strAddr: ' + strAddr)
          addr = int(strAddr,16)
#          print('addr: {:04x}'.format(addr))
          if(ch == 1):
            self.addrCh1 = addr
            # indico por que addr va el comando actual
            vaPorAddr = addr
          else:
            self.addrCh4 = addr
            # indico por que addr va el comando actual
            vaPorAddr = addr

        # sino
        elif(line == 'END'):

          cmd = 0x00
          # es un comando de sonido
          soundCmd = SoundCmd(vaPorAddr, ch, cmd)
          soundCmd.labels = currentLabels
          if(ch == 1):
            self.soundCmds1.append(soundCmd)
          else:
            self.soundCmds4.append(soundCmd)

          vaPorAddr += len(soundCmd.encodeRom())
          currentLabels = []

        # si es un label (termina en ':')
        elif(':' in line):

          # le quito el ':'
          label = line[:len(line)-1]
          currentLabels.append(label)

        elif(line.startswith('COUNTER')):
          idx0 = line.index(' ')
          strCounter = line[idx0:].strip()
          counter = int(strCounter)

          cmd = 0xf0 + counter
          # es un comando de sonido
          soundCmd = SoundCmd(vaPorAddr, ch, cmd)
          soundCmd.labels = currentLabels
          if(ch == 1):
            self.soundCmds1.append(soundCmd)
          else:
            self.soundCmds4.append(soundCmd)

          vaPorAddr += len(soundCmd.encodeRom())
          currentLabels = []


        elif(line.startswith('JUMP')):
#          idx0 = line.index(' ')
#          strAddr = line[idx0:].strip()
#          addr = int(strAddr,16)

          args = line.split()
          label = args[1]

          cmd = 0xef
          # es un comando de sonido
          soundCmd = SoundCmd(vaPorAddr, ch, cmd)
          soundCmd.labels = currentLabels
          soundCmd.jumpLabel = label
          if(ch == 1):
            self.soundCmds1.append(soundCmd)
          else:
            self.soundCmds4.append(soundCmd)

          vaPorAddr += len(soundCmd.encodeRom())
          currentLabels = []

 
        elif(line.startswith('LENGTH')):

          # find the first '=' 
          idx0 = line.replace('=', '@', 0).find('=')


          strLL = line[idx0+1:idx0+3]
#          print('strLL: ' + strLL)
          cmd = int(strLL,16)
          # es un comando de sonido
          soundCmd = SoundCmd(vaPorAddr, ch, cmd)
          soundCmd.labels = currentLabels
 


          # if it is channel 1
          if(ch == 1):

            idx1 = line.replace('=', '@', 1).find('=')
            idx2 = line.replace('=', '@', 2).find('=')
            idx3 = line.replace('=', '@', 3).find('=')
            idx4 = line.replace('=', '@', 4).find('=')
            idx5 = line.replace('=', '@', 5).find('=')

            strNR10 = line[idx1+1:idx1+3]
            strNR11 = line[idx2+1:idx2+3]
            strNR12 = line[idx3+1:idx3+3]
            strNR13 = line[idx4+1:idx4+3]
            strNR14 = line[idx5+1:idx5+3]

            params = [ int(strNR10,16), int(strNR11,16), int(strNR12,16), int(strNR13,16), int(strNR14,16) ]
            soundCmd.params = params
            self.soundCmds1.append(soundCmd)

          else:

            idx1 = line.replace('=', '@', 1).find('=')
            idx2 = line.replace('=', '@', 2).find('=')

            strNR10 = line[idx1+1:idx1+3]
            strNR11 = line[idx2+1:idx2+3]

            params = [ int(strNR10,16), int(strNR11,16) ]
            soundCmd.params = params
            self.soundCmds4.append(soundCmd)

          vaPorAddr += len(soundCmd.encodeRom())
          currentLabels = []

    # calculo los addr de los labels !!!
    self.refreshLabels()

  def refreshLabels(self):
    """ setea los addrs de los labels """

    # la primer nota está en addr del canal
    vaPorAddr = self.addrCh1

    # segunda pasada (para setear addr fisico de los labels)
    for soundCmd in self.soundCmds1:

      soundCmd.addr = vaPorAddr
      vaPorAddr += len(soundCmd.encodeRom())

      # si es una instrucción de salto (JUMP)
      if(soundCmd.cmd in [0xef]):
#        print('note: ' + str(nota))
        jumpLabel = soundCmd.jumpLabel
        for soundyCmd in self.soundCmds1:
          if(jumpLabel in soundyCmd.labels):
#            print('lo encontré: {:4x}'.format(soundyCmd.addr))
            soundCmd.jumpAddr = soundyCmd.addr

#    for nota in self.notas:
#      print('nota: ' + str(nota))

    # --- lo mismo pero en el canal 4

    # la primer nota está en addr del canal
    vaPorAddr = self.addrCh4

    # segunda pasada (para setear addr fisico de los labels)
    for soundCmd in self.soundCmds4:

      soundCmd.addr = vaPorAddr
      vaPorAddr += len(soundCmd.encodeRom())

      # si es una instrucción de salto (JUMP)
      if(soundCmd.cmd in [0xef]):
#        print('note: ' + str(nota))
        jumpLabel = soundCmd.jumpLabel
        for soundyCmd in self.soundCmds4:
          if(jumpLabel in soundyCmd.labels):
#            print('lo encontré: {:4x}'.format(soundyCmd.addr))
            soundCmd.jumpAddr = soundyCmd.addr


##########################################################
class SoundCmd:
  """ represents a sound command """

  def __init__(self, addr, ch, cmd):

    # la dirección física dentro del bank de la rom
    self.addr = addr
    # el canal donde se ejecuta el comando (1 ó 4)
    self.ch = ch
    self.cmd = cmd

    self.params = []
    self.jumpAddr = None
    # label al cual hace jump este comando 
    self.jumpLabel = None
    # lista de labels que se usan para saltar a este comando
    self.labels = []

  def decodeRom(self, array):

    cmd = array[0]
    self.cmd = cmd
    if(cmd >= 0x01 and cmd <= 0xee):

      if(self.ch == 1):
        subData = [array[i] for i in range(1,6)]
      elif(self.ch == 4):
        subData = [array[i] for i in range(1,3)]
#      print('{:02x}'.format(cmd) + ' - ' + mystic.util.strHexa(subData))
      self.params.extend(subData)
#      soundEffect.append({'data': '{:02x}'.format(data) + ' - ' + mystic.util.strHexa(subData) })

    elif(cmd == 0xef):

#      print('array: ' + mystic.util.strHexa(array[:5]))
      subAddr = array[2]*0x100 + array[1]
#      print('jump {:04x}'.format(subAddr))
      self.jumpAddr = subAddr - 0x4000
#      soundEffect.append({'data': '{:02x} {:04x}'.format(data, subAddr) })

    else:
      pass
#      print('{:02x}'.format(cmd))
#      soundEffect.append({'data': '{:02x}'.format(data)})


  def encodeRom(self):
    array = []

    array.append(self.cmd)
    array.extend(self.params)
    if(self.jumpAddr != None):
      addr = self.jumpAddr + 0x4000
      array.extend([addr&0xff, addr//0x100])

    return array

  def encodeTxt(self):
    lines = []

    if(self.cmd >= 0x01 and self.cmd <= 0xee):

      if(self.ch == 1):
        line = 'LENGTH={:02x} NR10={:02x} NR11={:02x} NR12={:02x} NR13={:02x} NR14={:02x}'.format(self.cmd, self.params[0], self.params[1], self.params[2], self.params[3], self.params[4])
      else:
        line = 'LENGTH={:02x} NR10={:02x} NR11={:02x}'.format(self.cmd, self.params[0], self.params[1])

    elif(self.cmd == 0xef):

#      line = 'JUMP {:04x}'.format(self.jumpAddr)
      line = 'JUMP ' + self.jumpLabel

    elif(self.cmd >= 0xf0 and self.cmd <= 0xff):
      val = self.cmd % 0x10
      line = 'COUNTER ' + str(val)


    elif(self.cmd == 0x00):

      line = 'END'

    else:
      line = '{:02x}'.format(self.cmd)

    lines.append(line)

    return lines

  def __str__(self):
    lines = self.encodeTxt()
    return lines[0]


