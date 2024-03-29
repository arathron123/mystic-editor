#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# command line arguments
import sys

#
# Ippy is an IPS ("International Patching System") patcher/builder.
#
# Thanks to:
#   + zerosoft fot the ips specifications: https://zerosoft.zophar.net/ips.php
#   + marcrobledo for RomPatcher.js:       https://github.com/marcrobledo/RomPatcher.js 
#   + Alcaro for Flips:                    https://github.com/Alcaro/Flips
#

def printHelp():
  print('Usage example for patching: ')
  print('  python3 ippy.py --patch in.bin out.bin patch.ips')
  print('Usage example for building an ips file: ')
  print('  python3 ippy.py --build in.bin out.bin patch.ips')
  print('Usage example for viewing an ips file: ')
  print('  python3 ippy.py --view patch.ips')
  print('--------------------------------------------------')


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


####################################

class RecordIPS:

  def __init__(self, offset, data):
    self.offset = offset
    self.data = data

  def encode(self):
    array = []

    byte1 = self.offset//0x10000
    byte2 = (self.offset % 0x010000)//0x100
    byte3 = (self.offset % 0x000100)
    # we encode the offset
    array.extend( [byte1, byte2, byte3] )

    byte1 = len(self.data)//0x100
    byte2 = len(self.data) %0x100
    # the length
    array.extend( [byte1, byte2] )

    # and the data itself
    array.extend(self.data)

    return array

  def __str__(self):
#    return 'IPS({:06x}, {:04x}, '.format(self.offset, len(self.data)) + strHexa(self.data[:5]) + '...)'
#    return 'IPS({:06x}, '.format(self.offset) + strHexa(self.data[:5]) + '...)'
    return 'IPS({:06x}, '.format(self.offset) + strHexa(self.data) + ')'

  def __repr__(self):
    return 'IPS({:06x})'.format(self.offset)



####################################

class RecordRLE:

  def __init__(self, offset, rleSize, rleByte):
    self.offset = offset
    self.rleSize = rleSize
    self.rleByte = rleByte

  def encode(self):
    array = []

    byte1 = self.offset//0x10000
    byte2 = (self.offset % 0x010000)//0x100
    byte3 = (self.offset % 0x000100)
    # we encode the offset
    array.extend( [byte1, byte2, byte3] )

    # set the length 0x0000 so that we know it is an rle record
    array.extend( [0x00, 0x00] )

    byte1 = self.rleSize//0x100
    byte2 = self.rleSize %0x100
    # the rle length
    array.extend( [byte1, byte2] )

    # and the rle byte
    array.append(self.rleByte)

    return array

  def __str__(self):
    return 'RLE({:06x}, {:04x}, {:02x})'.format(self.offset, self.rleSize, self.rleByte)

  def __repr__(self):
    return 'RLE({:06x})'.format(self.offset)


####################################

class Patch:
  """ An IPS patcher """

  def __init__(self):
    # by default don't truncate the file
    self.truncate = -1

    # the list of ips and rle records
    self.records = []

  def _generateExampleFiles(self):
    """ it creates some example files to test things """

    in1  = [ 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 
             0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80 ]
    out1 = [ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 
             0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ]

    in2  = [ 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F ]
    out2 = [ 0xFF, 0x01, 0x02, 0x03, 0x04, 0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ]

    in3  = [ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ]
    out3 = [ 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03 ]

    arrayToFile(in1, './in1.bin')
    arrayToFile(out1, './out1.bin')

    arrayToFile(in2, './in2.bin')
    arrayToFile(out2, './out2.bin')

    arrayToFile(in3, './in3.bin')
    arrayToFile(out3, './out3.bin')

  def _parseArrayIps(self, arrayIps):
    """ parses the ips array """

    self.records = []
    self.truncate = -1

    ending = arrayIps[len(arrayIps)-3:]
#    print('ending: {:02x} {:02x} {:02x}'.format(ending[0], ending[1], ending[2]))
    endingNumber = ending[0]*0x10000 + ending[1]*0x100 + ending[2]
