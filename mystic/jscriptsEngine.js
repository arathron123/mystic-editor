

// This file is copied to the encoding folder along with scripts.html and scripts/jscripts.js
// (it is not intended to be used separately) 


// default wait time in milliseconds
var defaultWait = 100;

// inicializo los flags 0x00-0x7f en False
var flags = Array(0x80).fill(false);
//flags[0x01] = true;

// inicializo el inventario vacío
var inventory = [];
// no tenemos nada equipado a mano
var at_hand = null;
// ni tampoco activamos ni desactivamos nada
var step_on_by = null;
var step_off_by = null;

/*
for(let i=0; i<flags.length; i++) {
  flag = flags[i];
  console.log('flag: ' + i.toString(16) + ',' + flag);
}
*/

/* convierte a un integer en un string hex (ej: toHex(0xf0,3) = "0f0" */
function toHex(val, pad) {
  hexs = val.toString(16).padStart(pad, '0');
  return hexs;
}


function cond_flags(params) {
  retVal = true;
  // recorro los parametros
  for(let param of params) {
    // si es positivo
    if(param >= 0) {
      val = flags[param];
    // sino, es negativo
    } else {
      // lo negamos
      val = !flags[~param];
    }
//    console.log('param: ' + param + ' val: ' + val);
    // si se cumplen todos es verdad
    retVal = retVal && val;
  }
  return retVal;
}


function cond_hand(params) {
  retVal = false;
  // recorro los parametros
  for(let param of params) {
    // si alguno está a mano es verdad
    retVal = retVal || at_hand == param;
  }
  return retVal;
}

function cond_inventory(params) {
  retVal = true;
  // recorro los parámetros
  for(let param of params) {
    // si están todos en el inventario es verdad
    retVal = retVal && inventory.includes(param);
  }
  return retVal;
}

function cond_step_on_by(params) {
  retVal = false;
  // recorro los parámetros
  for(let param of params) {
    // si lo activó alguno está bien
    retVal = retVal || step_on_by == param;
  }
  return retVal;
}

function cond_step_off_by(params) {
  retVal = false;
  // recorro los parámetros
  for(let param of params) {
    // si lo desactivó alguno está bien
    retVal = retVal || step_off_by == param;
  }
  return retVal;
}



const awaitSleep = ms => new Promise(r => setTimeout(r, ms));





async function getPersonaje(i) {
  var personajes = ['extra1', 'extra2', 'extra3', 'extra4', 'extra5', 'extra6', 'extra7', 'hero', 'partner'];
  return personajes[i];
}

/* extras */
async function extraiStepForward(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'StepForward');
}
async function extraiStepBack(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'StepBack');
}
async function extraiStepLeft(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'StepLeft');
}
async function extraiStepRight(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'StepRight');
}
async function extraiLookNorth(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'LookNorth');
}
async function extraiLookSouth(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'LookSouth');
}
async function extraiLookEast(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'LookEast');
}
async function extraiLookWest(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'LookWest');
}
async function extraiRemove(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'Remove');
}
async function extraiTeleport(i, xx,yy) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'Teleport(0x' + toHex(xx, 2) + ', 0x' + toHex(yy, 2) + ')');
}
async function extraiWalkFastSpeed(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'WalkFastSpeed');
}
async function extraiWalkNormalSpeed(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'WalkNormalSpeed');
}
async function extraiNoseC(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'NoseC');
}
async function extraiNoseD(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'NoseD');
}
async function extraiNoseE(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'NoseE');
}
async function extraiNoseF(i) {
  await awaitSleep(defaultWait);
  const personaje = await getPersonaje(i-1);
  console.log(personaje + 'NoseF');
}

