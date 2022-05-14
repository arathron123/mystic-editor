import mystic.variables

# diccionario de flags
flags = {}
for i in range(0,0x78):
  flags[i] = 'var_{:02x}'.format(i)
for i in range(0x78,0x80):
  flags[i] = 'var_sinbatt_{:02x}'.format(i)

# diccionario de monstruos grandes
bosses = {}
for i in range(0,0x15):
  bosses[i] = 'boss_{:02x}'.format(i)

# diccionario de personajes
personajes = {}
for i in range(0,0xbf):
  personajes[i] = 'pers_{:02x}'.format(i)


# diccionario de ventanas/paneles
windows = {}
for i in range(0,34):
  windows[i] = 'win_{:02x}'.format(i)

# diccionario de proyectiles
projectiles = {}
for i in range(0,40):
  projectiles[i] = 'proj_{:02x}'.format(i)



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
items.append('1e ff c6')
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
  flags[0x05] = 'INVENTARIO_LLENO' 
  # se setea automáticamente si no alcanza el dinero luego de comparar
  flags[0x06] = 'ORO_INSUFICIENTE' 
  # se setea automáticamente cuando mate a todos en el bloque?
  flags[0x07] = 'MATO_TODOS' 
  flags[0x08] = 'MURIO_WILLY'
  flags[0x09] = 'DARK_LORD_ME_DESCUBRIO'
  flags[0x0a] = 'RESCATAMOS_FUJI_HONGOS'
  flags[0x0b] = 'FUJI_SE_PRESENTO'
  flags[0x0c] = 'BOGARD_NOS_DIO_MATTOCK'
  flags[0x0d] = 'DRACULA_SECUESTRO_FUJI'
  flags[0x0e] = 'SUMO_RESCATO_FUJI_ATAUD'
  flags[0x10] = 'FUJI_VIO_SU_MADRE_WENDEL'
  flags[0x11] = 'JULIUS_SECUESTRO_FUJI_WENDEL'
  flags[0x12] = 'EMERGIO_TORRE_DESIERTO'
  flags[0x13] = 'VENCIMOS_METAL_CRAB_CANGREJO'
  flags[0x14] = 'ENCONTRAMOS_PLATA'
  flags[0x15] = 'VENCIMOS_MANTIS_ANT_COATI_GIGANTE'
  flags[0x16] = 'DESPEGO_ZEPELIN'
  flags[0x17] = 'VENCIMOS_DRAGON_ROJO'
  flags[0x18] = 'VENCIMOS_JULIUS2'
  flags[0x19] = 'NACIO_CHOCOBO'
  flags[0x1a] = 'DAVIAS_NOS_CONTO_CUEVA_MEDUZA'
  flags[0x1b] = 'AMANDA_SE_DISCULPO_POR_ROBAR_AMULETO'
  flags[0x1c] = 'SACRIFICAMOS_A_AMANDA'
  flags[0x1d] = 'LESTER_SE_CURO_DE_SER_PAPAGAYO'
  flags[0x1e] = 'RESCATAMOS_FUJI_DARK_LORD'
  flags[0x1f] = 'BOGARD_DISCUTIO_SUMO'
  flags[0x20] = 'SARAH_NOS_CONTO_ACCIDENTE_BOGARD'
  flags[0x21] = 'LISTO_CHOCOBOT'
  flags[0x22] = 'ESPADA_OXIDADA_RECUPERA_SU_ENERGIA'
  flags[0x23] = 'VENCIMOS_DRAGON_2_CABEZAS'
  flags[0x24] = 'VENCIMOS_LOBITO'
  flags[0x25] = 'VENCIMOS_LEE_DRACULA'
  flags[0x26] = 'VENCIMOS_MEGAPEDE_CIENPIES'
  flags[0x27] = 'VENCIMOS_MEDUSA'
  flags[0x28] = 'VENCIMOS_DAVIAS'
  flags[0x29] = 'VENCIMOS_CYCLOPE_DEJA_MORNINGSTAR'
  flags[0x2a] = 'VENCIMOS_CHIMERA_LEON_ALAS'
  flags[0x2b] = 'VENCIMOS_GOLEM_ROBOT_MORNINGSTAR'
  flags[0x2c] = 'VENCIMOS_DARK_LORD'
  flags[0x2d] = 'VENCIMOS_KARY_HIELO'
  flags[0x2e] = 'VENCIMOS_KRAKEN_PUENTE'
  flags[0x2f] = 'VENCIMOS_PIRUS_IFLYTE_BOLA_SOL'
  flags[0x30] = 'VENCIMOS_LICH_SENSEMANN_ESQUELETO'
  flags[0x31] = 'VENCIMOS_GARUDA_AGUILA'
  flags[0x32] = 'VENCIMOS_DRAGON'
  flags[0x34] = 'VENCIMOS_DRAGON_ZOMBIE'
  flags[0x35] = 'OBTUVIMOS_LAGRIMA_AMANDA'
  flags[0x36] = 'DESCUBRIMOS_CUEVA_DESIERTO'
  flags[0x37] = 'SE_DERRUMBO_PUENTE'
  flags[0x38] = 'OBTUVIMOS_EXCALIBUR'
  flags[0x39] = 'OBTUVIMOS_ROPA_ORO'
  flags[0x3a] = 'OBTUVIMOS_ESPADA_HIELO'
  flags[0x3b] = 'OBTUVIMOS_ESPADA_OXIDADA'
  flags[0x3c] = 'OBTUVIMOS_ESPADA_SANGRE'
  flags[0x3d] = 'OBTUVIMOS_ESCUDO_AEGIS'
  flags[0x3e] = 'OBTUVIMOS_HACHA_ZEUS'
  flags[0x3f] = 'OBTUVIMOS_HACHA_WERE'
  flags[0x40] = 'ENCONTRAMOS_LATIGO'
  flags[0x41] = 'ENCONTRAMOS_STICKLE'
  flags[0x43] = 'OBTUVIMOS_ESCUDO_DRAGON'
  flags[0x44] = 'OBTUVIMOS_ROPA_DRAGON'
  flags[0x46] = 'OBTUVIMOS_ESPADA_MISTERIOSA'
  flags[0x47] = 'ENTRAMOS_CUEVA_DESIERTO'
  flags[0x48] = 'ENCONTRAMOS_ESPEJO'
  flags[0x49] = 'ENCONTRAMOS_MAGIA_FUEGO'
  flags[0x4a] = 'ENCONTRAMOS_MAGIA_HIELO'
  flags[0x4c] = 'OBTUVIMOS_ESPADA_DRAGON'
  flags[0x4d] = 'ENCONTRAMOS_MATTOCK'
  flags[0x4e] = 'ENCONTRAMOS_MORNING_STAR'
  flags[0x4f] = 'ENCONTRAMOS_ESCUDO_HIELO'
  flags[0x51] = 'FUJI_ACOMPANIA'
  flags[0x52] = 'JULIUS_ACOMPANIA'
  flags[0x53] = 'WATTS_ACOMPANIA'
  flags[0x54] = 'BOGARD_ACOMPANIA'
  flags[0x55] = 'AMANDA_ACOMPANIA'
  flags[0x56] = 'LESTER_ACOMPANIA'
  flags[0x57] = 'MARCIE_ACOMPANIA'
  flags[0x58] = 'CHOCOBO_ACOMPANIA'
  flags[0x5b] = 'DEJE_CHOCOBO_EN_01'
  flags[0x5c] = 'DEJE_CHOCOBO_EN_02'
  flags[0x5d] = 'DEJE_CHOCOBO_EN_03'
  flags[0x5e] = 'DEJE_CHOCOBO_EN_04'
  flags[0x5f] = 'DEJE_CHOCOBO_EN_05'
  flags[0x60] = 'DEJE_CHOCOBO_EN_06'
  flags[0x61] = 'DEJE_CHOCOBO_EN_07'
  flags[0x62] = 'DEJE_CHOCOBO_EN_08'
  flags[0x63] = 'DEJE_CHOCOBO_EN_09'
  flags[0x64] = 'DEJE_CHOCOBO_EN_10'
  flags[0x65] = 'DEJE_CHOCOBO_EN_11'
  flags[0x66] = 'DEJE_CHOCOBO_EN_12'
  flags[0x67] = 'DEJE_CHOCOBO_EN_13'
  flags[0x68] = 'DEJE_CHOCOBO_EN_14'
  flags[0x69] = 'DEJE_CHOCOBO_EN_15'
  flags[0x6a] = 'DEJE_CHOCOBO_EN_16'
  flags[0x6b] = 'DEJE_CHOCOBO_EN_17'
  flags[0x6c] = 'DEJE_CHOCOBO_EN_18'
  flags[0x6d] = 'DEJE_CHOCOBO_EN_19'
  flags[0x6e] = 'DEJE_CHOCOBO_EN_20'
  flags[0x6f] = 'ARRIBA_DEL_CHOCOBO'
  flags[0x70] = 'CHOCOBOT_SOBRE_AGUA'
  # cuando nos hacen una pregunta si-no
