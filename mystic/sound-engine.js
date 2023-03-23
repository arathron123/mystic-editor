// create web audio api context
var audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playNote(frequency, duration, callback, ch) {
  // create Oscillator node
  var oscillator = audioCtx.createOscillator();
  var gainNode = audioCtx.createGain();
  oscillator.connect(gainNode);
  gainNode.connect(audioCtx.destination);

  if(ch == 1) {
    gainNode.gain.value = 0.05;
    oscillator.type = 'sine';
  } else if(ch == 2) {
    // el volumen
    gainNode.gain.value = 0.06;
//    oscillator.type = 'square';
    oscillator.type = 'sawtooth';
  } else if(ch == 3) {
    gainNode.gain.value = 0.1;
    oscillator.type = 'triangle';
  }
  oscillator.frequency.value = frequency; // value in hertz
  oscillator.onended = callback.bind(this, ch);
//  oscillator.start(0);
  oscillator.start(audioCtx.currentTime);
  oscillator.stop(audioCtx.currentTime + duration);
}


  /* searches a given label in a string array */
  function findLabel(arrayLines, label) {

    idx = -1;

    for (var i = 0; i < arrayLines.length; i++) { 
      line = arrayLines[i];
      if(line.startsWith(label)) {
//        console.log('lo encontró: ' + line + ' i: ' + i);
        idx = i;
      }
    }

    return idx;
  }


  var tempo = 60;


  function playMelody(ch) {
//    console.log('ch: ' + ch);

    if (notes[ch-1].length > 0){
      note = notes[ch-1].pop();
      // this is set ad-hoc and is probably wrong
      duration = 200/(note[1]*tempo);

//      console.log('duration: ' + duration + ' note: ' + note);
      playNote(note[0], duration, playMelody, ch);
    } else {
      if(vaPorLine[ch-1] < channelLines[ch-1].length ) {
        var txtPlay = channelLines[ch-1][vaPorLine[ch-1]];
//        console.log('----- txtPlay: ' + txtPlay);
        vaPorLine[ch-1]++;

        if(txtPlay.startsWith('PLAY')) {
          txtPlay = txtPlay.substring(4).trim();
//          console.log('play: ' + txtPlay);

          notes[ch-1] = parseMml(txtPlay, ch);
          playMelody(ch);

        } else if(txtPlay.startsWith('COUNTER')) {
//          console.log('counter: ' + txtPlay);
          txtCounter = txtPlay.substring(7).trim();
          counter[ch-1] = parseInt(txtCounter);
//          console.log('counter[' + (ch-1) + ']: ' + counter[ch-1]);

          playMelody(ch);

        } else if(txtPlay.endsWith(':')) {
//          console.log('label: ' + txtPlay);
          playMelody(ch);


        } else if(txtPlay.startsWith('TEMPO')) {
//          console.log('tempo: ' + txtPlay);

          txtTempo = txtPlay.substring(5).trim();
          tempo = parseInt(txtTempo,16);
//          console.log('tempo: ' + tempo);
          playMelody(ch);


        } else if(txtPlay.startsWith('VIBRATO')) {
//          console.log('vibrato: ' + txtPlay);
          playMelody(ch);

        } else if(txtPlay.startsWith('VOLUME')) {
//          console.log('vol: ' + txtPlay);
          playMelody(ch);

        } else if(txtPlay.startsWith('DUTYCYCLE')) {
//          console.log('duty: ' + txtPlay);
          playMelody(ch);

        } else if(txtPlay.startsWith('STEREO')) {
//          console.log('stereo: ' + txtPlay);
          playMelody(ch);

        } else if(txtPlay.startsWith('WAVETABLE')) {
//          console.log('wave: ' + txtPlay);
          playMelody(ch);

        } else if(txtPlay.startsWith('REPEAT')) {
//          console.log('repeat: ' + txtPlay + ' (counter: ' + counter[ch-1] + ')');
          label = txtPlay.substring(6).trim();
          
          if(counter[ch-1] > 1) {
            idx = findLabel(channelLines[ch-1], label);
            if(idx != -1) {
              vaPorLine[ch-1] = idx+1;
            } else {
              console.log('label not found :(');
            }

            counter[ch-1]--;
          }

          playMelody(ch);

        } else if(txtPlay.startsWith('JUMPIF')) {
//          console.log('jump if: ' + txtPlay);
          line = txtPlay.trim();
          args = txtPlay.split(' ');
          cant = parseInt(args[1]);
          label = args[2];


          if(counter[ch-1] == cant) {
            idx = findLabel(channelLines[ch-1], label);
            if(idx != -1) {
              vaPorLine[ch-1] = idx+1;
            } else {
              console.log('label not found :(');
            }
          }
          
          playMelody(ch);

        } else if(txtPlay.startsWith('JUMP')) {
//          console.log('jump: ' + txtPlay);
          label = txtPlay.substring(4).trim();

          idx = findLabel(channelLines[ch-1], label);
          if(idx != -1) {
            vaPorLine[ch-1] = idx;
          } else {
            console.log('label not found :(');
          }
          
          playMelody(ch);


        } else if(txtPlay.trim().length == 0) {
//          console.log('empty line');
          playMelody(ch);

        } else if(txtPlay.trim() == 'END') {

//          console.log('END');
          playMelody(ch);

        } else {
//          console.log('unknown line: ' + txtPlay);
        }


      }

    }
  }

    function parseMml(txtCancion, channel) {

      var listNotes = [];
      var listINotes = [];

      var dicPos = {'c':0, 'd':2, 'e':4, 'f':5, 'g':7, 'a':9, 'b':11, 'r':-1, 'w':-1, 'o':-1, '<':-1, '>':-1};

      // creo que esto no está perfecto
//      var dicLength = {'0':1, '1':4/3, '2':2, '4':8/3, '5':4, '7':16/3, '8':8, '9':32/3, '10':16, '11':64/3, '12':32, '13':32};

      // the length of each music note (whole, half, quarter, etc...)
      dicLength = {};
      var musicNoteDurations = [0x60, 0x48, 0x30, 0x20, 0x24, 0x18, 0x10, 0x12, 0x0c, 0x08, 0x06, 0x04, 0x03];
      for(let i=0; i<musicNoteDurations.length; i++) {
        dicLength[i] = 0x60/musicNoteDurations[i];
      }

/*
      var musicNoteFrequencies = [
        0x802c, 0x809d, 0x8107, 0x816b, 0x81c9, 0x8223, 0x8277, 0x82c7, 0x8312, 0x8358, 0x839b, 0x83da,
        0x8416, 0x844e, 0x8483, 0x84b5, 0x84e5, 0x8511, 0x853b, 0x8563, 0x8589, 0x85ac, 0x85ce, 0x85ed, 
        0x860b, 0x8627, 0x8642, 0x865b, 0x8672, 0x8689, 0x869e, 0x86b2, 0x86c4, 0x86d6, 0x86e7, 0x86f7, 
        0x8706, 0x8714, 0x8721, 0x872d, 0x8739, 0x8744, 0x874f, 0x8759, 0x8762, 0x876b, 0x8773, 0x877b, 
        0x8783, 0x878a, 0x8790, 0x8797, 0x879d, 0x87a2, 0x87a7, 0x87ac, 0x87b1, 0x87b6, 0x87ba, 0x87be, 
        0x87c1, 0x87c5, 0x87c8, 0x87cb, 0x87ce, 0x87d1, 0x87d4, 0x87d6, 0x87d9, 0x87db, 0x87dd, 0x87df,
        0x87e1, 0x87e2, 0x87e4, 0x87e6, 0x87e7, 0x87e9, 0x87ea, 0x87eb, 0x87ec, 0x87ed, 0x87ee, 0x87ef, 
        0x87f0
      ];

      for(let i=0; i<10; i++) {
//        var f0 = 440;
        var f0 = 65.406;
        var a = Math.pow(2, 1/12);
        n = i;
        var fn = f0 * Math.pow(a,n);

        console.log('n: ' + n + ' fn: ' + fn + ' freq: ' + musicNoteFrequencies[i]);
      }
*/

      // la nota actual
      currentNote = '';
      currentAccident = '';
      currentTilde = '';
      currentLength = '';
      currentINote = 0;

      for(let i=0; i < txtCancion.length; i++) {
        chara = txtCancion.charAt(i);
//        console.log('chara: ' + chara);
        // si es una nota musical
        if(['c','d','e','f','g','a','b','r','w','o','<','>'].indexOf(chara) >= 0) { 

          idxNote = dicPos[chara];

//          console.log('anterior: ' + currentNote + currentTilde + currentAccident + currentLength);
          if(currentNote != '') {
            listNotes.push([currentNote, currentTilde, currentAccident, parseInt(currentLength)]);
            listINotes.push([currentNote, currentINote, /*dicLength[currentLength]*/parseInt(currentLength)]);
          }

          if(chara != 'w') {
            // indico que es la nota actual
            currentNote = chara;
            currentINote = idxNote;

          }
          // por el momento no tiene accidente (bemol,sostenido)
          currentAccident = '';
          // ni tampo tilde (lo toca una octava mas alto)
          currentTilde = '';
          // ni tampoco length
          currentLength = '';


        // si es un tilde
        } else if(chara == "'") {
          // lo indico
          currentTilde = "'";
          // subo una octava
          currentINote += 12;

        // si es un accidente
        } else if(chara == '#') {
          // lo indico
          currentAccident = '#';
          // subo un half-step
          currentINote += 1;


        } else if(['0','1','2','3','4','5','6','7','8','9'].indexOf(chara) >= 0) {
          currentLength += chara;
        }
      }
      listNotes.push([currentNote, currentTilde, currentAccident, parseInt(currentLength)]);
      listINotes.push([currentNote, currentINote, /*dicLength[currentLength]*/parseInt(currentLength)]);

      var notas = [];

      for(let note of listINotes) {
//        console.log(note);

        // la frecuencia de base es A = 440Hz
        var f0 = 440;
        var a = Math.pow(2, 1/12);
        var n = 0;
        // la distancia en semitonos a A.
        n = note[1]+12*(currentOctave[channel-1]+1) - (9+12*4);

        var fn = f0 * Math.pow(a,n);
//        console.log('fn: ' + fn);

        // si la nota es una pausa
        if(note[0] == 'r') {
          // le pongo frecuencia cero
          fn = 0;
        }

        // si la nota es subir octava
        if(note[0] == '>') {

          currentOctave[channel-1] += 1;

        } else if(note[0] == '<') {

          currentOctave[channel-1] -= 1;

        } else if(note[0] == 'o') {

          currentOctave[channel-1] = note[2];


        } else {
          var length = note[2];
          var valLength = dicLength[length];
//          console.log('length: ' + length + ' valLength: ' + valLength);
          notas.push( [fn, valLength] );
        }

      }

      notas.reverse();
      return notas;

    }




    function playSelectedSong() {
      var comboSong = document.getElementById('comboSong');
      var selectedSong = comboSong.value;
      console.log('selectedSong: ' + selectedSong);

      // si eligió una canción del combo
      if(selectedSong != '') {
        // la seteamos
        playSong(selectedSong);
      }
    }

