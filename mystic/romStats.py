
import mystic.romStats

# los bancoDatas
banks = []

for k in range(0,0x10):
  # los creo en gris
  bancoData = [ (0xe0, 0xe0, 0xe0) for i in range(0,0x80 * 0x80)]
  banks.append(bancoData)

# los datos de que info hay en que parte de que bloques
datos = []


def appendDato(banco, iniAddr, finAddr, color, descrip):
  """ agrega un dato a la info de los bancos """
  mystic.romStats.datos.append( (banco, iniAddr, finAddr, color, descrip) )

def exportPng():

  from PIL import Image, ImageColor

  # creo data en blanco para contener los 16 bancos
  imgData = [ (0xff, 0xff, 0xff) ]*(0x200*0x200)

  width, height = 0x200, 0x200
  img = Image.new('RGB', (width, height))
  img.putdata(imgData)
  pixels = img.load()

  # para cada dato
  for dato in mystic.romStats.datos:
    banco   = dato[0]
    iniAddr = dato[1]
    finAddr = dato[2]
    color   = dato[3]
    descrip = dato[4]

#    print('procesando en banco: {:02x}'.format(banco))

    # agarro el bancoData correspondiente
    bancoData = mystic.romStats.banks[banco]

    # el intervalo indicado
    for i in range(iniAddr, finAddr):
      # lo coloreo del color indicado
      bancoData[i] = color

#    mystic.romStats.banks[banco] = bancoData

  # para cada uno de los 16 bancos
  for j in range(0,4):
    for i in range(0,4):

      # agarro el bancoData correspondiente
      bancoData = mystic.romStats.banks[j*4+i]

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


