import mystic.address

# dictionary with compression
dictCompress = {}
# dictionary without compression
dictNoCompress = {}

#listCharsCmds = ['·','·','·','·','·','·','·','·','·','·','·','·','·','·','·','·',
#listCharsCmds = ['[00]','[01]','[02]','[03]','[04]','[05]','[06]','[07]','[08]','[09]','[0a]','[0b]','[0c]','[0d]','[0e]','[0f]',
#                 '[OPENWIN]','[CLOSEWIN]','[PAUSE]','[ASK_YES_NO]','[SUMO]','[FUJI]','[16]','[17]','[18]','[19]','[NEWLINE]','[CLEAR]','[RIGHT]','[LEFT]','[UP]','[DOWN]']

listCharsCmds = ['[00]','[01]','[02]','[03]','[04]','[05]','[06]','[07]','[08]','[09]','[0a]','[0b]','[0c]','[0d]','[0e]','[0f]',
                 '[openwin]','[closewin]','[pause]','[ask_yes_no]','[sumo]','[fuji]','[16]','[17]','[18]','[19]','\\n','[clear]','[right]','[left]','[up]','[down]']

listCharsSpecial = ['ℍ','ℙ','𝕄','𝕊','ℝ','𝕃','𝔼','#','(','▏','█','▎','▌','▊',')','©' ]
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

  # we start with a generic dictionary
  for i in range(0, 0x100):
    mystic.dictionary.dictCompress[str(i)] = '[{:02x}]'.format(i)
    mystic.dictionary.dictNoCompress[str(i)] = '[{:02x}]'.format(i)

  listCharsCmds = mystic.dictionary.listCharsCmds
  # seteo los comandos
  for i in range(0x00, 0x20):
    mystic.dictionary.dictCompress[str(i)] = listCharsCmds[i]
    mystic.dictionary.dictNoCompress[str(i)] = listCharsCmds[i]

  listCharsSpecial = mystic.dictionary.listCharsSpecial
  # seteo las letras especiales
  for i in range(0x70, 0x80):
    mystic.dictionary.dictCompress[str(i)] = listCharsSpecial[i-0x70]
    mystic.dictionary.dictNoCompress[str(i)] = listCharsSpecial[i-0x70]



  if(lang in [mystic.language.ENGLISH, mystic.language.ENGLISH_UK]):

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dictCompress[str(i)] = listCharsIcons[i-0xa0]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dictCompress[str(i)] = listCharsEn[i-0xb0]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsEn[i-0xb0]


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
      # las demás combinaciones si se comprimen
      mystic.dictionary.dictCompress[str(index)] = chary


  elif(lang == mystic.language.FRENCH):

    listCharsDe = mystic.dictionary.listCharsDe
    # seteo las letras especiales deutsch
    for i in range(0x90, 0xa0):
      mystic.dictionary.dictCompress[str(i)] = listCharsDe[i-0x90]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsDe[i-0x90]

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dictCompress[str(i)] = listCharsIcons[i-0xa0]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dictCompress[str(i)] = listCharsEn[i-0xb0]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsEn[i-0xb0]

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
      mystic.dictionary.dictCompress[str(index)] = chary

  elif(lang == mystic.language.GERMAN):

    listCharsDe = mystic.dictionary.listCharsDe
    # seteo las letras especiales deutsch
    for i in range(0x90, 0xa0):
      mystic.dictionary.dictCompress[str(i)] = listCharsDe[i-0x90]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsDe[i-0x90]

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dictCompress[str(i)] = listCharsIcons[i-0xa0]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dictCompress[str(i)] = listCharsEn[i-0xb0]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsEn[i-0xb0]

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
      mystic.dictionary.dictCompress[str(index)] = chary

  elif(lang == mystic.language.JAPAN):

    listCharsJpLow = mystic.dictionary.listCharsJpLow
    # seteo las letras con dakuten
    for i in range(0x40, 0x70):
      mystic.dictionary.dictCompress[str(i)] = listCharsJpLow[i-0x40]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsJpLow[i-0x40]

    listCharsJp = mystic.dictionary.listCharsJp
    # seteo las letras normales
    for i in range(0x80, 0x100):
      mystic.dictionary.dictCompress[str(i)] = listCharsJp[i-0x80]
      mystic.dictionary.dictNoCompress[str(i)] = listCharsJp[i-0x80]

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
        mystic.dictionary.dictCompress[str(cont)] = string
#        print('dictu {:02x} '.format(cont) + string)
        cont +=1
        string = ''
      else:
        chary = mystic.dictionary.decodeByte(val, True)
        string += chary


def decodeByte(byte, compress):
  """ decodes a byte.  If not 'compress' then it does not 'decompress' non-control codes """

  char = '·'

  # we get the dictionary (with or without full compression)

  if(compress):
    dictio = mystic.dictionary.dictCompress
  else:
    dictio = mystic.dictionary.dictNoCompress

  strByte = str(byte)
  if(strByte in dictio.keys()):
    char = dictio[strByte]

  return char


def decodeArray(array, compress):
  string = ''
  for hexa in array:
    char = mystic.dictionary.decodeByte(hexa, compress)
    string += char
  return string

