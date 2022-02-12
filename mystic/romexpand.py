
import mystic.romSplitter
import mystic.ippy

def romExpand():

  print('rom expanding...')

  # choose one (or none) of the following available rom expansions,
  # you can also make your own custom romExpand...()

  romExpandMoveMaps()
#  romExpandMoveMusicBank()
#  romExpandIpsPatch('./roms/colorization/en_uk_256.ips')
#  romExpandIpsPatch('./roms/colorization/en_uk_kkzero.ips')

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