/* extra 1 */
async function extra1StepForward() {
  await extraiStepForward(1);
}
async function extra1StepBack() {
  await extraiStepBack(1);
}
async function extra1StepLeft() {
  await extraiStepLeft(1);
}
async function extra1StepRight() {
  await extraiStepRight(1);
}
async function extra1LookNorth() {
  await extraiLookNorth(1);
}
async function extra1LookSouth() {
  await extraiLookSouth(1);
}
async function extra1LookEast() {
  await extraiLookEast(1);
}
async function extra1LookWest() {
  await extraiLookWest(1);
}
async function extra1Remove() {
  await extraiRemove(1);
}
async function extra1Teleport(xx,yy) {
  await extraiTeleport(1,xx,yy);
}
async function extra1WalkFastSpeed() {
  await extraiWalkFastSpeed(1);
}
async function extra1WalkNormalSpeed() {
  await extraiWalkNormalSpeed(1);
}
async function extra1NoseC() {
  await extraiNoseC(1);
}
async function extra1NoseD() {
  await extraiNoseD(1);
}
async function extra1NoseE() {
  await extraiNoseE(1);
}
async function extra1NoseF() {
  await extraiNoseF(1);
}
/* extra 2 */
async function extra2StepForward() {
  await extraiStepForward(2);
}
async function extra2StepBack() {
  await extraiStepBack(2);
}
async function extra2StepLeft() {
  await extraiStepLeft(2);
}
async function extra2StepRight() {
  await extraiStepRight(2);
}
async function extra2LookNorth() {
  await extraiLookNorth(2);
}
async function extra2LookSouth() {
  await extraiLookSouth(2);
}
async function extra2LookEast() {
  await extraiLookEast(2);
}
async function extra2LookWest() {
  await extraiLookWest(2);
}
async function extra2Remove() {
  await extraiRemove(2);
}
async function extra2Teleport(xx,yy) {
  await extraiTeleport(2,xx,yy);
}
async function extra2WalkFastSpeed() {
  await extraiWalkFastSpeed(2);
}
async function extra2WalkNormalSpeed() {
  await extraiWalkNormalSpeed(2);
}
async function extra2NoseC() {
  await extraiNoseC(2);
}
async function extra2NoseD() {
  await extraiNoseD(2);
}
async function extra2NoseE() {
  await extraiNoseE(2);
}
async function extra2NoseF() {
  await extraiNoseF(2);
}
/* extra 3 */
async function extra3StepForward() {
  await extraiStepForward(3);
}
async function extra3StepBack() {
  await extraiStepBack(3);
}
async function extra3StepLeft() {
  await extraiStepLeft(3);
}
async function extra3StepRight() {
  await extraiStepRight(3);
}
async function extra3LookNorth() {
  await extraiLookNorth(3);
}
async function extra3LookSouth() {
  await extraiLookSouth(3);
}
async function extra3LookEast() {
  await extraiLookEast(3);
}
async function extra3LookWest() {
  await extraiLookWest(3);
}
async function extra3Remove() {
  await extraiRemove(3);
}
async function extra3Teleport(xx,yy) {
  await extraiTeleport(3,xx,yy);
}
async function extra3WalkFastSpeed() {
  await extraiWalkFastSpeed(3);
}
async function extra3WalkNormalSpeed() {
  await extraiWalkNormalSpeed(3);
}
async function extra3NoseC() {
  await extraiNoseC(3);
}
async function extra3NoseD() {
  await extraiNoseD(3);
}
async function extra3NoseE() {
  await extraiNoseE(3);
}
async function extra3NoseF() {
  await extraiNoseF(3);
}
/* extra 4 */
async function extra4StepForward() {
  await extraiStepForward(4);
}
async function extra4StepBack() {
  await extraiStepBack(4);
}
async function extra4StepLeft() {
  await extraiStepLeft(4);
}
async function extra4StepRight() {
  await extraiStepRight(4);
}
async function extra4LookNorth() {
  await extraiLookNorth(4);
}
async function extra4LookSouth() {
  await extraiLookSouth(4);
}
async function extra4LookEast() {
  await extraiLookEast(4);
}
async function extra4LookWest() {
  await extraiLookWest(4);
}
async function extra4Remove() {
  await extraiRemove(4);
}
async function extra4Teleport(xx,yy) {
  await extraiTeleport(4,xx,yy);
}
async function extra4WalkFastSpeed() {
  await extraiWalkFastSpeed(4);
}
async function extra4WalkNormalSpeed() {
  await extraiWalkNormalSpeed(4);
}
async function extra4NoseC() {
  await extraiNoseC(4);
}
async function extra4NoseD() {
  await extraiNoseD(4);
}
async function extra4NoseE() {
  await extraiNoseE(4);
}
async function extra4NoseF() {
  await extraiNoseF(4);
}
/* extra 5 */
async function extra5StepForward() {
  await extraiStepForward(5);
}
async function extra5StepBack() {
  await extraiStepBack(5);
}
async function extra5StepLeft() {
  await extraiStepLeft(5);
}
async function extra5StepRight() {
  await extraiStepRight(5);
}
async function extra5LookNorth() {
  await extraiLookNorth(5);
}
async function extra5LookSouth() {
  await extraiLookSouth(5);
}
async function extra5LookEast() {
  await extraiLookEast(5);
}
async function extra5LookWest() {
  await extraiLookWest(5);
}
async function extra5Remove() {
  await extraiRemove(5);
}
async function extra5Teleport(xx,yy) {
  await extraiTeleport(5,xx,yy);
}
async function extra5WalkFastSpeed() {
  await extraiWalkFastSpeed(5);
}
async function extra5WalkNormalSpeed() {
  await extraiWalkNormalSpeed(5);
}
async function extra5NoseC() {
  await extraiNoseC(5);
}
async function extra5NoseD() {
  await extraiNoseD(5);
}
async function extra5NoseE() {
  await extraiNoseE(5);
}
async function extra5NoseF() {
  await extraiNoseF(5);
}
/* extra 6 */
async function extra6StepForward() {
  await extraiStepForward(6);
}
async function extra6StepBack() {
  await extraiStepBack(6);
}
async function extra6StepLeft() {
  await extraiStepLeft(6);
}
async function extra6StepRight() {
  await extraiStepRight(6);
}
async function extra6LookNorth() {
  await extraiLookNorth(6);
}
async function extra6LookSouth() {
  await extraiLookSouth(6);
}
async function extra6LookEast() {
  await extraiLookEast(6);
}
async function extra6LookWest() {
  await extraiLookWest(6);
}
async function extra6Remove() {
  await extraiRemove(6);
}
async function extra6Teleport(xx,yy) {
  await extraiTeleport(6,xx,yy);
}
async function extra6WalkFastSpeed() {
  await extraiWalkFastSpeed(6);
}
async function extra6WalkNormalSpeed() {
  await extraiWalkNormalSpeed(6);
}
async function extra6NoseC() {
  await extraiNoseC(6);
}
async function extra6NoseD() {
  await extraiNoseD(6);
}
async function extra6NoseE() {
  await extraiNoseE(6);
}
async function extra6NoseF() {
  await extraiNoseF(6);
}
/* extra 7 */
async function extra7StepForward() {
  await extraiStepForward(7);
}
async function extra7StepBack() {
  await extraiStepBack(7);
}
async function extra7StepLeft() {
  await extraiStepLeft(7);
}
async function extra7StepRight() {
  await extraiStepRight(7);
}
async function extra7LookNorth() {
  await extraiLookNorth(7);
}
async function extra7LookSouth() {
  await extraiLookSouth(7);
}
async function extra7LookEast() {
  await extraiLookEast(7);
}
async function extra7LookWest() {
  await extraiLookWest(7);
}
async function extra7Remove() {
  await extraiRemove(7);
}
async function extra7Teleport(xx,yy) {
  await extraiTeleport(7,xx,yy);
}
async function extra7WalkFastSpeed() {
  await extraiWalkFastSpeed(7);
}
async function extra7WalkNormalSpeed() {
  await extraiWalkNormalSpeed(7);
}
async function extra7NoseC() {
  await extraiNoseC(7);
}
async function extra7NoseD() {
  await extraiNoseD(7);
}
async function extra7NoseE() {
  await extraiNoseE(7);
}
async function extra7NoseF() {
  await extraiNoseF(7);
}
/* hero (extra 8) */
async function heroStepForward() {
  await extraiStepForward(8);
}
async function heroStepBack() {
  await extraiStepBack(8);
}
async function heroStepLeft() {
  await extraiStepLeft(8);
}
async function heroStepRight() {
  await extraiStepRight(8);
}
async function heroLookNorth() {
  await extraiLookNorth(8);
}
async function heroLookSouth() {
  await extraiLookSouth(8);
}
async function heroLookEast() {
  await extraiLookEast(8);
}
async function heroLookWest() {
  await extraiLookWest(8);
}
async function heroRemove() {
  await extraiRemove(8);
}
async function heroTeleport(xx,yy) {
  await extraiTeleport(8,xx,yy);
}
async function heroWalkFastSpeed() {
  await extraiWalkFastSpeed(8);
}
async function heroWalkNormalSpeed() {
  await extraiWalkNormalSpeed(8);
}
async function heroNoseC() {
  await extraiNoseC(8);
}
async function heroNoseD() {
  await extraiNoseD(8);
}
async function heroNoseE() {
  await extraiNoseE(8);
}
async function heroNoseF() {
  await extraiNoseF(8);
}
/* partner (extra 9) */
async function partnerStepForward() {
  await extraiStepForward(9);
}
async function partnerStepBack() {
  await extraiStepBack(9);
}
async function partnerStepLeft() {
  await extraiStepLeft(9);
}
async function partnerStepRight() {
  await extraiStepRight(9);
}
async function partnerLookNorth() {
  await extraiLookNorth(9);
}
async function partnerLookSouth() {
  await extraiLookSouth(9);
}
async function partnerLookEast() {
  await extraiLookEast(9);
}
async function partnerLookWest() {
  await extraiLookWest(9);
}
async function partnerRemove() {
  await extraiRemove(9);
}
async function partnerTeleport(xx,yy) {
  await extraiTeleport(9,xx,yy);
}
async function partnerWalkFastSpeed() {
  await extraiWalkFastSpeed(9);
}
async function partnerWalkNormalSpeed() {
  await extraiWalkNormalSpeed(9);
}
/* this one is partnerSetPersonaje */
/*
async function partnerNoseC() {
  await extraiNoseC(9);
}
*/
async function partnerSetPersonaje(nn) {
  await awaitSleep(defaultWait);
  console.log('partnerSetPersonaje(' + nn + ');');

}

