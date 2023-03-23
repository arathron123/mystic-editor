import mystic.address


dict = {}


#listCharsCmds = ['·','·','·','·','·','·','·','·','·','·','·','·','·','·','·','·',
listCharsCmds = ['<00>','<01>','<02>','<03>','<04>','<05>','<06>','<07>','<08>','<09>','<0a>','<0b>','<0c>','<0d>','<0e>','<0f>',
                 '<TEXTBOX_SHOW>','<TEXTBOX_HIDE>','<PAUSE>','<ASK_YES_NO>','<SUMO>','<FUJI>','·','·','·','·','<ENTER>','<CLS>','·','<BACKSPACE>','·','<CARRY>']
listCharsSpecial = ['ℍ','ℙ','𝕄','𝕊','ℝ','𝕃','𝔼','/','[','▏','█','▎','▌','▊',']','©' ]
listCharsDe = [ '·','·','·','·','·','·','·','·','·',"Ä","Ö","Ü","ä","ö","ü","ß" ]
#listCharsIcons = ['🛡️','🎩','👕','🡔','🗡️','🪓','🔨','💣','🔗','💧','🔑','🍬','⛏️','💰','💎','🔮']
listCharsIcons = ['⛨','🎩','👕','🡔','🗡','🪓','🔨','💣','🔗','💧','🔑','🍬','𐇞','💰','💎','🔮']


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

  if(lang in [mystic.language.ENGLISH, mystic.language.ENGLISH_UK]):

    listCharsCmds = mystic.dictionary.listCharsCmds
    # seteo los comandos
    for i in range(0x00, 0x20):
      mystic.dictionary.dict[i] = listCharsCmds[i]

    listCharsSpecial = mystic.dictionary.listCharsSpecial
    # seteo las letras especiales
    for i in range(0x70, 0x80):
      mystic.dictionary.dict[i] = listCharsSpecial[i-0x70]

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dict[i] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dict[i] = listCharsEn[i-0xb0]

    # cargo el banco 0
    nroBank,addr = mystic.address.addrDictionary
    cant = mystic.address.cantDictionary
    bank0 = mystic.romSplitter.banks[nroBank]

    for i in range(0,cant):
      # agarro el valor
      val0 = bank0[addr+2*i]
      val1 = bank0[addr+2*i+1]
      char0 = mystic.dictionary.decodeByte(val0)
      char1 = mystic.dictionary.decodeByte(val1)
      chary = char0 + char1
      index = 0x20+i
      # se saltea el renglón 0x70 (especiales)
      if(index >= 0x70):
        index += 0x10
      # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
      if(chary != '..' and chary != 'LA'):
        # las demás combinaciones si se comprimen
        mystic.dictionary.dict[index] = chary


  elif(lang == mystic.language.FRENCH):

    listCharsCmds = mystic.dictionary.listCharsCmds
    # seteo los comandos
    for i in range(0x00, 0x20):
      mystic.dictionary.dict[i] = listCharsCmds[i]

    listCharsSpecial = mystic.dictionary.listCharsSpecial
    # seteo las letras especiales
    for i in range(0x70, 0x80):
      mystic.dictionary.dict[i] = listCharsSpecial[i-0x70]

    listCharsDe = mystic.dictionary.listCharsDe
    # seteo las letras especiales deutsch
    for i in range(0x90, 0xa0):
      mystic.dictionary.dict[i] = listCharsDe[i-0x90]

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dict[i] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dict[i] = listCharsEn[i-0xb0]

    # cargo el banco 0
    nroBank,addr = mystic.address.addrDictionary
    cant = mystic.address.cantDictionary
    bank0 = mystic.romSplitter.banks[nroBank]
    for i in range(0,cant):
      # agarro el valor
      val0 = bank0[addr+2*i]
      val1 = bank0[addr+2*i+1]
      char0 = mystic.dictionary.decodeByte(val0)
      char1 = mystic.dictionary.decodeByte(val1)
      chary = char0 + char1
      index = 0x20+i
      # se saltea el renglón 0x70 (especiales)
      if(index >= 0x70):
        index += 0x10
      # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
      if(chary != '..' and chary != 'LA'):
        # las demás combinaciones si se comprimen
        mystic.dictionary.dict[index] = chary

  elif(lang == mystic.language.GERMAN):

    listCharsCmds = mystic.dictionary.listCharsCmds
    # seteo los comandos
    for i in range(0x00, 0x20):
      mystic.dictionary.dict[i] = listCharsCmds[i]

    listCharsSpecial = mystic.dictionary.listCharsSpecial
    # seteo las letras especiales
    for i in range(0x70, 0x80):
      mystic.dictionary.dict[i] = listCharsSpecial[i-0x70]

    listCharsDe = mystic.dictionary.listCharsDe
    # seteo las letras especiales deutsch
    for i in range(0x90, 0xa0):
      mystic.dictionary.dict[i] = listCharsDe[i-0x90]

    listCharsIcons = mystic.dictionary.listCharsIcons
    # seteo las letras iconos
    for i in range(0xa0, 0xb0):
      mystic.dictionary.dict[i] = listCharsIcons[i-0xa0]

    listCharsEn = mystic.dictionary.listCharsEn
    # seteo las letras normales
    for i in range(0xb0, 0x100):
      mystic.dictionary.dict[i] = listCharsEn[i-0xb0]

    # cargo el banco 0
    nroBank,addr = mystic.address.addrDictionary
    cant = mystic.address.cantDictionary
    bank0 = mystic.romSplitter.banks[nroBank]

    for i in range(0,cant):
      # agarro el valor
      val0 = bank0[addr+2*i]
      val1 = bank0[addr+2*i+1]
      char0 = mystic.dictionary.decodeByte(val0)
      char1 = mystic.dictionary.decodeByte(val1)
      chary = char0 + char1
      index = 0x20+i
      # se saltea el renglón 0x70 (especiales)
      if(index >= 0x70):
        index += 0x10
      # no permito comprimir '..' pues no lo usa en la rom deutsch, ni 'LA' pues no lo usa la rom french
      if(chary != '..' and chary != 'LA'):
        # las demás combinaciones si se comprimen
        mystic.dictionary.dict[index] = chary

  elif(lang == mystic.language.JAPAN):

    listCharsCmds = mystic.dictionary.listCharsCmds
    # seteo los comandos
    for i in range(0x00, 0x20):
      mystic.dictionary.dict[i] = listCharsCmds[i]

    listCharsJpLow = mystic.dictionary.listCharsJpLow
    # seteo las letras con dakuten
    for i in range(0x40, 0x70):
      mystic.dictionary.dict[i] = listCharsJpLow[i-0x40]

    listCharsSpecial = mystic.dictionary.listCharsSpecial
    # seteo las letras especiales
    for i in range(0x70, 0x80):
      mystic.dictionary.dict[i] = listCharsSpecial[i-0x70]

    listCharsJp = mystic.dictionary.listCharsJp
    # seteo las letras normales
    for i in range(0x80, 0x100):
      mystic.dictionary.dict[i] = listCharsJp[i-0x80]

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
        mystic.dictionary.dict[cont] = string
