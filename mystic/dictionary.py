import mystic.address


dict = {}

#listCharsCmds = ['·','·','·','·','·','·','·','·','·','·','·','·','·','·','·','·',
#listCharsCmds = ['[00]','[01]','[02]','[03]','[04]','[05]','[06]','[07]','[08]','[09]','[0a]','[0b]','[0c]','[0d]','[0e]','[0f]',
#                 '[OPENWIN]','[CLOSEWIN]','[PAUSE]','[ASK_YES_NO]','[SUMO]','[FUJI]','[16]','[17]','[18]','[19]','[NEWLINE]','[CLEAR]','[RIGHT]','[LEFT]','[UP]','[DOWN]']

listCharsCmds = ['[00]','[01]','[02]','[03]','[04]','[05]','[06]','[07]','[08]','[09]','[0a]','[0b]','[0c]','[0d]','[0e]','[0f]',
                 '[openwin]','[closewin]','[pause]','[ask_yes_no]','[sumo]','[fuji]','[16]','[17]','[18]','[19]','\\n','[clear]','[right]','[left]','[up]','[down]']

listCharsSpecial = ['ℍ','ℙ','𝕄','𝕊','ℝ','𝕃','𝔼','/','[','▏','█','▎','▌','▊',']','©' ]
#listCharsIcons = ['🛡️','🎩','👕','🡔','🗡️','🪓','🔨','💣','🔗','💧','🔑','🍬','⛏️','💰','💎','🔮']
listCharsIcons = ['⛨','🎩','👕','🡔','🗡','🪓','🔨','💣','🔗','💧','🔑','🍬','𐇞','💰','💎','🔮']
listCharsDe = [ '[90]','[91]','[92]','[93]','[94]','[95]','[96]','[97]','[98]',"Ä","Ö","Ü","ä","ö","ü","ß" ]

listCharsEn = [
              '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',
              'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
              'W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l',
              'm','n','o','p','q','r','s','t','u','v','w','x','y','z',"'",",",
              ".","…",'-','!','?',':','/',"┌","─","┐","├","┤","└","┴","┘",' ']
# 0x40 empieza dakuten en か
listCharsJpLow = [
              'が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど','ば',
              'び','ぶ','べ','ぼ','ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ',
              'ヅ','デ','ド','バ','ビ','ブ','ボ','ぱ','ぴ','ぷ','ぺ','ぽ','パ','ピ','プ','ポ' ]
listCharsJp = [
              '0','1','2','3','4','5','6','7','8','9','あ','い','う','え','お','か',
              'き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','な','に',
              'ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','や','ゆ','よ',
              'ら','り','る','れ','ろ','わ','を','ん','っ','ゃ','ゅ','ょ','ア','イ','ウ','エ',
              'オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト',
              'ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','…','ホ','マ','ミ','ム','メ','モ','ヤ',
              'ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','「','ン','ァ','ィ','ッ','ャ','ュ','ョ',
              "゛","゜",'-','!','?','ェ','ォ',"┌","─","┐","├","┤","└","┴","┘",' ']


