
import mystic.romSplitter
import mystic.romStats
import mystic.variables

# The Mystic Language compiler (Javascript Version)

##########################################################
class JScripts:
  """ representa el conjunto de scripts """

  def __init__(self):
    self.scripts = []


  def getAddr(self, nroScript):
    """ retorna el addr del script indicado """

    script = self.scripts[nroScript]
    addr = script.addr
    return addr

  def getScript(self, addr):
    """ retorna el script del addr indicado """

    # para cada script
    for script in self.scripts:
      # si es el del addr indicado
      if(script.addr == addr):
        # lo retorno
        return script
    # si llegó acá no está el script del addr indicado
    return None


  def decodeRom(self):
    self.scripts = []

    nroBank,address = mystic.address.addrScriptAddrDic
    cantScripts = mystic.address.cantScripts

    bankDic = mystic.romSplitter.banks[nroBank]


    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    length = 2*cantScripts
    # agrego info al stats
    mystic.romStats.appendDato(nroBank, address, address+length, (rr, gg, bb), 'diccionario de addr de scripts')

    # por cada nroScript
    for nroScript in range(0,cantScripts):

      addr8 = address + 2*nroScript 
#      print('---addr8: {:04x} '.format(addr8))

      addr = bankDic[addr8:addr8+2]
      addr1 = addr[0]
      addr2 = addr[1]
      # obtengo su addr
      addr = addr2*0x100 + addr1
#      print('addr: {:04x}'.format(addr))

      script = Script(addr, 'function')
      script.nro = nroScript

      banco = 0x0d
      if(addr >= 0x4000):
        banco = 0x0e
        addr -= 0x4000
      array = mystic.romSplitter.banks[banco]
      # creo un array desde donde empieza el script
      array = array[addr:]

      # decodifico el script
      vaPorAddr = script.decodeRom(array)
      # y lo agrego a la lista de scripts 
      self.scripts.append(script)
#      print('script: ' + str(script))

      import random
      rr = random.randint(0,0xff)
      gg = random.randint(0,0xff)
      bb = random.randint(0,0xff)
      # grabo las romstats
      if(script.addr < 0x4000):
        mystic.romStats.appendDato(0x0d, script.addr, vaPorAddr, (rr, gg, bb), 'un script')
      else:
        mystic.romStats.appendDato(0x0e, script.addr - 0x4000, vaPorAddr - 0x4000, (rr, gg, bb), 'un script')
#      print('romstats {:04x} {:04x}'.format(script.addr, vaPorAddr))



  def encodeTxt(self):
    newLines = []

    newLines.append('');
    newLines.append('/******************************************************************************/');
    newLines.append('/*                                                                            */');
    newLines.append('/*                 Welcome to the mystic-jscript-language                     */');
    newLines.append('/*                                                                            */');
    newLines.append('/* Some observations to take care off, while jscript has a                    */');
    newLines.append('/*    javascript-like syntax, it is far less flexible, for example:           */');
    newLines.append('/*                                                                            */');
    newLines.append('/* 1. Multiline comments are not supported (only within the same line).       */');
    newLines.append('/* 2. It is heavily tab dependent, like python.                               */');
    newLines.append('/* 3. One space can break anything                                            */');
    newLines.append('/*     ( "} else {" is valid but "}else{" is not )                            */');
    newLines.append('/* 4. The ending block comments are mandatory, for the time being.            */');
    newLines.append('/*     ( "}//END_FUNCTION" is valid but "}" is not )                          */');
    newLines.append('/* 5. All script names must have the format script_HHHH                       */');
    newLines.append('/*     where HHHH is it\'s hex number                                         */');
    newLines.append('/* 6. Flags constants must start with "flag_" and boss constants with "boss_" */');
    newLines.append('/* 7. All integers must be written in hexadecimal format.                     */');
    newLines.append('/* 8. Enjoy!                                                                  */');
    newLines.append('/*                                                                            */');
    newLines.append('/******************************************************************************/');
    newLines.append('');

    newLines.append('/* flags */');
    for val in mystic.variables.flags.keys():
      var = mystic.variables.flags[val]
#      print('key: ' + labelVar + ' value: ' + str(nroVar))
      newLines.append('const ' + var + ' = 0x{:02x};'.format(val))

    newLines.append('');
    newLines.append('/* bosses */');
    for val in mystic.variables.bosses.keys():
      var = mystic.variables.bosses[val]
#      print('key: ' + labelVar + ' value: ' + str(nroVar))
      newLines.append('const ' + var + ' = 0x{:02x};'.format(val))


    txt = ''

    newLines.append('');
    newLines.append('// ----------------------- //');

    # para cada script
    for script in self.scripts:
      txt += script.encodeTxt()


    # 2da pasada (rellena CALLs)
#    filepath = path + '/scripts_00.txt'
#    f = open(filepath, 'r', encoding="utf-8")
#    txt = f.read()
#    f.close()

#    f = open('./en/pruebita.txt', 'w', encoding="utf-8")
#    f.write(txt)
#    f.close()

    lines = txt.splitlines()

    # para cada renglón
    for line in lines:
      # si no tiene CALL
#      if('CALL' not in line):
      if(not line.strip().startswith('script')):
        # lo deja como está
        newLines.append(line)
      # sino, el renglón tiene un CALL
      else:
        idx0 = line.find('script')

        # busco si tiene label
#        idxLabel = line.find('$')
        idxLabel = line.find('_')
        # si no tiene label (tiene addr físico)
        if(idxLabel == -1):

#          print('line: ' + line)

          strAddr = line[idx0+7: idx0+11]
#          print('analizando line: ' + line)
          addr = int(strAddr,16)
#          print('analizando addr: {:04x}'.format(addr))
          # traduzco el addr en nroScript
          script = self.getScript(addr)
          strNroScript = '{:04x}'.format(script.nro)
#          newLine = line[0:idx0+6] + '$' + strNroScript
          newLine = line[0:idx0+6] + '_' + strNroScript + '();'
          # y lo agrego
#          newLines.append('# old: ' + line)
          newLines.append(newLine)

        # sino, ya tiene label
        else:
          # (nunca se ejecuta?)
          print('ejecutando else!!')
          # salteo el símbolo '$'
          strLabel = line[idx0+6: idx0+10]
          print('strLabel: ' + strLabel)

          newLine = line[0:idx0+5] + strLabel
          # y lo agrego
#          newLines.append('# old: ' + line)
          newLines.append(newLine)

    return newLines


  def decodeTxt(self, lines):

    self.scripts = []

    script = None
    # los renglones del script actual
    subLines = []

    for line in lines:
      # comienza un nuevo script
      if('function script_' in line):

        # si había un script anterior
        if(script != None):

          # lo decodifico
          script.decodeTxt(subLines)
          # lo agrego a la lista
          self.scripts.append(script)
          # reinicio los renglones para el próximo script
          subLines = []

#        lineSplit = line.split()
#        nroScript = int(lineSplit[2],16)
#        addr = int(lineSplit[4],16)
#        print('nroScript: {:04x} addr: {:04x}'.format(nroScript, addr))
        nroScript = int(line[16:16+4],16)
#        print('nroScript: {:04x}'.format(nroScript))
        addr = 0x0000

        # creo el script
        script = Script(addr, 'function')
        script.nro = nroScript

#      elif('CALL:' in line):
#        print('callll: ' + line)

      else:
        if(line.strip().startswith('const flag')):
          line = line.strip()
          subLine = line[len('const'):].strip()
          idx0 = subLine.index('=')
          var = subLine[:idx0].strip()
          strVal = subLine[idx0+1:].strip()
          idx1 = strVal.index('x')
          idx2 = strVal.index(';')
          strVal = strVal[idx1+1:idx2].strip()
          val = int(strVal,16)
#          print('flag: ' + var + ' --- val: {:02x}'.format(val))
          mystic.variables.flags[val] = var

        elif(line.strip().startswith('const boss')):
          line = line.strip()
          subLine = line[len('const'):].strip()
          idx0 = subLine.index('=')
          var = subLine[:idx0].strip()
          strVal = subLine[idx0+1:].strip()
          idx1 = strVal.index('x')
          idx2 = strVal.index(';')
          strVal = strVal[idx1+1:idx2].strip()
          val = int(strVal,16)
#          print('boss: ' + var + ' --- val: {:02x}'.format(val))
          mystic.variables.bosses[val] = var
          
        else:
          subLines.append(line)

    # lo decodifico
    script.decodeTxt(subLines)
    # lo agrego a la lista
    self.scripts.append(script)
    # reinicio los renglones para el próximo script
    subLines = []


#  def _refreshLabels(self, nroBanco, ultimoNroScriptBanco0d):
  def _refreshLabels(self, nroBanco, startingScriptNro, endingScriptNro):
    """ refresca los labels de los CALLs con su addr física, según si es para el banco 0x0d ó 0x0e """

    # recorro todos los scripts
    for script in self.scripts:
      string, calls = script.iterarRecursivoRom(1)

      for cmd in calls:
        label = cmd.jumpLabel
#        print('label: ' + label)

        strNroScript = label[1:5]
#        print('strNroScript: ' + strNroScript)
        nroScript = int(strNroScript, 16)

        addr = self.getAddr(nroScript)
#        print('addr: {:04x}'.format(addr))

        addr1 = addr // 0x100
        addr2 = addr % 0x100

#        print('addr1 addr2 {:02x} {:02x}'.format(addr1, addr2))

        # actualizo su addr
        cmd.hexs = [0x02, addr1, addr2]
        # actualizo el call con el addr físico
        cmd.strCode = 'script {:04x}'.format(addr)

        # si es para el banco 0x0d pero el script no entra
#        if(nroBanco == 0x0d and script.nro > ultimoNroScriptBanco0d):
          # seteo addr en 0x0000
#          cmd.hexs = [0x02, 0x00, 0x00]
#          cmd.strCode = 'CALL {:04x}'.format(0x0000)



  def encodeRom(self):
    # los bancos a devolver 