async function partnerNoseD() {
  await extraiNoseD(9);
}
async function partnerNoseE() {
  await extraiNoseE(9);
}
async function partnerNoseF() {
  await extraiNoseF(9);
}


async function walkingAsChocobo() {
  await awaitSleep(defaultWait);
  console.log('walkingAsChocobo');
}
async function walkingAsChocobotLand() {
  await awaitSleep(defaultWait);
  console.log('walkingAsChocobotLand');
}
async function walkingAsChocobotWater() {
  await awaitSleep(defaultWait);
  console.log('walkingAsChocobotWater');
}
async function walkingAsWagon() {
  await awaitSleep(defaultWait);
  console.log('walkingAsWagon');
}
async function walkingAsNormal() {
  await awaitSleep(defaultWait);
  console.log('walkingAsNormal');
}
async function walkingAsFalling() {
  await awaitSleep(defaultWait);
  console.log('walkingAsFalling');
}
async function walkingAsDead() {
  await awaitSleep(defaultWait);
  console.log('walkingAsDead');
}

async function checkIfCurrentMapHasSmallmap() {
  await awaitSleep(defaultWait);
  console.log('checkIfCurrentMapHasSmallmap');
}

async function clearKilledAllRoom() {
  await awaitSleep(defaultWait);
  console.log('clearKilledAllRoom');
}