#    print('endingNumber: {:06x}'.format(endingNumber))

    # if it ends with 'EOF'
    if(endingNumber == 0x454f46):
      # we don't truncate the file
      self.truncate = -1
      # eliminate the 'PATCH' and 'EOF'
      arrayIps = arrayIps[5:len(arrayIps)-3]

    # otherwise
    else:
      # set the truncating offset
      self.truncate = endingNumber
      # eliminate the 'PATCH' and 'EOF' and 'truncate offset'
      arrayIps = arrayIps[5:len(arrayIps)-6]

#    print('truncate: {:06x}'.format(self.truncate))

#    while(False):
    while(len(arrayIps) > 0):

#      print('--------')
      offset = arrayIps[2] + arrayIps[1]*0x100 + arrayIps[0]*0x10000
#      print('offset: {:06x}'.format(offset))

      size = arrayIps[4] + arrayIps[3]*0x100
#      print('size: {:04x}'.format(size))

      # if it is an rle-encoded record
      if(size == 0):
        rleSize = arrayIps[6] + arrayIps[5]*0x100
#        print('rleSize: {:04x}'.format(rleSize))

        rleByte = arrayIps[7]
#        print('rleByte: {:02x}'.format(rleByte))

        recordRle = RecordRLE(offset, rleSize, rleByte)
        self.records.append(recordRle)

        # set the remainder of the file
        arrayIps = arrayIps[8:]

      else:
        data = arrayIps[5:5+size]
#        print('data: ' + strHexa(data))

        recordIps = RecordIPS(offset, data)
        self.records.append(recordIps)

        # set the remainder of the file
        arrayIps = arrayIps[5+size:]

#    print('---- showing ips records')
#    for record in self.records:
#      print('record: ' + str(record))


  def _applyPatch(self, arraySource):
    """ applies the current patch to the source array """

#    print('source: ' + strHexa(arraySource))

    # for each record
    for rec in self.records:

#      print('arraySource: ' + strHexa(arraySource))

#      print('rec: ' + str(rec))

      # if it is ips
      if(type(rec) == RecordIPS):
#        print('ips: ' + str(rec))

        for i in range(0, len(rec.data)):
          if(rec.offset+i < len(arraySource)):
            arraySource[rec.offset+i] = rec.data[i]
          else:
            arraySource.append(rec.data[i])


      elif(type(rec) == RecordRLE):
#        print('rle: ' + str(rec))

        for i in range(0, rec.rleSize):
          if(rec.offset+i < len(arraySource)):
            arraySource[rec.offset+i] = rec.rleByte
          else:
            arraySource.append(rec.rleByte)

    # if the file has to be truncated
    if(self.truncate != -1):
      # we do it
      arraySource = arraySource[:self.truncate]

#    print('arraySource: ' + strHexa(arraySource))
#    arrayToFile(arraySource, 'patched.gb')

    return arraySource


  def view(self, pathIps):
    """ shows the ips file on terminal """
    print('viewing ips=' + pathIps)

    arrayIps = fileToArray(pathIps)

    # first we parse the ips array
    self._parseArrayIps(arrayIps)

    # for each record
    for rec in self.records:
      print('rec: ' + str(rec))

      
  def patch(self, pathSource, pathTarget, pathIps):
    """ patches the source file with the ips file and saves as target file """

    print('patching source=' + pathSource + ' with ips=' + pathIps + ' and saving as target='  + pathTarget)

    arraySource = fileToArray(pathSource)
    arrayIps = fileToArray(pathIps)

    arrayTarget = self._patch(arraySource, arrayIps)

    # finally we save the generated target file
    arrayToFile(arrayTarget, pathTarget)


  def _patch(self, arraySource, arrayIps):
    """ patches the source array with the ips array, returns the target array """

    # first we parse the ips array
    self._parseArrayIps(arrayIps)

    # then we apply the patch to the source array
    arrayTarget = self._applyPatch(arraySource)

    return arrayTarget


  def buildIpsFromFiles(self, pathSource, pathTarget, pathIps):
    """ builds an ips file from a source and a target file """

    print('building ips=' + pathIps + ' with source=' + pathSource + ' and target='  + pathTarget)

    arraySource = fileToArray(pathSource)
    arrayTarget = fileToArray(pathTarget)

    # we build the ips records
    self._buildIps(arraySource, arrayTarget)