#    array0d = []
#    array0e = []
    encodedBanks = []
    # el último número de script de cada banco
    ultimoNroScriptBanco = []

    vaPorAddr = 0x0000
    # el último script que entró en el banco 0d
    ultimoNroScriptBanco0d = -1

    lang = mystic.address.language

    # por cual bank vamos (contando desde 0)
    vaPorBanco = 0

    # para cada script
#    for script in self.scripts:
    for i in range(0,len(self.scripts)):
      script = self.scripts[i]
      # lo codifico
      subArray = script.encodeRom()

      # calculo addr donde termina
      proxAddr = vaPorAddr + len(subArray)
      # si empieza antes pero termina después de 0x4000 (rom 'de' y custom)

#      addrDeCorte = 0x4000
      addrDeCorte = 0x4000*(vaPorBanco+1)
      # la rom 'jp' corta el banco un poco antes
      if(lang == mystic.language.JAPAN):
        addrDeCorte -= 4*16

#      if(vaPorAddr < 0x4000 and proxAddr >= 0x4000):
      if(vaPorAddr < addrDeCorte and proxAddr >= addrDeCorte):
        # cambio al bank siguiente
        vaPorBanco += 1
#        vaPorAddr = 0x4000
        vaPorAddr = 0x4000*vaPorBanco
        # el script anterior fué el último en entrar completo en el banco
#        ultimoNroScriptBanco0d = script.nro - 1
        ultimoNroScriptBanco.append(script.nro - 1)

        # si la rom es 'en', 'en_uk' ó 'fr' 
        if(lang in [mystic.language.ENGLISH, mystic.language.ENGLISH_UK, mystic.language.FRENCH]):
          # el script anterior se vuelve a copiar al principio del banco siguiente
#          self.scripts[i-1].addr = 0x4000
          self.scripts[i-1].addr = 0x4000*vaPorBanco
          vaPorAddr += len(self.scripts[i-1].encodeRom())
#          ultimoNroScriptBanco0d = script.nro - 2
          # borro el ultimo coso agregado
          del ultimoNroScriptBanco[-1]
          ultimoNroScriptBanco.append(script.nro - 2)

#      print('script {:04x} addrAnt {:04x} addrNew {:04x}'.format(script.nro, script.addr, vaPorAddr))

      # si no es un script vacío
      if(len(script.listComandos) > 0):
        # actualizo el addr del script !!
        script.addr = vaPorAddr
        # sumo para el addr del próximo script
        vaPorAddr += len(subArray)
      # sino, está en NULL
      else:
        # seteo su addr en 0x0000 
        script.addr = 0x0000

    ultimoNroScriptBanco.append(script.nro)

    # el banco donde comenzamos a quemar scripts
    startingScriptsBank = 0x0d
    # el primer script del banco
    startingScriptNro = 0

    # por cada banco que hay que quemar
    for i in range(0,vaPorBanco+1):
      # creo el banco en principio vacío
      array = []
      # me fijo en cual script termina
      endingScriptNro = ultimoNroScriptBanco[i]

#      self._refreshLabels(0x0d, ultimoNroScriptBanco0d)
      # refresco sus labels
      self._refreshLabels(startingScriptsBank + i, startingScriptNro, endingScriptNro)

      # recorro todos los scripts
      for script in self.scripts:

#        print('nro: {:04x} starting: {:04x} ending: {:04x}'.format(script.nro, startingScriptNro, endingScriptNro))
#        if(True):
#        if(script.nro <= ultimoNroScriptBanco0d):
        # si está en el rango de scripts de este banco
        if(script.nro >= startingScriptNro and script.nro <= endingScriptNro):
          subArray = script.encodeRom()

          # voy extendiendo el array
#          array0d.extend(subArray)
          array.extend(subArray)



#      print('len(array): ' + str(len(array)))

      sizeBank = min(len(array),0x4000)
      bank = array[:sizeBank]
      print('adding script bank {:02x} [0x0000,0x{:04x}] (from script {:04x} to {:04x})'.format(0x0d + i, sizeBank, startingScriptNro, endingScriptNro))
      encodedBanks.append(bank)

      startingScriptNro = endingScriptNro+1

    return encodedBanks



#    self._refreshLabels(0x0d, ultimoNroScriptBanco0d)

    # recorro todos los scripts
#    for script in self.scripts:

#      if(True):
#      if(script.nro <= ultimoNroScriptBanco0d):
#        subArray = script.encodeRom()

        # voy extendiendo el array
#        array0d.extend(subArray)

#    self._refreshLabels(0x0e, ultimoNroScriptBanco0d)

    # recorro todos los scripts
#    for script in self.scripts:

#      if(script.nro > ultimoNroScriptBanco0d):
#        subArray = script.encodeRom()

        # voy extendiendo el array
#        array0e.extend(subArray)

#    size0d = min(len(array0d),0x4000)
#    size0e = min(len(array0e),0x4000)

#    return array0d[:size0d], array0e[:size0e]

##########################################################
class Script:
  """ representa un script """

  def __init__(self, addr, tipoBloque):
    # el address en la rom 'd' o 'e' (si es >= 0x4000)
    self.addr = addr

    # tipo de bloque ('function', 'for', 'else', 'else_if', 'if', 'if_hand', 'if_inventory', 'if_triggered_on_by', 'if_triggered_off_by')
    self.tipoBloque = tipoBloque

    # el nroScript
    self.nro = 0x0000

    # la lista de comandos
    self.listComandos = []

  def iterarRecursivoRom(self, depth):

    string = ''
    calls = []

    for cmd in self.listComandos:
#      print('cmd: ' + (' ' * 2*depth) + ' ' + str(cmd))
#      string += (' ' * 2*depth) + ' ' + str(cmd) + '\n'
#      string += (' ' * 2*depth) + str(cmd) 
#      string += str(cmd)

#      if(cmd.strCode.startswith('ELSE')):
      if(cmd.strCode.startswith('} else {')):
        depth = depth-1
#      elif(cmd.strCode.startswith('}')):
#        depth = depth-1
      elif(cmd.strCode.startswith('}//END_IF')):
        depth = depth-1
#      elif(cmd.strCode.startswith('END_ELSE_IF')):
#        depth = depth-1
      elif(cmd.strCode.startswith('}//END_FOR')):
        depth = depth-1
      elif(cmd.strCode.startswith('}//END_FUNCTION')):
        depth = depth-1

      # si no está en modo texto
      if(cmd.textMode == False):
        # hay que tabular
        renglon = (' ' * 2*depth) + str(cmd) 
      # sino, es modo texto
      else:
        # y no hay que tabular
        renglon = str(cmd) 

      # si no es un inutil endif
#      if(not cmd.strCode.startswith('END_IF')):
#        print('textMode: ' + str(cmd.textMode) + ' | ' + renglon)
#        string += renglon

#      string += renglon

      # si no es un inutil end_else
#      if(cmd.strCode.strip() not in ['END_ELSE', 'END_ELSE_IF', 'END_IF']):
      if(cmd.strCode.strip() not in ['}//END_ELSE']):
#        print('textMode: ' + str(cmd.textMode) + ' | ' + renglon)
        string += renglon



      # si es un CALL (y no está comentado)
#      if(cmd.nro == 0x02):
#      if('CALL' in cmd.strCode and not cmd.strCode.startswith('#')):
      if(cmd.strCode.startswith('script')):
#        calls.append(cmd.strCode)
        calls.append(cmd)

      # si tiene script propio
      if(cmd.script != None):
#        print('cmd: ' + cmd.strCode)
        # lo llamo recursivamente
        newString,newCalls = cmd.script.iterarRecursivoRom(depth + 1)
        string += newString
        calls.extend(newCalls)

    return string, calls


  def decodeRom(self, array):
    """ decodifica un script """

    # inicializo por que addr vamos
    vaPorAddr = self.addr

    idx = 0
    # si está en modo texto o no
    textMode = False
    while(True):
      cmd = Comando(vaPorAddr, self)
      textMode = cmd.decodeRom(array[idx:], textMode)
#      print('cmd: ' + str(cmd) + ' size: ' + str(cmd.size))

      idx += cmd.size
#      vaPorAddr += len(cmd.hexs)
      vaPorAddr += cmd.size

      self.listComandos.append(cmd)

#      print('strCode: ' + cmd.strCode)

#      if(cmd.strCode.strip() in ['ERROR', 'END']):
#      if(cmd.strCode[:3] in ['ERR', 'END']):
#      if(cmd.strCode.startswith('ERROR') or cmd.strCode.startswith('}') or cmd.strCode.startswith('ENDIF')):
#      if(cmd.strCode.startswith('ERROR') or cmd.strCode.startswith('END_FOR') or cmd.strCode.startswith('END_FUNCTION') or cmd.strCode.startswith('END_IF')):
      if(cmd.strCode.startswith('ERROR') or cmd.strCode.startswith('}//END')):
#        break
        return vaPorAddr

  def decodeTxt(self, lines):
    """ decodifica un script txt """

    # si está en NULL
    if(len(lines)>0):
      firstLine = lines[0].strip()
#      if(firstLine == 'NULL'):
      if(firstLine.startswith('return null;')):
        # seteo el addr en 0
        self.addr = 0x0000
        # y retorno sin hacer mas nada
        return

    vaPorAddr = self.addr
    idx = 0
#    while(True):
    # mientras queden renglones por procesar
    while(len(lines[idx:])>0):

      cmd = Comando(vaPorAddr, self)
      cmd.decodeTxt(lines[idx:])
#      print('cmd: ' + str(cmd))
      idx += cmd.sizeLines

      vaPorAddr += len(cmd.hexs)
#      vaPorAddr += cmd.size 

      self.listComandos.append(cmd)

#      print('strCode: ' + cmd.strCode)

