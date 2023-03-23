
import mystic.address
import mystic.util


##########################################################
class Vibratos:
  """ represents the list of vibratos """

  def __init__(self):
    self.vibratos = []
    self.cantVibratos = 5

  def decodeRom(self, bank, addrVibratos):
    self.vibratos = []

    vaPorAddr = addrVibratos
    for i in range(0, self.cantVibratos):

#      print('--- decoding vibrato ' + str(i))
      vibrato = Vibrato(i)

      vibrato.decodeRom(bank, vaPorAddr)
      self.vibratos.append(vibrato)

      array = vibrato.encodeRom()
      vaPorAddr += len(array)

  def encodeTxt(self):
    lines = []

    for i in range(0, self.cantVibratos):
      vibrato = self.vibratos[i]

      lines.append('-------- vibrato: {:02} addr: {:04x} --------'.format(i, vibrato.addr))

      subLines = vibrato.encodeTxt()
      lines.extend(subLines)
      lines.append('')
      lines.append('')

    return lines

  def decodeTxt(self, lines):

    self.vibratos = []

    i=0
    vibratoLines = []

    for line in lines:
#      print('line: ' + line)

      # si es un nuevo vibrato
      if('vibrato' in line):
        # y es el primero
        if(i==0):
          # vamos agragando renglones
          vibratoLines.append(line)
        # sino
        else:

#          print('--- decoding vibrato {:02}'.format(i-1))
          vibrato = Vibrato(i-1)
          vibrato.decodeTxt(vibratoLines)
          self.vibratos.append(vibrato)
          vibratoLines = []
          vibratoLines.append(line)
        i += 1
      # sino, el renglón no tiene vibrato
      else:
        # voy agregando renglones
        vibratoLines.append(line)

#    print('--- decoding vibrato {:02}'.format(i-1))
    # terminó el archivo, ya esta listo el último vibrato
    vibrato = Vibrato(i-1)
    vibrato.decodeTxt(vibratoLines)
    self.vibratos.append(vibrato)
    vibratoLines = []
    vibratoLines.append(line)

  def encodeRom(self, addrVibratos):

    array = []

    vaPorAddr = addrVibratos

    for i in range(0,len(self.vibratos)):
      vibrato = self.vibratos[i]
#      print('encoding vibrato: ' + str(vibrato.nro))

      vibrato.addr = vaPorAddr
      vibrato.refreshLabels()

      subArray = vibrato.encodeRom()

#      print('vaPorAddr {:04x} subArray: '.format(vaPorAddr) + mystic.util.strHexa(subArray))
      array.extend(subArray)
      vaPorAddr += len(subArray)

    return array

##########################################################
class Vibrato:
  """ represents a vibrato """

  def __init__(self, nro):
    self.nro = nro
    self.addr = 0x0000

    self.vibratoCmds = []

  def decodeRom(self, bank, vaPorAddr):

    self.vibratoCmds = []
    self.addr = vaPorAddr

    cmd = bank[vaPorAddr]
    vibratoCmd = VibratoCmd(vaPorAddr, cmd)
    vibratoCmd.decodeRom(bank[vaPorAddr:])

#    print('vibratoCmd: ' + str(vibratoCmd))
    self.vibratoCmds.append(vibratoCmd)

    while(vibratoCmd.cmd != 0x00):
      array = vibratoCmd.encodeRom()
      vaPorAddr += len(array)

      cmd = bank[vaPorAddr]
      vibratoCmd = VibratoCmd(vaPorAddr, cmd)
      vibratoCmd.decodeRom(bank[vaPorAddr:])

#      print('vibratoCmd: ' + str(vibratoCmd))
      self.vibratoCmds.append(vibratoCmd)


    # inicio el contador de labels
    lblCount = 1
    for vibratoCmd in self.vibratoCmds:
      # si es un JUMP
      if(vibratoCmd.cmd in [0x00]):
#        print('cmd: ' + str(vibratoCmd))
        addr = vibratoCmd.jumpAddr
#        print('cmd: ' + str(vibratoCmd) + ' addr: {:04x}'.format(addr))

        # busco el cmando al cual saltar
        for vibratyCmd in self.vibratoCmds:
#          print('vibraty addr {:04x}'.format(vibratyCmd.addr))
          if(vibratyCmd.addr == addr):