#  flags[0x7f] = 'ELIGIMOS_NO'

  # nombres de los monstruos grandes
  bosses[0x00] = 'VAMPIRE_LEE'
  bosses[0x01] = 'HYDRA'
  bosses[0x02] = 'MEDUSA'
  bosses[0x03] = 'MEGAPEDE'
  bosses[0x04] = 'DAVIAS'
  bosses[0x05] = 'GOLEM_ROBOT'
  bosses[0x06] = 'CYCLOPS'
  bosses[0x07] = 'CHIMERA'
  bosses[0x08] = 'KARY'
  bosses[0x09] = 'KRAKEN'
  bosses[0x0a] = 'PIRUS_IFLYTE'
  bosses[0x0b] = 'LICH_SENSEMANN'
  bosses[0x0c] = 'GARUDA'
  bosses[0x0d] = 'DRAGON'
  bosses[0x0e] = 'JULIUS_2ND_FORM'
  bosses[0x0f] = 'DRAGON_ZOMBIE'
  bosses[0x10] = 'JACKAL_BIGCAT'
  bosses[0x11] = 'JULIUS_3RD_FORM'
  bosses[0x12] = 'METAL_CRAB_CANGREJO'
  bosses[0x13] = 'MANTIS_ANT'
  bosses[0x14] = 'DRAGON_RED'

  # nombres de los personajes
  personajes[0x00] = 'SNOWMAN_STILL'
  personajes[0x01] = 'FUJI_FOLLOWING'
  personajes[0x02] = 'MYSTERYMAN_FOLLOWING'
  personajes[0x03] = 'WATTS_FOLLOWING'
  personajes[0x04] = 'BOGARD_FOLLOWING'
  personajes[0x05] = 'AMANDA_FOLLOWING'
  personajes[0x06] = 'LESTER_FOLLOWING'
  personajes[0x07] = 'MARCIE_FOLLOWING'
  personajes[0x08] = 'CHOCOBO_FOLLOWING'
  personajes[0x09] = 'CHOCOBOT_FOLLOWING'
  personajes[0x0a] = 'WEREWOLF_1'
  personajes[0x0b] = 'INV_CURE'
  personajes[0x0c] = 'CHEST_1'
  personajes[0x0d] = 'CHEST_2'
  personajes[0x0e] = 'CHEST_3'
  personajes[0x0f] = 'CHEST_4'
  personajes[0x10] = 'CHIBIDEVIL'
  personajes[0x11] = 'RABBITE'
  personajes[0x12] = 'GOBLIN'
  personajes[0x13] = 'MUSHROOM'
  personajes[0x14] = 'JELLYFISH'
  personajes[0x15] = 'SWAMPMAN'
  personajes[0x16] = 'LIZARDMAN'
  personajes[0x17] = 'FLOWER'
  personajes[0x18] = 'FACEORB'
  personajes[0x19] = 'SKELETON'
  personajes[0x1a] = 'EVIL_PLANT'
  personajes[0x1b] = 'FLYING_FISH'
  personajes[0x1c] = 'ZOMBIE'
  personajes[0x1d] = 'MOUSE'
  personajes[0x1e] = 'PUMPKIN'
  personajes[0x1f] = 'OWL'
  personajes[0x20] = 'BEE'
  personajes[0x21] = 'CLOUD'
  personajes[0x22] = 'PIG'
  personajes[0x23] = 'CRAB'
  personajes[0x24] = 'SPIDER'
  personajes[0x25] = 'INV_OPEN_NORTH'
  personajes[0x26] = 'INV_OPEN_SOUTH'
  personajes[0x27] = 'INV_OPEN_EAST'
  personajes[0x28] = 'INV_OPEN_WEST'
  personajes[0x29] = 'MIMIC_CHEST'
  personajes[0x2a] = 'HOPPING_BUG'
  personajes[0x2b] = 'PORCUPINE'
  personajes[0x2c] = 'CARROT'
  personajes[0x2d] = 'EYE_SPY'
  personajes[0x2e] = 'WEREWOLF_2'
  personajes[0x2f] = 'GHOST'
  personajes[0x30] = 'BASILISK'
  personajes[0x31] = 'SCORPION'
  personajes[0x32] = 'SAURUS'
  personajes[0x33] = 'MUMMY'
  personajes[0x34] = 'PAKKUN_LIZARD'
  personajes[0x35] = 'SNAKE'
  personajes[0x36] = 'SHADOW'
  personajes[0x37] = 'BLACK_WIZARD'
  personajes[0x38] = 'FLAME'
  personajes[0x39] = 'GARGOYLE'
  personajes[0x3a] = 'MONKEY'
  personajes[0x3b] = 'MOLEBEAR'
  personajes[0x3c] = 'OGRE'
  personajes[0x3d] = 'BARNACLEJACK'
  personajes[0x3e] = 'PHANTASM'
  personajes[0x3f] = 'MINOTAUR'
  personajes[0x40] = 'GLAIVE_MAGE'
  personajes[0x41] = 'GLAIVE_KNIGHT'
  personajes[0x42] = 'DARK_LORD'
  personajes[0x43] = 'MEGA_FLYTRAP'
  personajes[0x44] = 'DRAGONFLY'
  personajes[0x45] = 'ARMADILLO'
  personajes[0x46] = 'SNOWMAN_MOVING'
  personajes[0x47] = 'SABER_CAT'
  personajes[0x48] = 'WALRUS'
  personajes[0x49] = 'DUCK_SOLDIER'
  personajes[0x4a] = 'POTO_RABBIT'
  personajes[0x4b] = 'CYCLONE'
  personajes[0x4c] = 'BEHOLDER_EYE'
  personajes[0x4d] = 'MANTA_RAY'
  personajes[0x4e] = 'JUMPING_HAND'
  personajes[0x4f] = 'TORTOISE'
  personajes[0x50] = 'FIRE_MOTH'
  personajes[0x51] = 'EARTH_DIGGER'
  personajes[0x52] = 'DENDEN_SNAIL'
  personajes[0x53] = 'DOPPEL_MIRROR'
  personajes[0x54] = 'GUARDIAN'
  personajes[0x55] = 'EVIL_SWORD'
  personajes[0x56] = 'GAUNTLET'
  personajes[0x57] = 'GARASHA_DUCK'
  personajes[0x58] = 'FUZZY_WONDER'
  personajes[0x59] = 'ELEPHANT'
  personajes[0x5a] = 'NINJA'
  personajes[0x5b] = 'JULIUS'
  personajes[0x5c] = 'DEMON_HEAD'
  personajes[0x5d] = 'INV_DESSERT_CAVE_STONE'
  personajes[0x5e] = 'WATER_DEMON'
  personajes[0x5f] = 'SEA_DRAGON'
  personajes[0x60] = 'GALL_FISH'
  personajes[0x61] = 'WILLY'
  personajes[0x62] = 'MYSTERYMAN_1'
  personajes[0x63] = 'AMANDA_1'
  personajes[0x64] = 'AMANDA_ILL'
  personajes[0x65] = 'AMANDA_DEAD'
  personajes[0x66] = 'FUJI_1'
  personajes[0x67] = 'FUJI_WINDOW'
  personajes[0x68] = 'MOTHER'
  personajes[0x69] = 'BOGARD_1'
  personajes[0x6a] = 'BOGARD_2'
  personajes[0x6b] = 'KETTS_WEREWOLF'
  personajes[0x6c] = 'INV_FUJI_COFFIN'
  personajes[0x6d] = 'CIBBA'
  personajes[0x6e] = 'GUY_WENDEL'
  personajes[0x6f] = 'WATTS'
  personajes[0x70] = 'MINECART'
  personajes[0x71] = 'CHOCOBO_EGG'
  personajes[0x72] = 'DAVIAS'
  personajes[0x73] = 'LESTER_1'
  personajes[0x74] = 'LESTER_PARROT'
  personajes[0x75] = 'BOWOW'
  personajes[0x76] = 'SARAH'
  personajes[0x77] = 'MARCIE_1'
  personajes[0x78] = 'KING_OF_LORIM'
  personajes[0x79] = 'GLADIATOR_FRIEND'
  personajes[0x7a] = 'INV_INN'
  personajes[0x7b] = 'GIRL_TOPPLE'
  personajes[0x7c] = 'GUY_TOPPLE'
  personajes[0x7d] = 'GUY_TOPPLE_HOUSE'
  personajes[0x7e] = 'GIRL_TOPPLE_HOUSE'
  personajes[0x7f] = 'OLDMAN_TOPPLE'
  personajes[0x80] = 'GUY_KETTS'
  personajes[0x81] = 'GIRL_KETTS'
  personajes[0x82] = 'GIRL_CIBBA'
  personajes[0x83] = 'GUY_WENDEL'
  personajes[0x84] = 'GUY_WENDEL_HOUSE'
  personajes[0x85] = 'WOMAN_CIBBA'
  personajes[0x86] = 'OLDMAN_WENDEL'
  personajes[0x87] = 'DWARF_1'
  personajes[0x88] = 'DWARF_2'
  personajes[0x89] = 'DWARF_3'
  personajes[0x8a] = 'DWARF_4'
  personajes[0x8b] = 'DWARF_5'
  personajes[0x8c] = 'GUY_AIRSHIP_1'
  personajes[0x8d] = 'GUY_AIRSHIP_2'
  personajes[0x8e] = 'GUY_AIRSHIP_3'
  personajes[0x8f] = 'GUY_AIRSHIP_4'
  personajes[0x90] = 'OLDMAN_MENOS_1'
  personajes[0x91] = 'GUY_MENOS'
  personajes[0x92] = 'GIRL_MENOS_1'
  personajes[0x93] = 'OLDMAN_MENOS_2'
  personajes[0x94] = 'GIRL_MENOS'
  personajes[0x95] = 'WOMAN_MENOS_2'
  personajes[0x96] = 'GIRL_JADD_1'
  personajes[0x97] = 'OLDMAN_JADD'
  personajes[0x98] = 'GIRL_JADD_2'
  personajes[0x99] = 'GUY_JADD'
  personajes[0x9a] = 'DWARF_JADD'
  personajes[0x9b] = 'SALESMAN_JADD'
  personajes[0x9c] = 'GIRL_JADD_3'
  personajes[0x9d] = 'BOY_JADD'
  personajes[0x9e] = 'OLDMAN_ISH'
  personajes[0x9f] = 'GUY_ISH_1'
  personajes[0xa0] = 'GUY_ISH_2'
  personajes[0xa1] = 'GIRL_ISH'
  personajes[0xa2] = 'GUY_ISH_3'
  personajes[0xa3] = 'GUY_ISH_4'
  personajes[0xa4] = 'INV_STONE_1'
  personajes[0xa5] = 'INV_STONE_2'
  personajes[0xa6] = 'INV_STONE_3'
  personajes[0xa7] = 'INV_STONE_4'
  personajes[0xa8] = 'INV_STONE_5'
  personajes[0xa9] = 'INV_STONE_6'
  personajes[0xaa] = 'INV_STONE_7'
  personajes[0xab] = 'INV_STONE_8'
  personajes[0xac] = 'GUY_LORIM_FROZEN'
  personajes[0xad] = 'GUY_LORIM_1'
  personajes[0xae] = 'GUY_LORIM_2'
  personajes[0xaf] = 'SALESMAN'
  personajes[0xb0] = 'INV_SALESMAN_1'
  personajes[0xb1] = 'FUJI_2'
  personajes[0xb2] = 'INV_SALESMAN_2'
  personajes[0xb3] = 'MYSTERYMAN_2'
  personajes[0xb4] = 'BOGARD_3'
  personajes[0xb5] = 'AMANDA_2'
  personajes[0xb6] = 'LESTER_2'
  personajes[0xb7] = 'MARCIE_2'
  personajes[0xb8] = 'CHOCOBOT'
  personajes[0xb9] = 'CHOCOBO_1'
  personajes[0xba] = 'CHOCOBO_2'
  personajes[0xbb] = 'PRISION_BARS'
  personajes[0xbc] = 'MUSIC_NOTES'
  personajes[0xbd] = 'MAGIC_SALESMAN'
  personajes[0xbe] = 'LAST_GUY'


  # nombres de las ventanas/paneles
  windows[0x00] = 'ITEM/MAGIC/EQUIP/ASK'
  windows[0x01] = 'ITEMS'
  windows[0x02] = 'MAGIC'
  windows[0x03] = 'EQUIP_HEADER'
  windows[0x04] = 'EQUIP'
  windows[0x06] = 'DIALOG_TOP'
  windows[0x0a] = 'CURRENT_ITEM'
  windows[0x11] = 'SELECT'
  windows[0x13] = 'GOLD'
  windows[0x1b] = 'SAVE_1'
  windows[0x1c] = 'SAVE_2'
  windows[0x1d] = 'NAMING_HEADER'
  windows[0x1e] = 'NAMING'
  windows[0x1f] = 'NEW_GAME_CONTINUE'
 

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