#        print('dictu {:02x} '.format(cont) + string)
        cont +=1
        string = ''
      else:
        chary = mystic.dictionary.decodeByte(val)
        string += chary

def tryJpCompress(string):
  """ for the JP rom, it compress a string """

  values = []
  while(len(string)>0):
    val = mystic.dictionary.tryJpCompressWord(string)
#    print('tenemos val: {:02x} para string '.format(val) + string)
    # if it could compress
    if(val != -1):
      values.append(val)
      palabra = mystic.dictionary.decodeByte(val)
      string = string[len(palabra):]

    # else, it couldn't compress
    else:
      char = string[0]

      if(char == u'\U0001F60A'):
        values.append(0x04)
      elif(char == u'\U0001F61E'):
        values.append(0x00)
      elif(char == u'\U0001F639'):
        values.append(0x10)
      elif(char == u'\U0001F63F'):
        values.append(0x11)
      elif(char == u'\U0001F610'):
        values.append(0x12)
      elif(char == u'\U0001F618'):
        values.append(0x1a)
      elif(char == u'\U0001F466'):
        values.append(0x14)
      elif(char == u'\U0001F467'):
        values.append(0x15)
      elif(char == u'\U0001F61D'):
        values.append(0x1b)
      elif(char == u'\U0001F47C'):
        values.append(0x1d)
      elif(char == u'\U0001F634'):
        values.append(0x1f)
      elif(char == u'\U0001F624'):
        values.append(0x13)
      elif(char == u'\U00002200'):
        values.append(0xa0)
      elif(char == u'\U00002201'):
        values.append(0xa1)
      elif(char == u'\U00002202'):
        values.append(0xa2)
      elif(char == u'\U00002203'):
        values.append(0xa3)
      elif(char == u'\U00002204'):
        values.append(0xa4)
      elif(char == u'\U00002205'):
        values.append(0xa5)
      elif(char == u'\U00002206'):
        values.append(0xa6)
      elif(char == u'\U00002207'):
        values.append(0xa7)
      elif(char == u'\U00002208'):
        values.append(0xa8)
      elif(char == u'\U00002209'):
        values.append(0xa9)
      elif(char == u'\U0000220a'):
        values.append(0xaa)
      elif(char == u'\U0000220b'):
        values.append(0xab)
      elif(char == u'\U0000220c'):
        values.append(0xac)
      elif(char == u'\U0000220d'):
        values.append(0xad)
      elif(char == u'\U0000220e'):
        values.append(0xae)
      elif(char == u'\U0000220f'):
        values.append(0xaf)
      else:

        # codifico el primer char
        val = mystic.dictionary.encodeChars(char)
        values.append(val)

      string = string[1:]