def decodeRom():

  lang = mystic.address.language

  for i in range(0, 0x100):
    mystic.dictionary.dict[str(i)] = '[{:02x}]'.format(i)


  if(lang in [mystic.language.ENGLISH, mystic.language.ENGLISH_UK]):

    listCharsCmds = mystic.dictionary.listCharsCmds
    # seteo los comandos
    for i in range(0x00, 0x20):
      mystic.dictionary.dict[str(i)] = listCharsCmds[i]

    listCharsSpecial = mystic.dictionary.listCharsSpecial
    # seteo las letras especiales
    for i in range(0x70, 0x80):
      mystic.dictionary.dict[str(i)] = listCharsSpecial[i-0x70]

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dict[str(i)] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dict[str(i)] = listCharsEn[i-0xb0]

    # cargo el banco 0
    nroBank,addr = mystic.address.addrDictionary
    cant = mystic.address.cantDictionary
    bank0 = mystic.romSplitter.banks[nroBank]

    for i in range(0,cant):
      # agarro el valor
      val0 = bank0[addr+2*i]
      val1 = bank0[addr+2*i+1]
      char0 = mystic.dictionary.decodeByte(val0, True)
      char1 = mystic.dictionary.decodeByte(val1, True)
      chary = char0 + char1
      index = 0x20+i
      # se saltea el renglón 0x70 (especiales)
      if(index >= 0x70):
        index += 0x10
      # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
      if(chary != '..' and chary != 'LA'):
        # las demás combinaciones si se comprimen
        mystic.dictionary.dict[str(index)] = chary


  elif(lang == mystic.language.FRENCH):

    listCharsCmds = mystic.dictionary.listCharsCmds
    # seteo los comandos
    for i in range(0x00, 0x20):
      mystic.dictionary.dict[str(i)] = listCharsCmds[i]

    listCharsSpecial = mystic.dictionary.listCharsSpecial
    # seteo las letras especiales
    for i in range(0x70, 0x80):
      mystic.dictionary.dict[str(i)] = listCharsSpecial[i-0x70]

    listCharsDe = mystic.dictionary.listCharsDe
    # seteo las letras especiales deutsch
    for i in range(0x90, 0xa0):
      mystic.dictionary.dict[str(i)] = listCharsDe[i-0x90]

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dict[str(i)] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dict[str(i)] = listCharsEn[i-0xb0]

    # cargo el banco 0
    nroBank,addr = mystic.address.addrDictionary
    cant = mystic.address.cantDictionary
    bank0 = mystic.romSplitter.banks[nroBank]
    for i in range(0,cant):
      # agarro el valor
      val0 = bank0[addr+2*i]
      val1 = bank0[addr+2*i+1]
      char0 = mystic.dictionary.decodeByte(val0, True)
      char1 = mystic.dictionary.decodeByte(val1, True)
      chary = char0 + char1
      index = 0x20+i
      # se saltea el renglón 0x70 (especiales)
      if(index >= 0x70):
        index += 0x10
      # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
#      if(chary != '..' and chary != 'LA'):
        # las demás combinaciones si se comprimen
#        mystic.dictionary.dict[str(index)] = chary
      mystic.dictionary.dict[str(index)] = chary

  elif(lang == mystic.language.GERMAN):

    listCharsCmds = mystic.dictionary.listCharsCmds
    # seteo los comandos
    for i in range(0x00, 0x20):
      mystic.dictionary.dict[str(i)] = listCharsCmds[i]

    listCharsSpecial = mystic.dictionary.listCharsSpecial
    # seteo las letras especiales
    for i in range(0x70, 0x80):
      mystic.dictionary.dict[str(i)] = listCharsSpecial[i-0x70]

    listCharsDe = mystic.dictionary.listCharsDe
    # seteo las letras especiales deutsch
    for i in range(0x90, 0xa0):
      mystic.dictionary.dict[str(i)] = listCharsDe[i-0x90]

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dict[str(i)] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dict[str(i)] = listCharsEn[i-0xb0]

    # cargo el banco 0
    nroBank,addr = mystic.address.addrDictionary
    cant = mystic.address.cantDictionary
    bank0 = mystic.romSplitter.banks[nroBank]

    for i in range(0,cant):
      # agarro el valor
      val0 = bank0[addr+2*i]
      val1 = bank0[addr+2*i+1]
      char0 = mystic.dictionary.decodeByte(val0, True)
      char1 = mystic.dictionary.decodeByte(val1, True)
      chary = char0 + char1
      index = 0x20+i
      # se saltea el renglón 0x70 (especiales)
      if(index >= 0x70):
        index += 0x10
      # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
#      if(chary != '..' and chary != 'LA'):
        # las demás combinaciones si se comprimen
