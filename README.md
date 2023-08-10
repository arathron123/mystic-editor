# mystic-editor

Hi! This is a Mystic Quest (also known as Final Fantasy Adventure) gameboy game editor version 0.95.14

Tutorial video here: 
https://www.youtube.com/watch?v=XKPYtgKAiQw

Place the mystic quest gameboy rom in the same folder of this script.  The md5sum of the english version should be **24cd3bdf490ef2e1aa6a8af380eccd78**

To run this script you need the following python libraries: pypng, Pillow.
You can install them with the following commands

pip install pypng
pip install Pillow

To decode the rom run
**python3 mystic-editor.py -d**

A folder named **en** (for english) will be created with all the maps, scripts, sprites, and audio files decoded from the rom.  This files can be edited and re-encoded again into the rom.

To encode the rom run
**python3 mystic-editor.py -e**

Optional Arguments:
--rom [filePath] specifies the rom file to decode, example:
**python3 mystic-editor.py --rom stockRoms/en.gb -e**

--addr [filePath] specifies the address-configuration file to encode, example:
**python3 mystic-editor.py --addr addr_en.js -e**

-x (or --romexpand) encodes an expanded rom with more banks, example:
**python3 mystic-editor.py --rom stockRoms/en.gb --addr addr/addr_en_romexpand.js --romexpand -e**

-m (or --mscripts) decodes/encodes the scripts into mscripts.txt instead of jscripts.js, example:
**python3 mystic-editor.py -dm**

-t (or --tilesetsLevel2) decodes/encodes the tilesetsLevel2 folder, overwriting the big tilesets.png file, example:
**python3 mystic-editor.py -dt**

-c (or --color) encodes a gameboy color rom (work in progress), example:
**python3 mystic-editor.py -ec**

-f (or --fix-checksum) fixes the header and global checksums of the rom, example:
**python3 mystic-editor.py -ef**

-i (or --ips) creates an .ips patch of the newRom.gb, example:
**python3 mystic-editor.py -ei**

--ffl2 path/to/ffl2.gb  (it decodes music from english version of FFL 2 rom with md5sum **2bb0df1b672253aaa5f9caf9aab78224**)

Feel free to join our discord server
https://discord.gg/mdTDMKh5FR

Github repository:
https://github.com/arathron123/mystic-editor