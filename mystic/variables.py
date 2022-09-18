import mystic.variables

# diccionario de flags
flags = {}
for i in range(0,0x78):
  flags[i] = 'flag_{:02x}'.format(i)
for i in range(0x78,0x80):
  flags[i] = 'flag_sinbatt_{:02x}'.format(i)

# diccionario de monstruos grandes
bosses = {}
for i in range(0,0x15):
  bosses[i] = 'boss_{:02x}'.format(i)

# diccionario de personajes
personajes = {}
for i in range(0,0xbf):
  personajes[i] = 'npc_{:02x}'.format(i)


# diccionario de ventanas/paneles
windows = {}
for i in range(0,34):
  windows[i] = 'win_{:02x}'.format(i)

# diccionario de proyectiles
projectiles = {}
for i in range(0,40):
  projectiles[i] = 'proj_{:02x}'.format(i)

# diccionario de proyectiles del heroe
hero_projectiles = {}
hero_projectiles[0] = 'hero_SWORD'
hero_projectiles[1] = 'hero_KAMEHAMEHA'
hero_projectiles[2] = 'hero_FIRE'
hero_projectiles[3] = 'hero_ICE'
hero_projectiles[4] = 'hero_FIRE1'
hero_projectiles[5] = 'hero_FIRE2'
hero_projectiles[6] = 'hero_ICE1'
hero_projectiles[7] = 'hero_ICE2'
hero_projectiles[8] = 'hero_ICE3'
hero_projectiles[9] = 'hero_ICE4'
hero_projectiles[10] = 'hero_CURE1'
hero_projectiles[11] = 'hero_CURE2'
hero_projectiles[12] = 'hero_CURE3'
hero_projectiles[13] = 'hero_CURE4'
hero_projectiles[14] = 'hero_PURE'
hero_projectiles[15] = 'hero_PURE1'
hero_projectiles[16] = 'hero_PURE2'
hero_projectiles[17] = 'hero_PURE3'
hero_projectiles[18] = 'hero_PURE4'
hero_projectiles[19] = 'hero_BLANK'
hero_projectiles[20] = 'hero_SLEEP1'
hero_projectiles[21] = 'hero_SLEEP2'
hero_projectiles[22] = 'hero_SLEEP3'
hero_projectiles[23] = 'hero_SLEEP4'
hero_projectiles[24] = 'hero_MUTE1'
hero_projectiles[25] = 'hero_MUTE2'
hero_projectiles[26] = 'hero_MUTE3'
hero_projectiles[27] = 'hero_MUTE4'
hero_projectiles[28] = 'hero_NUKE1'
hero_projectiles[29] = 'hero_NUKE2'
hero_projectiles[30] = 'hero_THUNDER1'
hero_projectiles[31] = 'hero_THUNDER2'
hero_projectiles[32] = 'hero_THUNDER3'
hero_projectiles[33] = 'hero_AXE'
hero_projectiles[34] = 'hero_CHAIN'
hero_projectiles[35] = 'hero_CHAIN1'
hero_projectiles[36] = 'hero_CHAIN2'
hero_projectiles[37] = 'hero_CHAIN3'
hero_projectiles[38] = 'hero_CHAIN4'
hero_projectiles[39] = 'hero_SICKLE'
hero_projectiles[40] = 'hero_SICKLE1'
hero_projectiles[41] = 'hero_SPEAR1'
hero_projectiles[42] = 'hero_SPEAR2'
hero_projectiles[43] = 'hero_MORNINGSTAR'
hero_projectiles[44] = 'hero_MATTOCK'
hero_projectiles[45] = 'hero_MATTOCK1'
hero_projectiles[46] = 'hero_MATTOCK2'
hero_projectiles[47] = 'hero_MATTOCK3'

hero_projs_animation_type = ['type_EXPLOSION',
                             'type_SWORD',
                             'type_AXE',
                             'type_CHAIN',
                             'type_SICKLE',
                             'type_SPEAR',
                             'type_MORNINGSTAR',
                             'type_NOTHING',
                             'type_CURE',
                             'type_PURE',
                             'type_MUTE',
                             'type_SLEEP',
                             'type_FIRE',
                             'type_ICE',
                             'type_THUNDER',
                             'type_NUKE'
                            ]