function setSong(nroSong) {

  channel2Lines = audio[nroSong][2];
  channel1Lines = audio[nroSong][1];
  channel3Lines = audio[nroSong][3];

  // los renglones a interpretar del canal
  channelLines = [];
  channelLines.push(channel1Lines);
  channelLines.push(channel2Lines);
  channelLines.push(channel3Lines);

  // current line to interpret of each channel
  vaPorLine = [];
  vaPorLine.push(0);
  vaPorLine.push(0);
  vaPorLine.push(0);

  // notes to be played of each channel;
  notes = [];
  notes.push([]);
  notes.push([]);
  notes.push([]);

  // la octava actual (de cada channel)
  currentOctave = [];
  currentOctave.push(4);
  currentOctave.push(4);
  currentOctave.push(4);

  // inicializo el contador de loops de cada canal (en 256)
  counter = [];
  counter.push(0xff);
  counter.push(0xff);
  counter.push(0xff);

}

    function playSong(selectedSong) {

      if(selectedSong == 0x00) {
        stopSong();
      } else {
        // la seteamos
        setSong(selectedSong);

        // reset the audio context (stop if it was playing sounds)
        audioCtx.close();
        audioCtx  = new (window.AudioContext || window.webkitAudioContext)();

        vaPorLine[1-1] = 0;
        // toco la melodía
        playMelody(1);

        vaPorLine[2-1] = 0;
        playMelody(2);

        vaPorLine[3-1] = 0;
        playMelody(3);
      }

    }

    function stopSong() {

      // reset the audio context (stop if it was playing sounds)
      audioCtx.close();
      audioCtx  = new (window.AudioContext || window.webkitAudioContext)();

    }

