
import mystic.address
import mystic.util



#Sounds can play on channel 1 and 4 (either or both).

#There is a table of pointers to channel 1 data at 0f:7b3c and channel 4 data at 0f:7b86. Each is 37 pointers.

#They point into data located at 0f:7bd0 and up (though there is nothing forcing them to).

#This data consists of four types of entries:
#1. 0xf0 to 0xff, the low nibble is loaded into a loop counter. I think 0xf0 is loop 255 and 0xf1 is loop zero?
#2. 0xef, if the loop counter is not one then the next two bytes are loaded into the current position pointer and the loop counter is decremented.
#3. 0x00 end of data.
#4. 0x01 to 0xee, this byte is a duration counter (in frames?) and the next bytes are fed to the channel. For channel 1 this would be followed by five bytes to be written into NR10 through NR14. For channel 4 it is followed by two bytes and NR44 is written with 0x80.

#An example from the airship sound (channel 4)

#7d8d:
#$f4		; load 4 into the counter (it is never going to allow this to hit zero)
#$03, $f8, $33	; durration=3, NR42=f8, NR43=33, NR44=80
#$02, $00, $00	; durration=2, NR42=00, NR43=00, NR44=80
#$03, $78, $43	; durration=3, NR42=78, NR43=43, NR44=80
#$02, $00, $00	; durration=2, NR42=00, NR43=00, NR44=80
#$ef, $8d, $7d	; jump 7d8d (back to start)
#$00 		; end (never reached)


##########################################################
class SoundNote:
  """ represents an instruction of mini-sound """



