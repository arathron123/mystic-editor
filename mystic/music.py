
import mystic.address
import mystic.util

##########################################################
class Canciones:
  """ representa la lista de canciones """

  def __init__(self):
    self.canciones = []

  def decodeRom(self, bank, addrMusic):
    self.canciones = []

    # initial value can be anything sufficiently large
    lowestSongAddress = 0x8000
    # assume song data follows the song address table (almost) directly
    # and use that to determine how many songs there are
    i = 0
    while (addrMusic + 0x4000 + 6 * (i+1) <= lowestSongAddress):

      cancion = Cancion(i)

#      base = 0x0a12 + 6*i
      base = addrMusic + 6*i
      addrCh2 = bank[base + 1]*0x100 + bank[base + 0]
      addrCh1 = bank[base + 3]*0x100 + bank[base + 2]
      addrCh3 = bank[base + 5]*0x100 + bank[base + 4]

      # la decodifico
      cancion.decodeRom(bank, addrCh2, addrCh1, addrCh3)

      print('--- ' + str(i) + ' i: {:02x} | cancion: '.format(i) + str(cancion))

      # y la agrego a la lista
      self.canciones.append(cancion)

      # this lets us figure out how many songs there are
      if (cancion.addrCh2 < lowestSongAddress):
        lowestSongAddress = cancion.addrCh2

      i += 1

    # the order of the songs in the pointer table does not always match the order their data is stored
    ordering = []
    for cancion in self.canciones:
      length = len(cancion.melody2.encodeRom())
      length += len(cancion.melody1.encodeRom())
      length += len(cancion.melody3.encodeRom())
      ordering.append((cancion.nro, cancion.addrCh2, length))
    ordering.sort(key=lambda x: x[1])
    for i in range(0, len(self.canciones)):
      self.canciones[ordering[i][0]].order = i

    # now that all song ranges are known headers (unused bytes between songs) can be extracted
    ordering.insert(0, (-1, addrMusic + 0x4000, 6 * len(self.canciones)))
    for i in range(len(self.canciones)):
      nro = ordering[i+1][0]
      start = ordering[i][1] + ordering[i][2] - 0x4000
      end = ordering[i+1][1] - 0x4000
      if start != end:
        self.canciones[nro].header = bank[start:end]

  def encodeTxt(self):

    lines = []

    basePath = mystic.address.basePath
    path = basePath + '/audio'

    # para cada canción
    for cancion in self.canciones:

      # agarro la canción
      subLines = cancion.encodeTxt()
      lines.extend(subLines)

    return lines
    
  def decodeTxt(self, lines):
    """ decodifica la lista de canciones del txt """

    self.canciones = []

    i=0
    songLines = []

    # por cada renglón
    for line in lines:

      # si es una nueva canción
      if('song' in line):
        # y es la primera
        if(i==0): 
          # vamos agregando renglones
          songLines.append(line)
        # sino
        else:
          cancion = Cancion(i-1)
          cancion.decodeTxt(songLines)
          self.canciones.append(cancion)
          songLines = []
          songLines.append(line)
        i += 1

      # sino, el renglón no tiene song
      else:
        # lo voy agregando
        songLines.append(line)
 
    # terminó el archivo, ya esta lista la ultima canción
    cancion = Cancion(i-1)
    cancion.decodeTxt(songLines)
    self.canciones.append(cancion)
    songLines = []
    songLines.append(line)

  def encodeRom(self, addrMusic):
    array = []

    # current data pointer
#    addrData = addrMusic + 0x4000 + 6 * len(self.canciones)
#    print('addrData: {:04x}'.format(addrData))

    # sorted by the order the data appears, which is sometimes different than the order in the table (nro)
    songs = sorted(self.canciones, key=lambda x: x.order)

    # el addr de la primer canción
    addrCancion = addrMusic + 0x4000 + 6 * len(songs)

    arrayAddresses = []
    arrayData = []

#    for i in range(0,30):
    for song in songs:
#      song = songs[i]
#      print('song nro: ' + str(song.nro))

      # codifico la canción (eso actualiza sus addrChx)
      arrayCancion = song.encodeRom(addrCancion)
      arrayData.extend(arrayCancion)
      addrCancion += len(arrayCancion)

#      if(song.nro == 0):
#        print('addrCh2: {:04x}'.format(song.addrCh2))
#        print('addrCh1: {:04x}'.format(song.addrCh1))
#        print('addrCh3: {:04x}'.format(song.addrCh3))

#        print('arrayCancion: ' + mystic.util.strHexa(arrayCancion))

#      print('cancion: ' + mystic.util.strHexa(arrayCancion))
#      print('addrCh2: {:04x}'.format(song.addrCh2))
#      print('addrCh1: {:04x}'.format(song.addrCh1))
#      print('addrCh3: {:04x}'.format(song.addrCh3))