#      if(cmd.strCode.strip() in ['ERROR', 'END']):
#      if(cmd.strCode[:3] in ['ERR', 'END']):
#      if(cmd.strCode.startswith('ERR') or cmd.strCode.startswith('}')):
#      if(cmd.strCode.startswith('ERROR') or cmd.strCode.startswith('}') or cmd.strCode.startswith('ENDIF')):
#      if(cmd.strCode.startswith('ERROR') or cmd.strCode.startswith('END_FOR') or cmd.strCode.startswith('END_FUNCTION') or cmd.strCode.startswith('END_IF')):
#      if(cmd.strCode.startswith('ERROR') or cmd.strCode.strip() in ['END_FUNCTION', 'END_FOR', 'END_IF']):
#      if(cmd.strCode.startswith('ERROR') or cmd.strCode.strip() in ['END_IF']):
      if(cmd.strCode.startswith('ERROR')):
        break

  def encodeTxt(self):
    string = ''

#    string += '\n--------------------\n'
#    string += 'script: {:04x}'.format(self.nro) + '\n'
#    string += 'addr: {:04x}'.format(self.addr) + '\n'
#    string += '\n--- script: {:04x} addr: {:04x} ------------------\n'.format(self.nro, self.addr)
    string += '\n/* ----------- addr: {:04x} ----------- */\n'.format(self.addr)
    string += 'function script_{:04x}()'.format(self.nro) + ' {\n'

    # cuando devuelve 0x0000 no es un script usado
    if(not (self.addr == 0x0000 and self.nro > 0)):
      strScript, newCalls = self.iterarRecursivoRom(depth=1)
      string += strScript
    else:
#      string += 'NULL\n'
      string += 'return null;}\n'

    return string


  def encodeRom(self):
    array = []

    for cmd in self.listComandos:
      array.extend(cmd.hexs)
      # si tiene script propio
      if(cmd.script != None):
        # lo llamo recursivamente
        newHexs = cmd.script.encodeRom()
        array.extend(newHexs)
    return array

  def __str__(self):
    return 'Script {:04x}'.format(self.nro)




##########################################################
class Comando:
  """ representa un comando de un script """

  def __init__(self, addr, bloque):
    # el addr del comando
    self.addr = addr

    # el bloque (objeto Script) al que pertenece
    self.bloque = bloque

    self.array = None
    self.lines = None

    # en principio no tiene script propio (solo FOR, IF, ELSE)
    self.script = None

    self.nro = None
    self.strCode = None
    self.strHex = None
    self.hexs = []

    self.textMode = None

    # label al cual hace CALL este comando
    self.jumpLabel = ''
    # lista de labels que se usan para saltar a este comando
    self.labels = []

  def decodeRom(self, array, textMode):
    """ lo decodifica """
    self.array = array

#    print('len array: ' + str(len(self.array)))
    self.textMode = textMode
    # si se terminó el bloque de IF o de ELSE
    if(len(self.array) == 0):
      if(self.bloque.tipoBloque == 'if'):
        self.strCode = '}//END_IF\n'
      elif(self.bloque.tipoBloque == 'if_hand'):
        self.strCode = '}//END_IF_HAND\n'
      elif(self.bloque.tipoBloque == 'if_inventory'):
        self.strCode = '}//END_IF_INVENTORY\n'
      elif(self.bloque.tipoBloque == 'if_triggered_on_by'):
        self.strCode = '}//END_IF_TRIGGERED_ON_BY\n'
      elif(self.bloque.tipoBloque == 'if_triggered_off_by'):
        self.strCode = '}//END_IF_TRIGGERED_OFF_BY\n'
      elif(self.bloque.tipoBloque == 'else'):
        self.strCode = '}//END_ELSE\n'
      elif(self.bloque.tipoBloque == 'else_if'):
        self.strCode = '}//END_ELSE_IF\n'

      self.size = 0
      self.strHex = '' # mystic.util.strHexa(self.array[0:self.size])

      return textMode


    # si no está en modo texto
    if(textMode == False):
      textMode = self.decodeNormal()
    # sino, está en modo texto
    else:
      textMode = self.decodeTextMode()

    return textMode

  def decodeTextMode(self):

    textMode = True

    # el número de comando es el primer byte
    self.nro = self.array[0]

    self.strHex = mystic.util.strHexa(self.array[0:20])
    self.strCode = 'ERROR_TEXT: ' + self.strHex + '\n'
    self.size = 0 

    # si es texto
    if(self.nro in mystic.dictionary.keys()):


      # agarro el char (o par de chars)
      char = mystic.dictionary.decodeByte(self.nro)

#      print('llegó: {:02x} '.format(self.nro) + char)

#      print('decodeByte {:02x}: '.format(self.nro) + char) 

      self.strCode = char 
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

      # si es <TEXT_MODE_OFF>
      if(self.nro == 0x00):
        # le agrego un enter
#        self.strCode = '<TEXT_MODE_OFF>\n'
#        self.strCode = '<TEXT_MODE_OFF>");\n'
        self.strCode = '");\n'
        # y salgo del modo texto
        textMode = False
 
    return textMode

  def decodeNormal(self):
    """ decodifica en modo normal (no en modo texto) """

    # asumo que no es en modo texto
    textMode = False
   
    # el número de comando es el primer byte
    self.nro = self.array[0]

#    print('nro: {:02x}'.format(self.nro))

#    print('array: ' + mystic.util.strHexa(self.array))
#    print('array: ' + mystic.util.strHexa(self.array[:min(20,len(self.array))]))

    self.strHex = mystic.util.strHexa(self.array[0:20])
    self.strCode = 'ERROR: ' + self.strHex + '\n'
    self.size = 0 


#    if(self.nro in [0xa9]):
    if(False):
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
      self.strCode = 'NI_IDEA_0: ' + self.strHex + '\n'

#    elif(self.nro in [0xc2, 0xc5]):
#    elif(self.nro in [0xc5]):
    elif(False):
      arg1 = self.array[1]
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
      self.strCode = 'NI_IDEA_1: ' + self.strHex + '\n'

#    elif(self.nro in [0xef]):
    elif(False):
#      print(mystic.util.strHexa(self.array[:min(20,len(self.array))]))
      arg1 = self.array[1]
      arg2 = self.array[2]
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
      self.strCode = 'NI_IDEA_2: ' + self.strHex + '\n'

    elif(self.nro == 0x12):
      self.strCode = 'PAUSE'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    # o bien termina un script, o bien termina un FOR
    elif(self.nro == 0x00):
      self.size = 1

#      self.strCode = 'END\n'
#      self.strCode = '}\n'
      if(self.bloque.tipoBloque == 'function'):
        self.strCode = '}//END_FUNCTION\n'
      elif(self.bloque.tipoBloque == 'for'):
        self.strCode = '}//END_FOR\n'

      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    # es un ELSE
    elif(self.nro == 0x01):
      cantBytes = self.array[1]

#      print('--- array: ' + mystic.util.strHexa(self.array))
#      print('--- cantBytes: {:02x}'.format(cantBytes))

      self.strHex = mystic.util.strHexa(self.array[0:self.size])
#      self.strCode = 'SMALL_JUMP_FW {:02x}\n'.format(arg1)
#      self.strCode = 'ELSE\n'
      self.strCode = '} else {\n'
      self.size = 2 + cantBytes

      bloque = Script(self.addr + 2, 'else')
      bloqueArray = self.array[2:2+cantBytes]
      bloque.decodeRom(bloqueArray)
      self.script = bloque

#      print('bloqueArray: ' + mystic.util.strHexa(bloqueArray))

    elif(self.nro == 0x02):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg1*0x100 + arg2
      self.strCode = 'script {:04x}\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    # FOR
    elif(self.nro == 0x03):
      cant = self.array[1]
      cantBytes = self.array[2] 
#      self.strCode = 'FOR 0 <= i < {:02x}\n'.format(cant)
      self.strCode = 'for(let i=0; i<0x{:02x}; i++)'.format(cant) + ' {\n'

      self.size = 3 + cantBytes
      self.strHex = mystic.util.strHexa(self.array[0:3])

      bloque = Script(self.addr + 3, 'for')
      bloqueArray = self.array[3:3+cantBytes]
      bloque.decodeRom(bloqueArray)
      self.script = bloque



    # IF
    elif(self.nro in [0x08, 0x09, 0x0a, 0x0b, 0x0c]):

      conds = []
      cond = self.array[1]
      i = 1
      while(cond != 0x00):
        conds.append(cond)
        cond = self.array[1+i]
        i += 1


      cantBytes = self.array[1+i]
      strConds = ''
#      for cond in conds:
      for k in range(0,len(conds)):
        cond = conds[k]
        strCond = '0x{:02x}'.format(cond)
        strConds += strCond
        if(k != len(conds)-1):
          strConds += ', '

      if(self.nro == 0x08):
#        self.strCode = 'IF(' + strConds + ')\n'
        strConds = ''
        for k in range(0,len(conds)):
          cond = conds[k]
          strCond = mystic.variables.getLabel(cond)
          strConds += strCond
          if(k != len(conds)-1):
            strConds += ', '

        self.strCode = 'if(if_flags([' + strConds + '])) {\n'
        bloque = Script(self.addr + len(conds) + 3, 'if')
      elif(self.nro == 0x09):
#        strConds = mystic.util.strHexa(conds)
        # condición sobre lo que tengo en la mano?
        self.strCode = 'if(if_hand([' + strConds + '])) {\n'
        bloque = Script(self.addr + len(conds) + 3, 'if_hand')
      elif(self.nro == 0x0a):
#        strConds = mystic.util.strHexa(conds)
        self.strCode = 'if(if_inventory([' + strConds + '])) {\n'
        bloque = Script(self.addr + len(conds) + 3, 'if_inventory')
      elif(self.nro == 0x0b):
#        strConds = mystic.util.strHexa(conds)
        # list of possible arguments (joined by 'or')  
        # c9 = hero
        # c1 = moogled_hero?
        # f1 = chocobot_over_land
        # f5 = chocobot_over_water
        # a9 = empty_chest or snowman
        # 91 = idk, npc following the hero? enemy?
        self.strCode = 'if(if_triggered_on_by([' + strConds + '])) {\n'
        bloque = Script(self.addr + len(conds) + 3, 'if_triggered_on_by')

      elif(self.nro == 0x0c):