#      print('queda string: ' + string)

  return values

def tryJpCompressWord(string):
  """ for the JP rom, it tries to compress a string word """

  lang = mystic.address.language

  val = -1
  # si es rom japonesa
  if(lang == mystic.language.JAPAN):

#    print('tratando de comprimir: ' + string)
    # busco entre las palabras comprimidas
    for i in range(0x20, 0x40):
      palabra = mystic.dictionary.dict[i]
#      print('viendo {:02x} '.format(i) + palabra)

      # si la palabra no está vacía y nuestro string comienza con esa palabra
      if(len(palabra)>0 and string.startswith(palabra)):

#        print('encontramos: ' + palabra + ' en ' + string)
#        print('encontramos: ' + palabra)

        # quitamos las excepciones? (algunas no las comprime aunque podría) (para que coincida con la rom)
        if(i == 0x34 and string.startswith('ている😐😿😞')):
          pass
        elif(i == 0x32 and string.startswith('どうくつが あるよ')):
          pass
        elif(i == 0x24 and string.startswith('てにいれたら')):
          pass
        elif(i == 0x34 and string.startswith('ているのですか?')):
          pass
        elif(i == 0x29 and string.startswith('わたしておくわ!')):
          pass
        elif(i == 0x34 and string.startswith('ている😘マナのひみつに')):
          pass
        elif(i == 0x34 and string.startswith('ている😐😝ふたたび')):
          pass
        elif(i == 0x34 and string.startswith('ているじゃろう')):
          pass
        elif(i == 0x34 and string.startswith('ているんですが…')):
          pass
        elif(i == 0x34 and string.startswith('ているらしい😐😝おくの')):
          pass
        elif(i == 0x26 and string.startswith('アマンダ「やっぱり')):
          pass
        elif(i == 0x29 and string.startswith('わたしのしゅじん')):
          pass
        elif(i == 0x29 and string.startswith('わたし おいてけぼり')):
          pass
        elif(i == 0x26 and string.startswith('アマンダ「いっしょ')):
          pass
        elif(i == 0x2c and string.startswith('ちからが😘はつ')):
          pass
        elif(i == 0x25 and string.startswith('マナのいちぞく😐😝マナのきをま')):
          pass
        elif(i == 0x25 and string.startswith('マナのきをまもる')):
          pass
        elif(i == 0x34 and string.startswith('ている😐😝😞')):
          pass
        elif(i == 0x26 and string.startswith('アマンダのかたきを')):
          pass

        else:
          val = i
#          print(' ---> la comprimió!')

  return val

def decodeByte(byte):
  char = '·'

  if(byte in mystic.dictionary.dict.keys()):
    char = mystic.dictionary.dict[byte]

  return char


def decodeArray(array):
  string = ''
  for hexa in array:
    char = mystic.dictionary.decodeByte(hexa)
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
  # invierto el diccionario
  invDict = {v: k for k, v in mystic.dictionary.dict.items()}
  # busco en el diccionario invertido
  hexy = invDict[chars]
  # retorno lo encontrado
  return hexy

