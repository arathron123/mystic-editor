
import mystic.address


data = []

def appendData(initAddr, dataSize, dataFilepath):
  """ append data to the rom info """
  data.append( (initAddr, dataSize, dataFilepath) )

def _globalAddrToStrAddr(globalAddr):

  numBank = globalAddr // 0x4000
  offset = globalAddr % 0x4000

  strAddr = '{:02x}:{:04x}'.format(numBank, offset)
  return strAddr

def _getLastBank():
  """ returns the last bank number being used """

  lastBank = -1

  for iniAddr, dataSize, dataFilepath in data:
    numBank = iniAddr // 0x4000
    if(numBank > lastBank):
      lastBank = numBank

  return lastBank

def _getJsonData(jsonData):

#  print('data: ' + str(data))
  sortedData = sorted(data)
#  print('sortedData: ' + str(sortedData))

  for d in sortedData:
    iniAddr = d[0]
    dataSize = d[1]
    dataFilepath = d[2]
    strIniAddr = _globalAddrToStrAddr(iniAddr)
    strEndAddr = _globalAddrToStrAddr(iniAddr+dataSize-1)
#    print('initAddr: ' + strInitAddr + ' endAddr: ' + strEndAddr + ' filepath: '.format(iniAddr, dataSize) + dataFilepath)
#    jsonData.append({'iniAddr' : strIniAddr, 'endAddr' : strEndAddr, 'filepath' : dataFilepath})

    numBank = iniAddr // 0x4000
    oIniAddr = iniAddr % 0x4000
    oEndAddr = oIniAddr + dataSize
    strOIniAddr = '{:04x}'.format(oIniAddr)
    strOEndAddr = '{:04x}'.format(oEndAddr)

#    print('insertando en banco: ' + str(numBank))
    jsonData[numBank]['data'].append( {'iniAddr' : strOIniAddr, 'endAddr' : strOEndAddr, 'filePath' : dataFilepath } )


  return jsonData


def _exportJson(rom_info, jsonData):

  basePath = mystic.address.basePath

  import json
  # for allowing kana characters in json ensure_ascii=False
  strJson = json.dumps(jsonData, indent=2, ensure_ascii=False)
#  strJson = json.dumps(data)
  f = open(basePath+'/' + rom_info + '.js', 'w', encoding="utf-8")
  f.write(rom_info + ' = \n' + strJson)
  f.close()



def exportData(rom_info):

  jsonData = []

  lastBank = _getLastBank()

#  print('lastBank: ' + str(lastBank))

  # comienzo con los bancos vacios
  for i in range(0,lastBank+1):
    jsonData.append({'bank' : i, 'data' : []})


  jsonData = _getJsonData(jsonData)
  _exportJson(rom_info, jsonData)


##################################### all bellow this is deprecated and should be deleted


# los bancoDatas
banks = []

for k in range(0,0x10):
  # los creo en gris
  bancoData = [ (0xe0, 0xe0, 0xe0) for i in range(0,0x80 * 0x80)]
  banks.append(bancoData)

# los datos de que info hay en que parte de que bloques
datos = []


#def appendDato(banco, iniAddr, finAddr, color, descrip):
#  """ agrega un dato a la info de los bancos """
#  datos.append( (banco, iniAddr, finAddr, color, descrip) )

def exportPng():

  from PIL import Image, ImageColor

  # creo data en blanco para contener los 16 bancos
  imgData = [ (0xff, 0xff, 0xff) ]*(0x200*0x200)

  width, height = 0x200, 0x200
  img = Image.new('RGB', (width, height))
  img.putdata(imgData)
  pixels = img.load()

  # para cada dato
  for dato in datos:
    banco   = dato[0]
    iniAddr = dato[1]
    finAddr = dato[2]
    color   = dato[3]
    descrip = dato[4]

#    print('procesando en banco: {:02x}'.format(banco))

    # agarro el bancoData correspondiente
    bancoData = banks[banco]

    # el intervalo indicado
    for i in range(iniAddr, finAddr):
      # lo coloreo del color indicado
      bancoData[i] = color

#    banks[banco] = bancoData

  # para cada uno de los 16 bancos
  for j in range(0,4):
    for i in range(0,4):

      # agarro el bancoData correspondiente
      bancoData = banks[j*4+i]

      imgBank = Image.new('RGB', (0x80, 0x80))
      imgBank.putdata(bancoData)

      x = 0x80*i
      y = 0x80*j
      img.paste(imgBank, (x,y, x+0x80, y+0x80))


  # creo las rayas horizontales
  for i in range(0,0x200):
    j = 1*0x200//4
    pixels[i,j] = (0x00, 0x00, 0x00)
    j = 2*0x200//4
    pixels[i,j] = (0x00, 0x00, 0x00)
    j = 3*0x200//4
    pixels[i,j] = (0x00, 0x00, 0x00)
  # y verticales
  for j in range(0,0x200):
    i = 1*0x200//4
    pixels[i,j] = (0x00, 0x00, 0x00)
    i = 2*0x200//4
    pixels[i,j] = (0x00, 0x00, 0x00)
    i = 3*0x200//4
    pixels[i,j] = (0x00, 0x00, 0x00)


  basePath = mystic.address.basePath
  # grabo la imagen
  img.save(basePath + '/rom_info.png')