#        strConds = mystic.util.strHexa(conds)
        self.strCode = 'if(if_triggered_off_by([' + strConds + '])) {\n' 
        bloque = Script(self.addr + len(conds) + 3, 'if_triggered_off_by')

      self.strHex = mystic.util.strHexa(self.array[0:i+2])
      bloqueArray = self.array[2+i:2+i+cantBytes]
      self.size = 2 + i + cantBytes


      # el bloque puede continuar con un ELSE
#      bloqueArray = self.array[2+i:]
      bloque.decodeRom(bloqueArray)

      # miro cual fué el último comando (antes del endif)
      ultimoCmd = bloque.listComandos[len(bloque.listComandos)-2]
#      print('ultimoCmd: ' + str(ultimoCmd))

      # si tiene else
#      if(ultimoCmd.strCode == 'ELSE\n'):
      if(ultimoCmd.strCode == '} else {\n'):
 
        # miro el largo del bloque else
        lenElse = bloqueArray[len(bloqueArray)-1]
#        print('lenElse: {:02x}'.format(lenElse))

        bloque = Script(self.addr + len(conds) + 3, 'else_if')
        # y se lo sumo al tamaño del bloque del if
        bloqueArray = self.array[2+i:2+i+cantBytes+lenElse]
        self.size = 2 + i + cantBytes+lenElse

        # ahora si decodifico el bloque if (incluyendo su else)
        bloque.decodeRom(bloqueArray)

      self.script = bloque

    # es uno de los 7 posibles personajes extras
    elif(self.nro >= 0x10 and self.nro <= 0x7f):

#      print('nro: {:02x}'.format(self.nro))
      primer = self.nro // 0x10
      segund = self.nro % 0x10
#      print('primer: {:01x}'.format(primer))
#      print('segund: {:01x}'.format(segund))

      # EXTRA
      extras = ['extra1', 'extra2', 'extra3', 'extra4', 'extra5', 'extra6', 'extra7']

      actions = ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'Teleport', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseC', 'NoseD', 'NoseE', 'NoseF' ]
      strExtra = extras[primer-1]
      strAction = actions[segund]
      strCmd = strExtra + strAction

      if(strAction in ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseC', 'NoseD', 'NoseE', 'NoseF']):

        self.strCode = strCmd + '();\n'
        self.size = 1
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

      elif(strAction in ['Teleport']):

        xx = self.array[1]
        yy = self.array[2]

        # cambia las coordenadas del extra dentro del bloque actual
#        self.strCode = strCmd + ' (XX,YY) = ({:02x}, {:02x})\n'.format(xx,yy)
        self.strCode = strCmd + '(xx=0x{:02x}, yy=0x{:02x});\n'.format(xx,yy)
        self.size = 3
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

    # es el extra especial
    elif(self.nro >= 0x90 and self.nro <= 0x9f):

      primer = self.nro // 0x10
      segund = self.nro % 0x10

      actions = ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'Teleport', 'WalkFastSpeed', 'WalkNormalSpeed', 'SetPersonaje', 'NoseD', 'NoseE', 'NoseF' ]

      # PARTNER
      strExtra = 'partner'
      strAction = actions[segund]
      strCmd = strExtra + strAction

      if(strAction in ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseD', 'NoseE', 'NoseF']):

        self.strCode = strCmd + '();\n'
        self.size = 1
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

      elif(strAction in ['Teleport']):

        xx = self.array[1]
        yy = self.array[2]

        # cambia las coordenadas del extra dentro del bloque actual
#        self.strCode = strCmd + ' (XX,YY) = ({:02x}, {:02x})\n'.format(xx,yy)
        self.strCode = strCmd + '(xx=0x{:02x}, yy=0x{:02x});\n'.format(xx,yy)
        self.size = 3
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

      elif(strAction in ['SetPersonaje']):

        arg = self.array[1]
        # turn extra1 into extra9 (extraspecial)
        self.strCode = strCmd + '({:02x});\n'.format(arg)
        self.size = 2
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0x8b):
      # it makes the hero make a small jump (the arg is unknown)
      arg = self.array[1]
#      self.strCode = 'HOP_JUMP {:02x}\n'.format(arg)
      self.strCode = 'hopJump(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    # es el hero
    elif(self.nro >= 0x80 and self.nro <= 0x8f):

      primer = self.nro // 0x10
      segund = self.nro % 0x10

      actions = ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'WalkFastSpeed', 'WalkNormalSpeed', 'Teleport', 'NoseB', 'NoseC', 'NoseD', 'NoseE', 'NoseF' ]

      # HERO
      strExtra = 'hero'
      strAction = actions[segund]
      strCmd = strExtra + strAction

      if(strAction in ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseB', 'NoseC', 'NoseD', 'NoseE', 'NoseF']):

        self.strCode = strCmd + '();\n'
        self.size = 1
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

      elif(strAction in ['Teleport']):

        xx = self.array[1]
        yy = self.array[2]

        # cambia las coordenadas del extra dentro del bloque actual
#        self.strCode = strCmd + ' (XX,YY) = ({:02x}, {:02x})\n'.format(xx,yy)
        self.strCode = strCmd + '(xx=0x{:02x}, yy=0x{:02x});\n'.format(xx,yy)
        self.size = 3
        self.strHex = mystic.util.strHexa(self.array[0:self.size])



    elif(self.nro == 0xa0):
#      self.strCode = 'WALKING_AS_CHOCOBO\n'
      self.strCode = 'walkingAsChocobo();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa1):
#      self.strCode = 'WALKING_AS_CHOCOBOT_LAND\n'
      self.strCode = 'walkingAsChocobotLand();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa2):
#      self.strCode = 'WALKING_AS_CHOCOBOT_WATER\n'
      self.strCode = 'walkingAsChocobotWater();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa3):
#      self.strCode = 'WALKING_AS_TROLLEY_WAGON\n'
      self.strCode = 'walkingAsWagon();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa4):
#      self.strCode = 'WALKING_AS_NORMAL\n'
      self.strCode = 'walkingAsNormal();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa5):
#      self.strCode = 'WALKING_AS_FALLING\n'
      self.strCode = 'walkingAsFalling();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa6):
#      self.strCode = 'WALKING_AS_DEAD\n'
      self.strCode = 'walkingAsDead();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xa9):
      # Sets flag 0x7f to false if current map is 0x01, 0x0e, or 0x0f. Sets to true otherwise.
#      self.strCode = 'CHECK_IF_CURRENT_MAP_HAS_SMALLMAP\n'
      self.strCode = 'checkIfCurrentMapHasSmallmap();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xab):
#      self.strCode = 'CLEAR_MATO_TODOS\n'
      self.strCode = 'clearKilledAllRoom();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xac):
#      self.strCode = 'SMALLMAP_OPEN\n'
      self.strCode = 'smallmapOpen();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xad):
#      self.strCode = 'SMALLMAP_IDLE\n'
      self.strCode = 'smallmapIdle();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xae):
#      self.strCode = 'SMALLMAP_CLOSE\n'
      self.strCode = 'smallmapClose();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xaf):
#      self.strCode = 'OPEN_CHEST\n'
      self.strCode = 'openChest();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    elif(self.nro == 0xb0):
      nn = self.array[1]
      xx = self.array[2]
      yy = self.array[3]

      # cambia el sprite de fondo por el indicado en NN, en las coordenadas XX,YY del bloque actual
#      self.strCode = 'SPRITE (NN,XX,YY) = (' + strNn + ',' + strXx + ',' + strYy + ')\n'
      self.strCode = 'sprite(nn=0x{:02x}, xx=0x{:02x}, yy=0x{:02x});\n'.format(nn,xx,yy)
      self.size = 4
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro in [0xba]):
      tipo = self.array[1]
      xx = self.array[2]
      yy = self.array[3]

#      strTipo = '{:02x}'.format(tipo)
#      strXx = '{:02x}'.format(xx)
#      strYy = '{:02x}'.format(yy)

#      self.strCode = 'ATTACK_EFFECT (TT,XX,YY) = (' + strTipo + ',' + strXx + ',' + strYy + ')\n'
      self.strCode = 'attackEffect(tt=0x{:02x}, xx=0x{:02x}, yy=0x{:02x});\n'.format(tipo, xx, yy)
      self.size = 4
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xb6):
#      self.strCode = 'LETTERBOX_EFFECT\n'
      self.strCode = 'letterboxEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xbc):
      # fades in from both fade_out and wash_out
#      self.strCode = 'FADE_IN\n'
      self.strCode = 'fadeInEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xbd):
      # fades to black screen
#      self.strCode = 'FADE_OUT\n'
      self.strCode = 'fadeOutEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xbe):
      # fades to white screen
#      self.strCode = 'WASH_OUT\n'
      self.strCode = 'washOutEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xbf):
#      self.strCode = 'PARPADEO\n'
      self.strCode = 'eyeblinkEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    elif(self.nro == 0xc0):
#      self.strCode = 'RECOVER_HP\n'
      self.strCode = 'recoverHp();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc1):
#      self.strCode = 'RECOVER_MP\n'
      self.strCode = 'recoverMp();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc2):
      arg = self.array[1]
#      self.strCode = 'HEAL_DISEASE {:02x}\n'.format(arg)
      self.strCode = 'healDisease(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc3):
      # it's a NOP, it does nothing.  unused in the original script
#      self.strCode = 'PASS\n'
      self.strCode = 'nop();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc4):
      # bitwise del argumento 
      # [][][][a][m][s][d][p]
      # p = poison
      # d = darkness
      # s = stone (no puede caminar)
      # m = moogle
      # a = avisar que se enfermó (0 = avisa, 1 = no avisa) (para curar: 0x10 = 0b10000)
      arg = self.array[1]
#      self.strCode = 'DISEASE {:02x}\n'.format(arg)
      self.strCode = 'disease(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc5):
      # stores arg as a 6-bit integer into flags 72..77 in reverse order: 0x01 = flag 77, 0x20 = flag 72
      arg = self.array[1]
