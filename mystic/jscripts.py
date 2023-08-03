
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
      if(addr < 0x4000):
        banco += 0
        addr -= 0*0x4000
      elif(addr >= 0x4000 and addr < 0x8000):
        banco += 1
        addr -= 1*0x4000
      elif(addr >= 0x8000 and addr < 0xc000):
        banco += 2
        addr -= 2*0x4000
      elif(addr >= 0xc000 and addr < 0x10000):
        banco += 3
        addr -= 3*0x4000
 

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

      banco = 0x0d
      addr0 = script.addr
      addr1 = vaPorAddr
      # grabo las romstats
      if(script.addr < 0x4000):
        banco += 0
        addr0 -= 0*0x4000
        addr1 -= 0*0x4000
      elif(script.addr >= 0x4000 and script.addr < 0x8000):
        banco += 1
        addr0 -= 1*0x4000
        addr1 -= 1*0x4000
      elif(script.addr >= 0x8000 and script.addr < 0xc000):
        banco += 2
        addr0 -= 2*0x4000
        addr1 -= 2*0x4000
      elif(script.addr >= 0xc000 and script.addr < 0x10000):
        banco += 3
        addr0 -= 3*0x4000
        addr1 -= 3*0x4000

#      print('script banco: {:02x} addr0: {:04x} addr1: {:04x}'.format(banco, addr0, addr1))
      mystic.romStats.appendDato(banco, addr0, addr1, (rr, gg, bb), 'un script')

#      print('romstats {:04x} {:04x}'.format(script.addr, vaPorAddr))



  def encodeTxt(self):
    newLines = []

    newLines.append("");
    newLines.append("/******************************************************************************/");
    newLines.append("/*                                                                            */");
    newLines.append("/*                 Welcome to the mystic-jscript-language                     */");
    newLines.append("/*                                                                            */");
    newLines.append("/* Some observations to take care off, while jscript has a                    */");
    newLines.append("/*    javascript-like syntax, it is far less flexible, for example:           */");
    newLines.append("/*                                                                            */");
    newLines.append("/* 1. Multiline comments are not supported (only within the same line).       */");
    newLines.append("/* 2. It is heavily tab dependent, like python.                               */");
    newLines.append("/* 3. One space can break anything                                            */");
    newLines.append("/*     ( '} else {' is valid but '}else{' is not )                            */");
    newLines.append("/* 4. The ending block comments are mandatory, for the time being.            */");
    newLines.append("/*     ( '}//END_FUNCTION' is valid but '}' is not )                          */");
    newLines.append("/* 5. All script names must have the format script_HHHH                       */");
    newLines.append("/*     where HHHH is it's hex number                                          */");
    newLines.append("/* 6. Flags constants must start with 'flag_' and boss constants with 'boss_' */");
    newLines.append("/* 7. All integers must be written in hexadecimal format.                     */");
    newLines.append("/* 8. Enjoy!                                                                  */");
    newLines.append("/*                                                                            */");
    newLines.append("/******************************************************************************/");
    newLines.append("");

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


    newLines.append('');
    newLines.append('/* songs */');
    for val in mystic.variables.songs.keys():
      var = mystic.variables.songs[val]
#      print('key: ' + labelVar + ' value: ' + str(nroVar))
      newLines.append('const ' + var + ' = 0x{:02x};'.format(val))


    newLines.append('');
    newLines.append('/* sfx */');
    for val in mystic.variables.sounds.keys():
      var = mystic.variables.sounds[val]
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
      if(not line.strip().startswith('await script')):
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
      if('async function script_' in line):

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
        nroScript = int(line[22:22+4],16)
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

        elif(line.strip().startswith('const song')):
          line = line.strip()
          subLine = line[len('const'):].strip()
          idx0 = subLine.index('=')
          var = subLine[:idx0].strip()
          strVal = subLine[idx0+1:].strip()
          idx1 = strVal.index('x')
          idx2 = strVal.index(';')
          strVal = strVal[idx1+1:idx2].strip()
          val = int(strVal,16)
#          print('song: ' + var + ' --- val: {:02x}'.format(val))
          mystic.variables.songs[val] = var

        elif(line.strip().startswith('const sfx')):
          line = line.strip()
          subLine = line[len('const'):].strip()
          idx0 = subLine.index('=')
          var = subLine[:idx0].strip()
          strVal = subLine[idx0+1:].strip()
          idx1 = strVal.index('x')
          idx2 = strVal.index(';')
          strVal = strVal[idx1+1:idx2].strip()
          val = int(strVal,16)
#          print('sfx: ' + var + ' --- val: {:02x}'.format(val))
          mystic.variables.sounds[val] = var
 
          
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
        cmd.strCode = 'await script {:04x}'.format(addr)

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