#    print('---- showing ips records')
#    for record in self.records:
#      print('record: ' + str(record))

#    print('--------- optimizing encode: ' + str(len(self._encode())))

    # we make a copy of the records
    newRecords = [record for record in self.records]

    # we start with step 0
    i = 0
    # asume it is not already optimal
    isOpt = False
#    print('step ' + str(i) + ' - newRecords: ' + str(newRecords))
#    print('step ' + str(i) )
    # while it is not optimal
    while(not isOpt):
      i += 1
      # optimize the size by splitting the IPS records into RLE records when convenient
      newRecords, isOpt = self._optimize(newRecords)
#      print(str(i) + ' - newRecords: ' + str(newRecords))
#      print('step ' + str(i) )
 
#    for rec in newRecords:
#      print('req: ' + str(rec))

    self.records = newRecords
#    print('--------- optimized encode: ' + str(len(self._encode())))

    # we create the ips array
    arrayIps = self._encode()

#    for record in self.records:
#      print('rec: ' + str(record))

    # and save it in a file
    arrayToFile(arrayIps, pathIps)

  def _optimize(self, records):
    """ splits the ips into rle records when needed for space optimization """

    newRecords = []

    # asume it is already optimized
    alreadyOpt = True

    # for each record
    for i in range(0,len(records)):
      record = records[i]
#      print('record: ' + str(record))

      # we try to compress it
      equivRecords = self._optimizeRecord(record)
#      print('equivRecords: ' + str(equivRecords))

      # if it could
      if(len(equivRecords) > 1):
        # we indicate that it is still not optimized
        alreadyOpt = False
      
      # and append the returned new records in the new list
      newRecords.extend(equivRecords)

    return newRecords, alreadyOpt




  def _optimizeRecord(self, record):
    """ given a record, it analizes if it is worth compressing it, and in that case it returns the compressed equivalent records """

    # if it is an rle record
    if(type(record) != RecordIPS):
      # it is already opt
      return [record]

#    print('tratando de optimizar rec: ' + str(record))

    data = record.data
#    print('--- data: ' + strHexa(data) + 'len: ' + str(len( record.encode())))

    length = 0
    prevEqual = False
    offset = -1
#    searchedByte = 0xff

    # the set of different bytes
    possibleBytes = set(record.data)
#    print('possibleBytes: ' + strHexa(possibleBytes))

    # for each possible to be repeated byte
    for searchedByte in possibleBytes:

      # for each byte of data
      for j in range(0,len(data)):
        bity = data[j]

        # if it equals the searched byte
        if(bity == searchedByte):
          length += 1

          # if the previous was not the searched byte
          if(not prevEqual):

            # starting a possible rle record buffer
            prevEqual = True
            offset = j
        # if not, it is not the searched byte
        else:

          # but if the last byte was equal
          if(prevEqual):
            # ending a possible rle record buffer
            records, comp = self._tryToCompress(record, offset, length, searchedByte)
            if(comp):
              return records

          prevEqual = False
          length = 0
          offset = -1

      # if the last byte was equal
      if(prevEqual):
        records, comp = self._tryToCompress(record, offset, length, searchedByte)
        if(comp):
          return records

    # if it reached here it was not worth compressing
    return [record]


  def _tryToCompress(self, record, offset, length, searchedByte):

#    print('searchedByte: {:02x} length: '.format(searchedByte) + str(length))
    data = record.data
#    print('offset: ' + str(offset) + ' length: ' + str(length))
    # if the buffer is at the beginning or ending of the data
    if((offset == 0) or (offset+length == len(data))):
      # we would need 8 bytes of header overhead for the rle-record
      overhead = 8
#      print('initial or final')
      # if it is worthy of making the rle-record
      if(length > overhead):
#        print('worth it compressing')
        # if it is an initial buffer
        if(offset == 0):
          rec1 = RecordRLE(record.offset, length, searchedByte)
          rec2 = RecordIPS(record.offset+length, data[length:])