#      self.strCode = 'SET_FLAGS_72_TO_77 {:02x}\n'.format(arg)
      self.strCode = 'setFlags72To77(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc6):
#      self.strCode = 'INPUT_NAMES_SUMO_FUJI\n'
      self.strCode = 'inputNames();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc7):
#      self.strCode = 'RANDOMIZE_7E7F\n'
      self.strCode = 'randomize7E7F();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc8):
#      self.strCode = 'RESET_GAME\n'
      self.strCode = 'resetGame();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc9):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg1*0x100 + arg2
#      self.strCode = 'SET_CHEST1_SCRIPT {:04x}\n'.format(arg)
      self.strCode = 'setChest1Script(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xca):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg1*0x100 + arg2
#      self.strCode = 'SET_CHEST2_SCRIPT {:04x}\n'.format(arg)
      self.strCode = 'setChest2Script(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xcb):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg1*0x100 + arg2
#      self.strCode = 'SET_CHEST3_SCRIPT {:04x}\n'.format(arg)
      self.strCode = 'setChest3Script(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])




    elif(self.nro == 0xcc):
      # stops listening to key inputs
#      self.strCode = 'INPUT_STOP\n'
      self.strCode = 'stopInput();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xd0):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg2*0x100 + arg1
#      self.strCode = 'INCREASE_GOLD {:02x} {:02x}\n'.format(arg1,arg2)
      self.strCode = 'increaseGold(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd1):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg2*0x100 + arg1
#      self.strCode = 'DECREASE_GOLD {:02x} {:02x}\n'.format(arg1,arg2)
      self.strCode = 'decreaseGold(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xd2):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg2*0x100 + arg1
#      self.strCode = 'INCREASE_EXP {:02x} {:02x}\n'.format(arg1,arg2)
      self.strCode = 'increaseExp(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd3):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg2*0x100 + arg1
#      self.strCode = 'DECREASE_EXP {:02x} {:02x}\n'.format(arg1,arg2)
      self.strCode = 'decreaseExp(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xd4):
      arg = self.array[1]
#      self.strCode = 'PICK_ITEM {:02x}\n'.format(arg)
      self.strCode = 'pickItem(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd5):
      arg = self.array[1]
#      self.strCode = 'DROP_ITEM {:02x}\n'.format(arg)
      self.strCode = 'dropItem(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd6):
      arg = self.array[1]
#      self.strCode = 'PICK_MAGIC {:02x}\n'.format(arg)
      self.strCode = 'pickMagic(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd7):
      arg = self.array[1]
#      self.strCode = 'DROP_MAGIC {:02x}\n'.format(arg)
      self.strCode = 'dropMagic(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd8):
      arg = self.array[1]
#      self.strCode = 'PICK_WEAPON {:02x}\n'.format(arg)
      self.strCode = 'pickWeapon(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd9):
      arg = self.array[1]
#      self.strCode = 'DROP_WEAPON {:02x}\n'.format(arg)
      self.strCode = 'dropWeapon(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xda):
      arg = self.array[1]
      label = mystic.variables.getLabel(arg)
#      self.strCode = 'FLAG_ON ' + label + '\n'
      self.strCode = 'flagOn(' + label + ');\n'
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xdb):
      arg = self.array[1]
      label = mystic.variables.getLabel(arg)
#      self.strCode = 'FLAG_OFF ' + label + '\n'
      self.strCode = 'flagOff(' + label + ');\n'
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xdc):
#      self.strCode = 'TEXT_SPEED_LOCK\n'
      self.strCode = 'textSpeedLock();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xdd):
#      self.strCode = 'TEXT_SPEED_UNLOCK\n'
      self.strCode = 'textSpeedUnlock();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    elif(self.nro == 0xde):
#      self.strCode = 'CONSUME_ITEM_AT_HAND\n'
      self.strCode = 'consumeItem();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
 

    elif(self.nro == 0xe0):
#      self.strCode = 'OPEN_DOOR_NORTH\n'
      self.strCode = 'openDoorNorth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe1):
#      self.strCode = 'CLOSE_DOOR_NORTH\n'
      self.strCode = 'closeDoorNorth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe2):
#      self.strCode = 'OPEN_DOOR_SOUTH\n'
      self.strCode = 'openDoorSouth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe3):
#      self.strCode = 'CLOSE_DOOR_SOUTH\n'
      self.strCode = 'closeDoorSouth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe4):
#      self.strCode = 'OPEN_DOOR_EAST\n'
      self.strCode = 'openDoorEast();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe5):
#      self.strCode = 'CLOSE_DOOR_EAST\n'
      self.strCode = 'closeDoorEast();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe6):
#      self.strCode = 'OPEN_DOOR_WEST\n'
      self.strCode = 'openDoorWest();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe7):
#      self.strCode = 'CLOSE_DOOR_WEST\n'
      self.strCode = 'closeDoorWest();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xe8):
      # la pantalla hace scroll al bloque hacia abajo
#      self.strCode = 'SCROLL_ABAJO\n'
      self.strCode = 'scrollSouth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe9):
      # la pantalla hace scroll al bloque hacia arriba
#      self.strCode = 'SCROLL_ARRIBA\n'
      self.strCode = 'scrollNorth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xea):
      # la pantalla hace scroll al bloque de la izquierda
#      self.strCode = 'SCROLL_IZQUIERDA\n'
      self.strCode = 'scrollLeft();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xeb):
      # la pantalla hace scroll al bloque de la derecha
#      self.strCode = 'SCROLL_DERECHA\n'
      self.strCode = 'scrollRight();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xec):
      # salta al script que se ejecuta al entrar a dicho bloque?
#      self.strCode = 'SCRIPT_ENTRAR_BLOQUE\n'
      self.strCode = 'enterRoomScript();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xed):
      # salta al script que se ejecuta al salir de dicho bloque
#      self.strCode = 'SCRIPT_SALIR_BLOQUE\n'
      self.strCode = 'exitRoomScript();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xee):
      # salta al script que se ejecuta al matar todos los enemigos del bloque
#      self.strCode = 'SCRIPT_MATOTODOS_BLOQUE\n'
      self.strCode = 'killedAllRoomScript();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    elif(self.nro in [0xef]):
#      print(mystic.util.strHexa(self.array[:min(20,len(self.array))]))
      xx = self.array[1]
      yy = self.array[2]
#      self.strCode = 'PROXIMO_BLOQUE (XX,YY) = ({:02x},{:02x})\n'.format(xx,yy)
      self.strCode = 'nextRoom(xx=0x{:02x}, yy=0x{:02x});\n'.format(xx,yy)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf3):
      mm = self.array[1]
      bb = self.array[2]
      xx = self.array[3]
      yy = self.array[4]

      strMm = '{:02x}'.format(mm)
      strBb = '{:02x}'.format(bb)
      strXx = '{:02x}'.format(xx)
      strYy = '{:02x}'.format(yy)

      # creo que la diferencia con el otro teleport está en que este no refresca los tiles de cambio de mapa?
#      self.strCode = 'TELEPORT2 (MM,BB,XX,YY) = (' + strMm + ',' + strBb + ',' + strXx + ',' + strYy + ')\n'
      self.strCode = 'teleport2(mm=0x' + strMm + ', bb=0x' + strBb + ', xx=0x' + strXx + ', yy=0x' + strYy + ');\n'
      self.size = 5
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf4):
      mm = self.array[1]
      bb = self.array[2]
      xx = self.array[3]
      yy = self.array[4]

      strMm = '{:02x}'.format(mm)
      strBb = '{:02x}'.format(bb)
      strXx = '{:02x}'.format(xx)
      strYy = '{:02x}'.format(yy)

#      self.strCode = 'TELEPORT (MM,BB,XX,YY) = (' + strMm + ',' + strBb + ',' + strXx + ',' + strYy + ')\n'
      self.strCode = 'teleport(mm=0x' + strMm + ', bb=0x' + strBb + ', xx=0x' + strXx + ', yy=0x' + strYy + ');\n'
      self.size = 5
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf6):
      # validos: del 0x00 al 0x10 inclusive
      arg = self.array[1]
#      self.strCode = 'VENDEDOR {:02x}\n'.format(arg)
      self.strCode = 'salesman(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf8):
      # indico como mapea con el número de canción del banco 0x0f (0x00 = mute, 0x01 = intro song, ... 0x1e = ill (last song))
      arg = self.array[1]
#      self.strCode = 'MUSIC {:02x}\n'.format(arg)
      self.strCode = 'music(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf9):
      arg = self.array[1]
#      self.strCode = 'SOUND_EFFECT {:02x}\n'.format(arg)
      self.strCode = 'soundEffect(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xfb):
      # la pantalla hace scroll al bloque de la derecha
#      self.strCode = 'SCREEN_SHAKE\n'
      self.strCode = 'shakeScreen();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xfc):
      arg = self.array[1]
#      self.strCode = 'LOAD_GRUPO_PERSONAJE {:02x}\n'.format(arg)
      self.strCode = 'loadGrupoPersonaje(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xfd):
      arg = self.array[1]
#      self.strCode = 'ADD_PERSONAJE {:02x}\n'.format(arg)
      self.strCode = 'addPersonaje(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xfe):
      arg = self.array[1]
      label = mystic.variables.getLabelBoss(arg)
#      self.strCode = 'ADD_MONSTRUO_GRANDE {:02x}\n'.format(arg)
#      self.strCode = 'ADD_MONSTRUO_GRANDE ' + label + '\n'
      self.strCode = 'addBoss(' + label + ');\n'
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf0):
      arg = self.array[1]
#      self.strCode = 'SLEEP {:02x}\n'.format(arg)
      self.strCode = 'sleep(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0x04):
      # pasamos a text mode
#      self.strCode = '<TEXT_MODE_ON>'
#      self.strCode = 'text("<TEXT_MODE_ON>'
      self.strCode = 'text("'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

      textMode = True