#      print('i: ' + str(i) + ' subArray: ' + mystic.util.strHexa(subArray))

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

    # tipo de bloque ('function', 'for', 'else', 'else_if', 'cond_flags', 'cond_hand', 'cond_inventory', 'cond_step_on_by', 'cond_step_off_by')
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
      if(cmd.strCode.startswith('await script')):
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
    string += 'async function script_{:04x}()'.format(self.nro) + ' {\n'

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

#      if(self.bloque.tipoBloque == 'cond_flags'):
#        self.strCode = '}//END_IF_FLAGS\n'
#      elif(self.bloque.tipoBloque == 'cond_hand'):
#        self.strCode = '}//END_IF_HAND\n'
#      elif(self.bloque.tipoBloque == 'cond_inventory'):
#        self.strCode = '}//END_IF_INVENTORY\n'
#      elif(self.bloque.tipoBloque == 'cond_step_on_by'):
#        self.strCode = '}//END_IF_STEP_ON_BY\n'
#      elif(self.bloque.tipoBloque == 'cond_step_off_by'):
#        self.strCode = '}//END_IF_STEP_OFF_BY\n'
      if(self.bloque.tipoBloque in ['cond_flags', 'cond_hand', 'cond_inventory', 'cond_step_on_by', 'cond_step_off_by']):
        self.strCode = '}//END_IF\n'

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
    if(str(self.nro) in mystic.dictionary.keys()):

      # agarro el char (o par de chars)
      char = mystic.dictionary.decodeByte(self.nro, True)

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
      self.strCode = 'await script {:04x}\n'.format(arg)
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


    # TEXT MODE
    elif(self.nro == 0x04):
      # pasamos a text mode
#      self.strCode = '<TEXT_MODE_ON>'
#      self.strCode = 'text("<TEXT_MODE_ON>'
      self.strCode = 'await text("'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

      textMode = True


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

        self.strCode = 'if(cond_flags([' + strConds + '])) {\n'
        bloque = Script(self.addr + len(conds) + 3, 'cond_flags')
      elif(self.nro == 0x09):
#        strConds = mystic.util.strHexa(conds)
        # condición sobre lo que tengo en la mano?
        self.strCode = 'if(cond_hand([' + strConds + '])) {\n'
        bloque = Script(self.addr + len(conds) + 3, 'cond_hand')
      elif(self.nro == 0x0a):
#        strConds = mystic.util.strHexa(conds)
        self.strCode = 'if(cond_inventory([' + strConds + '])) {\n'
        bloque = Script(self.addr + len(conds) + 3, 'cond_inventory')
      elif(self.nro == 0x0b):
#        strConds = mystic.util.strHexa(conds)
        # list of possible arguments (joined by 'or')  
        # c9 = hero
        # c1 = moogled_hero?
        # f1 = chocobot_over_land
        # f5 = chocobot_over_water
        # a9 = empty_chest or snowman
        # 91 = idk, npc following the hero? enemy?
        self.strCode = 'if(cond_step_on_by([' + strConds + '])) {\n'
        bloque = Script(self.addr + len(conds) + 3, 'cond_step_on_by')

      elif(self.nro == 0x0c):
#        strConds = mystic.util.strHexa(conds)
        self.strCode = 'if(cond_step_off_by([' + strConds + '])) {\n' 
        bloque = Script(self.addr + len(conds) + 3, 'cond_step_off_by')

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


    # maybe this is only for text mode and we should delete it from here?
    elif(self.nro == 0x12):
      self.strCode = 'PAUSE'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


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

        self.strCode = 'await ' + strCmd + '();\n'
        self.size = 1
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

      elif(strAction in ['Teleport']):

        xx = self.array[1]
        yy = self.array[2]

        # cambia las coordenadas del extra dentro del bloque actual
#        self.strCode = strCmd + ' (XX,YY) = ({:02x}, {:02x})\n'.format(xx,yy)
        self.strCode = 'await ' + strCmd + '(xx=0x{:02x}, yy=0x{:02x});\n'.format(xx,yy)
        self.size = 3
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

    # es el extra especial (partner)
    elif(self.nro >= 0x90 and self.nro <= 0x9f):

      primer = self.nro // 0x10
      segund = self.nro % 0x10

      actions = ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'Teleport', 'WalkFastSpeed', 'WalkNormalSpeed', 'SetPersonaje', 'NoseD', 'NoseE', 'NoseF' ]

      # PARTNER
      strExtra = 'partner'
      strAction = actions[segund]
      strCmd = strExtra + strAction

      if(strAction in ['StepForward', 'StepBack', 'StepLeft', 'StepRight', 'LookNorth', 'LookSouth', 'LookEast', 'LookWest', 'Remove', 'WalkFastSpeed', 'WalkNormalSpeed', 'NoseD', 'NoseE', 'NoseF']):

        self.strCode = 'await ' + strCmd + '();\n'
        self.size = 1
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

      elif(strAction in ['Teleport']):

        xx = self.array[1]
        yy = self.array[2]

        # cambia las coordenadas del extra dentro del bloque actual
