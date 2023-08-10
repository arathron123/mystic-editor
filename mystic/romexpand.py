
import mystic.romSplitter
import mystic.ippy

def romExpand():

  print('rom expanding...')

  # choose one (or none) of the following available rom expansions,
  # you can also make your own custom romExpand...()

  romExpandMoveMaps()
#  romExpandMoveMusicBank()
#  romExpandMoveMusicBankAndExpandScriptsToFourBanks()
#  romExpandIpsPatch('./roms/colorization/en_uk_256.ips')
#  romExpandIpsPatch('./roms/colorization/en_uk_kkzero.ips')

def romExpandDX():

  print('rom expanding dx...')

  romExpandMoveMaps()
  romExpandColorizeSprites()



#################################################
def romExpandMoveMaps():
  """" This patches the rom before encoding, to add extra capabilities. """

  # changing the rom header, see
  # https://gbdev.gg8.se/wiki/articles/The_Cartridge_Header
  bank0 = mystic.romSplitter.banks[0]

  # Cartridge Type = MBC5+RAM+BATTERY
  bank0[0x0147] = 0x1b
  # ROM size = 32 banks
  bank0[0x0148] = 0x04
  # RAM Size = 02
  bank0[0x0149] = 0x02
  # Header Checksum
  bank0[0x014d] = 0xb8

  # we add 16 more banks
  for i in range(0,16):
    clean = [0x00] * 0x4000
    mystic.romSplitter.banks.append(clean)


  bank5 = mystic.romSplitter.banks[5]
  # we clean bank5, where map 00 (the overworld) used to be. 
  # (then encode with addr_en_romexpand.txt to burn maps in bank 0x12)
  for i in range(0,0x4000):
    bank5[i] = 0xff


#################################################
def romExpandMoveMusicBank():
  """" Moving the music bank 0xF around """

  # changing the rom header, see
  # https://gbdev.gg8.se/wiki/articles/The_Cartridge_Header
  bank0 = mystic.romSplitter.banks[0]

  # Cartridge Type = MBC5+RAM+BATTERY
  bank0[0x0147] = 0x1b
  # ROM size = 32 banks
  bank0[0x0148] = 0x04
  # RAM Size = 02
  bank0[0x0149] = 0x02
  # Header Checksum
  bank0[0x014d] = 0xb8

  # we add 16 more banks
  for i in range(0,16):
    clean = [0x00] * 0x4000
    mystic.romSplitter.banks.append(clean)


  bankf = mystic.romSplitter.banks[0xf]
  bank17 = mystic.romSplitter.banks[0x17]
  for i in range(0,0x4000):
    # muevo el banco 0xf a 0x17
    bank17[i] = bankf[i]
    # y borro el banco 0xf
    bankf[i] = 0xff

  
  bank0 = mystic.romSplitter.banks[0x0]
  # set the music bank in asm
  bank0[0x2053] = 0x17
  bank0[0x217c] = 0x17

#################################################
def romExpandMoveMusicBankAndExpandScriptsToFourBanks():

  # first we move the music bank
  romExpandMoveMusicBank()

  bankf = mystic.romSplitter.banks[0x0f]
  # we clean bankf
  for i in range(0,0x4000):
    bankf[i] = 0xff

  # hacked asm for supporting more than 2 script banks (thanks @xenophile!)  
  improved = [0xfa, 0xb6, 0xd8, 0x6f, 0xfa, 0xb7, 0xd8, 0x67, 0xfe, 0xd6, 0x28, 0x10, 0x06, 0x0c, 0x04, 0xd6, 0x40, 0xfe, 0x40, 0x30, 0xf9, 0xc6, 0x40]

  bank0 = mystic.romSplitter.banks[0x0]
  bank0[0x3c44:0x3c44 + len(improved)] = improved