#    print('strCode: ' + self.strCode)
    return textMode


  def decodeTxt(self, lines):
    """ lo decodifica """

    self.textMode = False

    self.lines = lines

    line = self.lines[0].strip()
    self.strCode = line + '\n'
#    print('cmd line: ' + line)

    # si es un comentario
    if(line.startswith('//') or line.startswith('/*') or len(line) == 0):

#      self.hexs.append(0x00)
      # el sizeLines es la cantidad de renglones del comando (1 salvo FOR, IF, ELSE que tienen script propio)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

      # retorno sin mas
      return

#    if(line == 'END'):
#    if(line == '}'):
    if(line == '}//END_FUNCTION' or line == '}//END_FOR'):
      self.hexs.append(0x00)
      # el sizeLines es la cantidad de renglones del comando (1 salvo FOR, IF, ELSE que tienen script propio)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
      return

    elif(line.startswith('}//END_IF') or line.startswith('}//END_ELSE')):
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    if(line.startswith('NI_IDEA')):

      idx0 = line.find(':')
      argTxt = line[idx0+2: ]
#      print('argTxt: ' + argTxt)

      argsTxt = argTxt.split(' ')

      args = []
      for strArg in argsTxt:
#        print('strArg: ' + strArg)
        arg = int(strArg, 16)
#        print('arg: {:02x}'.format(arg))
        args.append(arg)

      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('script')):

      argTxt = line[len('script')+1:]
      strArg1 = argTxt[0:2]
      strArg2 = argTxt[2:4]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)
      args = [arg1, arg2]

      self.jumpLabel = '${:04x}'.format(arg1*0x100 + arg2)
#      print('jumpLabel: ' + self.jumpLabel)
      self.hexs.append(0x02)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('FOR')):
    elif(line.startswith('for(')):

#      idx0 = line.rfind('<')
      idx0 = line.rfind('x')
      strI = line[idx0+1:idx0+3]
      i = int(strI,16)

      sizeLines = 1
      deep = 1
      bloqueLines = []
      while( deep != 0 ):

        subLine = self.lines[sizeLines].strip()
        bloqueLines.append(subLine)
        sizeLines += 1

#        if(subLine.startswith('FOR')):
        if(subLine.startswith('for(')):
          deep += 1
#        elif(subLine == 'END'):
#        elif(subLine == '}'):
        elif(subLine == '}//END_FOR'):
          deep -= 1

      bloque = Script(self.addr + 3, 'for')
      bloque.decodeTxt(bloqueLines)
      self.script = bloque

      self.hexs.append(0x03)
      self.hexs.append(i)

      hexs = bloque.encodeRom()

      strHex = mystic.util.strHexa(hexs)
#      print('strHex: ' + strHex)
      self.hexs.append( len(hexs) )

      self.sizeLines = sizeLines
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('ELSE')):
    elif(line.startswith('} else {')):

      line0 = self.lines[0]
      origDeep = len(line0) - len(line0.lstrip(' '))
      sizeLines = 1
      deep = 9999
      bloqueLines = []
      while( deep > origDeep and sizeLines < len(self.lines) ):

        linei = self.lines[sizeLines]
        deep = len(linei) - len(linei.lstrip(' '))

#        subLine = self.lines[sizeLines].strip()
        subLine = self.lines[sizeLines]
        bloqueLines.append(subLine)
        sizeLines += 1

#      if(sizeLines < len(self.lines)):
      # si retomó el nivel de profundidad
      if(deep == origDeep):
        # elimino el último renglón (ya es de otro bloque, o un ELSE)
        proximo = bloqueLines.pop()
        sizeLines -= 1

      self.hexs.append(0x01)

      bloque = Script(self.addr + 2, 'else')
      bloque.decodeTxt(bloqueLines)
      self.script = bloque


      hexs = bloque.encodeRom()
      strHex = mystic.util.strHexa(hexs)

      self.hexs.append( len(hexs) )

      strHex = mystic.util.strHexa(self.hexs)

      self.sizeLines = sizeLines
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('IF')):
    elif(line.startswith('if(')):

      # en principio asumo que no tiene ELSE
      hasElse = False

      idx0 = line.find('[')
      idx1 = line.find(']')

      argTxt = line[idx0+1: idx1]
#      print('argTxt: ' + argTxt)

      argsTxt = argTxt.split(',')
      argsTxt = [argTxt.strip() for argTxt in argsTxt]
#      print('argsTxt: ' + str(argsTxt))
      # elimino el último (está vacío, por el espacio al final antes del paréntesis)
#      argsTxt.pop()

      line0 = self.lines[0]
      origDeep = len(line0) - len(line0.lstrip(' '))
      sizeLines = 1
      deep = 9999
      bloqueLines = []
      while( deep > origDeep and sizeLines < len(self.lines)):

        linei = self.lines[sizeLines]
        deep = len(linei) - len(linei.lstrip(' '))

#        subLine = self.lines[sizeLines].strip()
        subLine = self.lines[sizeLines]
        bloqueLines.append(subLine)
        sizeLines += 1

      proximo = 'nada'
#      if(sizeLines < len(self.lines)):
      # si retomó el nivel de profundidad
      if(deep == origDeep):
        # elimino el último renglón (ya es de otro bloque, o un ELSE)
        proximo = bloqueLines.pop()
        sizeLines -= 1

      # si lo que le sigue es un else
#      if(proximo.strip() == 'ELSE'):
      if(proximo.strip() == '} else {'):
        # lo dejo indicado
        hasElse = True

#      if(line.startswith('IF(')):
      if(line.startswith('if(if_flags([')):
        self.hexs.append(0x08)

        args = []
        for strArg in argsTxt:
          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'if')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

#      elif(line.startswith('IF_HAND(')):
      elif(line.startswith('if(if_hand([')):
        self.hexs.append(0x09)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'if_hand')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

#      elif(line.startswith('IF_INVENTORY(')):
      elif(line.startswith('if(if_inventory([')):
        self.hexs.append(0x0a)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'if_inventory')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

#      elif(line.startswith('IF_TRIGGERED_ON_BY(')):
      elif(line.startswith('if(if_triggered_on_by([')):
        self.hexs.append(0x0b)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'if_triggered_on_by')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