#        self.strCode = strCmd + ' (XX,YY) = ({:02x}, {:02x})\n'.format(xx,yy)
        self.strCode = 'await ' + strCmd + '(xx=0x{:02x}, yy=0x{:02x});\n'.format(xx,yy)
        self.size = 3
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

      elif(strAction in ['SetPersonaje']):

        arg = self.array[1]
        # turn extra1 into extra9 (extraspecial)
        self.strCode = 'await ' + strCmd + '(0x{:02x});\n'.format(arg)
        self.size = 2
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0x8b):
      # it makes the hero make a small jump (the arg is unknown)
      arg = self.array[1]
#      self.strCode = 'HOP_JUMP {:02x}\n'.format(arg)
      self.strCode = 'await hopJump(0x{:02x});\n'.format(arg)
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

        self.strCode = 'await ' + strCmd + '();\n'
        self.size = 1
        self.strHex = mystic.util.strHexa(self.array[0:self.size])

      elif(strAction in ['Teleport']):

        xx = self.array[1]
        yy = self.array[2]

        # cambia las coordenadas del extra dentro del bloque actual
#        self.strCode = strCmd + ' (XX,YY) = ({:02x}, {:02x})\n'.format(xx,yy)
        self.strCode = 'await ' + strCmd + '(xx=0x{:02x}, yy=0x{:02x});\n'.format(xx,yy)
        self.size = 3
        self.strHex = mystic.util.strHexa(self.array[0:self.size])



    elif(self.nro == 0xa0):
#      self.strCode = 'WALKING_AS_CHOCOBO\n'
      self.strCode = 'await walkingAsChocobo();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa1):
#      self.strCode = 'WALKING_AS_CHOCOBOT_LAND\n'
      self.strCode = 'await walkingAsChocobotLand();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa2):
#      self.strCode = 'WALKING_AS_CHOCOBOT_WATER\n'
      self.strCode = 'await walkingAsChocobotWater();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa3):
#      self.strCode = 'WALKING_AS_TROLLEY_WAGON\n'
      self.strCode = 'await walkingAsWagon();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa4):
#      self.strCode = 'WALKING_AS_NORMAL\n'
      self.strCode = 'await walkingAsNormal();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa5):
#      self.strCode = 'WALKING_AS_FALLING\n'
      self.strCode = 'await walkingAsFalling();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xa6):
#      self.strCode = 'WALKING_AS_DEAD\n'
      self.strCode = 'await walkingAsDead();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xa9):
      # Sets flag 0x7f to false if current map is 0x01, 0x0e, or 0x0f. Sets to true otherwise.
#      self.strCode = 'CHECK_IF_CURRENT_MAP_HAS_SMALLMAP\n'
      self.strCode = 'await checkIfCurrentMapHasMiniMap();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xab):
#      self.strCode = 'CLEAR_MATO_TODOS\n'
      self.strCode = 'await clearKilledAllRoom();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xac):
#      self.strCode = 'SMALLMAP_OPEN\n'
      self.strCode = 'await miniMapOpen();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xad):
#      self.strCode = 'SMALLMAP_IDLE\n'
      self.strCode = 'await miniMapIdle();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xae):
#      self.strCode = 'SMALLMAP_CLOSE\n'
      self.strCode = 'await miniMapClose();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xaf):
#      self.strCode = 'OPEN_CHEST\n'
      self.strCode = 'await openChest();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    elif(self.nro == 0xb0):
      nn = self.array[1]
      xx = self.array[2]
      yy = self.array[3]

      # cambia el sprite de fondo por el indicado en NN, en las coordenadas XX,YY del bloque actual
#      self.strCode = 'SPRITE (NN,XX,YY) = (' + strNn + ',' + strXx + ',' + strYy + ')\n'
      self.strCode = 'await drawSprite(nn=0x{:02x}, xx=0x{:02x}, yy=0x{:02x});\n'.format(nn,xx,yy)
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
      self.strCode = 'await attackEffect(tt=0x{:02x}, xx=0x{:02x}, yy=0x{:02x});\n'.format(tipo, xx, yy)
      self.size = 4
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xb6):
#      self.strCode = 'LETTERBOX_EFFECT\n'
      self.strCode = 'await letterboxEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xbc):
      # fades in from both fade_out and wash_out
#      self.strCode = 'FADE_IN\n'
      self.strCode = 'await fadeInEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xbd):
      # fades to black screen
#      self.strCode = 'FADE_OUT\n'
      self.strCode = 'await fadeOutEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xbe):
      # fades to white screen
#      self.strCode = 'WASH_OUT\n'
      self.strCode = 'await washOutEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xbf):
