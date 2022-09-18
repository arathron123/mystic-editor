

// This file is copied to the encoding folder along with scripts.html and scripts/jscripts.js
// (it is not intended to be used separately) 


/* convierte a un integer en un string hex (ej: toHex(0xf0,3) = "0f0" */
function toHex(val, pad) {
  hexs = val.toString(16).padStart(pad, '0');
  return hexs;
}

// inicializo los flags 0x00-0x7f en False
var flags = Array(0x80).fill(false);
//flags[0x01] = true;

// inicializo el inventario vacío
var inventory = [];
// no tenemos nada equipado a mano
var at_hand = null;
// ni tampoco activamos ni desactivamos nada
var triggered_on_by = null;
var triggered_off_by = null;

/*
for(let i=0; i<flags.length; i++) {
  flag = flags[i];
  console.log('flag: ' + i.toString(16) + ',' + flag);
}
*/

function if_flags(params) {
  val = true;
  // recorro los parametros
  for(let param of params) {
    // si se cumplen todos es verdad
    val = val && flags[param];
  }
  return val;
}

function if_hand(params) {
  val = false;
  // recorro los parametros
  for(let param of params) {
    // si alguno está a mano es verdad
    val = val || at_hand == param;
  }
  return val;
}

function if_inventory(params) {
  val = true;
  // recorro los parámetros
  for(let param of params) {
    // si están todos en el inventario es verdad
    val = val && inventory.includes(param);
  }
  return val;
}

function if_triggered_on_by(params) {
  val = false;
  // recorro los parámetros
  for(let param of params) {
    // si lo activó alguno está bien
    val = val || triggered_on_by == param;
  }
  return val;
}

function if_triggered_off_by(params) {
  val = false;
  // recorro los parámetros
  for(let param of params) {
    // si lo desactivó alguno está bien
    val = val || triggered_off_by == param;
  }
  return val;
}


var personajes = ['extra1', 'extra2', 'extra3', 'extra4', 'extra5', 'extra6', 'extra7', 'hero', 'partner'];
/* extras */
function extraiStepForward(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'StepForward');
}
function extraiStepBack(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'StepBack');
}
function extraiStepLeft(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'StepLeft');
}
function extraiStepRight(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'StepRight');
}
function extraiLookNorth(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'LookNorth');
}
function extraiLookSouth(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'LookSouth');
}
function extraiLookEast(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'LookEast');
}
function extraiLookWest(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'LookWest');
}
function extraiRemove(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'Remove');
}
function extraiTeleport(i, xx,yy) {
  var personaje = personajes[i-1];
  console.log(personaje + 'Teleport(0x' + toHex(xx, 2) + ', 0x' + toHex(yy, 2) + ')');
}
function extraiWalkFastSpeed(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'WalkFastSpeed');
}
function extraiWalkNormalSpeed(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'WalkNormalSpeed');
}
function extraiNoseC(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'NoseC');
}
function extraiNoseD(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'NoseD');
}
function extraiNoseE(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'NoseE');
}
function extraiNoseF(i) {
  var personaje = personajes[i-1];
  console.log(personaje + 'NoseF');
}