# diccionario de behaviours de hero_projectiles
hero_projs_behavs = {}
#for i in range(0,110):
for i in range(0,114):
  hero_projs_behavs[i] = 'behav_{:03}'.format(i)

#self.equipamiento = {}
# 0x09 empieza los items de items
# 0x42 empieza los items de armas

items = []
items.append('💧Cure')
items.append('💧X-Cure')
items.append('💧Ether')
items.append('💧X-Ether')
items.append('💧Elixir')
items.append('💧Pure')
items.append('💧Eyedrp')
items.append('💧Soft')
items.append('💧Moogle')
items.append('💧Unicorn')
items.append('🔮Silence')
items.append('🔮Pillow')
items.append('0c af e5')
items.append('0d d7 e5')
items.append('🔮Flame')
items.append('🔮Blaze')
items.append('🔮Blizrd')
items.append('🔮Frost')
items.append('🔮Litblt')
items.append('🔮Thundr')
items.append('🍬Candy')
items.append('15 8a a7')
items.append('🔑Key')
items.append('🔑Bone')
items.append('🔑Bronze')
items.append('19 a4 a2')
items.append('1a 94 50')
items.append('1b 8a 8e')
items.append('1c 8a 8f')
items.append('1d da d0')
items.append(' Mirror')
items.append('1f db c8')
items.append('20 c8 cb')
items.append('💧Amanda')
items.append('22 63 e2')
items.append('23 dc f2')
items.append('💧Oil')
items.append('25 c7 d0')
items.append('26 c7 d0')
items.append('27 c7 d0')
items.append('28 c7 d0')
items.append('💎Crystal')
items.append('2a dc f2')
items.append('💎Nectar')
items.append('💎Stamina')
items.append('💎Wisdom')
items.append('💎Will')
items.append('2f 99 8b')
items.append('30 62 e7')
items.append('💰Gold')
items.append('💰Fang')
items.append('33 4a 8b')
items.append('34 de f2')
items.append('𐇞Mattok')
items.append('💰Ruby')
items.append('💰Opal')
items.append('38 e3 59')

magias = []
magias.append('Cure')
magias.append('Heal')
magias.append('Mute')
magias.append('Slep')
magias.append('Fire')
magias.append('Ice ')
magias.append('Lit ')
magias.append('Nuke')

armas = []
armas.append('🗡Broad')
armas.append('🪓Battle')
armas.append('🔨Sickle')
armas.append('🔗Chain')
armas.append('🗡Silver')
armas.append('🡔Wind')
armas.append('🪓Were')
armas.append('💣Star')
armas.append('🗡Blood')
armas.append('🗡Dragon')
armas.append('🔗Flame')
armas.append('🗡Ice')
armas.append('🪓Zeus')
armas.append('🗡Rusty')
armas.append('🡔Thunder')
armas.append('🗡XCalibr')
armas.append('👕Bronze')
armas.append('👕Iron')
armas.append('👕Silver')
armas.append('👕Gold')
armas.append('👕Flame')
armas.append('👕Ice')
armas.append('👕Dragon')
armas.append('👕Samurai')
armas.append('👕Opal')
armas.append('19 e1 e6')
armas.append('1a e1 e6')
armas.append('⛨Bronze')
armas.append('⛨Iron')
armas.append('⛨Silver')
armas.append('⛨Gold')
armas.append('⛨Flame')
armas.append('⛨Dragon')
armas.append('⛨Aegis')
armas.append('⛨Opal')
armas.append('⛨Ice')
armas.append('24 99 9c')
armas.append('25 99 9c')
armas.append('🎩Bronze')
armas.append('🎩Iron')
armas.append('🎩Silver')
armas.append('🎩Gold')
armas.append('🎩Opal')
armas.append('🎩Samurai')
armas.append('2c 8f 51')
armas.append('2d 8f 51')