#      self.strCode = 'PARPADEO\n'
      self.strCode = 'await eyeblinkEffect();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    elif(self.nro == 0xc0):
#      self.strCode = 'RECOVER_HP\n'
      self.strCode = 'await recoverHp();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc1):
#      self.strCode = 'RECOVER_MP\n'
      self.strCode = 'await recoverMp();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc2):
      arg = self.array[1]
#      self.strCode = 'HEAL_DISEASE {:02x}\n'.format(arg)
      self.strCode = 'await healDisease(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc3):
      # it's a NOP, it does nothing.  unused in the original script
#      self.strCode = 'PASS\n'
      self.strCode = 'await nop();\n'
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
      self.strCode = 'await disease(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc5):
      # stores arg as a 6-bit integer into flags 72..77 in reverse order: 0x01 = flag 77, 0x20 = flag 72
      arg = self.array[1]
#      self.strCode = 'SET_FLAGS_72_TO_77 {:02x}\n'.format(arg)
      self.strCode = 'await setFlags72To77(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc6):
#      self.strCode = 'INPUT_NAMES_SUMO_FUJI\n'
      self.strCode = 'await inputNames();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc7):
#      self.strCode = 'RANDOMIZE_7E7F\n'
      self.strCode = 'await randomize7E7F();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc8):
#      self.strCode = 'RESET_GAME\n'
      self.strCode = 'await resetGame();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xc9):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg1*0x100 + arg2
#      self.strCode = 'SET_CHEST1_SCRIPT {:04x}\n'.format(arg)
      self.strCode = 'await setChest1Script(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xca):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg1*0x100 + arg2
#      self.strCode = 'SET_CHEST2_SCRIPT {:04x}\n'.format(arg)
      self.strCode = 'await setChest2Script(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xcb):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg1*0x100 + arg2
#      self.strCode = 'SET_CHEST3_SCRIPT {:04x}\n'.format(arg)
      self.strCode = 'await setChest3Script(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])




    elif(self.nro == 0xcc):
      # stops listening to key inputs
#      self.strCode = 'INPUT_STOP\n'
      self.strCode = 'await stopInput();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xd0):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg2*0x100 + arg1
#      self.strCode = 'INCREASE_GOLD {:02x} {:02x}\n'.format(arg1,arg2)
      self.strCode = 'await increaseGold(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd1):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg2*0x100 + arg1
#      self.strCode = 'DECREASE_GOLD {:02x} {:02x}\n'.format(arg1,arg2)
      self.strCode = 'await decreaseGold(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xd2):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg2*0x100 + arg1
#      self.strCode = 'INCREASE_EXP {:02x} {:02x}\n'.format(arg1,arg2)
      self.strCode = 'await increaseExp(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd3):
      arg1 = self.array[1]
      arg2 = self.array[2]
      arg = arg2*0x100 + arg1
#      self.strCode = 'DECREASE_EXP {:02x} {:02x}\n'.format(arg1,arg2)
      self.strCode = 'await decreaseExp(0x{:04x});\n'.format(arg)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xd4):
      arg = self.array[1]
#      self.strCode = 'PICK_ITEM {:02x}\n'.format(arg)
      self.strCode = 'await pickItem(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd5):
      arg = self.array[1]
#      self.strCode = 'DROP_ITEM {:02x}\n'.format(arg)
      self.strCode = 'await dropItem(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd6):
      arg = self.array[1]
#      self.strCode = 'PICK_MAGIC {:02x}\n'.format(arg)
      self.strCode = 'await pickMagic(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd7):
      arg = self.array[1]
#      self.strCode = 'DROP_MAGIC {:02x}\n'.format(arg)
      self.strCode = 'await dropMagic(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd8):
      arg = self.array[1]
#      self.strCode = 'PICK_WEAPON {:02x}\n'.format(arg)
      self.strCode = 'await pickWeapon(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xd9):
      arg = self.array[1]
#      self.strCode = 'DROP_WEAPON {:02x}\n'.format(arg)
      self.strCode = 'await dropWeapon(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xda):
      arg = self.array[1]
      label = mystic.variables.getLabel(arg)
#      self.strCode = 'FLAG_ON ' + label + '\n'
      self.strCode = 'await flagOn(' + label + ');\n'
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xdb):
      arg = self.array[1]
      label = mystic.variables.getLabel(arg)
#      self.strCode = 'FLAG_OFF ' + label + '\n'
      self.strCode = 'await flagOff(' + label + ');\n'
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xdc):
#      self.strCode = 'TEXT_SPEED_LOCK\n'
      self.strCode = 'await textSpeedLock();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xdd):
#      self.strCode = 'TEXT_SPEED_UNLOCK\n'
      self.strCode = 'await textSpeedUnlock();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    elif(self.nro == 0xde):