def keys(compress):

  if(compress):
    dictio = mystic.dictionary.dictCompress
  else:
    dictio = mystic.dictionary.dictNoCompress

  keys = dictio.keys()
  return keys

def chars(compress):

  if(compress):
    dictio = mystic.dictionary.dictCompress
  else:
    dictio = mystic.dictionary.dictNoCompress

  """ retorna lista de los chars disponibles en el dicconario """
  # invierto el diccionario
  invDict = {v: k for k, v in dictio.items()}
  # los chars son las keys del diccionario invertido
  chars = invDict.keys()
  # los retorno
  return chars
 

def encodeChars(chars, compress):
  """ codifica un char, o un par de chars """

#  print('tyring to invert: ' + chars)

  if(compress):
    dictio = mystic.dictionary.dictCompress
  else:
    dictio = mystic.dictionary.dictNoCompress

  # invierto el diccionario
  invDict = {v: k for k, v in dictio.items()}
  # busco en el diccionario invertido
  strVal = invDict[chars]

#  print('invierte: ' + chars + ' resultado: ' + strVal)
  val = int(strVal)

  # retorno lo encontrado
  return val


def tryCompress(string, compress):
  """ it compress a string.  If 'compress' then it uses compression """

#  print('trying to full=' + str(full) + ' compress: ' + string)

  values = []
  while(len(string)>0):
    val = mystic.dictionary.tryCompressWord(string, compress)
#    print('tenemos val: {:02x} para string '.format(val) + string)

    # if it could compress
    if(val != -1):
      values.append(val)
      palabra = mystic.dictionary.decodeByte(val, compress)
      string = string[len(palabra):]

    # else, it couldn't compress
    else:
      char = string[0]

      # codifico el primer char
      val = mystic.dictionary.encodeChars(char, compress)
      values.append(val)

      string = string[1:]
#      print('queda string: ' + string)

  return values


def tryCompressWord(string, compress):
  """ it tries to compress a string word.  If 'compress' then it uses compression """

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
  jpExceptions = ['ている[pause][closewin][00]', 'どうくつが あるよ', 'てにいれたら', 'ているのですか?', 'わたしておくわ!', 'ている\\nマナのひみつに', 'ている[pause][clear]ふたたび', 'ているじゃろう', 'ているんですが…', 'ているらしい[pause][clear]おくの', 'アマンダ「やっぱり', 'わたしのしゅじん', 'わたし おいてけぼり', 'アマンダ「いっしょ', 'ちからが\\nはつ', 'マナのいちぞく[pause][clear]マナのきをま', 'マナのきをまもる', 'ている[pause][clear][00]', 'アマンダのかたきを']
  exceptions.extend(jpExceptions)


  # for each exception
  for excep in exceptions:
    # if the string starts with the exceptions
    if(string.startswith(excep)):
      # return that we can't compress it     
      return val

  # we get the dictionary (with or without full compression)
  if(compress):
    dictio = mystic.dictionary.dictCompress
  else:
    dictio = mystic.dictionary.dictNoCompress

#  print('dictio: ' + str(dictio))

  # we search over the compressed words
  for cCode in range(0,0x100):
    palabra = dictio[str(cCode)]
#    print('viendo {:02x} '.format(cCode) + palabra)

    # if the word is not empty and our string starts with this word
    if(len(palabra)>0 and string.startswith(palabra)):
      # we return the found compressed code
      val = int(cCode)
      break

  return val


def encodeRom():

  array = []

  # we invert the dictionary
  invDict = {v: k for k, v in mystic.dictionary.dictCompress.items()}

#  print('dict: ' + str(dict)) 

  codes = _getCompressedCodes()

  for code in codes:
    string = mystic.dictionary.dictCompress[str(code)]
#    print('string: ' + str(string))
    subArray = []
    for char in string:
#      print('char: ' + char)
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


def _getCompressedCodes():
  """ returns the codes of compressed strings according to the used language. """

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
    compressedCodes.extend( range(0x80,0x90) )

  elif(lang == mystic.language.JAPAN):
    # the codes of compressed strings in the dictionary
    compressedCodes.extend( range(0x20,0x40) )

  return compressedCodes


def exportJs(filepath):

  jsonDict = mystic.dictionary.dictCompress

  import json
  # for allowing kana characters in json ensure_ascii=False
  strJson = json.dumps(jsonDict, indent=2, ensure_ascii=False)
#  strJson = json.dumps(data)
  f = open(filepath, 'w', encoding="utf-8")
  f.write('textDictionary = \n' + strJson)
  f.close()

def importJs(filepath):

  # first we decode the dictionary from the rom (to have the no-compress version)
  decodeRom()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # elimino el primer renglón (no es json)
  lines.pop(0)
  data = '\n'.join(lines)

#  print('data: ' + data)

  import json
  jsonDict = json.loads(data)
#  print('jsonDict: ' + str(jsonDict))
  mystic.dictionary.dictCompress = jsonDict
#  mystic.dictionary.dictNoCompress = jsonDict

#  print('-----dictCompress: ' + str(mystic.dictionary.dictCompress))
#  print('-----dictNoCompress: ' + str(mystic.dictionary.dictNoCompress))