#        mystic.dictionary.dict[str(index)] = chary
      mystic.dictionary.dict[str(index)] = chary

  elif(lang == mystic.language.JAPAN):

    listCharsCmds = mystic.dictionary.listCharsCmds
    # seteo los comandos
    for i in range(0x00, 0x20):
      mystic.dictionary.dict[str(i)] = listCharsCmds[i]

    listCharsJpLow = mystic.dictionary.listCharsJpLow
    # seteo las letras con dakuten
    for i in range(0x40, 0x70):
      mystic.dictionary.dict[str(i)] = listCharsJpLow[i-0x40]

    listCharsSpecial = mystic.dictionary.listCharsSpecial
    # seteo las letras especiales
    for i in range(0x70, 0x80):
      mystic.dictionary.dict[str(i)] = listCharsSpecial[i-0x70]

    listCharsJp = mystic.dictionary.listCharsJp
    # seteo las letras normales
    for i in range(0x80, 0x100):
      mystic.dictionary.dict[str(i)] = listCharsJp[i-0x80]

    # cargo el banco 0
    dic = []
    string = ''
    nroBank,vaPorAddr = mystic.address.addrDictionary
    bank0 = mystic.romSplitter.banks[nroBank]
    cont = 0x20
    # entre 0x20 y 0x40 seteo las palabras comprimidas
    while(cont < 0x40):
      val = bank0[vaPorAddr]
      vaPorAddr += 1
      if(val == 0x00):
        mystic.dictionary.dict[str(cont)] = string
#        print('dictu {:02x} '.format(cont) + string)
        cont +=1
        string = ''
      else:
        chary = mystic.dictionary.decodeByte(val, True)
        string += chary


def decodeByte(byte, full):
  """ decodes a byte.  If not 'full' then it does not 'decompress' non-control codes """

  char = '·'

  # we get the dictionary (with or without full compression)
  dictio = mystic.dictionary.dict if full else _getNotFullDict()

  strByte = str(byte)
  if(strByte in dictio.keys()):
    char = mystic.dictionary.dict[strByte]


  return char


def decodeArray(array, full):
  string = ''
  for hexa in array:
    char = mystic.dictionary.decodeByte(hexa, full)
    string += char
  return string

def keys():

  keys = mystic.dictionary.dict.keys()
  return keys

def chars():
  """ retorna lista de los chars disponibles en el dicconario """
  # invierto el diccionario
  invDict = {v: k for k, v in mystic.dictionary.dict.items()}
  # los chars son las keys del diccionario invertido
  chars = invDict.keys()
  # los retorno
  return chars
 

def encodeChars(chars):
  """ codifica un char, o un par de chars """

#  print('tyring to invert: ' + chars)

  # invierto el diccionario
  invDict = {v: k for k, v in mystic.dictionary.dict.items()}
  # busco en el diccionario invertido
  strVal = invDict[chars]

#  print('invierte: ' + chars + ' resultado: ' + strVal)
  val = int(strVal)

  # retorno lo encontrado
  return val




def tryCompress(string, full):
  """ it compress a string.  If not 'full' then it only 'compress' the control codes """

#  print('trying to full=' + str(full) + ' compress: ' + string)

  values = []
  while(len(string)>0):
    val = mystic.dictionary.tryCompressWord(string, full)
#    print('tenemos val: {:02x} para string '.format(val) + string)

    # if it could compress
    if(val != -1):
      values.append(val)
      palabra = mystic.dictionary.decodeByte(val, full)
      string = string[len(palabra):]

    # else, it couldn't compress
    else:
      char = string[0]

      # codifico el primer char
      val = mystic.dictionary.encodeChars(char)
      values.append(val)

      string = string[1:]
#      print('queda string: ' + string)

  return values






def tryCompressWord(string, full):
  """ it tries to compress a string word.  If not 'full' then it only 'compress' the control codes """

  val = -1