#      self.strCode = 'CONSUME_ITEM_AT_HAND\n'
      self.strCode = 'await consumeItem();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
 

    elif(self.nro == 0xe0):
#      self.strCode = 'OPEN_DOOR_NORTH\n'
      self.strCode = 'await openDoorNorth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe1):
#      self.strCode = 'CLOSE_DOOR_NORTH\n'
      self.strCode = 'await closeDoorNorth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe2):
#      self.strCode = 'OPEN_DOOR_SOUTH\n'
      self.strCode = 'await openDoorSouth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe3):
#      self.strCode = 'CLOSE_DOOR_SOUTH\n'
      self.strCode = 'await closeDoorSouth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe4):
#      self.strCode = 'OPEN_DOOR_EAST\n'
      self.strCode = 'await openDoorEast();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe5):
#      self.strCode = 'CLOSE_DOOR_EAST\n'
      self.strCode = 'await closeDoorEast();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe6):
#      self.strCode = 'OPEN_DOOR_WEST\n'
      self.strCode = 'await openDoorWest();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe7):
#      self.strCode = 'CLOSE_DOOR_WEST\n'
      self.strCode = 'await closeDoorWest();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xe8):
      # la pantalla hace scroll al bloque hacia abajo
#      self.strCode = 'SCROLL_ABAJO\n'
      self.strCode = 'await scrollSouth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xe9):
      # la pantalla hace scroll al bloque hacia arriba
#      self.strCode = 'SCROLL_ARRIBA\n'
      self.strCode = 'await scrollNorth();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xea):
      # la pantalla hace scroll al bloque de la izquierda
#      self.strCode = 'SCROLL_IZQUIERDA\n'
      self.strCode = 'await scrollLeft();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])
    elif(self.nro == 0xeb):
      # la pantalla hace scroll al bloque de la derecha
#      self.strCode = 'SCROLL_DERECHA\n'
      self.strCode = 'await scrollRight();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xec):
      # salta al script que se ejecuta al entrar a dicho bloque?
#      self.strCode = 'SCRIPT_ENTRAR_BLOQUE\n'
      self.strCode = 'await enterRoomScript();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xed):
      # salta al script que se ejecuta al salir de dicho bloque
#      self.strCode = 'SCRIPT_SALIR_BLOQUE\n'
      self.strCode = 'await exitRoomScript();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xee):
      # salta al script que se ejecuta al matar todos los enemigos del bloque
#      self.strCode = 'SCRIPT_MATOTODOS_BLOQUE\n'
      self.strCode = 'await killedAllRoomScript();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


    elif(self.nro in [0xef]):
#      print(mystic.util.strHexa(self.array[:min(20,len(self.array))]))
      xx = self.array[1]
      yy = self.array[2]
#      self.strCode = 'PROXIMO_BLOQUE (XX,YY) = ({:02x},{:02x})\n'.format(xx,yy)
      self.strCode = 'await nextRoom(xx=0x{:02x}, yy=0x{:02x});\n'.format(xx,yy)
      self.size = 3
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf0):
      arg = self.array[1]
#      self.strCode = 'SLEEP {:02x}\n'.format(arg)
      self.strCode = 'await sleep(0x{:02x});\n'.format(arg)
      self.size = 2
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
      self.strCode = 'await teleport2(mm=0x' + strMm + ', bb=0x' + strBb + ', xx=0x' + strXx + ', yy=0x' + strYy + ');\n'
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
      self.strCode = 'await teleport(mm=0x' + strMm + ', bb=0x' + strBb + ', xx=0x' + strXx + ', yy=0x' + strYy + ');\n'
      self.size = 5
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf6):
      # validos: del 0x00 al 0x10 inclusive
      arg = self.array[1]
#      self.strCode = 'VENDEDOR {:02x}\n'.format(arg)
      self.strCode = 'await salesman(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf8):
      # indico como mapea con el número de canción del banco 0x0f (0x00 = mute, 0x01 = intro song, ... 0x1e = ill (last song))
      arg = self.array[1]
      label = mystic.variables.getLabelSong(arg)
#      self.strCode = 'MUSIC {:02x}\n'.format(arg)
#      self.strCode = 'music(0x{:02x});\n'.format(arg)
#      self.strCode = 'music(' + label + ');\n'
      self.strCode = 'await music(' + label + ');\n'
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xf9):
      arg = self.array[1]
      label = mystic.variables.getLabelSFX(arg)
#      self.strCode = 'SOUND_EFFECT {:02x}\n'.format(arg)
#      self.strCode = 'soundEffect(0x{:02x});\n'.format(arg)
      self.strCode = 'await soundEffect(' + label + ');\n'
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xfb):
      # la pantalla hace scroll al bloque de la derecha