#            print('lo encontré: ' + str(vibratyCmd))
            # y le agrego el label
            vibratoCmd.jumpLabel = 'label{:}'.format(lblCount)
            vibratyCmd.labels.append('label{:}'.format(lblCount))
            # incremento el contador de labels
            lblCount += 1


  def encodeRom(self):
    array = []

    for vibratoCmd in self.vibratoCmds:
      subArray = vibratoCmd.encodeRom()
      array.extend(subArray)

    return array

  def encodeTxt(self):
    lines = []

#    lines.append('--- VIBRATO: {:02x} addr: {:04x}'.format(self.nro, self.addr))

    for vibratoCmd in self.vibratoCmds:

      # si tiene labels los imprimo
      for label in vibratoCmd.labels:
        lines.append(label + ':')

      lines.append(str(vibratoCmd))

    return lines


  def decodeTxt(self, lines):

    self.addr = None
    self.vibratoCmds = []

    # el addr del comando actual
    vaPorAddr = 0
    # los labels del comando actual
    currentLabels = []

    for line in lines:
      line = line.strip()

#      print('line: ' + line)

      # si es un comentario
      if(line.startswith('#') or len(line) == 0):
        # no hago nada
        pass
      # sino, no es un comentario
      else:

        # si comienza un canal
        if('vibrato' in line):
          tag = 'addr: '
          idx0 = line.index(tag)
          strAddr = line[idx0+6:idx0+10]
#          print('strAddr: ' + strAddr)
          addr = int(strAddr,16)
#          print('addr: {:04x}'.format(addr))
          self.addr = addr
          vaPorAddr = addr

        # si es un label (termina en ':')
        elif(':' in line):

          # le quito el ':'
          label = line[:len(line)-1]
          currentLabels.append(label)

        elif(line.startswith('LENGTH')):

          # find the first '=' 
          idx0 = line.replace('=', '@', 0).find('=')

          strLL = line[idx0+1:idx0+3]
#          print('strLL: ' + strLL)
          cmd = int(strLL,16)
          # es un comando de sonido
          vibratoCmd = VibratoCmd(vaPorAddr, cmd)
          vibratoCmd.labels = currentLabels
 
          idx1 = line.replace('=', '@', 1).find('=')
          strVal = line[idx1+1:idx1+3]
#          print('strVal: ' + strVal)
          val = int(strVal,16)
          vibratoCmd.arg = val

          self.vibratoCmds.append(vibratoCmd)

#          print('{:04x} cmd: '.format(vaPorAddr) + str(vibratoCmd))
#          print('{:04x} cmd: '.format(vibratoCmd.addr) + str(vibratoCmd))

          vaPorAddr += len(vibratoCmd.encodeRom())
          currentLabels = []

        elif(line.startswith('JUMP')):
#          idx0 = line.index(' ')
#          strAddr = line[idx0:].strip()
#          addr = int(strAddr,16)

          args = line.split()
          label = args[1]

          cmd = 0x00
          # es un comando de vibrato
          vibratoCmd = VibratoCmd(vaPorAddr, cmd)
          vibratoCmd.labels = currentLabels
          vibratoCmd.jumpLabel = label
#          vibratoCmd.jumpAddr = addr
          self.vibratoCmds.append(vibratoCmd)

#          print('{:04x} cmd: '.format(vaPorAddr) + str(vibratoCmd))
#          print('{:04x} cmd: '.format(vibratoCmd.addr) + str(vibratoCmd))

          vaPorAddr += len(vibratoCmd.encodeRom())
          currentLabels = []


#    for vibratoCmd in self.vibratoCmds:
#      print('{:04x} cmd: '.format(vibratoCmd.addr) + str(vibratoCmd) + str(vibratoCmd.labels))

    # calculo los addr de los labels !!!
    self.refreshLabels()

  def refreshLabels(self):
    """ setea los addrs de los labels """

    # el primer comando está en el addr
    vaPorAddr = self.addr

    # segunda pasada (para setear addr fisico de los labels)
    for vibratoCmd in self.vibratoCmds:

      vibratoCmd.addr = vaPorAddr
      vaPorAddr += len(vibratoCmd.encodeRom())

      # si es una instrucción de salto (JUMP)
      if(vibratoCmd.cmd in [0x00]):
#        print('vibratoCmd: ' + str(vibratoCmd))
        jumpLabel = vibratoCmd.jumpLabel
        for vibratyCmd in self.vibratoCmds:
          if(jumpLabel in vibratyCmd.labels):
#            print('lo encontré: {:4x}'.format(vibratyCmd.addr))
            vibratoCmd.jumpAddr = vibratyCmd.addr

 