#################################################
def romExpandColorizeSprites():
  """ it's equivalent to applying en_uk_256.ips, and only colorizes the hero """

  # we add 16 more banks
  for i in range(0,16):
    clean = [0x00] * 0x4000
    mystic.romSplitter.banks.append(clean)

  bank0 = mystic.romSplitter.banks[0x0]
  # change the gameboy header to make it gbc
  header = [0x80, 0x00, 0x00, 0x00, 0x13, 0x04, 0x01, 0x01, 0x01, 0x00, 0xc2, 0x36, 0x7a]
  bank0[0x0143:0x0143 + len(header)] = header

  # change code/data
  data = [0x3e, 0x10, 0xea, 0x00, 0x21, 0xcd, 0x00, 0x40, 0x00, 0x00, 0x00]
  bank0[0x1ff4:0x1ff4 + len(data)] = data

  bank0[0x2e99] = 0x21

  bank1 = mystic.romSplitter.banks[0x1]
  # change the hero sprite attributes
  # this gets overwritten by hero.js! you have to change "attrib" to "21", "01, "01", "01" respectively
  attrib = [0x21, 0x02, 0x00, 0x01, 0x00, 0x02, 0x01, 0x00, 0x02, 0x01]
  bank1[0x0752:0x0752 + len(attrib)] = attrib

  # new palletes in bank 0x10 ?
  bank10 = mystic.romSplitter.banks[0x10]
  data = [0xcd, 0x68, 0x21, 0x11, 0x60, 0x41, 0xcd, 0x00, 0x41, 0x11, 0x60, 0x40, 0x21, 0x80, 0xff, 0x06, 0x10, 0x1a, 0x13, 0x22, 0x05, 0x20, 0xfa, 0x40, 0xc3, 0x80, 0xff]
  bank10[0x0000:0x0000 + len(data)] = data

  data = [0x3e, 0x01, 0xea, 0x00, 0x21, 0x3e, 0x00, 0x21, 0x00, 0xc0, 0x01, 0x00, 0x20, 0xc9]
  bank10[0x0060:0x0060 + len(data)] = data

  data = [0xd5, 0x21, 0x68, 0xff, 0x3e, 0x80, 0x22, 0xcd, 0x20, 0x41, 0xd1, 0x21, 0x6a, 0xff, 0x3e, 0x80, 0x22, 0xcd, 0x20, 0x41, 0xc9, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3e, 0x40, 0x47, 0x1a, 0x77, 0x78, 0x3d, 0xc8, 0x13, 0x18, 0xf7]
  bank10[0x0100:0x0100 + len(data)] = data

  data = [0x18, 0x7f, 0x4a, 0x29, 0xa5, 0x14, 0x00, 0x00, 0x18, 0x7f, 0x9f, 0x52, 0x1f, 0x00, 0x00, 0x00, 0x18, 0x7f, 0xff, 0x3d, 0x1f, 0x00, 0x0f, 0x00, 0x18, 0x7f, 0xff, 0x3f, 0x1f, 0x00, 0xef, 0x01, 0x18, 0x7f, 0xef, 0x3f, 0xe0, 0x03, 0xe0, 0x01, 0x18, 0x7f, 0xff, 0x7d, 0x1f, 0x7c, 0x0f, 0x3c, 0x18, 0x7f, 0xef, 0x7d, 0x00, 0x7c, 0x00, 0x3c, 0x18, 0x7f, 0x9f, 0x52, 0xff, 0x7f, 0x00, 0x00, 0x18, 0x7f, 0x9f, 0x52, 0x1f]
  bank10[0x0160:0x0160 + len(data)] = data

 
#################################################
def romExpandIpsPatch(pathIps):
  """ patches the rom with the ips file """

  patch = mystic.ippy.Patch()

  # the rom array
  arraySource = mystic.romSplitter.getRomArrayFromBanks()
  # the ips array
  arrayIps = mystic.util.fileToArray(pathIps)

  arrayTarget = patch._patch(arraySource, arrayIps)
#  print('arrayTarget: ' + mystic.util.strHexa(arrayTarget[:0x200]))
#  for i in range(0,0x20):
#    print('line: ' + mystic.util.strHexa(arrayTarget[0x10*i:0x10*(i+1)]))

  # load the banks
  mystic.romSplitter.loadBanksFromArray(arrayTarget)