#      elif(line.startswith('IF_TRIGGERED_OFF_BY(')):
      elif(line.startswith('if(if_triggered_off_by([')):
        self.hexs.append(0x0c)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'if_triggered_off_by')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

      self.hexs.extend(args)
      self.hexs.append(0x00)

      hexs = bloque.encodeRom()
      strHex = mystic.util.strHexa(hexs)

      if(hasElse):
        self.hexs.append( len(hexs)+2 )
      else:
        self.hexs.append( len(hexs) )

      strHex = mystic.util.strHexa(self.hexs)

      self.sizeLines = sizeLines
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('HOP_JUMP')):
    elif(line.startswith('hopJump(')):
      idx0 = len('hopJump(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0x8b)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('hero')):
      idx = line.index('(')
      strAction = line[4:idx]
#      print('strAction: ' + strAction)

      nroExtra = 8

      if(strAction in ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseB', 'NoseC', 'NoseD', 'NoseE', 'NoseF']):

        actions = ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'WalkFastSpeed', 'WalkNormalSpeed', 'Teleport', 'NoseB', 'NoseC', 'NoseD', 'NoseE', 'NoseF']
        nroAction = actions.index(strAction)

        nroCmd = nroExtra * 0x10 + nroAction
        self.hexs.append(nroCmd)
        self.sizeLines = 1
        self.sizeBytes = len(self.hexs)

      elif(strAction.startswith('Teleport')):

        nroAction = 0xa

        idx0 = line.index('xx=0x')
        strXx = line[idx0+5:idx0+7]
        idx0 = line.index('yy=0x')
        strYy = line[idx0+5:idx0+7]
        strArgsSplit = [strXx, strYy]
        args = [ int(u, 16) for u in strArgsSplit ]

        nroCmd = nroExtra * 0x10 + nroAction
        self.hexs.append(nroCmd)
        self.hexs.extend(args)
        self.sizeLines = 1
        self.sizeBytes = len(self.hexs)

    elif(line.startswith('partner')):

      idx = line.index('(')
      strAction = line[7:idx]
#      print('strAction: ' + strAction)

      nroExtra = 9
 
      if(strAction in ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseD', 'NoseE', 'NoseF']):

        actions = ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'Teleport', 'WalkFastSpeed', 'WalkNormalSpeed', 'SetPersonaje', 'NoseD', 'NoseE', 'NoseF']
        nroAction = actions.index(strAction)

        nroCmd = nroExtra * 0x10 + nroAction
        self.hexs.append(nroCmd)
        self.sizeLines = 1
        self.sizeBytes = len(self.hexs)

      elif(strAction.startswith('Teleport')):

        nroAction = 0x9

        idx0 = line.index('xx=0x')
        strXx = line[idx0+5:idx0+7]
        idx0 = line.index('yy=0x')
        strYy = line[idx0+5:idx0+7]
        strArgsSplit = [strXx, strYy]
        args = [ int(u, 16) for u in strArgsSplit ]


        nroCmd = nroExtra * 0x10 + nroAction
        self.hexs.append(nroCmd)
        self.hexs.extend(args)
        self.sizeLines = 1
        self.sizeBytes = len(self.hexs)

      elif(strAction.startswith('SetPersonaje')):

        idx0 = line.rfind('(')
        idx1 = line.rfind(')')
        strArg = line[idx0+1:idx1]
        arg = int(strArg,16)
#        print('partner set personaje: {:02x}'.format(arg))

        self.hexs.append(0x9c)
        self.hexs.append(arg)
        self.sizeLines = 1
        self.sizeBytes = len(self.hexs)


    elif(line.startswith('extra')):

      idx = line.index('(')
      strAction = line[6:idx]
#      print('strAction: ' + strAction)

      nroExtra = int(line[5])
 
      if(strAction in ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseC', 'NoseD', 'NoseE', 'NoseF']):

        actions = ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'Teleport', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseC', 'NoseD', 'NoseE', 'NoseF']
        nroAction = actions.index(strAction)

        nroCmd = nroExtra * 0x10 + nroAction
        self.hexs.append(nroCmd)
        self.sizeLines = 1
        self.sizeBytes = len(self.hexs)

      elif(strAction.startswith('Teleport')):

        nroAction = 0x9

        idx0 = line.index('xx=0x')
        strXx = line[idx0+5:idx0+7]
        idx0 = line.index('yy=0x')
        strYy = line[idx0+5:idx0+7]
        strArgsSplit = [strXx, strYy]
        args = [ int(u, 16) for u in strArgsSplit ]

        nroCmd = nroExtra * 0x10 + nroAction
        self.hexs.append(nroCmd)
        self.hexs.extend(args)
        self.sizeLines = 1
        self.sizeBytes = len(self.hexs)


#    elif(line.startswith('WALKING_AS_CHOCOBO') and not line.startswith('WALKING_AS_CHOCOBOT')):
    elif(line.startswith('walkingAsChocobo(')):
      self.hexs.append(0xa0)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_CHOCOBOT_LAND')):
    elif(line.startswith('walkingAsChocobotLand(')):
      self.hexs.append(0xa1)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_CHOCOBOT_WATER')):
    elif(line.startswith('walkingAsChocobotWater(')):
      self.hexs.append(0xa2)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_TROLLEY_WAGON')):
    elif(line.startswith('walkingAsWagon(')):
      self.hexs.append(0xa3)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_NORMAL')):
    elif(line.startswith('walkingAsNormal(')):
      self.hexs.append(0xa4)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_FALLING')):
    elif(line.startswith('walkingAsFalling(')):
      self.hexs.append(0xa5)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_DEAD')):
    elif(line.startswith('walkingAsDead(')):
      self.hexs.append(0xa6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('CHECK_IF_CURRENT_MAP_HAS_SMALLMAP')):
    elif(line.startswith('checkIfCurrentMapHasSmallmap(')):
      self.hexs.append(0xa9)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('CLEAR_MATO_TODOS')):
    elif(line.startswith('clearKilledAllRoom(')):
      self.hexs.append(0xab)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SMALLMAP_OPEN')):
    elif(line.startswith('smallmapOpen(')):
      self.hexs.append(0xac)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SMALLMAP_IDLE')):
    elif(line.startswith('smallmapIdle(')):
      self.hexs.append(0xad)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SMALLMAP_CLOSE')):
    elif(line.startswith('smallmapClose(')):
      self.hexs.append(0xae)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('OPEN_CHEST')):
    elif(line.startswith('openChest(')):
      self.hexs.append(0xaf)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('sprite(')):

      idx0 = line.index('nn=0x')
      strNn = line[idx0+5:idx0+7]
      idx0 = line.index('xx=0x')
      strXx = line[idx0+5:idx0+7]
      idx0 = line.index('yy=0x')
      strYy = line[idx0+5:idx0+7]
      strArgsSplit = [strNn, strXx, strYy]
      args = [ int(u, 16) for u in strArgsSplit ]

      self.hexs.append(0xb0)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('attackEffect(')):

      idx0 = line.index('tt=0x')
      strTt = line[idx0+5:idx0+7]
      idx0 = line.index('xx=0x')
      strXx = line[idx0+5:idx0+7]
      idx0 = line.index('yy=0x')
      strYy = line[idx0+5:idx0+7]
      strArgsSplit = [strTt, strXx, strYy]
      args = [ int(u, 16) for u in strArgsSplit ]

      self.hexs.append(0xba)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('LETTERBOX_EFFECT')):
    elif(line.startswith('letterboxEffect(')):
      self.hexs.append(0xb6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('FADE_IN')):
    elif(line.startswith('fadeInEffect(')):
      self.hexs.append(0xbc)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('FADE_OUT')):
    elif(line.startswith('fadeOutEffect(')):
      self.hexs.append(0xbd)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WASH_OUT')):
    elif(line.startswith('washOutEffect(')):
      self.hexs.append(0xbe)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('PARPADEO')):
    elif(line.startswith('eyeblinkEffect(')):
      self.hexs.append(0xbf)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('RECOVER_HP')):
    elif(line.startswith('recoverHp(')):
      self.hexs.append(0xc0)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('RECOVER_MP')):
    elif(line.startswith('recoverMp(')):
      self.hexs.append(0xc1)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('HEAL_DISEASE')):
    elif(line.startswith('healDisease(')):
      idx0 = len('healDisease(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xc2)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('PASS')):
    elif(line.startswith('nop(')):
      self.hexs.append(0xc3)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('DISEASE')):
    elif(line.startswith('disease(')):
      idx0 = len('disease(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xc4)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SET_FLAGS_72_TO_77')):
    elif(line.startswith('setFlags72To77(')):
      idx0 = len('setFlags72To77(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xc5)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('INPUT_NAMES_SUMO_FUJI')):
    elif(line.startswith('inputNames();')):
      self.hexs.append(0xc6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('RANDOMIZE_7E7F')):
    elif(line.startswith('randomize7E7F(')):
      self.hexs.append(0xc7)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('RESET_GAME')):
    elif(line.startswith('resetGame();')):
      self.hexs.append(0xc8)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SET_CHEST1_SCRIPT')):
    elif(line.startswith('setChest1Script(')):
#      argTxt = line[len('SET_CHEST1_SCRIPT')+1:]
#      strArg1 = argTxt[0:2]
#      strArg2 = argTxt[2:4]
#      arg1 = int(strArg1, 16)
#      arg2 = int(strArg2, 16)

      idx = len('setChest1Script(0x')
      strArg1 = line[idx:idx+2]
      strArg2 = line[idx+2:idx+4]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)

      args = [arg1, arg2]

      self.hexs.append(0xc9)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SET_CHEST2_SCRIPT')):
    elif(line.startswith('setChest2Script(')):
      idx = len('setChest2Script(0x')
      strArg1 = line[idx:idx+2]
      strArg2 = line[idx+2:idx+4]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)

      args = [arg1, arg2]

      self.hexs.append(0xca)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SET_CHEST3_SCRIPT')):
    elif(line.startswith('setChest3Script(')):

      idx = len('setChest3Script(0x')
      strArg1 = line[idx:idx+2]
      strArg2 = line[idx+2:idx+4]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)
      args = [arg1, arg2]

      self.hexs.append(0xcb)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('INPUT_STOP')):
    elif(line.startswith('stopInput(')):
      self.hexs.append(0xcc)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('INCREASE_GOLD')):
    elif(line.startswith('increaseGold(')):
      idx = len('increaseGold(0x')
      strArg1 = line[idx:idx+2]
      strArg2 = line[idx+2:idx+4]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)
      args = [arg2, arg1]

      self.hexs.append(0xd0)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('DECREASE_GOLD')):
    elif(line.startswith('decreaseGold(')):
      idx = len('decreaseGold(0x')
      strArg1 = line[idx:idx+2]
      strArg2 = line[idx+2:idx+4]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)
      args = [arg2, arg1]

      self.hexs.append(0xd1)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('INCREASE_EXP')):
    elif(line.startswith('increaseExp(')):
      idx = len('increaseExp(0x')
      strArg1 = line[idx:idx+2]
      strArg2 = line[idx+2:idx+4]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)
      args = [arg2, arg1]

      self.hexs.append(0xd2)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('DECREASE_EXP')):
    elif(line.startswith('decreaseExp(')):
      idx = len('increaseExp(0x')
      strArg1 = line[idx:idx+2]
      strArg2 = line[idx+2:idx+4]
      arg1 = int(strArg1, 16)
      arg2 = int(strArg2, 16)
      args = [arg2, arg1]

      self.hexs.append(0xd3)
      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('PICK_ITEM')):
    elif(line.startswith('pickItem(')):
      idx0 = len('pickItem(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd4)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('DROP_ITEM')):
    elif(line.startswith('dropItem(')):
      idx0 = len('dropItem(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd5)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('PICK_MAGIC')):
    elif(line.startswith('pickMagic(')):
      idx0 = len('pickMagic(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd6)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('DROP_MAGIC')):
    elif(line.startswith('dropMagic(')):
      idx0 = len('dropMagic(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd7)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('PICK_WEAPON')):
    elif(line.startswith('pickWeapon(')):
      idx0 = len('pickWeapon(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd8)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('DROP_WEAPON')):
    elif(line.startswith('dropWeapon(')):
      idx0 = len('dropWeapon(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd9)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('FLAG_ON')):
    elif(line.startswith('flagOn(')):
      argTxt = line[len('flagOn('):]
      argTxt = argTxt[:argTxt.index(')')]
      arg = mystic.variables.getVal(argTxt)

      self.hexs.append(0xda)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('FLAG_OFF')):
    elif(line.startswith('flagOff(')):
      argTxt = line[len('flagOff('):]
      argTxt = argTxt[:argTxt.index(')')]
      arg = mystic.variables.getVal(argTxt)

      self.hexs.append(0xdb)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('TEXT_SPEED_LOCK')):
    elif(line.startswith('textSpeedLock(')):
      self.hexs.append(0xdc)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('TEXT_SPEED_UNLOCK')):
    elif(line.startswith('textSpeedUnlock(')):
      self.hexs.append(0xdd)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('CONSUME_ITEM_AT_HAND')):
    elif(line.startswith('consumeItem(')):
      self.hexs.append(0xde)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('OPEN_DOOR_NORTH')):
    elif(line.startswith('openDoorNorth(')):
      self.hexs.append(0xe0)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('CLOSE_DOOR_NORTH')):
    elif(line.startswith('closeDoorNorth(')):
      self.hexs.append(0xe1)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('OPEN_DOOR_SOUTH')):
    elif(line.startswith('openDoorSouth(')):
      self.hexs.append(0xe2)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('CLOSE_DOOR_SOUTH')):
    elif(line.startswith('closeDoorSouth(')):
      self.hexs.append(0xe3)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('OPEN_DOOR_EAST')):
    elif(line.startswith('openDoorEast(')):
      self.hexs.append(0xe4)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('CLOSE_DOOR_EAST')):
    elif(line.startswith('closeDoorEast(')):
      self.hexs.append(0xe5)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('OPEN_DOOR_WEST')):
    elif(line.startswith('openDoorWest(')):
      self.hexs.append(0xe6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('CLOSE_DOOR_WEST')):
    elif(line.startswith('closeDoorWest(')):
      self.hexs.append(0xe7)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SCROLL_ABAJO')):
    elif(line.startswith('scrollSouth(')):
      self.hexs.append(0xe8)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCROLL_ARRIBA')):
    elif(line.startswith('scrollNorth(')):
      self.hexs.append(0xe9)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCROLL_IZQUIERDA')):
    elif(line.startswith('scrollLeft(')):
      self.hexs.append(0xea)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCROLL_DERECHA')):
    elif(line.startswith('scrollRight(')):
      self.hexs.append(0xeb)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCRIPT_ENTRAR_BLOQUE')):
    elif(line.startswith('enterRoomScript(')):
      self.hexs.append(0xec)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCRIPT_SALIR_BLOQUE')):
    elif(line.startswith('e')):
      self.hexs.append(0xed)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCRIPT_MATOTODOS_BLOQUE')):
    elif(line.startswith('killedAllRoomScript(')):
      self.hexs.append(0xee)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('SLEEP')):
    elif(line.startswith('sleep(')):
      idx = len('sleep(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xf0)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('PROXIMO_BLOQUE')):
    elif(line.startswith('nextRoom(')):
      idx0 = line.index('xx=0x')
      strXx = line[idx0+5:idx0+7]
      idx0 = line.index('yy=0x')
      strYy = line[idx0+5:idx0+7]
      strArgsSplit = [strXx, strYy]
      args = [ int(u, 16) for u in strArgsSplit ]

      self.hexs.append(0xef)

      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('TELEPORT')):
    elif(line.startswith('teleport')):

