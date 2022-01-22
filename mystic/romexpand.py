
import mystic.romSplitter

def romExpand():
  """" This patches the rom before encoding, to add extra capabilities. """

  print('rom expanding...')

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