#      self.strCode = 'SCREEN_SHAKE\n'
      self.strCode = 'await shakeScreen();\n'
      self.size = 1
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xfc):
      arg = self.array[1]
#      self.strCode = 'LOAD_GRUPO_PERSONAJE {:02x}\n'.format(arg)
      self.strCode = 'await loadGrupoPersonaje(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xfd):
      arg = self.array[1]
#      self.strCode = 'ADD_PERSONAJE {:02x}\n'.format(arg)
      self.strCode = 'await addPersonaje(0x{:02x});\n'.format(arg)
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])

    elif(self.nro == 0xfe):
      arg = self.array[1]
      label = mystic.variables.getLabelBoss(arg)
#      self.strCode = 'ADD_MONSTRUO_GRANDE {:02x}\n'.format(arg)
#      self.strCode = 'ADD_MONSTRUO_GRANDE ' + label + '\n'
      self.strCode = 'await addBoss(' + label + ');\n'
      self.size = 2
      self.strHex = mystic.util.strHexa(self.array[0:self.size])


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


    elif(line.startswith('await script')):

      argTxt = line[len('await script')+1:]
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
      if(line.startswith('if(cond_flags([')):
        self.hexs.append(0x08)

        args = []
        for strArg in argsTxt:
          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'cond_flags')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

#      elif(line.startswith('IF_HAND(')):
      elif(line.startswith('if(cond_hand([')):
        self.hexs.append(0x09)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'cond_hand')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

#      elif(line.startswith('IF_INVENTORY(')):
      elif(line.startswith('if(cond_inventory([')):
        self.hexs.append(0x0a)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'cond_inventory')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

#      elif(line.startswith('IF_TRIGGERED_ON_BY(')):
      elif(line.startswith('if(cond_step_on_by([')):
        self.hexs.append(0x0b)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'cond_step_on_by')
        bloque.decodeTxt(bloqueLines)
        self.script = bloque

#      elif(line.startswith('IF_TRIGGERED_OFF_BY(')):
      elif(line.startswith('if(cond_step_off_by([')):
        self.hexs.append(0x0c)

        args = []
        for strArg in argsTxt:
#          print('strArg: ' + strArg)
          arg = int(strArg, 16)
#          arg = mystic.variables.getVal(strArg)
#          print('arg: {:02x}'.format(arg))
          args.append(arg)

        bloque = Script(self.addr + len(args) + 3, 'cond_step_off_by')
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
    elif(line.startswith('await hopJump(')):
      idx0 = len('await hopJump(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0x8b)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('await hero')):
      idx = line.index('(')
      strAction = line[len('await hero'):idx]
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

    elif(line.startswith('await partner')):

      idx = line.index('(')
      strAction = line[len('await partner'):idx]
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


    elif(line.startswith('await extra')):

      idx = line.index('(')
      strAction = line[len('await extra')+1:idx]
#      print('strAction: ' + strAction)

      nroExtra = int(line[len('await extra')])
#      print('nroExtra: ' + str(nroExtra))
 
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
    elif(line.startswith('await walkingAsChocobo(')):
      self.hexs.append(0xa0)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_CHOCOBOT_LAND')):
    elif(line.startswith('await walkingAsChocobotLand(')):
      self.hexs.append(0xa1)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_CHOCOBOT_WATER')):
    elif(line.startswith('await walkingAsChocobotWater(')):
      self.hexs.append(0xa2)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_TROLLEY_WAGON')):
    elif(line.startswith('await walkingAsWagon(')):
      self.hexs.append(0xa3)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_NORMAL')):
    elif(line.startswith('await walkingAsNormal(')):
      self.hexs.append(0xa4)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_FALLING')):
    elif(line.startswith('await walkingAsFalling(')):
      self.hexs.append(0xa5)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WALKING_AS_DEAD')):
    elif(line.startswith('await walkingAsDead(')):
      self.hexs.append(0xa6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('CHECK_IF_CURRENT_MAP_HAS_SMALLMAP')):
    elif(line.startswith('await checkIfCurrentMapHasMiniMap(')):
      self.hexs.append(0xa9)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('CLEAR_MATO_TODOS')):
    elif(line.startswith('await clearKilledAllRoom(')):
      self.hexs.append(0xab)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SMALLMAP_OPEN')):
    elif(line.startswith('await miniMapOpen(')):
      self.hexs.append(0xac)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SMALLMAP_IDLE')):
    elif(line.startswith('await miniMapIdle(')):
      self.hexs.append(0xad)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SMALLMAP_CLOSE')):
    elif(line.startswith('await miniMapClose(')):
      self.hexs.append(0xae)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('OPEN_CHEST')):
    elif(line.startswith('await openChest(')):
      self.hexs.append(0xaf)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('await drawSprite(')):

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

    elif(line.startswith('await attackEffect(')):

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
    elif(line.startswith('await letterboxEffect(')):
      self.hexs.append(0xb6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('FADE_IN')):
    elif(line.startswith('await fadeInEffect(')):
      self.hexs.append(0xbc)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('FADE_OUT')):
    elif(line.startswith('await fadeOutEffect(')):
      self.hexs.append(0xbd)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('WASH_OUT')):
    elif(line.startswith('await washOutEffect(')):
      self.hexs.append(0xbe)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('PARPADEO')):
    elif(line.startswith('await eyeblinkEffect(')):
      self.hexs.append(0xbf)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('RECOVER_HP')):
    elif(line.startswith('await recoverHp(')):
      self.hexs.append(0xc0)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('RECOVER_MP')):
    elif(line.startswith('await recoverMp(')):
      self.hexs.append(0xc1)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('HEAL_DISEASE')):
    elif(line.startswith('await healDisease(')):
      idx0 = len('await healDisease(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xc2)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('PASS')):
    elif(line.startswith('await nop(')):
      self.hexs.append(0xc3)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('DISEASE')):
    elif(line.startswith('await disease(')):
      idx0 = len('await disease(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xc4)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SET_FLAGS_72_TO_77')):
    elif(line.startswith('await setFlags72To77(')):
      idx0 = len('await setFlags72To77(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xc5)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('INPUT_NAMES_SUMO_FUJI')):
    elif(line.startswith('await inputNames();')):
      self.hexs.append(0xc6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('RANDOMIZE_7E7F')):
    elif(line.startswith('await randomize7E7F(')):
      self.hexs.append(0xc7)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('RESET_GAME')):
    elif(line.startswith('await resetGame();')):
      self.hexs.append(0xc8)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SET_CHEST1_SCRIPT')):
    elif(line.startswith('await setChest1Script(')):
