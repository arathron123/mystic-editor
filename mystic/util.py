# pip3 install pypng
import png
 
def fileToArray(filepath):

  array = []

  dataBytes = []
  with open(filepath, 'rb') as f:
    # leo el .bpp
    dataBytes = f.read()

  for byte in dataBytes:
    array.append(byte)

  return array


def arrayToFile(array, filepath):

  f = open(filepath, 'wb')
  f.write( bytes(array) )
  f.close()


def md5sum(filepath):
  """ calcula el md5sum de un archivo """
  import hashlib
  hash_md5 = hashlib.md5()
  with open(filepath, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()


def strHexa(bytes):
  """ convierte array de bytes en string hexa """

  string = ''
  for byte in bytes:
    string += '{:02x} '.format(byte)
  return string

def hexaStr(strHexa):
  """ convierte string hexa en array de bytes """

  hexas = []
  strHexas = strHexa.split(' ')
  for strHexa in strHexas:
    hexa = int(strHexa, 16)
#    print('strHexa: ' + strHexa)
#    print('hexa: {:02x}'.format(hexa))
    hexas.append(hexa)

  return hexas

def pngToArray(filepath):
  """ dado un archivo.png devuelve matriz de int con sus colores """

  f = open(filepath, 'rb')
  r = png.Reader(f)
  data = r.read()

  rows = list(data[2])

  array = []
  for row in rows:
    newRow = []
    for color in row:
      # invierto los colores (en el gb funcionan asi)
#      newColor = 3 - color
      newColor = 3 - color//(255//3)
      newRow.append(newColor)

    array.append(newRow)

  return array

def arrayToPng(array, w, h, filepath):
  """ dada una matriz de int representando colores, sus dimensiones, y el filepath, lo graba en un archivo.png """

  for j in range(0,h):
    for i in range(0,w):
      # invierto los colores (en el gb funcionan asi)
#      array[j][i] = 3 - array[j][i]
      array[j][i] = 255 - array[j][i]*(255//3)

  f = open(filepath, 'wb')
#  w = png.Writer(w, h, greyscale=True, bitdepth=2)
  w = png.Writer(w, h, greyscale=True)
  w.write(f, array)
  f.close()


def compareFiles(filepath1, filepath2, idx0, cantBytes):
  """ compara si dos archivos binarios son iguales entre los índices indicados """

  iguales = True

  f = open(filepath1, 'rb')
  array1 = f.read()
  f.close()

  g = open(filepath2, 'rb')
  array2 = g.read()
  g.close()

  for i in range(0, cantBytes):

    byte1 = array1[idx0 + i]
    byte2 = array2[i]

#    print('addr: {:04x} - byte1: {:02x} - byte2: {:02x}'.format(idx0 + i, byte1,byte2))

    # si son distintos
    if(byte1 != byte2):
      iguales = False

      print('byte1, byte2 = {:02x}, {:02x}'.format(byte1,byte2))

      print('diferencia en addr: 0x{:04x}'.format(idx0 + i))
      break

  return iguales