#  print('trying to compress: ' + string)

  exceptions = []
  # not compressed words in deutsch
  deExceptions = ['..']
  exceptions.extend(deExceptions)
  # not compressed words in french
  frExceptions = ['LA']
  exceptions.extend(frExceptions)
  # not compressed words in japan
  jpExceptions = ['ている[PAUSE][CLOSEWIN][00]', 'どうくつが あるよ', 'てにいれたら', 'ているのですか?', 'わたしておくわ!', 'ている[NEWLINE]マナのひみつに', 'ている[PAUSE][CLEAR]ふたたび', 'ているじゃろう', 'ているんですが…', 'ているらしい[PAUSE][CLEAR]おくの', 'アマンダ「やっぱり', 'わたしのしゅじん', 'わたし おいてけぼり', 'アマンダ「いっしょ', 'ちからが[NEWLINE]はつ', 'マナのいちぞく[PAUSE][CLEAR]マナのきをま', 'マナのきをまもる', 'ている[PAUSE][CLEAR][00]', 'アマンダのかたきを']
  exceptions.extend(jpExceptions)


  # for each exception
  for excep in exceptions:
    # if the string starts with the exceptions
    if(string.startswith(excep)):
      # return that we can't compress it     
      return val

  # get the codes of the compressed words of the dictionary
  compressedCodes = _getCompressedCodesAndControlCodes()

  # we get the dictionary (with or without full compression)
  dictio = mystic.dictionary.dict if full else _getNotFullDict()

  # we search over the compressed words
  for cCode in compressedCodes:
    palabra = dictio[str(cCode)]
#    print('viendo {:02x} '.format(i) + palabra)

    # if the word is not empty and our string starts with this word
    if(len(palabra)>0 and string.startswith(palabra)):
      # we return the found compressed code
      val = int(cCode)
      break

  return val


def encodeRom():

  array = []

  compressedCodes = _getCompressedCodes(False)

  # we invert the dictionary
  invDict = {v: k for k, v in mystic.dictionary.dict.items()}

#  print('dict: ' + str(dict)) 

  for code in compressedCodes:
    string = dict[str(code)]
    subArray = []
    for char in string:
      cCode = invDict[char]
      intCode = int(cCode)
      subArray.append(intCode)


    lang = mystic.address.language
    # the jp rom ends each compressed word with 0x00
    if(lang == mystic.language.JAPAN):
      subArray.append(0x00)

#    print('code: {:02x}'.format(code) + ' string: ' + string + ' array: ' + mystic.util.strHexa(subArray))
    array.extend(subArray)
  return array


def _getCompressedCodes(extended):
  """ returns the codes of compressed strings according to the used language.
      If not extended then it returns only the ones that are burned into the rom """

  compressedCodes = []

  lang = mystic.address.language
  # first we update the singelCharStart according to the rom language
  if(lang in [mystic.language.ENGLISH, mystic.language.ENGLISH_UK]):
    # the codes of compressed strings in the dictionary
    compressedCodes.extend( range(0x20,0x70) )
    compressedCodes.extend( range(0x80,0xa0) )

  elif(lang in [mystic.language.FRENCH, mystic.language.GERMAN]):
    # the codes of compressed strings in the dictionary
    compressedCodes.extend( range(0x20,0x70) )
    if(extended):
      compressedCodes.extend( range(0x80,0x98) )
    else:
      compressedCodes.extend( range(0x80,0x90) )

  elif(lang == mystic.language.JAPAN):
    # the codes of compressed strings in the dictionary
    compressedCodes.extend( range(0x20,0x40) )

  return compressedCodes

def _getNotFullDict():
  """ returns the dictionary without compression """

  # we start with the full dict
  notFullDict = mystic.dictionary.dict
  compressedCodes = _getCompressedCodes(True)

  # we replace the compressed codes
  for code in compressedCodes:
    # with uncompressed string codes
    notFullDict[str(code)] = '[{:02x}]'.format(code)
 
  return notFullDict

def _getControlCodes():
  ctrlCodes = []

  controlCodes = range(0x00,0x20)
  ctrlCodes.extend( controlCodes )

  return ctrlCodes


def _getCompressedCodesAndControlCodes():
  codes = []

  controlCodes = _getControlCodes()
  codes.extend( controlCodes )

  compressedCodes = _getCompressedCodes(True)
  codes.extend( compressedCodes )

  return codes