#      argTxt = line[len('SET_CHEST1_SCRIPT')+1:]
#      strArg1 = argTxt[0:2]
#      strArg2 = argTxt[2:4]
#      arg1 = int(strArg1, 16)
#      arg2 = int(strArg2, 16)

      idx = len('await setChest1Script(0x')
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
    elif(line.startswith('await setChest2Script(')):
      idx = len('await setChest2Script(0x')
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
    elif(line.startswith('await setChest3Script(')):

      idx = len('await setChest3Script(0x')
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
    elif(line.startswith('await stopInput(')):
      self.hexs.append(0xcc)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('INCREASE_GOLD')):
    elif(line.startswith('await increaseGold(')):
      idx = len('await increaseGold(0x')
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
    elif(line.startswith('await decreaseGold(')):
      idx = len('await decreaseGold(0x')
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
    elif(line.startswith('await increaseExp(')):
      idx = len('await increaseExp(0x')
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
    elif(line.startswith('await decreaseExp(')):
      idx = len('await increaseExp(0x')
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
    elif(line.startswith('await pickItem(')):
      idx0 = len('await pickItem(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd4)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('DROP_ITEM')):
    elif(line.startswith('await dropItem(')):
      idx0 = len('await dropItem(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd5)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('PICK_MAGIC')):
    elif(line.startswith('await pickMagic(')):
      idx0 = len('await pickMagic(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd6)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('DROP_MAGIC')):
    elif(line.startswith('await dropMagic(')):
      idx0 = len('await dropMagic(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd7)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('PICK_WEAPON')):
    elif(line.startswith('await pickWeapon(')):
      idx0 = len('await pickWeapon(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd8)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('DROP_WEAPON')):
    elif(line.startswith('await dropWeapon(')):
      idx0 = len('await dropWeapon(0x')
      argTxt = line[idx0:idx0+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xd9)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('FLAG_ON')):
    elif(line.startswith('await flagOn(')):
      argTxt = line[len('await flagOn('):]
      argTxt = argTxt[:argTxt.index(')')]
      arg = mystic.variables.getVal(argTxt)

      self.hexs.append(0xda)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('FLAG_OFF')):
    elif(line.startswith('await flagOff(')):
      argTxt = line[len('await flagOff('):]
      argTxt = argTxt[:argTxt.index(')')]
      arg = mystic.variables.getVal(argTxt)

      self.hexs.append(0xdb)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('TEXT_SPEED_LOCK')):
    elif(line.startswith('await textSpeedLock(')):
      self.hexs.append(0xdc)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('TEXT_SPEED_UNLOCK')):
    elif(line.startswith('await textSpeedUnlock(')):
      self.hexs.append(0xdd)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('CONSUME_ITEM_AT_HAND')):
    elif(line.startswith('await consumeItem(')):
      self.hexs.append(0xde)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('OPEN_DOOR_NORTH')):
    elif(line.startswith('await openDoorNorth(')):
      self.hexs.append(0xe0)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('CLOSE_DOOR_NORTH')):
    elif(line.startswith('await closeDoorNorth(')):
      self.hexs.append(0xe1)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('OPEN_DOOR_SOUTH')):
    elif(line.startswith('await openDoorSouth(')):
      self.hexs.append(0xe2)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('CLOSE_DOOR_SOUTH')):
    elif(line.startswith('await closeDoorSouth(')):
      self.hexs.append(0xe3)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('OPEN_DOOR_EAST')):
    elif(line.startswith('await openDoorEast(')):
      self.hexs.append(0xe4)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('CLOSE_DOOR_EAST')):
    elif(line.startswith('await closeDoorEast(')):
      self.hexs.append(0xe5)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('OPEN_DOOR_WEST')):
    elif(line.startswith('await openDoorWest(')):
      self.hexs.append(0xe6)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('CLOSE_DOOR_WEST')):
    elif(line.startswith('await closeDoorWest(')):
      self.hexs.append(0xe7)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('SCROLL_ABAJO')):
    elif(line.startswith('await scrollSouth(')):
      self.hexs.append(0xe8)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCROLL_ARRIBA')):
    elif(line.startswith('await scrollNorth(')):
      self.hexs.append(0xe9)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCROLL_IZQUIERDA')):
    elif(line.startswith('await scrollLeft(')):
      self.hexs.append(0xea)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCROLL_DERECHA')):
    elif(line.startswith('await scrollRight(')):
      self.hexs.append(0xeb)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCRIPT_ENTRAR_BLOQUE')):
    elif(line.startswith('await enterRoomScript(')):
      self.hexs.append(0xec)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCRIPT_SALIR_BLOQUE')):
    elif(line.startswith('await exitRoomScript(')):
      self.hexs.append(0xed)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