async function smallmapOpen() {
  await awaitSleep(defaultWait);
  console.log('smallmapOpen');
}
async function smallmapIdle() {
  await awaitSleep(defaultWait);
  console.log('smallmapIdle');
}
async function smallmapClose() {
  await awaitSleep(defaultWait);
  console.log('smallmapClose');
}

async function openChest() {
  await awaitSleep(defaultWait);
  console.log('openChest');
}

async function drawSprite(nn,xx,yy) {
  await awaitSleep(defaultWait);
  console.log('drawSprite nn=' + toHex(nn, 2) + ' xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

async function attackEffect(tt,xx,yy) {
  await awaitSleep(defaultWait);
  console.log('attackEffect tt=' + toHex(nn, 2) + ' xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

async function letterboxEffect() {
  await awaitSleep(defaultWait);
  console.log('letterboxEffect');
}
async function fadeInEffect() {
  await awaitSleep(defaultWait);
  console.log('fadeInEffect');
}
async function fadeOutEffect() {
  await awaitSleep(defaultWait);
  console.log('fadeOutEffect');
}
async function washOutEffect() {
  await awaitSleep(defaultWait);
  console.log('washOutEffect');
}
async function eyeblinkEffect() {
  await awaitSleep(defaultWait);
  console.log('eyeblinkEffect');
}

async function recoverHp() {
  await awaitSleep(defaultWait);
  console.log('recoverHp');
}
async function recoverMp() {
  await awaitSleep(defaultWait);
  console.log('recoverMp');
}

async function healDisease(val) {
  await awaitSleep(defaultWait);
  console.log('healDisease ' + toHex(val, 2));
}
async function nop() {
  await awaitSleep(defaultWait);
  console.log('nop');
}
async function disease(val) {
  await awaitSleep(defaultWait);
  console.log('disease ' + toHex(val, 2));
}

async function setFlags72To77(val) {
  await awaitSleep(defaultWait);
  console.log('setFlags72To77 ' + toHex(val, 2));
}

async function inputNames() {
  await awaitSleep(defaultWait);
  console.log('inputNames()');
}
async function randomize7E7F() {
  await awaitSleep(defaultWait);
  console.log('randomize7E7F');
}
async function resetGame() {
  await awaitSleep(defaultWait);
  console.log('resetGame');
}

async function setChest1Script(val) {
  await awaitSleep(defaultWait);
  console.log('setChest1Script ' + toHex(val, 2));
}
async function setChest2Script(val) {
  await awaitSleep(defaultWait);
  console.log('setChest2Script ' + toHex(val, 2));
}
async function setChest3Script(val) {
  await awaitSleep(defaultWait);
  console.log('setChest3Script ' + toHex(val, 2));
}

async function stopInput() {
  await awaitSleep(defaultWait);
  console.log('stopInput');
}

async function increaseGold(val) {
  await awaitSleep(defaultWait);
  console.log('increaseGold ' + toHex(val, 2));
}
async function decreaseGold(val) {
  await awaitSleep(defaultWait);
  console.log('decreaseGold ' + toHex(val, 2));
}
async function increaseExp(val) {
  await awaitSleep(defaultWait);
  console.log('increaseExp ' + toHex(val, 2));
}
async function decreaseExp(val) {
  await awaitSleep(defaultWait);
  console.log('decreaseExp ' + toHex(val, 2));
}

async function pickItem(val) {
  await awaitSleep(defaultWait);
  console.log('pickItem ' + toHex(val, 2));
}
async function dropItem(val) {
  await awaitSleep(defaultWait);
  console.log('dropItem ' + toHex(val, 2));
}
async function pickMagic(val) {
  await awaitSleep(defaultWait);
  console.log('pickMagic ' + toHex(val, 2));
}
async function dropMagic(val) {
  await awaitSleep(defaultWait);
  console.log('dropMagic ' + toHex(val, 2));
}
async function pickWeapon(val) {
  await awaitSleep(defaultWait);
  console.log('pickWeapon ' + toHex(val, 2));
}
async function dropWeapon(val) {
  await awaitSleep(defaultWait);
  console.log('dropWeapon ' + toHex(val, 2));
}

async function flagOn(val) {
  await awaitSleep(defaultWait);
  console.log('flagOn ' + toHex(val, 2));
}
async function flagOff(val) {
  await awaitSleep(defaultWait);
  console.log('flagOff ' + toHex(val, 2));
}

async function textSpeedLock() {
  await awaitSleep(defaultWait);
  console.log('textSpeedLock');
}
async function textSpeedUnlock() {
  await awaitSleep(defaultWait);
  console.log('textSpeedUnlock');
}

async function consumeItem() {
  await awaitSleep(defaultWait);
  console.log('consumeItem');
}

async function openDoorNorth() {
  await awaitSleep(defaultWait);
  console.log('openDoorNorth');
}
async function closeDoorNorth() {
  await awaitSleep(defaultWait);
  console.log('closeDoorNorth');
}
async function openDoorSouth() {
  await awaitSleep(defaultWait);
  console.log('openDoorSouth');
}
async function closeDoorSouth() {
  await awaitSleep(defaultWait);
  console.log('closeDoorSouth');
}
async function openDoorEast() {
  await awaitSleep(defaultWait);
  console.log('openDoorEast');
}
async function closeDoorEast() {
  await awaitSleep(defaultWait);
  console.log('closeDoorEast');
}
async function openDoorWest() {
  await awaitSleep(defaultWait);
  console.log('openDoorWest');
}
async function closeDoorWest() {
  await awaitSleep(defaultWait);
  console.log('closeDoorWest');
}

async function scrollSouth() {
  await awaitSleep(defaultWait);
  console.log('scrollSouth');
}
async function scrollNorth() {
  await awaitSleep(defaultWait);
  console.log('scrollNorth');
}
async function scrollLeft() {
  await awaitSleep(defaultWait);
  console.log('scrollLeft');
}
async function scrollRight() {
  await awaitSleep(defaultWait);
  console.log('scrollRight');
}

async function enterRoomScript() {
  await awaitSleep(defaultWait);
  console.log('enterRoomScript');
}
async function exitRoomScript() {
  await awaitSleep(defaultWait);
  console.log('exitRoomScript');
}
async function killedAllRoomScript() {
  await awaitSleep(defaultWait);
  console.log('killedAllRoomScript');
}

async function nextRoom(xx,yy) {
  await awaitSleep(defaultWait);
  console.log('nextRoom xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

async function teleport2(mm,bb,xx,yy) {

  await awaitSleep(defaultWait);
  nroMapaActual = mm;
  mapaActual = mapas[nroMapaActual];
  bloqueX = parseInt(toHex(bb,2).substring(0,1),16);
  bloqueY = parseInt(toHex(bb,2).substring(1,2),16);

  console.log('teleporting2 to mm=' + toHex(mm, 2) + ' bb=' + toHex(bb, 2) + ' xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2));
}

async function teleport(mm,bb,xx,yy) {

  await awaitSleep(defaultWait);
  nroMapaActual = mm;
  mapaActual = mapas[nroMapaActual];
  bloqueX = parseInt(toHex(bb,2).substring(0,1),16);
  bloqueY = parseInt(toHex(bb,2).substring(1,2),16);

  console.log('teleporting to mm=' + toHex(mm, 2) + ' bb=' + toHex(bb, 2) + ' xx=' + toHex(xx, 2) + ' yy=' + toHex(yy, 2) + ' bloqueX: ' + bloqueX + ' bloqueY: ' + bloqueY);
}

async function music(val) {

  await awaitSleep(defaultWait);

  console.log('playing song ' + toHex(val, 2) + ' (' + val + ')');
  playSong(val);
}
async function soundEffect(val) {

//const asyncB = async () => {

  await awaitSleep(defaultWait);
  console.log('playing sound effect ' + toHex(val, 2));
}

async function shakeScreen() {
  await awaitSleep(defaultWait);
  console.log('shakeScreen');
}

async function loadGrupoPersonaje(val) {
  await awaitSleep(defaultWait);
  console.log('loadGrupoPersonaje ' + toHex(val, 2));
}
async function addPersonaje(val) {
  await awaitSleep(defaultWait);
  console.log('addPersonaje ' + toHex(val, 2));
}

async function addBoss(val) {
  await awaitSleep(defaultWait);
  console.log('addBoss ' + toHex(val, 2));
}

async function sleep(val) {
  await awaitSleep(defaultWait);
  console.log('sleeping: ' + toHex(val, 2));
}

async function text(speech) {
  await awaitSleep(defaultWait);
  console.log('text: ' + speech);
}