/* extra 1 */
function extra1StepForward() {
  extraiStepForward(1);
}
function extra1StepBack() {
  extraiStepBack(1);
}
function extra1StepLeft() {
  extraiStepLeft(1);
}
function extra1StepRight() {
  extraiStepRight(1);
}
function extra1LookNorth() {
  extraiLookNorth(1);
}
function extra1LookSouth() {
  extraiLookSouth(1);
}
function extra1LookEast() {
  extraiLookEast(1);
}
function extra1LookWest() {
  extraiLookWest(1);
}
function extra1Remove() {
  extraiRemove(1);
}
function extra1Teleport(xx,yy) {
  extraiTeleport(1,xx,yy);
}
function extra1WalkFastSpeed() {
  extraiWalkFastSpeed(1);
}
function extra1WalkNormalSpeed() {
  extraiWalkNormalSpeed(1);
}
function extra1NoseC() {
  extraiNoseC(1);
}
function extra1NoseD() {
  extraiNoseD(1);
}
function extra1NoseE() {
  extraiNoseE(1);
}
function extra1NoseF() {
  extraiNoseF(1);
}
/* extra 2 */
function extra2StepForward() {
  extraiStepForward(2);
}
function extra2StepBack() {
  extraiStepBack(2);
}
function extra2StepLeft() {
  extraiStepLeft(2);
}
function extra2StepRight() {
  extraiStepRight(2);
}
function extra2LookNorth() {
  extraiLookNorth(2);
}
function extra2LookSouth() {
  extraiLookSouth(2);
}
function extra2LookEast() {
  extraiLookEast(2);
}
function extra2LookWest() {
  extraiLookWest(2);
}
function extra2Remove() {
  extraiRemove(2);
}
function extra2Teleport(xx,yy) {
  extraiTeleport(2,xx,yy);
}
function extra2WalkFastSpeed() {
  extraiWalkFastSpeed(2);
}
function extra2WalkNormalSpeed() {
  extraiWalkNormalSpeed(2);
}
function extra2NoseC() {
  extraiNoseC(2);
}
function extra2NoseD() {
  extraiNoseD(2);
}
function extra2NoseE() {
  extraiNoseE(2);
}
function extra2NoseF() {
  extraiNoseF(2);
}
/* extra 3 */
function extra3StepForward() {
  extraiStepForward(3);
}
function extra3StepBack() {
  extraiStepBack(3);
}
function extra3StepLeft() {
  extraiStepLeft(3);
}
function extra3StepRight() {
  extraiStepRight(3);
}
function extra3LookNorth() {
  extraiLookNorth(3);
}
function extra3LookSouth() {
  extraiLookSouth(3);
}
function extra3LookEast() {
  extraiLookEast(3);
}
function extra3LookWest() {
  extraiLookWest(3);
}
function extra3Remove() {
  extraiRemove(3);
}
function extra3Teleport(xx,yy) {
  extraiTeleport(3,xx,yy);
}
function extra3WalkFastSpeed() {
  extraiWalkFastSpeed(3);
}
function extra3WalkNormalSpeed() {
  extraiWalkNormalSpeed(3);
}
function extra3NoseC() {
  extraiNoseC(3);
}
function extra3NoseD() {
  extraiNoseD(3);
}
function extra3NoseE() {
  extraiNoseE(3);
}
function extra3NoseF() {
  extraiNoseF(3);
}
/* extra 4 */
function extra4StepForward() {
  extraiStepForward(4);
}
function extra4StepBack() {
  extraiStepBack(4);
}
function extra4StepLeft() {
  extraiStepLeft(4);
}
function extra4StepRight() {
  extraiStepRight(4);
}
function extra4LookNorth() {
  extraiLookNorth(4);
}
function extra4LookSouth() {
  extraiLookSouth(4);
}
function extra4LookEast() {
  extraiLookEast(4);
}
function extra4LookWest() {
  extraiLookWest(4);
}
function extra4Remove() {
  extraiRemove(4);
}
function extra4Teleport(xx,yy) {
  extraiTeleport(4,xx,yy);
}
function extra4WalkFastSpeed() {
  extraiWalkFastSpeed(4);
}
function extra4WalkNormalSpeed() {
  extraiWalkNormalSpeed(4);
}
function extra4NoseC() {
  extraiNoseC(4);
}
function extra4NoseD() {
  extraiNoseD(4);
}
function extra4NoseE() {
  extraiNoseE(4);
}
function extra4NoseF() {
  extraiNoseF(4);
}
/* extra 5 */
function extra5StepForward() {
  extraiStepForward(5);
}
function extra5StepBack() {
  extraiStepBack(5);
}
function extra5StepLeft() {
  extraiStepLeft(5);
}
function extra5StepRight() {
  extraiStepRight(5);
}
function extra5LookNorth() {
  extraiLookNorth(5);
}
function extra5LookSouth() {
  extraiLookSouth(5);
}
function extra5LookEast() {
  extraiLookEast(5);
}
function extra5LookWest() {
  extraiLookWest(5);
}
function extra5Remove() {
  extraiRemove(5);
}
function extra5Teleport(xx,yy) {
  extraiTeleport(5,xx,yy);
}
function extra5WalkFastSpeed() {
  extraiWalkFastSpeed(5);
}
function extra5WalkNormalSpeed() {
  extraiWalkNormalSpeed(5);
}
function extra5NoseC() {
  extraiNoseC(5);
}
function extra5NoseD() {
  extraiNoseD(5);
}
function extra5NoseE() {
  extraiNoseE(5);
}
function extra5NoseF() {
  extraiNoseF(5);
}
/* extra 6 */
function extra6StepForward() {
  extraiStepForward(6);
}
function extra6StepBack() {
  extraiStepBack(6);
}
function extra6StepLeft() {
  extraiStepLeft(6);
}
function extra6StepRight() {
  extraiStepRight(6);
}
function extra6LookNorth() {
  extraiLookNorth(6);
}
function extra6LookSouth() {
  extraiLookSouth(6);
}
function extra6LookEast() {
  extraiLookEast(6);
}
function extra6LookWest() {
  extraiLookWest(6);
}
function extra6Remove() {
  extraiRemove(6);
}
function extra6Teleport(xx,yy) {
  extraiTeleport(6,xx,yy);
}
function extra6WalkFastSpeed() {
  extraiWalkFastSpeed(6);
}
function extra6WalkNormalSpeed() {
  extraiWalkNormalSpeed(6);
}
function extra6NoseC() {
  extraiNoseC(6);
}
function extra6NoseD() {
  extraiNoseD(6);
}
function extra6NoseE() {
  extraiNoseE(6);
}
function extra6NoseF() {
  extraiNoseF(6);
}
/* extra 7 */
function extra7StepForward() {
  extraiStepForward(7);
}
function extra7StepBack() {
  extraiStepBack(7);
}
function extra7StepLeft() {
  extraiStepLeft(7);
}
function extra7StepRight() {
  extraiStepRight(7);
}
function extra7LookNorth() {
  extraiLookNorth(7);
}
function extra7LookSouth() {
  extraiLookSouth(7);
}
function extra7LookEast() {
  extraiLookEast(7);
}
function extra7LookWest() {
  extraiLookWest(7);
}
function extra7Remove() {
  extraiRemove(7);
}
function extra7Teleport(xx,yy) {
  extraiTeleport(7,xx,yy);
}
function extra7WalkFastSpeed() {
  extraiWalkFastSpeed(7);
}
function extra7WalkNormalSpeed() {
  extraiWalkNormalSpeed(7);
}
function extra7NoseC() {
  extraiNoseC(7);
}
function extra7NoseD() {
  extraiNoseD(7);
}
function extra7NoseE() {
  extraiNoseE(7);
}
function extra7NoseF() {
  extraiNoseF(7);
}
/* hero (extra 8) */
function heroStepForward() {
  extraiStepForward(8);
}
function heroStepBack() {
  extraiStepBack(8);
}
function heroStepLeft() {
  extraiStepLeft(8);
}
function heroStepRight() {
  extraiStepRight(8);
}
function heroLookNorth() {
  extraiLookNorth(8);
}
function heroLookSouth() {
  extraiLookSouth(8);
}
function heroLookEast() {
  extraiLookEast(8);
}
function heroLookWest() {
  extraiLookWest(8);
}
function heroRemove() {
  extraiRemove(8);
}
function heroTeleport(xx,yy) {
  extraiTeleport(8,xx,yy);
}
function heroWalkFastSpeed() {
  extraiWalkFastSpeed(8);
}
function heroWalkNormalSpeed() {
  extraiWalkNormalSpeed(8);
}
function heroNoseC() {
  extraiNoseC(8);
}
function heroNoseD() {
  extraiNoseD(8);
}
function heroNoseE() {
  extraiNoseE(8);
}
function heroNoseF() {
  extraiNoseF(8);
}
/* partner (extra 9) */
function partnerStepForward() {
  extraiStepForward(9);
}
function partnerStepBack() {
  extraiStepBack(9);
}
function partnerStepLeft() {
  extraiStepLeft(9);
}
function partnerStepRight() {
  extraiStepRight(9);
}
function partnerLookNorth() {
  extraiLookNorth(9);
}
function partnerLookSouth() {
  extraiLookSouth(9);
}
function partnerLookEast() {
  extraiLookEast(9);
}
function partnerLookWest() {
  extraiLookWest(9);
}
function partnerRemove() {
  extraiRemove(9);
}
function partnerTeleport(xx,yy) {
  extraiTeleport(9,xx,yy);
}
function partnerWalkFastSpeed() {
  extraiWalkFastSpeed(9);
}
function partnerWalkNormalSpeed() {
  extraiWalkNormalSpeed(9);
}
function partnerNoseC() {
  extraiNoseC(9);
}
function partnerNoseD() {
  extraiNoseD(9);
}
function partnerNoseE() {
  extraiNoseE(9);
}
function partnerNoseF() {
  extraiNoseF(9);
}