#          print('rec1: ' + str(rec1))
#          print('rec2: ' + str(rec2))
#          print('total len: ' + str( len(rec1.encode()) + len(rec2.encode())))
 
          # if it is also final
          if(offset+length == len(data)):
            return [rec1],True
          # else, it is only initial
          else:
            return [rec1, rec2],True

        # if not, it is a final buffer
        else:
          rec1 = RecordIPS(record.offset, data[:offset])
          rec2 = RecordRLE(record.offset+offset, length, searchedByte)

#          print('rec1: ' + str(rec1))
#          print('rec2: ' + str(rec2))
#          print('total len: ' + str( len(rec1.encode()) + len(rec2.encode())))
          return [rec1, rec2],True
 
    # else, the buffer is at the middle of the data
    else:
      # we would need 8 bytes of header overhead for the rle-record and 5 bytes of header for the second ips-record
      overhead = 8+5
#      print('middle')
      # if it is worthy of making the rle-record
      if(length > overhead):
#        print('worth it compressing in the middle')

        rec1 = RecordIPS(record.offset, data[:offset])
        rec2 = RecordRLE(record.offset+offset, length, searchedByte)
        rec3 = RecordIPS(record.offset+offset+length, data[offset+length:])

#        print('rec1: ' + str(rec1))
#        print('rec2: ' + str(rec2))
#        print('rec3: ' + str(rec3))
#        print('total len: ' + str( len(rec1.encode()) + len(rec2.encode()) + len(rec3.encode()) ))
        return [rec1, rec2, rec3],True

    # if it gets here, it is not worth compressing 
    return [record],False


  def _buildIps(self, arraySource, arrayTarget):
    """ It builds an ips array from the source and target arrays.  It only creates IPS records (no RLE records) """

    # by default don't truncate the file
    self.truncate = -1
    # the list of ips and rle records
    self.records = []

#    print('source: ' + strHexa(arraySource))
#    print('target: ' + strHexa(arrayTarget))

    # if the target file is shorter
    if(len(arrayTarget) < len(arraySource)):
      # we indicate it has to be truncated
      self.truncate = len(arrayTarget)

    i = 0
    # iterate the arrayTarget
    while(i < len(arrayTarget)):

#      print('--- va por i: {:08x}'.format(i))

      # read a byte from each file
      b1 = arraySource[i] if i <= len(arraySource)-1 else None
      b2 = arrayTarget[i]

#      print('b1, b2: {:02x}, {:02x}'.format(b1,b2))

      # if the bytes are different
      if(b1 != b2):

        differentData = []
        startOffset = i

        # while the data is different
#        while(b1 != b2 and len(differentData) < 0xffff and i < len(arrayTarget)):
        while(b1 != b2):

          # we append it to the array
          differentData.append(b2)
          # if the byte is different from the first in the record
          if(b2 != differentData[0]):
            # it will not be an rle record
            rleMode = False

          # if the next step reachs the end of the file, or the differentData is full
          if(i+1 == len(arrayTarget) or len(differentData) == 0xffff):
#            print('breaking')
            # we end the differentData
            break

          i += 1

          # read a byte from each file
          b1 = arraySource[i] if i <= len(arraySource)-1 else None
          b2 = arrayTarget[i]

#        print('differentData: ' + strHexa(differentData))

        # we create it as an ips record
        rec = RecordIPS(startOffset, differentData)

#        print('rec: ' + str(rec))

        # we add the record to the list
        self.records.append(rec)

      i += 1



  def _buildIpsOld(self, arraySource, arrayTarget):
    """ It builds an ips array from the source and target arrays.  It is not yet space-optimized """

    # by default don't truncate the file
    self.truncate = -1
    # the list of ips and rle records
    self.records = []

#    print('source: ' + strHexa(arraySource))
#    print('target: ' + strHexa(arrayTarget))

    # if the target file is shorter
    if(len(arrayTarget) < len(arraySource)):
      # we indicate it has to be truncated
      self.truncate = len(arrayTarget)

    i = 0
    # iterate the arrayTarget
    while(i < len(arrayTarget)):

