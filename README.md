# mystic-editor

Hi! This is a Mystic Quest (also known as Final Fantasy Adventure) gameboy game editor version 0.95.3

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

If you want more control, you can specify the rom-file and address-configuration file like this example
**python3 mystic-editor.py --rom stockRoms/en.gb --addr addr_en.txt -d**

If you want to expand the rom to 32 banks add the --romexpand argument before encoding like this example
**python3 mystic-editor.py --rom stockRoms/en.gb --addr addr_en_romexpand.txt --romexpand -e**

Feel free to join our discord server
https://discord.gg/mdTDMKh5FR

Github repository:
https://github.com/arathron123/mystic-editor