#    elif(line.startswith('SCRIPT_MATOTODOS_BLOQUE')):
    elif(line.startswith('await killedAllRoomScript(')):
      self.hexs.append(0xee)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('SLEEP')):
    elif(line.startswith('await sleep(')):
      idx = len('await sleep(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xf0)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('PROXIMO_BLOQUE')):
    elif(line.startswith('await nextRoom(')):
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
    elif(line.startswith('await teleport')):

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
      if(not line[len('await teleport')] == '2'): 
        self.hexs.append(0xf4)
      # sino, es el teleport 2
      else:
        self.hexs.append(0xf3)

      self.hexs.extend(args)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('VENDEDOR')):
    elif(line.startswith('await salesman(')):
      idx = len('await salesman(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xf6)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


#    elif(line.startswith('MUSIC')):
    elif(line.startswith('await music(')):
      argTxt = line[len('await music('):].strip()
      argTxt = argTxt[:argTxt.index(')')]
#      print('argTxt: ' + argTxt)
#      arg = int(argTxt, 16)
      arg = mystic.variables.getValSong(argTxt)
      self.hexs.append(0xf8)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)


    elif(line.startswith('await soundEffect(')):
      argTxt = line[len('await soundEffect('):].strip()
      argTxt = argTxt[:argTxt.index(')')]
#      print('argTxt: ' + argTxt)
#      arg = int(argTxt, 16)
      arg = mystic.variables.getValSFX(argTxt)
      self.hexs.append(0xf9)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)




#    elif(line.startswith('SCREEN_SHAKE')):
    elif(line.startswith('await shakeScreen(')):
      self.hexs.append(0xfb)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

    elif(line.startswith('await loadGrupoPersonaje(')):
      idx = len('await loadGrupoPersonaje(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xfc)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)
    elif(line.startswith('await addPersonaje(')):
      idx = len('await addPersonaje(0x')
      argTxt = line[idx:idx+2]
      arg = int(argTxt, 16)
      self.hexs.append(0xfd)
      self.hexs.append(arg)
      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)

#    elif(line.startswith('ADD_MONSTRUO_GRANDE')):
    elif(line.startswith('await addBoss(')):
      argTxt = line[len('await addBoss('):].strip()
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
    elif(line.startswith('await text(')):
      # indico que es en modo texto
      self.textMode = True

#      print('LINE: ' + line)

      # remove the javascript text
      line = line.replace('await text("', '')
      line = line.replace('");', '')
      # add the text opening and ending codes (needed for detecting jp non-compressable word exceptions)
      line = '[04]' + line + '[00]'

      self.hexs = []
#      self.hexs.append(0x04)
      # get the compressed bytes
      values = mystic.dictionary.tryCompress(line, True)
      self.hexs.extend(values)
#      self.hexs.append(0x00)

      self.sizeLines = 1
      self.sizeBytes = len(self.hexs)




  def __str__(self):
#    return self.strCode + ' | ' + self.strHex
    return self.strCode
#    return '\n{:04x} '.format(self.addr) + self.strCode
#    return '(' + self.strHex + ')' + self.strCode 