##########################################################
class VibratoCmd:
  """ represents a vibrato command """

  def __init__(self, addr, cmd):

    # la dirección física dentro del bank de la rom
    self.addr = addr
    self.cmd = cmd
    self.arg = None

    self.jumpAddr = 0x0000
    # label al cual hace jump este comando 
    self.jumpLabel = None
    # lista de labels que se usan para saltar a este comando
    self.labels = []

  def decodeRom(self, array):

    cmd = array[0]
    self.cmd = cmd
    if(cmd != 0x00):
      self.arg = array[1]
    else:
      subAddr = array[2]*0x100 + array[1]
      self.jumpAddr = subAddr - 0x4000

  def encodeRom(self):
    array = []

    array.append(self.cmd)
    if(self.cmd != 0x00):
      array.append(self.arg)
    else:
      addr = self.jumpAddr + 0x4000
      array.extend([addr&0xff, addr//0x100])

    return array

  def __str__(self):

    if(self.cmd != 0x00):
      string = 'LENGTH={:02x} VAL={:02x}'.format(self.cmd, self.arg)
    else:
#      string = 'JUMP {:04x}'.format(self.jumpAddr)
      string = 'JUMP ' + str(self.jumpLabel)

#    string = '{:04x} - '.format(self.addr) + string
    return string

##########################################################
class Volumes:
  """ represents the list of volume envelopes """

  def __init__(self):
    self.volumes = []
    self.cantVolumes = 37

  def decodeRom(self, bank, addrVolumes):
    self.volumes = []

    vaPorAddr = addrVolumes
    for i in range(0, self.cantVolumes):

#      print('--- decoding volume ' + str(i))
      subArray = bank[vaPorAddr : vaPorAddr+2]
#      print('subArray: ' + mystic.util.strHexa(subArray))

      self.volumes.append(subArray)

      vaPorAddr += 2

  def encodeTxt(self):
    lines = []

    for i in range(0, self.cantVolumes):
      subArray = self.volumes[i]
      lines.append('LENGTH={:02x} VAL={:02x}'.format(subArray[0], subArray[1]))
    return lines

  def encodeRom(self, addrVolume):

    array = []

    vaPorAddr = addrVolume

    for i in range(0,len(self.volumes)):
      subArray = self.volumes[i]

#      print('vaPorAddr {:04x} subArray: '.format(vaPorAddr) + mystic.util.strHexa(subArray))
      array.extend(subArray)
      vaPorAddr += len(subArray)


    return array


  def decodeTxt(self, lines):

    self.volumes = []

    for line in lines:
      line = line.strip()
#      print('line: ' + line)

      # find the first '=' 
      idx0 = line.replace('=', '@', 0).find('=')
      strLL = line[idx0+1:idx0+3]
#      print('strLL: ' + strLL)
      length = int(strLL,16)

      # find the second '=' 
      idx0 = line.replace('=', '@', 1).find('=')
      strVal = line[idx0+1:idx0+3]
#      print('strVal: ' + strVal)
      val = int(strVal,16)

      volume = [length, val]
      self.volumes.append(volume)




##########################################################
class Waves:
  """ represents the list of waves """

  def __init__(self):
    self.waves = []
    self.cantWaves = 7

  def decodeRom(self, bank, addrWaves):
    self.waves = []

    vaPorAddr = addrWaves
    for i in range(0, self.cantWaves):

#      print('--- decoding wave ' + str(i))
      subArray = bank[vaPorAddr : vaPorAddr+16]
#      print('subArray: ' + mystic.util.strHexa(subArray))

      self.waves.append(subArray)

      vaPorAddr += 16

  def encodeTxt(self):
    lines = []

    for i in range(0, self.cantWaves):
      subArray = self.waves[i]
      lines.append('WAVE=' + mystic.util.strHexa(subArray))
    return lines

  def encodeRom(self, addrVolume):

    array = []

    vaPorAddr = addrVolume

    for i in range(0,len(self.waves)):
      subArray = self.waves[i]

#      print('vaPorAddr {:04x} subArray: '.format(vaPorAddr) + mystic.util.strHexa(subArray))
      array.extend(subArray)
      vaPorAddr += len(subArray)


    return array

  def decodeTxt(self, lines):

    self.waves = []

    for line in lines:
      line = line.strip()
#      print('line: ' + line)

      # find the first '=' 
      idx0 = line.replace('=', '@', 0).find('=')

      strWave = line[idx0+1:]
#      print('strWave: ' + strWave)
      subArray = mystic.util.hexaStr(strWave)
#      print('subArray: ' + mystic.util.strHexa(subArray))
      self.waves.append(subArray)