#      idx0 = line.find('=')
#      strArgs = line[idx0+3: len(line)-1]
#      strArgsSplit = strArgs.split(',')

      idx0 = line.index('mm=0x')
      strMm = line[idx0+5:idx0+7]
      idx0 = line.index('bb=0x')
      strBb = line[idx0+5:idx0+7]
      idx0 = line.index('xx=0x')
      strXx = line[idx0+5:idx0+7]
      idx0 = line.index('yy=0x')
      strYy = line[idx0+5:idx0+7]
      strArgsSplit = [strMm, strBb, strXx, strYy]
      args = [ int(u, 16) for u in strArgsSplit ]

      # si es el teleport 1
      if(not line[8] == '2'): 
        self.hexs.append(0xf4)
      # sino, es el teleport 2
      else:
        self.hexs.append(0xf3)

      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('VENDEDOR')):
    elif(line.startswith('salesman(')):
      idx = len('salesman(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xf6)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('MUSIC')):
    elif(line.startswith('music(')):
      idx = len('music(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)

      self.hexs.append(0xf8)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('soundEffect(')):
      idx = len('soundEffect(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xf9)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SCREEN_SHAKE')):
    elif(line.startswith('shakeScreen(')):
      self.hexs.append(0xfb)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('loadGrupoPersonaje(')):
      idx = len('loadGrupoPersonaje(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xfc)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('addPersonaje(')):
      idx = len('addPersonaje(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xfd)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('ADD_MONSTRUO_GRANDE')):
    elif(line.startswith('addBoss(')):
      argTxt = line[len('addBoss('):].strip()
      argTxt = argTxt[:argTxt.index(')')]
#      print('argTxt: ' + argTxt)
#      arg = int(argTxt, 16)
      arg = mystic.variables.getValBoss(argTxt)
      self.hexs.append(0xfe)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    # si es texto
#    elif(line.startswith('<')):
    elif(line.startswith('text(')):
      # indico que es en modo texto
      self.textMode = True

#      print('LINE: ' + line)

#      compactLine = line.replace('text("<TEXT_MODE_ON>',         u'\U0001F60A')
      compactLine = line.replace('text("',         u'\U0001F60A')
#      compactLine = compactLine.replace('<TEXT_MODE_OFF>");', u'\U0001F61E')
      compactLine = compactLine.replace('");', u'\U0001F61E')
      compactLine = compactLine.replace('<TEXTBOX_SHOW>',  u'\U0001F639')
      compactLine = compactLine.replace('<TEXTBOX_HIDE>',  u'\U0001F63F')
      compactLine = compactLine.replace('<PAUSE>',         u'\U0001F610')
      compactLine = compactLine.replace('<ENTER>',         u'\U0001F618')
      compactLine = compactLine.replace('<SUMO>',          u'\U0001F466')
      compactLine = compactLine.replace('<FUJI>',          u'\U0001F467')
      compactLine = compactLine.replace('<CLS>',           u'\U0001F61D')
      compactLine = compactLine.replace('<BACKSPACE>',     u'\U0001F47C')
      compactLine = compactLine.replace('<CARRY>',         u'\U0001F634')
      compactLine = compactLine.replace('<ASK_YES_NO>',       u'\U0001F624')
      compactLine = compactLine.replace('<ICON a0>', u'\U00002200')
      compactLine = compactLine.replace('<ICON a1>', u'\U00002201')
      compactLine = compactLine.replace('<ICON a2>', u'\U00002202')
      compactLine = compactLine.replace('<ICON a3>', u'\U00002203')
      compactLine = compactLine.replace('<ICON a4>', u'\U00002204')
      compactLine = compactLine.replace('<ICON a5>', u'\U00002205')
      compactLine = compactLine.replace('<ICON a6>', u'\U00002206')
      compactLine = compactLine.replace('<ICON a7>', u'\U00002207')
      compactLine = compactLine.replace('<ICON a8>', u'\U00002208')
      compactLine = compactLine.replace('<ICON a9>', u'\U00002209')
      compactLine = compactLine.replace('<ICON aa>', u'\U0000220a')
      compactLine = compactLine.replace('<ICON ab>', u'\U0000220b')
      compactLine = compactLine.replace('<ICON ac>', u'\U0000220c')
      compactLine = compactLine.replace('<ICON ad>', u'\U0000220d')
      compactLine = compactLine.replace('<ICON ae>', u'\U0000220e')
      compactLine = compactLine.replace('<ICON af>', u'\U0000220f')


      lang = mystic.address.language
      # si es la rom 'jp'
      if(lang == mystic.language.JAPAN):
        # tiene su propia forma de comprimir palabras
        self.hexs = mystic.dictionary.tryJpCompress(compactLine)
        strHex = mystic.util.strHexa(self.hexs)
#        print('japancomprimi strHex: ' + strHex)

      else:

        sizeLine = len(compactLine)
        i = 0
        while(i < sizeLine):
          char = compactLine[i]

          if(char == u'\U0001F60A'):
            self.hexs.append(0x04)
          elif(char == u'\U0001F61E'):
            self.hexs.append(0x00)
          elif(char == u'\U0001F639'):
            self.hexs.append(0x10)
          elif(char == u'\U0001F63F'):
            self.hexs.append(0x11)
          elif(char == u'\U0001F610'):
            self.hexs.append(0x12)
          elif(char == u'\U0001F618'):
            self.hexs.append(0x1a)
          elif(char == u'\U0001F466'):
            self.hexs.append(0x14)
          elif(char == u'\U0001F467'):
            self.hexs.append(0x15)
          elif(char == u'\U0001F61D'):
            self.hexs.append(0x1b)
          elif(char == u'\U0001F47C'):
            self.hexs.append(0x1d)
          elif(char == u'\U0001F634'):
            self.hexs.append(0x1f)
          elif(char == u'\U0001F624'):
            self.hexs.append(0x13)
          elif(char == u'\U00002200'):
            self.hexs.append(0xa0)
          elif(char == u'\U00002201'):
            self.hexs.append(0xa1)
          elif(char == u'\U00002202'):
            self.hexs.append(0xa2)
          elif(char == u'\U00002203'):
            self.hexs.append(0xa3)
          elif(char == u'\U00002204'):
            self.hexs.append(0xa4)
          elif(char == u'\U00002205'):
            self.hexs.append(0xa5)
          elif(char == u'\U00002206'):
            self.hexs.append(0xa6)
          elif(char == u'\U00002207'):
            self.hexs.append(0xa7)
          elif(char == u'\U00002208'):
            self.hexs.append(0xa8)
          elif(char == u'\U00002209'):
            self.hexs.append(0xa9)
          elif(char == u'\U0000220a'):
            self.hexs.append(0xaa)
          elif(char == u'\U0000220b'):
            self.hexs.append(0xab)
          elif(char == u'\U0000220c'):
            self.hexs.append(0xac)
          elif(char == u'\U0000220d'):
            self.hexs.append(0xad)
          elif(char == u'\U0000220e'):
            self.hexs.append(0xae)
          elif(char == u'\U0000220f'):
            self.hexs.append(0xaf)

          else:
            # agarro dos chars seguidos
            chars = compactLine[i:i+2]

#            if(chars in mystic.dictionary.invDeDict.keys()):
            if(chars in mystic.dictionary.chars()):
#              hexy = mystic.dictionary.invDeDict[chars]
              hexy = mystic.dictionary.encodeChars(chars)
#              print('chars: ' + chars + ' - hex: {:02x}'.format(hexy))

              i += 1
            else:
              char = chars[0]
#              hexy = mystic.dictionary.invDeDict[char]
              hexy = mystic.dictionary.encodeChars(char)
#              print('char: ' + char + ' - hex: {:02x}'.format(hexy))
          
            self.hexs.append(hexy)

          i += 1

      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)



  def __str__(self):
#    return self.strCode + ' | ' + self.strHex
    return self.strCode
#    return '\n{:04x} '.format(self.addr) + self.strCode
#    return '(' + self.strHex + ')' + self.strCode 