#nombresOriginales = False
nombresOriginales = True
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  # se setea automáticamente si al intentar agregar un item resulta que estaba lleno
  flags[0x05] = 'flag_INVENTARIO_LLENO' 
  # se setea automáticamente si no alcanza el dinero luego de comparar
  flags[0x06] = 'flag_ORO_INSUFICIENTE' 
  # se setea automáticamente cuando mate a todos en el bloque?
  flags[0x07] = 'flag_MATO_TODOS' 
  flags[0x08] = 'flag_MURIO_WILLY'
  flags[0x09] = 'flag_DARK_LORD_ME_DESCUBRIO'
  flags[0x0a] = 'flag_RESCATAMOS_FUJI_HONGOS'
  flags[0x0b] = 'flag_FUJI_SE_PRESENTO'
  flags[0x0c] = 'flag_BOGARD_NOS_DIO_MATTOCK'
  flags[0x0d] = 'flag_DRACULA_SECUESTRO_FUJI'
  flags[0x0e] = 'flag_SUMO_RESCATO_FUJI_ATAUD'
  flags[0x10] = 'flag_FUJI_VIO_SU_MADRE_WENDEL'
  flags[0x11] = 'flag_JULIUS_SECUESTRO_FUJI_WENDEL'
  flags[0x12] = 'flag_EMERGIO_TORRE_DESIERTO'
  flags[0x13] = 'flag_VENCIMOS_METAL_CRAB_CANGREJO'
  flags[0x14] = 'flag_ENCONTRAMOS_PLATA'
  flags[0x15] = 'flag_VENCIMOS_MANTIS_ANT_COATI_GIGANTE'
  flags[0x16] = 'flag_DESPEGO_ZEPELIN'
  flags[0x17] = 'flag_VENCIMOS_DRAGON_ROJO'
  flags[0x18] = 'flag_VENCIMOS_JULIUS2'
  flags[0x19] = 'flag_NACIO_CHOCOBO'
  flags[0x1a] = 'flag_DAVIAS_NOS_CONTO_CUEVA_MEDUZA'
  flags[0x1b] = 'flag_AMANDA_SE_DISCULPO_POR_ROBAR_AMULETO'
  flags[0x1c] = 'flag_SACRIFICAMOS_A_AMANDA'
  flags[0x1d] = 'flag_LESTER_SE_CURO_DE_SER_PAPAGAYO'
  flags[0x1e] = 'flag_RESCATAMOS_FUJI_DARK_LORD'
  flags[0x1f] = 'flag_BOGARD_DISCUTIO_SUMO'
  flags[0x20] = 'flag_SARAH_NOS_CONTO_ACCIDENTE_BOGARD'
  flags[0x21] = 'flag_LISTO_CHOCOBOT'
  flags[0x22] = 'flag_ESPADA_OXIDADA_RECUPERA_SU_ENERGIA'
  flags[0x23] = 'flag_VENCIMOS_DRAGON_2_CABEZAS'
  flags[0x24] = 'flag_VENCIMOS_LOBITO'
  flags[0x25] = 'flag_VENCIMOS_LEE_DRACULA'
  flags[0x26] = 'flag_VENCIMOS_MEGAPEDE_CIENPIES'
  flags[0x27] = 'flag_VENCIMOS_MEDUSA'
  flags[0x28] = 'flag_VENCIMOS_DAVIAS'
  flags[0x29] = 'flag_VENCIMOS_CYCLOPE_DEJA_MORNINGSTAR'
  flags[0x2a] = 'flag_VENCIMOS_CHIMERA_LEON_ALAS'
  flags[0x2b] = 'flag_VENCIMOS_GOLEM_ROBOT_MORNINGSTAR'
  flags[0x2c] = 'flag_VENCIMOS_DARK_LORD'
  flags[0x2d] = 'flag_VENCIMOS_KARY_HIELO'
  flags[0x2e] = 'flag_VENCIMOS_KRAKEN_PUENTE'
  flags[0x2f] = 'flag_VENCIMOS_PIRUS_IFLYTE_BOLA_SOL'
  flags[0x30] = 'flag_VENCIMOS_LICH_SENSEMANN_ESQUELETO'
  flags[0x31] = 'flag_VENCIMOS_GARUDA_AGUILA'
  flags[0x32] = 'flag_VENCIMOS_DRAGON'
  flags[0x34] = 'flag_VENCIMOS_DRAGON_ZOMBIE'
  flags[0x35] = 'flag_OBTUVIMOS_LAGRIMA_AMANDA'
  flags[0x36] = 'flag_DESCUBRIMOS_CUEVA_DESIERTO'
  flags[0x37] = 'flag_SE_DERRUMBO_PUENTE'
  flags[0x38] = 'flag_OBTUVIMOS_EXCALIBUR'
  flags[0x39] = 'flag_OBTUVIMOS_ROPA_ORO'
  flags[0x3a] = 'flag_OBTUVIMOS_ESPADA_HIELO'
  flags[0x3b] = 'flag_OBTUVIMOS_ESPADA_OXIDADA'
  flags[0x3c] = 'flag_OBTUVIMOS_ESPADA_SANGRE'
  flags[0x3d] = 'flag_OBTUVIMOS_ESCUDO_AEGIS'
  flags[0x3e] = 'flag_OBTUVIMOS_HACHA_ZEUS'
  flags[0x3f] = 'flag_OBTUVIMOS_HACHA_WERE'
  flags[0x40] = 'flag_ENCONTRAMOS_LATIGO'
  flags[0x41] = 'flag_ENCONTRAMOS_STICKLE'
  flags[0x43] = 'flag_OBTUVIMOS_ESCUDO_DRAGON'
  flags[0x44] = 'flag_OBTUVIMOS_ROPA_DRAGON'
  flags[0x46] = 'flag_OBTUVIMOS_ESPADA_MISTERIOSA'
  flags[0x47] = 'flag_ENTRAMOS_CUEVA_DESIERTO'
  flags[0x48] = 'flag_ENCONTRAMOS_ESPEJO'
  flags[0x49] = 'flag_ENCONTRAMOS_MAGIA_FUEGO'
  flags[0x4a] = 'flag_ENCONTRAMOS_MAGIA_HIELO'
  flags[0x4c] = 'flag_OBTUVIMOS_ESPADA_DRAGON'
  flags[0x4d] = 'flag_ENCONTRAMOS_MATTOCK'
  flags[0x4e] = 'flag_ENCONTRAMOS_MORNING_STAR'
  flags[0x4f] = 'flag_ENCONTRAMOS_ESCUDO_HIELO'
  flags[0x51] = 'flag_FUJI_ACOMPANIA'
  flags[0x52] = 'flag_JULIUS_ACOMPANIA'
  flags[0x53] = 'flag_WATTS_ACOMPANIA'
  flags[0x54] = 'flag_BOGARD_ACOMPANIA'
  flags[0x55] = 'flag_AMANDA_ACOMPANIA'
  flags[0x56] = 'flag_LESTER_ACOMPANIA'
  flags[0x57] = 'flag_MARCIE_ACOMPANIA'
  flags[0x58] = 'flag_CHOCOBO_ACOMPANIA'
  flags[0x5b] = 'flag_DEJE_CHOCOBO_EN_01'
  flags[0x5c] = 'flag_DEJE_CHOCOBO_EN_02'
  flags[0x5d] = 'flag_DEJE_CHOCOBO_EN_03'
  flags[0x5e] = 'flag_DEJE_CHOCOBO_EN_04'
  flags[0x5f] = 'flag_DEJE_CHOCOBO_EN_05'
  flags[0x60] = 'flag_DEJE_CHOCOBO_EN_06'
  flags[0x61] = 'flag_DEJE_CHOCOBO_EN_07'
  flags[0x62] = 'flag_DEJE_CHOCOBO_EN_08'
  flags[0x63] = 'flag_DEJE_CHOCOBO_EN_09'
  flags[0x64] = 'flag_DEJE_CHOCOBO_EN_10'
  flags[0x65] = 'flag_DEJE_CHOCOBO_EN_11'
  flags[0x66] = 'flag_DEJE_CHOCOBO_EN_12'
  flags[0x67] = 'flag_DEJE_CHOCOBO_EN_13'
  flags[0x68] = 'flag_DEJE_CHOCOBO_EN_14'
  flags[0x69] = 'flag_DEJE_CHOCOBO_EN_15'
  flags[0x6a] = 'flag_DEJE_CHOCOBO_EN_16'
  flags[0x6b] = 'flag_DEJE_CHOCOBO_EN_17'
  flags[0x6c] = 'flag_DEJE_CHOCOBO_EN_18'
  flags[0x6d] = 'flag_DEJE_CHOCOBO_EN_19'
  flags[0x6e] = 'flag_DEJE_CHOCOBO_EN_20'
  flags[0x6f] = 'flag_ARRIBA_DEL_CHOCOBO'
  flags[0x70] = 'flag_CHOCOBOT_SOBRE_AGUA'
  # cuando nos hacen una pregunta si-no