#      arrayAddresses.extend([song.addrCh2&0xff, song.addrCh2//0x100])
#      arrayAddresses.extend([song.addrCh1&0xff, song.addrCh1//0x100])
#      arrayAddresses.extend([song.addrCh3&0xff, song.addrCh3//0x100])

    # los addresses van en el orden de canción (no el orden en que se queman)
    for song in self.canciones:
      arrayAddresses.extend([song.addrCh2&0xff, song.addrCh2//0x100])
      arrayAddresses.extend([song.addrCh1&0xff, song.addrCh1//0x100])
      arrayAddresses.extend([song.addrCh3&0xff, song.addrCh3//0x100])

    # agrego el array de addresses
    array.extend(arrayAddresses)
    # y el array de data de melodias
    array.extend(arrayData)

#    print('arrayAddresses: ' + mystic.util.strHexa(arrayAddresses))
#    print('arrayData: ' + mystic.util.strHexa(arrayData))

    return array


##########################################################
class Cancion:
  """ representa una cancion """

  def __init__(self, nro):
    self.nro = nro
    self.order = nro

    # si la canción puede terminar en repeat en lugar de loop
    # solo la cancion 2, que se le permite terminar en repeat por un bug en la rom
    self.repeatTermina = (nro == 2)

    # optional (not very useful) data header
    self.header = []

    self.addrCh2 = None
    self.addrCh1 = None
    self.addrCh3 = None

    self.melody2 = None
    self.melody1 = None
    self.melody3 = None

  def decodeRom(self, bank, addrCh2, addrCh1, addrCh3):
    """ decodifica una cancion """

    self.addrCh2 = addrCh2
    self.addrCh1 = addrCh1
    self.addrCh3 = addrCh3


    melody2 = Melody(nroChannel=2, addr=self.addrCh2, repeatTermina=self.repeatTermina)
    melody2.decodeRom(bank)
    self.melody2 = melody2
    melody1 = Melody(nroChannel=1, addr=self.addrCh1, repeatTermina=self.repeatTermina)
    melody1.decodeRom(bank)
    self.melody1 = melody1
    melody3 = Melody(nroChannel=3, addr=self.addrCh3, repeatTermina=self.repeatTermina)
    melody3.decodeRom(bank)
    self.melody3 = melody3

  def encodeRom(self, addrCancion):
    array = []

    # headers are useless, but preserved to ensure no unnecessary changes
    array.extend(self.header)

    vaPorAddr = addrCancion + len(self.header)
    self.addrCh2 = vaPorAddr
    self.melody2.addr = vaPorAddr
    self.melody2.refreshLabels()
#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

#    print('melody2 addr: {:04x}'.format(self.melody2.addr))
    melody2Rom = self.melody2.encodeRom()
    array.extend(melody2Rom)
#    print('melody2: ' + mystic.util.strHexa(melody2Rom))

    vaPorAddr += len(melody2Rom)
    self.addrCh1 = vaPorAddr
    self.melody1.addr = vaPorAddr
    self.melody1.refreshLabels()
#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

#    melody1Addr = self.melody1.addr
#    print('melody1 addr: {:04x}'.format(melody1Addr))
    # update the addr where the next channel starts
    self.melody1.addr = vaPorAddr
    melody1Rom = self.melody1.encodeRom()
    array.extend(melody1Rom)
#    print('melody1: ' + mystic.util.strHexa(melody1Rom))

    vaPorAddr += len(melody1Rom)
    self.addrCh3 = vaPorAddr
    self.melody3.addr = vaPorAddr
    self.melody3.refreshLabels()
#    print('vaPorAddr: {:04x}'.format(vaPorAddr))

#    melody3Addr = self.melody3.addr
#    print('melody3 addr: {:04x}'.format(melody3Addr))
    # update the addr where the next channel starts
    self.melody3.addr = vaPorAddr
    melody3Rom = self.melody3.encodeRom()
    array.extend(melody3Rom)
#    print('melody3: ' + mystic.util.strHexa(melody3Rom))

    return array


  def encodeTxt(self):
    lines = []

    lines.append('\n--------- song {:02} ---------'.format(self.nro))

    if self.order != self.nro:
      lines.append('\nORDER {}'.format(self.order))

    if self.header is not None:
      header = '\nHEADER'
      for i in self.header:
        header += ' {:x}'.format(i)
      lines.append(header)

    lines.extend(self.melody2.encodeTxt())
    lines.extend(self.melody1.encodeTxt())
    lines.extend(self.melody3.encodeTxt())

    return lines

  def decodeTxt(self, lines):
    """ decodifica una cancion del txt """

    currAddr = 0x0000
    channels = [2,1,3]
    i=0
    chLines = []

    # por cada renglón
    for line in lines:

      if('ORDER' in line):
        self.order = int(line.split()[1])
      elif('HEADER' in line):
        self.header = []
        for n in line.split()[1:]:
          self.header.append(int(n, base=16))
      # si es un nuevo channel
      elif('CHANNEL' in line):
        # y es el primero
        if(i==0): 
          # vamos agregando renglones
          chLines.append(line)
        # si es la segunda vez que aparece
        elif(i==1):
          # ya esta listo el CHANNEL 2
          self.addrCh2 = currAddr
          melody2 = Melody(nroChannel=2, addr=self.addrCh2, repeatTermina=self.repeatTermina)
          melody2.decodeTxt(chLines)
          self.melody2 = melody2
          chLines = []
          chLines.append(line)
        # si es la tercera vez que aparece
        elif(i==2):
          # ya esta listo el CHANNEL 1
          self.addrCh1 = currAddr
          melody1 = Melody(nroChannel=1, addr=self.addrCh1, repeatTermina=self.repeatTermina)
          melody1.decodeTxt(chLines)
          self.melody1 = melody1
          chLines = []
          chLines.append(line)

        idx0 = line.rfind(':')+1
        strAddr=line[idx0:].strip()
        currAddr = int(strAddr,16) 
        i += 1

      # sino, el renglón no tiene CHANNEL
      else:
        # lo voy agregando
        chLines.append(line)
 
    # terminó el archivo, ya esta listo el CHANNEL 3
    self.addrCh3 = currAddr
    melody3 = Melody(nroChannel=3, addr=self.addrCh3, repeatTermina=self.repeatTermina)
    melody3.decodeTxt(chLines)
    self.melody3 = melody3
    chLines = []



#    strHexa = mystic.util.strHexa(array)
#    print(strHexa)

#    for note in self.melody2.notas:
#      print('notu: ' + note.longString())


  def encodeLilypond(self):
    lines = []

    # los canales a exportar
    canales = [1,2,3]
#    canales = [2,3]

#    tempo = 60
    tempo = 120

    time = '4/4'
#    time = '3/4'

    lines.append('\\version "2.20.0"')
    if(2 in canales):
      lines.append('ch_two = {')
      lines.append('  \\clef treble')
      lines.append('  \\key c \\major')
      lines.append('  \\time ' + time)
#      lines.append('  \\tempo 4 = ' + str(tempo))
      lines.append('  ' + self.melody2.encodeLilypond())
      lines.append('}')

    if(1 in canales):
      lines.append('ch_one = {')
      lines.append('  \\clef treble')
      lines.append('  \\key c \\major')
      lines.append('  \\time ' + time)
#      lines.append('  \\tempo 4 = ' + str(tempo))
      lines.append('  ' + self.melody1.encodeLilypond())
      lines.append('}')

    if(3 in canales):
      lines.append('ch_three = {')
      lines.append('%  \\clef bass')
      lines.append('  \\clef treble')
      lines.append('  \\key c \\major')
      lines.append('  \\time ' + time)
#      lines.append('  \\tempo 4 = ' + str(tempo))
      lines.append('  ' + self.melody3.encodeLilypond())
      lines.append('}')

    lines.append('\\score {')
    lines.append('  <<')

    if(2 in canales):
      lines.append('    \\new Staff {')
      lines.append('      \set Staff.midiInstrument = "violin"')   # "string ensemble 1"  "violin"  "flute" "harmonica"
      lines.append('      \\new Voice = "ch2" \\ch_two')
      lines.append('    }')

    if(1 in canales):
      lines.append('    \\new Staff {')
      lines.append('      \set Staff.midiInstrument = "piano"')  # "bass section"   "electric guitar (steel)"
      lines.append('      \\new Voice = "ch1" \\ch_one')
      lines.append('    }')

    if(3 in canales):
      lines.append('    \\new Staff {')
      lines.append('      \set Staff.midiInstrument = "cello"')
      lines.append('      \\new Voice = "ch3" \\ch_three')
      lines.append('    }')

    lines.append('  >>')
    lines.append('  \\layout { }')
    lines.append('  \\midi { }')
    lines.append('}')

    return lines

  def exportLilypond(self):

    basePath = mystic.address.basePath
    path = basePath + '/audio'
 
    fileTxt = 'song_{:02}.txt'.format(self.nro)
    fileLily = 'song_{:02}_lily.txt'.format(self.nro)
    fileMidi = 'song_{:02}_lily.midi'.format(self.nro)
    fileMp3 = 'song_{:02}_lily.mp3'.format(self.nro)

    lines = self.encodeTxt()
    strTxt = '\n'.join(lines)
    f = open(path + '/' + fileTxt, 'w', encoding="utf-8")
    f.write(strTxt)
    f.close()

#    exportaLily = False
    exportaLily = True
    # si quiero exportar al lilypond
    if(exportaLily):
      
      lines = self.encodeLilypond()
      strLily = '\n'.join(lines)

      f = open(path + '/' + fileLily, 'w', encoding="utf-8")
      f.write(strLily)
      f.close()

      compilarLily = False
#      compilarLily = True
      # si además quiero compilarlo
      if(compilarLily):
        os.chdir(path)
        os.system('lilypond ./' + fileLily)
        os.system('timidity -Ow -o - ' + fileMidi + ' | lame - ' + fileMp3)
        os.chdir('../..')



  def __str__(self):
    string = 'addrCh2: {:04x} | addrCh1: {:04x} | addrCh3: {:04x}'.format(self.addrCh2, self.addrCh1, self.addrCh3)
    return string

##########################################################
class Melody:
  """ representa una melodía de un canal de una canción """

  def __init__(self, nroChannel=None, addr=None, repeatTermina=False):
    # si es pulso (ch2 y ch1) o wave (ch3)  (cambia el comando 0xe0)
    self.nroChannel = nroChannel
    # el address donde se quema
    self.addr = addr
    # si puede terminar con repeat en vez de loop (por el bug en la rom)
    self.repeatTermina = repeatTermina

    # las notas (comandos) de la melodía
    self.notas = []
 
  def decodeRom(self, bank):
    """ decodifica una melodía """

#    strHexa = mystic.util.strHexa(array[0:16])
#    print('melody: ' + strHexa)

    array = bank[self.addr - 0x4000:]

    currAddr = self.addr

    while(True):

      cmd = array[0]

      # si es el comando 0xe0
      if(cmd == 0xe0):
        # si estamos en el wave channel (ch3)
        if(self.nroChannel == 3):
          arg = array[1]
          nota = NotaMusical(currAddr, 2, cmd, arg)
          array = array[2:]
          currAddr += nota.length
        # sino, estamos en un ch2 ó ch1
        else:
          arg1 = array[1]
          arg2 = array[2]
          arg = arg2*0x100 + arg1
          nota = NotaMusical(currAddr, 3, cmd, arg)
          array = array[3:]
          currAddr += nota.length

      elif(cmd in [0xe3, 0xe5, 0xe6, 0xe7]):
        arg = array[1]
        nota = NotaMusical(currAddr, 2, cmd, arg)
        array = array[2:]
        currAddr += nota.length

      #0xe1 AAAA (LOOP AAAA) (loop infinito)
      #0xe2 AAAA (REPEAT AAAA) (repite una vez)
      elif(cmd in [0xe1, 0xe2, 0xe4, 0xe8]):
        arg1 = array[1]
        arg2 = array[2]
        arg = arg2*0x100 + arg1
        nota = NotaMusical(currAddr, 3, cmd, arg)
        array = array[3:]
        currAddr += nota.length

      # eb 01 xxyy    (repetir una vez y saltar al addr yyxx ?) 
      elif(cmd in [0xeb]):
        arg = array[1]
        arg21 = array[2]
        arg22 = array[3]

        arg2 = arg22*0x100 + arg21

        nota = NotaMusical(currAddr, 4, cmd, arg, arg2)
        array = array[4:]
        currAddr += nota.length

      else:
        arg = None
        nota = NotaMusical(currAddr, 1, cmd, arg)
        array = array[1:]
        currAddr += nota.length

#      print('nota: ' + str(nota))
      self.notas.append(nota)

      # si el comando es loop o 0xff
      if(cmd in [0xff, 0xe1]):
        # termino la melodía
        break
      # si permito terminar con repeat (por el bug en la rom) y es el comando repeat
      elif(self.repeatTermina and cmd == 0xe2):
        # termino la melodía
        break


    # inicio el contador de labels
    lblCount = 1
    # por cada nota
    for nota in self.notas:
#      print('notaa: ' + str(nota))
      # si es un jump
      if(nota.cmd in [0xe1, 0xe2, 0xeb]):
        addr = nota.arg
        # en el caso del jumpif
        if(nota.cmd == 0xeb):
          # el addr está indicado en el argumento 2
          addr = nota.arg2

#        print('es un e1 {:4x} '.format(arg))
        # busco la nota a la cual saltar
        for noty in self.notas:
          if(noty.addr == addr):
#            print('encontre: ' + str(noty))
            # y le agrego el label
            nota.jumpLabel = 'label{:}'.format(lblCount)
            noty.labels.append('label{:}'.format(lblCount))
            # incremento contador de labels
            lblCount += 1

#    print('----')
          

  def encodeTxt(self):

    string = ''


    string += '\n--- CHANNEL: {:02x} addr: {:4x}\n'.format(self.nroChannel, self.addr)

    # si el comando anterior fue una nota musical
    anteriorFueNota = False
    # por cada nota
    for nota in self.notas:

      # si tiene labels
      if(len(nota.labels) > 0):
        # si estaba imprimiendo notas musicales
        if(anteriorFueNota):
          # dejo un renglón
          string += '\n'
        # ya no estoy imprimiendo notas musicales
        anteriorFueNota = False
        # imprimo los labels
        for label in nota.labels:
          string += label + ':\n'

#      print('notaa: ' + str(nota))
      # si es un comando (salvo subir o bajar escala)
      if(nota.cmd1 == 0xe):
        # si estaba imprimiendo notas musicales
        if(anteriorFueNota):
          # dejo un enter
          string += '\n'
        # muestro el comando
        string += str(nota) + '\n'
        # ya no estoy imprimiendo notas musicales
        anteriorFueNota = False
      # sino, es una nota musical
      else:
        # si ya estaba imprimiendo notas musicales
        if(anteriorFueNota):
          # sigo al lado
          string += ' ' + str(nota)
        # sino
        else:
          # es un nuevo comando play
          string += 'PLAY ' + str(nota)
        # indico que estoy imprimiendo notas musicales
        anteriorFueNota = True

    lines = string.splitlines()
    return lines

  def decodeTxt(self, lines):
    """ decodifica el canal a partir de un txt """

    # reinicio el listado de notas
    self.notas = []

    # el addr de la nota actual
    vaPorAddr = 0
    # los labels de la nota actual
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
        if('CHANNEL' in line):

          idx0 = line.find(':')+2
          strCh = line[idx0:idx0+2]
          nroChannel = int(strCh)
          self.nroChannel = nroChannel

          idx1 = line.rfind(':')+2
          strAddr = line[idx1:idx1+4]
          addr = int(strAddr,16)
          self.addr = addr

          # indico por que addr va la instrucción actual
          vaPorAddr = addr

        elif('TEMPO' in line):

#          print('line: ' + line)
          args = line.split()
          tempo = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 2, 0xe7, tempo)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('VIBRATO' in line):
 
#          print('line: ' + line)
          args = line.split()
          e4Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 3, 0xe4, e4Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('WAVETABLE' in line):
 
#          print('line: ' + line)
          args = line.split()
          e8Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 3, 0xe8, e8Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('VOLUME' in line):
 
#          print('line: ' + line)
          cantBytes = 3
          if(self.nroChannel==3):
            cantBytes=2

          args = line.split()
          e0Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, cantBytes, 0xe0, e0Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('DUTYCYCLE' in line):
 
#          print('line: ' + line)
          args = line.split()
          e5Arg = int(args[1],16) * 64
          nota = NotaMusical(vaPorAddr, 2, 0xe5, e5Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('STEREO' in line):
 
#          print('line: ' + line)
          args = line.split()
          e6Arg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 2, 0xe6, e6Arg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        # si es un label (termina en ':')
        elif(':' in line):
          # le quito el ':'
          label = line[:len(line)-1]
#          print('label: ' + label)
          currentLabels.append(label)
 
        elif('COUNTER' in line):
 
#          print('line: ' + line)
          args = line.split()
          counterArg = int(args[1],16)
          nota = NotaMusical(vaPorAddr, 2, 0xe3, counterArg)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('OCTAVE' in line):
 
#          print('line: ' + line)
          idx0 = line.find('OCTAVE')+7
          strOctave = line[idx0:idx0+2]
          octave = int(strOctave,16)

          nota = NotaMusical(vaPorAddr, 1, octave, None)
          nota.labels = currentLabels
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('JUMPIF' in line):
 
#          print('line: ' + line)
          args = line.split()
          arg = int(args[1])
          label = args[2]

          nota = NotaMusical(vaPorAddr, 4, 0xeb, arg)
          nota.labels = currentLabels
          nota.jumpLabel = label
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('REPEAT' in line):
 
#          print('line: ' + line)
          args = line.split()
          label = args[1]
          nota = NotaMusical(vaPorAddr, 3, 0xe2, None)
          nota.labels = currentLabels
          nota.jumpLabel = label
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('JUMP' in line and 'JUMPIF' not in line):
 
#          print('line: ' + line)
          args = line.split()
          label = args[1]
          nota = NotaMusical(vaPorAddr, 3, 0xe1, None)
          nota.labels = currentLabels
          nota.jumpLabel = label
          self.notas.append(nota)
          vaPorAddr += nota.length
          currentLabels = []
#          print('nota: ' + str(nota))

        elif('PLAY' in line):
#          print('line: ' + line)

          idx0 = line.find('PLAY')+5
          strNotas = line[idx0:]

          # diccionario para armar el cmd2 (la segunda parte del byte nota musical)
#          valCmd2 = { 'c':0x0, 'd':0x2, 'e':0x4, 'f':0x5, 'g':0x7, 'a':0x9, 'b':0xb, 'r':0xf}
          valCmd2 = { 'c':0x0, 'd':0x2, 'e':0x4, 'f':0x5, 'g':0x7, 'a':0x9, 'b':0xb, 'w':0xe, 'r':0xf, 'o':0xd0}

          cmd = 0
          currentNote = ''
          currentAccident = ''
          currentTilde = ''
          currentLength = ''

          strNotas = strNotas.replace('<<<<', '(')
          strNotas = strNotas.replace('<<<', '[')
          strNotas = strNotas.replace('<<', '{')
          strNotas = strNotas.replace('>>>>', ')')
          strNotas = strNotas.replace('>>>', ']')
          strNotas = strNotas.replace('>>', '}')
#          print('strNotas: ' + strNotas)

          # por cada caracter del string con todas las notas
          for chara in strNotas:

            # si es una nota musical
#            if(chara in ['c','d','e','f','g','a','b','r','<','>']):
            if(chara in ['c','d','e','f','g','a','b','w','r','o','>','}',']',')','<','{','[','(']):

              # si hay una nota anterior
              if(currentNote != ''):

                # la nota anterior está terminada
                if(currentNote == 'o'):
                  continue
                elif(currentNote == '>'):
                  cmd = 0xd8
                elif(currentNote == '}'):
                  cmd = 0xd9
                elif(currentNote == ']'):
                  cmd = 0xda
                elif(currentNote == ')'):
                  cmd = 0xdb
                elif(currentNote == '<'):
                  cmd = 0xdc
                elif(currentNote == '{'):
                  cmd = 0xdd
                elif(currentNote == '['):
                  cmd = 0xde
                elif(currentNote == '('):
                  cmd = 0xdf
                else:
                  cmd2 = valCmd2[currentNote]
                  if(currentTilde == "'"):
                    cmd2 += 12
                  if(currentAccident == "#"):
                    cmd2 += 1

                  # pongo un length default
                  if(currentLength == ''):
                    cmd1 = 0x8
                  else:
                    cmd1 = int(currentLength, 10)

#                  print('cnd1: ' + str(cmd1))
                  cmd = cmd1*0x10 + cmd2
                # la creo
                nota = NotaMusical(vaPorAddr, 1, cmd, None)
                nota.labels = currentLabels
                # y agrego al listado de notas
                self.notas.append(nota)
                vaPorAddr += nota.length
                currentLabels = []


              currentNote = chara
              currentAccident = ''
              currentTilde = ''
              currentLength = ''

            # si es un tilde
            elif(chara == "'"):
              currentTilde = "'" 
            # si es un accidente
            elif(chara in ['#', '+']):
              currentAccident = '#'

            elif(chara in ['0','1','2','3','4','5','6','7','8','9']):
              currentLength += chara
              if(currentNote == 'o'):
                if int(currentLength) > 7:
                  print("Octave {} out of range.".format(chara))
                  print(line)
                  traceback()
                  exit()
                cmd = 0xd0 + int(currentLength)
                nota = NotaMusical(vaPorAddr, 1, cmd, None)
                nota.labels = currentLabels
                self.notas.append(nota)
                vaPorAddr += nota.length
                currentLabels = []
                currentNote = ''

          # la nota anterior está terminada
          if(currentNote == ''):
            pass
          elif(currentNote == '>'):
            cmd = 0xd8
          elif(currentNote == '}'):
            cmd = 0xd9
          elif(currentNote == ']'):
            cmd = 0xda
          elif(currentNote == ')'):
            cmd = 0xdb
          elif(currentNote == '<'):
            cmd = 0xdc
          elif(currentNote == '{'):
            cmd = 0xdd
          elif(currentNote == '['):
            cmd = 0xde
          elif(currentNote == '('):
            cmd = 0xdf
          else:
            cmd2 = valCmd2[currentNote]
            if(currentTilde == "'"):
              cmd2 += 12
            if(currentAccident == "#"):
              cmd2 += 1

            # pongo un length default
            if(currentLength == ''):
              cmd1 = 0x8
            else:
              cmd1 = int(currentLength, 10)

            cmd = cmd1*0x10 + cmd2
          # la creo
          if(currentNote != ''):
            nota = NotaMusical(vaPorAddr, 1, cmd, None)
            nota.labels = currentLabels
            # y agrego al listado de notas
            self.notas.append(nota)
            vaPorAddr += nota.length
            currentLabels = []

    # calculo los addr de los labels !!!
    self.refreshLabels()

  def refreshLabels(self):
    """ setea los addrs de los labels """

    # la primer nota está en addr del canal
    vaPorAddr = self.addr

    # segunda pasada (para setear addr fisico de los labels)
    for nota in self.notas:

      nota.addr = vaPorAddr
      vaPorAddr += nota.length

      # si es una instrucción de salto (JUMP, REPEAT, JUMPIF)
      if(nota.cmd in [0xe1, 0xe2, 0xeb]):
#        print('note: ' + str(nota))
        jumpLabel = nota.jumpLabel
        for noty in self.notas:
          if(jumpLabel in noty.labels):
#            print('lo encontré: {:4x}'.format(noty.addr))
            if(nota.cmd in [0xe1, 0xe2]):
              nota.arg = noty.addr
            else:
              nota.arg2 = noty.addr

#    for nota in self.notas:
#      print('nota: ' + str(nota))


  def encodeRom(self):
    array = []

    for nota in self.notas:
      array.extend(nota.toBytes())

    return array


  def encodeLilypond(self):

    string = ''

    dicLong = {
                0x0 : '1',   # 0x60 (96)
                0x1 : '2.',  # 0x48 (72)
                0x2 : '2',   # 0x30 (48)
                0x4 : '4.',  # 0x24 (36)
                0x5 : '4',   # 0x18 (24)
                0x7 : '8.',  # 0x12 (18)
                0x8 : '8',   # 0x0c (12)
                0xa : '16',  # 0x06 (06)
                0xb : '16.', # 0x04 (04)  # se usar para triplets
                0xc : '32',  # 0x03 (03)

                0xf : '1',   # 0xc1?      # 0xff se usa para indicar el final de la canción ?

                0x3 : '2',   # 0x20 (32)  # no se usa
                0x6 : '4',   # 0x10 (16)  # no se usa
                0x9 : '8'    # 0x08 (08)
              }

    dicNotas = { 0x0 : 'c',
                 0x1 : 'cis',
                 0x2 : 'd', 
                 0x3 : 'dis',
                 0x4 : 'e',
                 0x5 : 'f',
                 0x6 : 'fis',
                 0x7 : 'g',
                 0x8 : 'gis',
                 0x9 : 'a',
                 0xa : 'ais',
                 0xb : 'b',
                 0xc : 'c',
                 0xd : 'cis',
#                 0xe : 'd',
                 0xe : '~',
                 0xf : 'r'
               }

    # índice del último label visto
    lastLabelIndex = 0

    # eligo valores de mano y octava default
    mano = 0x3
    octava = 1
    # para cada nota
    for i in range(0, len(self.notas)):
      # la agarro
      nota = self.notas[i]

      # si tiene labels
      if(len(nota.labels)>0):
        # voy indicando que es la última vista con labels
        lastLabelIndex = i

      # si es REPEAT
      if(nota.cmd == 0xe2):
        # indico en el último label que hay repeat
        self.notas[lastLabelIndex].repeatsTo = True



    # el contador de repeticiones
    counter = 0
    # si el repeat actual tiene jumpif
    tieneJumpif = False

    # vuelvo a iterar sobre las notas
    for nota in self.notas:

      # si es COUNTER
      if(nota.cmd == 0xe3):
        counter = nota.arg

      # si tiene label que inicia un repeat
      if(nota.repeatsTo):
#        string += "  \\repeat volta " + str(counter) + " {\n"
        string += "  \\repeat unfold " + str(counter) + " {\n"

      # si es JUMPIF
      if(nota.cmd == 0xeb):
        string += "\n  | }\\alternative {{ \n"
        # indico que tieneJumpif
        tieneJumpif = True

      # si es REPEAT
      if(nota.cmd == 0xe2):
        if(tieneJumpif):
          string += "\n    }{}}\n"
        else:
          string += "\n    | }\n"
        # reseteo tieneJumpif para la próxima
        tieneJumpif = False


      # si cambia donde va la mano
      if(nota.cmd1 == 0xd):
        mano = nota.cmd2
#        print('mano: {:x} '.format(mano))

        # d0 to d7 sets current octave globally
        if(mano <= 0x7):
          octava = mano-1
        # d8 to df sets current octave relatively
        elif(mano in [0x8]):
          octava += 1
        elif(mano in [0x9]):
          octava += 2
        elif(mano in [0xa]):
          octava += 3
        elif(mano in [0xb]):
          octava += 4
        elif(mano in [0xc]):
          octava -= 1
        elif(mano in [0xd]):
          octava -= 2
        elif(mano in [0xe]):
          octava -= 3
        elif(mano in [0xf]):
          octava -= 4

#      print('comando: {:x}'.format(nota.cmd))

      # tempo
      if(nota.cmd == 0xe7):
        # trato de emular el tempo correcto (no se cual es el valor exacto)
        string += '\n  \\tempo 4 = ' + str(int((100*nota.arg/84))) + '\n  '
#        string += '\n  \\tempo 4 = ' + str(int(nota.arg)) + '\n  '
        pass

      # si es un comando de octava
      if(nota.cmd1 == 0xd):
        # no muestro nada
        pass
      # si es un comando normal
      elif(nota.cmd1 == 0xe):
        pass

      # sino, es una nota musical
      else:

        lilyNota = dicNotas[nota.cmd2]

        saltaOctava = 0
        # si la nota es 0xc o mas alta (salvo 0xe que creo que es vibrato)
        if(nota.cmd2 in [0xc, 0xd]):
          # es de la octava siguiente
          saltaOctava = 1

        # si es la nota de longitud rara
        if(nota.cmd1 == 0xb):
          string += '\\tuplet 3/2 {' + lilyNota
          if(lilyNota not in ['~', 'r']):
            string += '\''*(octava + saltaOctava)
          string += '16}'

        # sino, es de longitud normal
        else:
          string += lilyNota

          if(lilyNota not in ['~', 'r']):
            string += '\''*(octava + saltaOctava)

          if(nota.cmd1 in dicLong):
            lilyLength = dicLong[nota.cmd1]
            string += lilyLength


        string += ' '


    return string


  def __str__(self):

    string = '\n'
    for nota in self.notas:
      string += str(nota) + '\n'

    return string



##########################################################
class NotaMusical:
  """ representa una nota o comando musical de una melodía """

  def __init__(self, addr, length, cmd, arg, arg2=None):
    # la dirección física dentro del bank de la rom
    self.addr = addr
    # la longitud en bytes de la nota
    self.length = length
    # el comando de la nota
    self.cmd = cmd
    # sus posibles argumentos
    self.arg = arg
    self.arg2 = arg2

    # guardo el primer y segundo char hexa del comando por separados
    self.cmd1 = (cmd & 0xf0)//0x10
    self.cmd2 = (cmd & 0x0f)

    # label al cual hace jump esta nota 
    self.jumpLabel = ''
    # lista de labels que se usan para saltar a esta nota
    self.labels = []
    # se usa para indicar si tiene algún label que proviene de un REPEAT
    self.repeatsTo = False

    self.dicNotas = {
                 0x0 : "c",
                 0x1 : "c#",
                 0x2 : "d", 
                 0x3 : "d#",
                 0x4 : "e",
                 0x5 : "f",
                 0x6 : "f#",
                 0x7 : "g",
                 0x8 : "g#",
                 0x9 : "a",
                 0xa : "a#",
                 0xb : "b",
                 0xc : "c'",
                 0xd : "c'#",
#                 0xe : "d'",
                 0xe : "w",
                 0xf : "r"
               }

  def toBytes(self):
    array = []

    array.append(self.cmd)

    # si tiene un primer argumento
    if(self.arg != None):
      # si ocupa un solo byte
      if(self.arg <= 0xff):

        # lo agrego
        array.append(self.arg)

      # sino, ocupa dos bytes
      else:
        # los separo
        argu1 = self.arg // 0x100
        argu2 = self.arg % 0x100
        # y los agrego
        array.append(argu2)
        array.append(argu1)

    # si tiene un segundo argumento (siempre es de 2 bytes)
    if(self.arg2 != None):
      # los separo
      argu1 = self.arg2 // 0x100
      argu2 = self.arg2 % 0x100
      # y los agrego
      array.append(argu2)
      array.append(argu1)

    return array

  def longString(self):

    string = ''

    string += '{:04x} | '.format(self.addr)

#    string += '{:04x} | {:02x} '.format(self.addr, self.cmd)
#    if(self.arg != None):
#      string += '{:04x} '.format(self.arg)

    # imprimo los labels
    for label in self.labels:
#      string += label + ':\n'
      string += label + ' '

    string += str(self)
    return string

 
  def __str__(self):
    string = ''

#    string += '{:04x} | '.format(self.addr)

#    string += '{:04x} | {:02x} '.format(self.addr, self.cmd)
#    if(self.arg != None):
#      string += '{:04x} '.format(self.arg)

    # imprimo los labels
#    for label in self.labels:
#      string += label + ':\n'
#      string += label + ' '

    # si es un comando de octava
    if(self.cmd1 == 0xd):
      if(self.cmd2 == 0x8):
        string += '>'    # > 
      elif(self.cmd2 == 0x9):
        string += '>>'   # }
      elif(self.cmd2 == 0xa):
        string += '>>>'  # ] 
      elif(self.cmd2 == 0xb):
        string += '>>>>' # )
      elif(self.cmd2 == 0xc):
        string += '<'    # <
      elif(self.cmd2 == 0xd):
        string += '<<'   # {
      elif(self.cmd2 == 0xe):
        string += '<<<'  # [
      elif(self.cmd2 == 0xf):
        string += '<<<<' # (
      else:
        string += 'o{:01x}'.format(self.cmd2)

    # sino, si es un comando general
    elif(self.cmd1 == 0xe):

      # volume
      if(self.cmd2 == 0x0):
        string += 'VOLUME {:x}'.format(self.arg)
      # jump
      elif(self.cmd2 == 0x1):
        string += 'JUMP ' + self.jumpLabel
      # repeat
      elif(self.cmd2 == 0x2):
        string += 'REPEAT ' + self.jumpLabel
      # contador
      elif(self.cmd2 == 0x3):
        string += 'COUNTER {:x}'.format(self.arg)
      # instr e4
      elif(self.cmd2 == 0x4):
        string += 'VIBRATO {:x}'.format(self.arg)
      # instrumento?
      elif(self.cmd2 == 0x5):
        string += 'DUTYCYCLE {:x}'.format(self.arg // 64)
      # stereo panning
      elif(self.cmd2 == 0x6):
        if True:
          string += 'STEREO {}'.format(self.arg)
        elif self.arg == 0:
          string += 'pS' # Silent
        elif self.arg == 1:
          string += 'pR' # Right only
        elif self.arg == 2:
          string += 'pL' # Left only
        elif self.arg == 3:
          string += 'pC' # Center (both left and right)
      # tempo
      elif(self.cmd2 == 0x7):
        string += 'TEMPO {:x}'.format(self.arg)
      # instr e8
      elif(self.cmd2 == 0x8):
        string += 'WAVETABLE {:x}'.format(self.arg)
      # jumpif
      elif(self.cmd2 == 0xb):
        string += 'JUMPIF {:x} '.format(self.arg) + self.jumpLabel
      else:
        string += '{:02x} '.format(self.cmd, self.arg)
        if(self.arg != None):
          string += '{:x} '.format(self.arg)
        if(self.arg2 != None):
          string += '{:x} '.format(self.arg2)

    # sino, es una nota musical
    else:
      lilyNota = self.dicNotas[self.cmd2]
      lilyLength = str(self.cmd1)
#      if(self.cmd1 == 0xb):
#        lilyLength = 'coco'
      string += lilyNota + lilyLength



    return string