function walkingAsChocobo() {
  console.log('walkingAsChocobo');
}
function walkingAsChocobotLand() {
  console.log('walkingAsChocobotLand');
}
function walkingAsChocobotWater() {
  console.log('walkingAsChocobotWater');
}
function walkingAsWagon() {
  console.log('walkingAsWagon');
}
function walkingAsNormal() {
  console.log('walkingAsNormal');
}
function walkingAsFalling() {
  console.log('walkingAsFalling');
}
function walkingAsDead() {
  console.log('walkingAsDead');
}

function checkIfCurrentMapHasSmallmap() {
  console.log('checkIfCurrentMapHasSmallmap');
}

function clearKilledAllRoom() {
  console.log('clearKilledAllRoom');
}

function smallmapOpen() {
  console.log('smallmapOpen');
}
function smallmapIdle() {
  console.log('smallmapIdle');
}
function smallmapClose() {
  console.log('smallmapClose');
}

function openChest() {
  console.log('openChest');
}

function drawSprite(nn,xx,yy) {
  console.log('drawSprite nn=' + toHex(nn, 2) + ' xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

function attackEffect(tt,xx,yy) {
  console.log('attackEffect tt=' + toHex(nn, 2) + ' xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

function letterboxEffect() {
  console.log('letterboxEffect');
}
function fadeInEffect() {
  console.log('fadeInEffect');
}
function fadeOutEffect() {
  console.log('fadeOutEffect');
}
function washOutEffect() {
  console.log('washOutEffect');
}
function eyeblinkEffect() {
  console.log('eyeblinkEffect');
}

function recoverHp() {
  console.log('recoverHp');
}
function recoverMp() {
  console.log('recoverMp');
}

function healDisease(val) {
  console.log('healDisease ' + toHex(val, 2));
}
function nop() {
  console.log('nop');
}
function disease(val) {
  console.log('disease ' + toHex(val, 2));
}

function setFlags72To77(val) {
  console.log('setFlags72To77 ' + toHex(val, 2));
}

function inputNames() {
  console.log('inputNames');
}
function randomize7E7F() {
  console.log('randomize7E7F');
}
function resetGame() {
  console.log('resetGame');
}

function setChest1Script(val) {
  console.log('setChest1Script ' + toHex(val, 2));
}
function setChest2Script(val) {
  console.log('setChest2Script ' + toHex(val, 2));
}
function setChest3Script(val) {
  console.log('setChest3Script ' + toHex(val, 2));
}

function stopInput() {
  console.log('stopInput');
}

function increaseGold(val) {
  console.log('increaseGold ' + toHex(val, 2));
}
function decreaseGold(val) {
  console.log('decreaseGold ' + toHex(val, 2));
}
function increaseExp(val) {
  console.log('increaseExp ' + toHex(val, 2));
}
function decreaseExp(val) {
  console.log('decreaseExp ' + toHex(val, 2));
}

function pickItem(val) {
  console.log('pickItem ' + toHex(val, 2));
}
function dropItem(val) {
  console.log('dropItem ' + toHex(val, 2));
}
function pickMagic(val) {
  console.log('pickMagic ' + toHex(val, 2));
}
function dropMagic(val) {
  console.log('dropMagic ' + toHex(val, 2));
}
function pickWeapon(val) {
  console.log('pickWeapon ' + toHex(val, 2));
}
function dropWeapon(val) {
  console.log('dropWeapon ' + toHex(val, 2));
}

function flagOn(val) {
  console.log('flagOn ' + toHex(val, 2));
}
function flagOff(val) {
  console.log('flagOff ' + toHex(val, 2));
}

function textSpeedLock() {
  console.log('textSpeedLock');
}
function textSpeedUnlock() {
  console.log('textSpeedUnlock');
}

function consumeItem() {
  console.log('consumeItem');
}

function openDoorNorth() {
  console.log('openDoorNorth');
}
function closeDoorNorth() {
  console.log('closeDoorNorth');
}
function openDoorSouth() {
  console.log('openDoorSouth');
}
function closeDoorSouth() {
  console.log('closeDoorSouth');
}
function openDoorEast() {
  console.log('openDoorEast');
}
function closeDoorEast() {
  console.log('closeDoorEast');
}
function openDoorWest() {
  console.log('openDoorWest');
}
function closeDoorWest() {
  console.log('closeDoorWest');
}

function scrollSouth() {
  console.log('scrollSouth');
}
function scrollNorth() {
  console.log('scrollNorth');
}
function scrollLeft() {
  console.log('scrollLeft');
}
function scrollRight() {
  console.log('scrollRight');
}

function enterRoomScript() {
  console.log('enterRoomScript');
}
function exitRoomScript() {
  console.log('exitRoomScript');
}
function killedAllRoomScript() {
  console.log('killedAllRoomScript');
}

function nextRoom(xx,yy) {
  console.log('nextRoom xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

function teleport2(mm,bb,xx,yy) {
  console.log('teleporting2 to mm=' + toHex(mm, 2) + ' bb=' + toHex(bb, 2) + ' xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

function teleport(mm,bb,xx,yy) {
  console.log('teleporting to mm=' + toHex(mm, 2) + ' bb=' + toHex(bb, 2) + ' xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

function music(val) {
  console.log('setting music ' + toHex(val, 2));
}
function soundEffect(val) {
  console.log('playing sound effect ' + toHex(val, 2));
}

function shakeScreen() {
  console.log('shakeScreen');
}

function loadGrupoPersonaje(val) {
  console.log('loadGrupoPersonaje ' + toHex(val, 2));
}
function addPersonaje(val) {
  console.log('addPersonaje ' + toHex(val, 2));
}

function addBoss(val) {
  console.log('addBoss ' + toHex(val, 2));
}

function sleep(val) {
  console.log('sleeping: ' + toHex(val, 2));
}

function text(speech) {
  console.log('text: ' + speech);
}