#  flags[0x7f] = 'ELIGIMOS_NO'

  # nombres de los monstruos grandes
  bosses[0x00] = 'boss_VAMPIRE_LEE'
  bosses[0x01] = 'boss_HYDRA'
  bosses[0x02] = 'boss_MEDUSA'
  bosses[0x03] = 'boss_MEGAPEDE'
  bosses[0x04] = 'boss_DAVIAS'
  bosses[0x05] = 'boss_GOLEM_ROBOT'
  bosses[0x06] = 'boss_CYCLOPS'
  bosses[0x07] = 'boss_CHIMERA'
  bosses[0x08] = 'boss_KARY'
  bosses[0x09] = 'boss_KRAKEN'
  bosses[0x0a] = 'boss_PIRUS_IFLYTE'
  bosses[0x0b] = 'boss_LICH_SENSEMANN'
  bosses[0x0c] = 'boss_GARUDA'
  bosses[0x0d] = 'boss_DRAGON'
  bosses[0x0e] = 'boss_JULIUS_2ND_FORM'
  bosses[0x0f] = 'boss_DRAGON_ZOMBIE'
  bosses[0x10] = 'boss_JACKAL_BIGCAT'
  bosses[0x11] = 'boss_JULIUS_3RD_FORM'
  bosses[0x12] = 'boss_METAL_CRAB_CANGREJO'
  bosses[0x13] = 'boss_MANTIS_ANT'
  bosses[0x14] = 'boss_DRAGON_RED'

  # nombres de los personajes
  personajes[0x00] = 'npc_SNOWMAN_STILL'
  personajes[0x01] = 'npc_FUJI_FOLLOWING'
  personajes[0x02] = 'npc_MYSTERYMAN_FOLLOWING'
  personajes[0x03] = 'npc_WATTS_FOLLOWING'
  personajes[0x04] = 'npc_BOGARD_FOLLOWING'
  personajes[0x05] = 'npc_AMANDA_FOLLOWING'
  personajes[0x06] = 'npc_LESTER_FOLLOWING'
  personajes[0x07] = 'npc_MARCIE_FOLLOWING'
  personajes[0x08] = 'npc_CHOCOBO_FOLLOWING'
  personajes[0x09] = 'npc_CHOCOBOT_FOLLOWING'
  personajes[0x0a] = 'npc_WEREWOLF_1'
  personajes[0x0b] = 'npc_INV_CURE'
  personajes[0x0c] = 'npc_CHEST_1'
  personajes[0x0d] = 'npc_CHEST_2'
  personajes[0x0e] = 'npc_CHEST_3'
  personajes[0x0f] = 'npc_CHEST_OPEN'
  personajes[0x10] = 'npc_CHIBIDEVIL'
  personajes[0x11] = 'npc_RABBITE'
  personajes[0x12] = 'npc_GOBLIN'
  personajes[0x13] = 'npc_MUSHROOM'
  personajes[0x14] = 'npc_JELLYFISH'
  personajes[0x15] = 'npc_SWAMPMAN'
  personajes[0x16] = 'npc_LIZARDMAN'
  personajes[0x17] = 'npc_FLOWER'
  personajes[0x18] = 'npc_FACEORB'
  personajes[0x19] = 'npc_SKELETON'
  personajes[0x1a] = 'npc_EVIL_PLANT'
  personajes[0x1b] = 'npc_FLYING_FISH'
  personajes[0x1c] = 'npc_ZOMBIE'
  personajes[0x1d] = 'npc_MOUSE'
  personajes[0x1e] = 'npc_PUMPKIN'
  personajes[0x1f] = 'npc_OWL'
  personajes[0x20] = 'npc_BEE'
  personajes[0x21] = 'npc_CLOUD'
  personajes[0x22] = 'npc_PIG'
  personajes[0x23] = 'npc_CRAB'
  personajes[0x24] = 'npc_SPIDER'
  personajes[0x25] = 'npc_INV_OPEN_NORTH'
  personajes[0x26] = 'npc_INV_OPEN_SOUTH'
  personajes[0x27] = 'npc_INV_OPEN_EAST'
  personajes[0x28] = 'npc_INV_OPEN_WEST'
  personajes[0x29] = 'npc_MIMIC_CHEST'
  personajes[0x2a] = 'npc_HOPPING_BUG'
  personajes[0x2b] = 'npc_PORCUPINE'
  personajes[0x2c] = 'npc_CARROT'
  personajes[0x2d] = 'npc_EYE_SPY'
  personajes[0x2e] = 'npc_WEREWOLF_2'
  personajes[0x2f] = 'npc_GHOST'
  personajes[0x30] = 'npc_BASILISK'
  personajes[0x31] = 'npc_SCORPION'
  personajes[0x32] = 'npc_SAURUS'
  personajes[0x33] = 'npc_MUMMY'
  personajes[0x34] = 'npc_PAKKUN_LIZARD'
  personajes[0x35] = 'npc_SNAKE'
  personajes[0x36] = 'npc_SHADOW'
  personajes[0x37] = 'npc_BLACK_WIZARD'
  personajes[0x38] = 'npc_FLAME'
  personajes[0x39] = 'npc_GARGOYLE'
  personajes[0x3a] = 'npc_MONKEY'
  personajes[0x3b] = 'npc_MOLEBEAR'
  personajes[0x3c] = 'npc_OGRE'
  personajes[0x3d] = 'npc_BARNACLEJACK'
  personajes[0x3e] = 'npc_PHANTASM'
  personajes[0x3f] = 'npc_MINOTAUR'
  personajes[0x40] = 'npc_GLAIVE_MAGE'
  personajes[0x41] = 'npc_GLAIVE_KNIGHT'
  personajes[0x42] = 'npc_DARK_LORD'
  personajes[0x43] = 'npc_MEGA_FLYTRAP'
  personajes[0x44] = 'npc_DRAGONFLY'
  personajes[0x45] = 'npc_ARMADILLO'
  personajes[0x46] = 'npc_SNOWMAN_MOVING'
  personajes[0x47] = 'npc_SABER_CAT'
  personajes[0x48] = 'npc_WALRUS'
  personajes[0x49] = 'npc_DUCK_SOLDIER'
  personajes[0x4a] = 'npc_POTO_RABBIT'
  personajes[0x4b] = 'npc_CYCLONE'
  personajes[0x4c] = 'npc_BEHOLDER_EYE'
  personajes[0x4d] = 'npc_MANTA_RAY'
  personajes[0x4e] = 'npc_JUMPING_HAND'
  personajes[0x4f] = 'npc_TORTOISE'
  personajes[0x50] = 'npc_FIRE_MOTH'
  personajes[0x51] = 'npc_EARTH_DIGGER'
  personajes[0x52] = 'npc_DENDEN_SNAIL'
  personajes[0x53] = 'npc_DOPPEL_MIRROR'
  personajes[0x54] = 'npc_GUARDIAN'
  personajes[0x55] = 'npc_EVIL_SWORD'
  personajes[0x56] = 'npc_GAUNTLET'
  personajes[0x57] = 'npc_GARASHA_DUCK'
  personajes[0x58] = 'npc_FUZZY_WONDER'
  personajes[0x59] = 'npc_ELEPHANT'
  personajes[0x5a] = 'npc_NINJA'
  personajes[0x5b] = 'npc_JULIUS'
  personajes[0x5c] = 'npc_DEMON_HEAD'
  personajes[0x5d] = 'npc_INV_DESSERT_CAVE_STONE'
  personajes[0x5e] = 'npc_WATER_DEMON'
  personajes[0x5f] = 'npc_SEA_DRAGON'
  personajes[0x60] = 'npc_GALL_FISH'
  personajes[0x61] = 'npc_WILLY'
  personajes[0x62] = 'npc_MYSTERYMAN_1'
  personajes[0x63] = 'npc_AMANDA_1'
  personajes[0x64] = 'npc_AMANDA_ILL'
  personajes[0x65] = 'npc_AMANDA_DEAD'
  personajes[0x66] = 'npc_FUJI_1'
  personajes[0x67] = 'npc_FUJI_WINDOW'
  personajes[0x68] = 'npc_MOTHER'
  personajes[0x69] = 'npc_BOGARD_1'
  personajes[0x6a] = 'npc_BOGARD_2'
  personajes[0x6b] = 'npc_KETTS_WEREWOLF'
  personajes[0x6c] = 'npc_INV_FUJI_COFFIN'
  personajes[0x6d] = 'npc_CIBBA'
  personajes[0x6e] = 'npc_GUY_WENDEL'
  personajes[0x6f] = 'npc_WATTS'
  personajes[0x70] = 'npc_MINECART'
  personajes[0x71] = 'npc_CHOCOBO_EGG'
  personajes[0x72] = 'npc_DAVIAS'
  personajes[0x73] = 'npc_LESTER_1'
  personajes[0x74] = 'npc_LESTER_PARROT'
  personajes[0x75] = 'npc_BOWOW'
  personajes[0x76] = 'npc_SARAH'
  personajes[0x77] = 'npc_MARCIE_1'
  personajes[0x78] = 'npc_KING_OF_LORIM'
  personajes[0x79] = 'npc_GLADIATOR_FRIEND'
  personajes[0x7a] = 'npc_INV_INN'
  personajes[0x7b] = 'npc_GIRL_TOPPLE'
  personajes[0x7c] = 'npc_GUY_TOPPLE'
  personajes[0x7d] = 'npc_GUY_TOPPLE_HOUSE'
  personajes[0x7e] = 'npc_GIRL_TOPPLE_HOUSE'
  personajes[0x7f] = 'npc_OLDMAN_TOPPLE'
  personajes[0x80] = 'npc_GUY_KETTS'
  personajes[0x81] = 'npc_GIRL_KETTS'
  personajes[0x82] = 'npc_GIRL_CIBBA'
  personajes[0x83] = 'npc_GUY_WENDEL_2'
  personajes[0x84] = 'npc_GUY_WENDEL_HOUSE'
  personajes[0x85] = 'npc_WOMAN_CIBBA'
  personajes[0x86] = 'npc_OLDMAN_WENDEL'
  personajes[0x87] = 'npc_DWARF_1'
  personajes[0x88] = 'npc_DWARF_2'
  personajes[0x89] = 'npc_DWARF_3'
  personajes[0x8a] = 'npc_DWARF_4'
  personajes[0x8b] = 'npc_DWARF_5'
  personajes[0x8c] = 'npc_GUY_AIRSHIP_1'
  personajes[0x8d] = 'npc_GUY_AIRSHIP_2'
  personajes[0x8e] = 'npc_GUY_AIRSHIP_3'
  personajes[0x8f] = 'npc_GUY_AIRSHIP_4'
  personajes[0x90] = 'npc_OLDMAN_MENOS_1'
  personajes[0x91] = 'npc_GUY_MENOS'
  personajes[0x92] = 'npc_GIRL_MENOS_1'
  personajes[0x93] = 'npc_OLDMAN_MENOS_2'
  personajes[0x94] = 'npc_GIRL_MENOS'
  personajes[0x95] = 'npc_WOMAN_MENOS_2'
  personajes[0x96] = 'npc_GIRL_JADD_1'
  personajes[0x97] = 'npc_OLDMAN_JADD'
  personajes[0x98] = 'npc_GIRL_JADD_2'
  personajes[0x99] = 'npc_GUY_JADD'
  personajes[0x9a] = 'npc_DWARF_JADD'
  personajes[0x9b] = 'npc_SALESMAN_JADD'
  personajes[0x9c] = 'npc_GIRL_JADD_3'
  personajes[0x9d] = 'npc_BOY_JADD'
  personajes[0x9e] = 'npc_OLDMAN_ISH'
  personajes[0x9f] = 'npc_GUY_ISH_1'
  personajes[0xa0] = 'npc_GUY_ISH_2'
  personajes[0xa1] = 'npc_GIRL_ISH'
  personajes[0xa2] = 'npc_GUY_ISH_3'
  personajes[0xa3] = 'npc_GUY_ISH_4'
  personajes[0xa4] = 'npc_INV_STONE_1'
  personajes[0xa5] = 'npc_INV_STONE_2'
  personajes[0xa6] = 'npc_INV_STONE_3'
  personajes[0xa7] = 'npc_INV_STONE_4'
  personajes[0xa8] = 'npc_INV_STONE_5'
  personajes[0xa9] = 'npc_INV_STONE_6'
  personajes[0xaa] = 'npc_INV_STONE_7'
  personajes[0xab] = 'npc_INV_STONE_8'
  personajes[0xac] = 'npc_GUY_LORIM_FROZEN'
  personajes[0xad] = 'npc_GUY_LORIM_1'
  personajes[0xae] = 'npc_GUY_LORIM_2'
  personajes[0xaf] = 'npc_SALESMAN'
  personajes[0xb0] = 'npc_INV_SALESMAN_1'
  personajes[0xb1] = 'npc_FUJI_2'
  personajes[0xb2] = 'npc_INV_SALESMAN_2'
  personajes[0xb3] = 'npc_MYSTERYMAN_2'
  personajes[0xb4] = 'npc_BOGARD_3'
  personajes[0xb5] = 'npc_AMANDA_2'
  personajes[0xb6] = 'npc_LESTER_2'
  personajes[0xb7] = 'npc_MARCIE_2'
  personajes[0xb8] = 'npc_CHOCOBOT'
  personajes[0xb9] = 'npc_CHOCOBO_1'
  personajes[0xba] = 'npc_CHOCOBO_2'
  personajes[0xbb] = 'npc_PRISION_BARS'
  personajes[0xbc] = 'npc_MUSIC_NOTES'
  personajes[0xbd] = 'npc_MAGIC_SALESMAN'
  personajes[0xbe] = 'npc_LAST_GUY'


  # nombres de las ventanas/paneles
  windows[0x00] = 'win_ITEM/MAGIC/EQUIP/ASK'
  windows[0x01] = 'win_ITEMS'
  windows[0x02] = 'win_MAGIC'
  windows[0x03] = 'win_EQUIP_HEADER'
  windows[0x04] = 'win_EQUIP'
  windows[0x06] = 'win_DIALOG_TOP'
  windows[0x0a] = 'win_CURRENT_ITEM'
  windows[0x11] = 'win_SELECT'
  windows[0x13] = 'win_GOLD'
  windows[0x1b] = 'win_SAVE_1'
  windows[0x1c] = 'win_SAVE_2'
  windows[0x1d] = 'win_NAMING_HEADER'
  windows[0x1e] = 'win_NAMING'
  windows[0x1f] = 'win_NEW_GAME_CONTINUE'
 

  def getLabel(val):
    # el primer bit indica si hay que negar la variable
    neg = val >= 0x80
    if(neg):
      val -= 0x80
    strNeg = '' if not neg else '!'
#    strVar = 'var[{:02x}] '.format(cond)
    strVar = flags[val]
    label = strNeg + strVar
    return label

  def getVal(label):
    retVal = -1
#    print('ejecutando getVal(\'' + label + '\')')

    neg = False
    # si esta negada
    if(label.startswith('!')):
      # lo indico
      neg = True
      # y quito el '!' del label 
      label = label[1:]

    # por cada valor del diccionario de variables
    for val in flags.keys():
      # me fijo el label
      lbl = flags[val]
      # si lo encontré
      if(lbl == label):
        retVal = val
        # si estaba negada
        if(neg):
          # seteamos el primer bit
          retVal += 0x80

        break

    return retVal


  def getLabelBoss(val):
    label = bosses[val]
    return label
  def getValBoss(label):
    # por cada monstruo 
    for val in bosses.keys():
      # me fijo el label
      lbl = bosses[val]
      # si lo encontré
      if(lbl == label):
        retVal = val
        break
    return retVal