#      print('--- va por i: {:08x}'.format(i))

      # read a byte from each file
      b1 = arraySource[i] if i <= len(arraySource)-1 else None
      b2 = arrayTarget[i]

#      print('b1, b2: {:02x}, {:02x}'.format(b1,b2))

      # if the bytes are different
      if(b1 != b2):

        rleMode = True
        differentData = []
        startOffset = i

        # while the data is different
#        while(b1 != b2 and len(differentData) < 0xffff and i < len(arrayTarget)):
        while(b1 != b2):

          # we append it to the array
          differentData.append(b2)
          # if the byte is different from the first in the record
          if(b2 != differentData[0]):
            # it will not be an rle record
            rleMode = False

          # if the next step reachs the end of the file, or the differentData is full
          if(i+1 == len(arrayTarget) or len(differentData) == 0xffff):
#            print('breaking')
            # we end the differentData
            break

          i += 1

          # read a byte from each file
          b1 = arraySource[i] if i <= len(arraySource)-1 else None
          b2 = arrayTarget[i]

#        print('differentData: ' + strHexa(differentData))

        # if it is an rle block
#        if(rleMode):
        if(rleMode and len(differentData) > 2):
          # we create it
          rec = RecordRLE(startOffset, len(differentData), differentData[0])
        # otherwise
        else:
          # we create it as an ips record
          rec = RecordIPS(startOffset, differentData)

#        print('rec: ' + str(rec))

        # we add the record to the list
        self.records.append(rec)

      i += 1

  def _encode(self):
    """ return the ips array of the current records """

    # array of the ips file
    arrayIps = []

    # header 'PATCH'
    arrayIps.extend( [0x50, 0x41, 0x54, 0x43, 0x48] )

    # for each record
    for rec in self.records:
#      print('rec: ' + str(rec))
      array = rec.encode()
#      print('array: ' + strHexa(array))

      # we encode it and append it to the file
      arrayIps.extend(array)

    # footer 'EOF'
    arrayIps.extend( [0x45, 0x4f, 0x46] )

    # if the file has to be truncated
    if(self.truncate != -1):
      byte1 = self.truncate//0x10000
      byte2 = (self.truncate % 0x010000)//0x100
      byte3 = (self.truncate % 0x000100)
      # we append its size
      arrayIps.extend( [byte1,byte2,byte3] )

    # we return the ips array
    return arrayIps

#################################
def main(argv):
  print('Welcome to ippy ips-patcher...')

  # create the patcher
  patch = Patch()


  # if the number of arguments 2
  if(len(argv) == 2):

    pathIps    = argv[1]

    # if he wants to view an ips
    if('--view' in argv):
      patch.view(pathIps)

  # else, if the number of arguments is 4
  elif(len(argv) == 4):

    pathSource = argv[1]
    pathTarget = argv[2]
    pathIps    = argv[3]

#    print('pathSource: ' + pathSource)
#    print('pathTarget: ' + pathTarget)
#    print('pathIps: ' + pathIps)

    # if he wants to patch a file
    if('--patch' in argv):
      patch.patch(pathSource, pathTarget, pathIps)
    # if he wants to create an ips file
    elif('--build' in argv):
      patch.buildIpsFromFiles(pathSource, pathTarget, pathIps)

  # else, the number of arguments is incorrect
  else:
    # show usage help
    printHelp()




#  patch._generateExampleFiles()

#  patch.buildIpsFromFiles('./in1.bin', './out1.bin', './generated1.ips')
#  patch.buildIpsFromFiles('./in2.bin', './out2.bin', './generated2.ips')
#  patch.buildIpsFromFiles('./in3.bin', './out3.bin', './generated3.ips')

#  patch.patch('./in1.bin', './generated1.bin', './generated1.ips')
#  patch.patch('./in2.bin', './generated2.bin', './generated2.ips')
#  patch.patch('./in3.bin', './generated3.bin', './generated3.ips')

if __name__ == "__main__":
  main(sys.argv[1:])

