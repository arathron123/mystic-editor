import mystic.variables


#nombresOriginales = False
nombresOriginales = True

# diccionario de flags
flags = {}
for i in range(0,0x78):
  flags[i] = 'flag_{:02x}'.format(i)
for i in range(0x78,0x80):
  flags[i] = 'flag_sinbatt_{:02x}'.format(i)
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


# diccionario de monstruos grandes
bosses = {}
for i in range(0,0x15):
  bosses[i] = 'boss_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
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


# dictionary of npcs
npc = {}
for i in range(0,0xbf):
  npc[i] = 'npc_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  # names of the npcs
  npc[0x00] = 'npc_SNOWMAN_STILL'
  npc[0x01] = 'npc_FUJI_FOLLOWING'
  npc[0x02] = 'npc_MYSTERYMAN_FOLLOWING'
  npc[0x03] = 'npc_WATTS_FOLLOWING'
  npc[0x04] = 'npc_BOGARD_FOLLOWING'
  npc[0x05] = 'npc_AMANDA_FOLLOWING'
  npc[0x06] = 'npc_LESTER_FOLLOWING'
  npc[0x07] = 'npc_MARCIE_FOLLOWING'
  npc[0x08] = 'npc_CHOCOBO_FOLLOWING'
  npc[0x09] = 'npc_CHOCOBOT_FOLLOWING'
  npc[0x0a] = 'npc_WEREWOLF_1'
  npc[0x0b] = 'npc_INV_CURE'
  npc[0x0c] = 'npc_CHEST_1'
  npc[0x0d] = 'npc_CHEST_2'
  npc[0x0e] = 'npc_CHEST_3'
  npc[0x0f] = 'npc_CHEST_OPEN'
  npc[0x10] = 'npc_CHIBIDEVIL'
  npc[0x11] = 'npc_RABBITE'
  npc[0x12] = 'npc_GOBLIN'
  npc[0x13] = 'npc_MUSHROOM'
  npc[0x14] = 'npc_JELLYFISH'
  npc[0x15] = 'npc_SWAMPMAN'
  npc[0x16] = 'npc_LIZARDMAN'
  npc[0x17] = 'npc_FLOWER'
  npc[0x18] = 'npc_FACEORB'
  npc[0x19] = 'npc_SKELETON'
  npc[0x1a] = 'npc_EVIL_PLANT'
  npc[0x1b] = 'npc_FLYING_FISH'
  npc[0x1c] = 'npc_ZOMBIE'
  npc[0x1d] = 'npc_MOUSE'
  npc[0x1e] = 'npc_PUMPKIN'
  npc[0x1f] = 'npc_OWL'
  npc[0x20] = 'npc_BEE'
  npc[0x21] = 'npc_CLOUD'
  npc[0x22] = 'npc_PIG'
  npc[0x23] = 'npc_CRAB'
  npc[0x24] = 'npc_SPIDER'
  npc[0x25] = 'npc_INV_OPEN_NORTH'
  npc[0x26] = 'npc_INV_OPEN_SOUTH'
  npc[0x27] = 'npc_INV_OPEN_EAST'
  npc[0x28] = 'npc_INV_OPEN_WEST'
  npc[0x29] = 'npc_MIMIC_CHEST'
  npc[0x2a] = 'npc_HOPPING_BUG'
  npc[0x2b] = 'npc_PORCUPINE'
  npc[0x2c] = 'npc_CARROT'
  npc[0x2d] = 'npc_EYE_SPY'
  npc[0x2e] = 'npc_WEREWOLF_2'
  npc[0x2f] = 'npc_GHOST'
  npc[0x30] = 'npc_BASILISK'
  npc[0x31] = 'npc_SCORPION'
  npc[0x32] = 'npc_SAURUS'
  npc[0x33] = 'npc_MUMMY'
  npc[0x34] = 'npc_PAKKUN_LIZARD'
  npc[0x35] = 'npc_SNAKE'
  npc[0x36] = 'npc_SHADOW'
  npc[0x37] = 'npc_BLACK_WIZARD'
  npc[0x38] = 'npc_FLAME'
  npc[0x39] = 'npc_GARGOYLE'
  npc[0x3a] = 'npc_MONKEY'
  npc[0x3b] = 'npc_MOLEBEAR'
  npc[0x3c] = 'npc_OGRE'
  npc[0x3d] = 'npc_BARNACLEJACK'
  npc[0x3e] = 'npc_PHANTASM'
  npc[0x3f] = 'npc_MINOTAUR'
  npc[0x40] = 'npc_GLAIVE_MAGE'
  npc[0x41] = 'npc_GLAIVE_KNIGHT'
  npc[0x42] = 'npc_DARK_LORD'
  npc[0x43] = 'npc_MEGA_FLYTRAP'
  npc[0x44] = 'npc_DRAGONFLY'
  npc[0x45] = 'npc_ARMADILLO'
  npc[0x46] = 'npc_SNOWMAN_MOVING'
  npc[0x47] = 'npc_SABER_CAT'
  npc[0x48] = 'npc_WALRUS'
  npc[0x49] = 'npc_DUCK_SOLDIER'
  npc[0x4a] = 'npc_POTO_RABBIT'
  npc[0x4b] = 'npc_CYCLONE'
  npc[0x4c] = 'npc_BEHOLDER_EYE'
  npc[0x4d] = 'npc_MANTA_RAY'
  npc[0x4e] = 'npc_JUMPING_HAND'
  npc[0x4f] = 'npc_TORTOISE'
  npc[0x50] = 'npc_FIRE_MOTH'
  npc[0x51] = 'npc_EARTH_DIGGER'
  npc[0x52] = 'npc_DENDEN_SNAIL'
  npc[0x53] = 'npc_DOPPEL_MIRROR'
  npc[0x54] = 'npc_GUARDIAN'
  npc[0x55] = 'npc_EVIL_SWORD'
  npc[0x56] = 'npc_GAUNTLET'
  npc[0x57] = 'npc_GARASHA_DUCK'
  npc[0x58] = 'npc_FUZZY_WONDER'
  npc[0x59] = 'npc_ELEPHANT'
  npc[0x5a] = 'npc_NINJA'
  npc[0x5b] = 'npc_JULIUS'
  npc[0x5c] = 'npc_DEMON_HEAD'
  npc[0x5d] = 'npc_INV_DESSERT_CAVE_STONE'
  npc[0x5e] = 'npc_WATER_DEMON'
  npc[0x5f] = 'npc_SEA_DRAGON'
  npc[0x60] = 'npc_GALL_FISH'
  npc[0x61] = 'npc_WILLY'
  npc[0x62] = 'npc_MYSTERYMAN_1'
  npc[0x63] = 'npc_AMANDA_1'
  npc[0x64] = 'npc_AMANDA_ILL'
  npc[0x65] = 'npc_AMANDA_DEAD'
  npc[0x66] = 'npc_FUJI_1'
  npc[0x67] = 'npc_FUJI_WINDOW'
  npc[0x68] = 'npc_MOTHER'
  npc[0x69] = 'npc_BOGARD_1'
  npc[0x6a] = 'npc_BOGARD_2'
  npc[0x6b] = 'npc_KETTS_WEREWOLF'
  npc[0x6c] = 'npc_INV_FUJI_COFFIN'
  npc[0x6d] = 'npc_CIBBA'
  npc[0x6e] = 'npc_GUY_WENDEL'
  npc[0x6f] = 'npc_WATTS'
  npc[0x70] = 'npc_TROLLEY'
  npc[0x71] = 'npc_CHOCOBO_EGG'
  npc[0x72] = 'npc_DAVIAS'
  npc[0x73] = 'npc_LESTER_1'
  npc[0x74] = 'npc_LESTER_PARROT'
  npc[0x75] = 'npc_BOWOW'
  npc[0x76] = 'npc_SARAH'
  npc[0x77] = 'npc_MARCIE_1'
  npc[0x78] = 'npc_KING_OF_LORIM'
  npc[0x79] = 'npc_GLADIATOR_FRIEND'
  npc[0x7a] = 'npc_INV_INN'
  npc[0x7b] = 'npc_GIRL_TOPPLE'
  npc[0x7c] = 'npc_GUY_TOPPLE'
  npc[0x7d] = 'npc_BOY_TOPPLE_HOUSE'
  npc[0x7e] = 'npc_GIRL_TOPPLE_HOUSE'
  npc[0x7f] = 'npc_OLDMAN_TOPPLE'
  npc[0x80] = 'npc_GUY_KETTS'
  npc[0x81] = 'npc_GIRL_KETTS'
  npc[0x82] = 'npc_GIRL_CIBBA'
  npc[0x83] = 'npc_BOY_WENDEL'
  npc[0x84] = 'npc_GUY_WENDEL_HOUSE'
  npc[0x85] = 'npc_WOMAN_CIBBA'
  npc[0x86] = 'npc_OLDMAN_WENDEL'
  npc[0x87] = 'npc_DWARF_1'
  npc[0x88] = 'npc_DWARF_2'
  npc[0x89] = 'npc_DWARF_3'
  npc[0x8a] = 'npc_DWARF_4'
  npc[0x8b] = 'npc_DWARF_5'
  npc[0x8c] = 'npc_GUY_AIRSHIP_1'
  npc[0x8d] = 'npc_GUY_AIRSHIP_2'
  npc[0x8e] = 'npc_GUY_AIRSHIP_3'
  npc[0x8f] = 'npc_GUY_AIRSHIP_4'
  npc[0x90] = 'npc_OLDMAN_MENOS_1'
  npc[0x91] = 'npc_BOY_MENOS'
  npc[0x92] = 'npc_GIRL_MENOS_1'
  npc[0x93] = 'npc_OLDMAN_MENOS_2'
  npc[0x94] = 'npc_GIRL_MENOS'
  npc[0x95] = 'npc_WOMAN_MENOS_2'
  npc[0x96] = 'npc_GIRL_JADD_1'
  npc[0x97] = 'npc_OLDMAN_JADD'
  npc[0x98] = 'npc_GIRL_JADD_2'
  npc[0x99] = 'npc_BOY_JADD'
  npc[0x9a] = 'npc_DWARF_JADD'
  npc[0x9b] = 'npc_SALESMAN_JADD'
  npc[0x9c] = 'npc_GIRL_JADD_3'
  npc[0x9d] = 'npc_GUY_JADD'
  npc[0x9e] = 'npc_OLDMAN_ISH'
  npc[0x9f] = 'npc_GUY_ISH_1'
  npc[0xa0] = 'npc_GUY_ISH_2'
  npc[0xa1] = 'npc_GIRL_ISH'
  npc[0xa2] = 'npc_GUY_ISH_3'
  npc[0xa3] = 'npc_BOY_ISH'
  npc[0xa4] = 'npc_INV_STONE_1'
  npc[0xa5] = 'npc_INV_STONE_2'
  npc[0xa6] = 'npc_INV_STONE_3'
  npc[0xa7] = 'npc_INV_STONE_4'
  npc[0xa8] = 'npc_INV_STONE_5'
  npc[0xa9] = 'npc_INV_STONE_6'
  npc[0xaa] = 'npc_INV_STONE_7'
  npc[0xab] = 'npc_INV_STONE_8'
  npc[0xac] = 'npc_GUY_LORIM_FROZEN'
  npc[0xad] = 'npc_GUY_LORIM_1'
  npc[0xae] = 'npc_GUY_LORIM_2'
  npc[0xaf] = 'npc_SALESMAN'
  npc[0xb0] = 'npc_INV_SALESMAN_1'
  npc[0xb1] = 'npc_FUJI_2'
  npc[0xb2] = 'npc_INV_SALESMAN_2'
  npc[0xb3] = 'npc_MYSTERYMAN_2'
  npc[0xb4] = 'npc_BOGARD_3'
  npc[0xb5] = 'npc_AMANDA_2'
  npc[0xb6] = 'npc_LESTER_2'
  npc[0xb7] = 'npc_MARCIE_2'
  npc[0xb8] = 'npc_CHOCOBOT'
  npc[0xb9] = 'npc_CHOCOBO_1'
  npc[0xba] = 'npc_CHOCOBO_2'
  npc[0xbb] = 'npc_PRISION_BARS'
  npc[0xbc] = 'npc_MUSIC_NOTES'
  npc[0xbd] = 'npc_MAGIC_SALESMAN'
  npc[0xbe] = 'npc_LAST_GUY'


# dictionary of projectiles
projectiles = {}
for i in range(0,40):
  projectiles[i] = 'proj_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  projectiles[0x00] = 'proj_GOBLIN_DAGGER'
  projectiles[0x01] = 'proj_VOICE'
  projectiles[0x02] = 'proj_NEEDLE'
  projectiles[0x03] = 'proj_HARPOON'
  projectiles[0x04] = 'proj_HERO_MIMIC'
  projectiles[0x05] = 'proj_GUARDIAN_LASER'
  projectiles[0x06] = 'proj_MINOTAUR_AXE'
  projectiles[0x07] = 'proj_PINCER'
  projectiles[0x08] = 'proj_RIBINGUUMU'
  projectiles[0x09] = 'proj_BOULDER'
  projectiles[0x0a] = 'proj_SHURIKEN'
  projectiles[0x0b] = 'proj_BEAM'
  projectiles[0x0c] = 'proj_FIRE'
  projectiles[0x0d] = 'proj_BLIZZARD'
  projectiles[0x0e] = 'proj_THUNDERBOLT'
  projectiles[0x0f] = 'proj_POISON_STRING'
  projectiles[0x10] = 'proj_LIZARDMAN_ARROW'
  projectiles[0x11] = 'proj_GLAIVE_SWORD'
  projectiles[0x12] = 'proj_RAPIER'
  projectiles[0x13] = 'proj_SCORPION_TAIL'
  projectiles[0x14] = 'proj_FIRE_BREATH'
  projectiles[0x15] = 'proj_TALON'
  projectiles[0x16] = 'proj_NUKE'
  projectiles[0x17] = 'proj_MIMIC'
  projectiles[0x18] = 'proj_BOGARD_SWORD'
  projectiles[0x19] = 'proj_WATTS_AXE'
  projectiles[0x1a] = 'proj_AMANDA_DAGGER'
  projectiles[0x1b] = 'proj_LESTER_ARROW'
  projectiles[0x1c] = 'proj_MARCIE_LASER'
  projectiles[0x1d] = 'proj_MYSTERYMAN_FIRE'
  projectiles[0x1e] = 'proj_BAT'
  projectiles[0x1f] = 'proj_HYDRA_FIREBALL'
  projectiles[0x20] = 'proj_SNAKE'
  projectiles[0x21] = 'proj_FEATHER'
  projectiles[0x22] = 'proj_SKULL'
  projectiles[0x23] = 'proj_CHIMERA_FIREBALL'
  projectiles[0x24] = 'proj_JULIUS_THUNDERBOLT'
  projectiles[0x25] = 'proj_JULIUS_NUKE'
  projectiles[0x26] = 'proj_DAVIAS_VORTEX'
  projectiles[0x27] = 'proj_DRAGON_VORTEX'


# dictionary of hero sprites
hero = {}
for i in range(0,22):
  hero[i] = 'hero_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  hero[0x00] = 'hero_STANDING'
  hero[0x01] = 'hero_WALKING'
  hero[0x02] = 'hero_FALLING'
  hero[0x03] = 'hero_UNUSED_1'
  hero[0x04] = 'hero_ATTACK_START'
  hero[0x05] = 'hero_ATTACK_END'
  hero[0x06] = 'hero_SPECIAL_ATTACK'
  hero[0x07] = 'hero_ATTACK_2'
  hero[0x08] = 'hero_ATTACK_3'
  hero[0x09] = 'hero_ATTACK_4'
  hero[0x0a] = 'hero_TROLLEY'
  hero[0x0b] = 'hero_DEAD'
  hero[0x0c] = 'hero_MOOGLE_STANDING'
  hero[0x0d] = 'hero_MOOGLE_WALKING'
  hero[0x0e] = 'hero_MOOGLE_HEAD'
  hero[0x0f] = 'hero_UNUSED_2'
  hero[0x10] = 'hero_CHOCOBO_STANDING'
  hero[0x11] = 'hero_CHOCOBO_WALKING'
  hero[0x12] = 'hero_CHOCOBOT_STANDING'
  hero[0x13] = 'hero_CHOCOBOT_WALKING'
  hero[0x14] = 'hero_CHOCOBOAT_STANDING'
  hero[0x15] = 'hero_CHOCOBOAT_WALKING'


# diccionario de ventanas/paneles
windows = {}
for i in range(0,34):
  windows[i] = 'win_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  # nombres de las ventanas/paneles
  windows[0x00] = 'win_START_MENU'
  windows[0x01] = 'win_ITEMS'
  windows[0x02] = 'win_MAGIC'
  windows[0x03] = 'win_EQUIP_TOP'
  windows[0x04] = 'win_EQUIP_BOTTOM'
  windows[0x05] = 'win_UNUSED1'
  windows[0x06] = 'win_DIALOG'
  windows[0x07] = 'win_YES_NO'
  windows[0x08] = 'win_UNUSED2'
  windows[0x09] = 'win_MENU_STATUS_POIS'
  windows[0x0a] = 'win_MENU_EQUIPED'
  windows[0x0b] = 'win_VENDOR_BUY_SELL'
  windows[0x0c] = 'win_VENDOR_GOLD'
  windows[0x0d] = 'win_VENDOR_SELL_TOP'
  windows[0x0e] = 'win_VENDOR_BUY_TOP'
  windows[0x0f] = 'win_VENDOR_TEXT_TOP'
  windows[0x10] = 'win_VENDOR_SELL_NO'
  windows[0x11] = 'win_SELECT_MENU'
  windows[0x12] = 'win_STATUS_RIGHT'
  windows[0x13] = 'win_STATUS_GOLD'
  windows[0x14] = 'win_STATUS_HP_MP'
  windows[0x15] = 'win_STATUS_TOP_NAME'
  windows[0x16] = 'win_UNUSED3'
  windows[0x17] = 'win_LEVEL_UP_STATS'
  # esta está anulada?
  windows[0x18] = 'win_LEVEL_UP_STATS_OPTIONS'
  windows[0x19] = 'win_YES_NO'
  windows[0x1a] = 'win_STATUS_AP_DP'
  windows[0x1b] = 'win_SAVE_TOP'
  windows[0x1c] = 'win_SAVE_BOTTOM'
  windows[0x1d] = 'win_NAMING_TOP'
  windows[0x1e] = 'win_NAMING_BOTTOM'
  windows[0x1f] = 'win_NEW_GAME_CONTINUE'
  windows[0x20] = 'win_STATUS_EFFECT_POIS'
  windows[0x21] = 'win_LEVEL_UP'

#  windows[0x17] = 'win_STATUS_EFFECT'
  # esta está anulada?
#  windows[0x18] = 'win_LEVEL_UP_STATS'
#  windows[0x19] = 'win_LEVEL_UP_STATS1'
#  windows[0x1a] = 'win_LEVEL_UP_STATS_OPTIONS'
#  windows[0x1b] = 'win_YES_NO'
#  windows[0x1c] = 'win_SAVE_1'
#  windows[0x1d] = 'win_SAVE_2'
#  windows[0x1e] = 'win_NAMING_TOP'
#  windows[0x1f] = 'win_NAMING'
#  windows[0x20] = 'win_NEW_GAME_CONTINUE'
#  windows[0x21] = 'win_STATUS_EFFECT'
#  windows[0x22] = 'win_LEVEL_UP'

 


# diccionario de canciones
songs = {}
for i in range(0,31):
  songs[i] = 'song_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  # nombres de las canciones
  songs[0x00] = 'song_MUTE'             # 0
  songs[0x01] = 'song_RISING_SUN'       # 1
  songs[0x02] = 'song_IN_SORROW'        # 2
  songs[0x03] = 'song_MANA_MISION'      # 3
  songs[0x04] = 'song_VILLAGE'          # 4
  songs[0x05] = 'song_CHOCOBOS_BIRTH'   # 5
  songs[0x06] = 'song_CHOCOBOS_THEME'   # 6
  songs[0x07] = 'song_DUNGEON_1'        # 7
  songs[0x08] = 'song_DUNGEON_2'        # 8
  songs[0x09] = 'song_DANGER'           # 9
  songs[0x0a] = 'song_JULIUS_AMBITION'  # 10
  songs[0x0b] = 'song_ROYAL_PALACE'     # 11
  songs[0x0c] = 'song_DUNGEON_3'        # 12
  songs[0x0d] = 'song_LET_THOUGHTS_RIDE_ON_KNOWLEDGE' #13
  songs[0x0e] = 'song_GLANCE_DUKEDOM'   # 14
  songs[0x0f] = 'song_FIGHT_1'          # 15
  songs[0x10] = 'song_FINAL_BATTLE'     # 16
  songs[0x11] = 'song_JINGLE'           # 17
  songs[0x12] = 'song_MOOGLES'          # 18
  songs[0x13] = 'song_FIGHT_2'          # 19
  songs[0x14] = 'song_OVERWORLD_1'      # 20
  songs[0x15] = 'song_SUNSET'           # 21
  songs[0x16] = 'song_MANA_PALACE'      # 22
  songs[0x17] = 'song_REQUIEM'          # 23
  songs[0x18] = 'song_DWARVES_THEME'    # 24
  songs[0x19] = 'song_OVERWORLD_2'      # 25
  songs[0x1a] = 'song_FIGHTING_ARENA'   # 26
  songs[0x1b] = 'song_GEMMAS_REALIZATION' # 27
  songs[0x1c] = 'song_LEVEL_UP'         # 28
  songs[0x1d] = 'song_TENSION'          # 29
  songs[0x1e] = 'song_ILL'              # 30


# diccionario de los efectos de sonido sfx
sounds = {}
for i in range(0,38):
  sounds[i] = 'sfx_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  sounds[0x00] = 'sfx_MUTE'
  sounds[0x01] = 'sfx_SWORD_SLIDE'
  sounds[0x02] = 'sfx_SWORD_STRAIGHT'
  sounds[0x03] = 'sfx_FIRE'
  sounds[0x04] = 'sfx_BREAK_WALL_IDK'
  sounds[0x05] = 'sfx_CURE'
  sounds[0x06] = 'sfx_LESTER_CURED'
  sounds[0x07] = 'sfx_CUACK'
  sounds[0x08] = 'sfx_KAMEHAMEHA'
  sounds[0x09] = 'sfx_STRANGE_FALL_IDK'
  sounds[0x0a] = 'sfx_BLING'
  sounds[0x0b] = 'sfx_ENEMY_DEFEATED'
  sounds[0x0c] = 'sfx_FALLING'
  sounds[0x0d] = 'sfx_ENEMY_HIT'
  sounds[0x0e] = 'sfx_WRONG_PHONE'
  sounds[0x0f] = 'sfx_OPEN_CHEST'
  sounds[0x10] = 'sfx_CLOSE_DOOR'
  sounds[0x11] = 'sfx_HUGE_EXPLOSION'
  sounds[0x12] = 'sfx_ITEM_SELECT'
  sounds[0x13] = 'sfx_MAGIC_BLEEP'
  sounds[0x14] = 'sfx_SPLASH'
  sounds[0x15] = 'sfx_SHIELD_BLOCKING'
  sounds[0x16] = 'sfx_METAL_CLASHING'
  sounds[0x17] = 'sfx_NEVERENDING_STEAM_ENGINE'
  sounds[0x18] = 'sfx_PASSAGE_FOUND'
  sounds[0x19] = 'sfx_SMALL_EXPLOSION'
  sounds[0x1a] = 'sfx_MEDIUM_EXPLOSION'
  sounds[0x1b] = 'sfx_NEVERENDING_HELICOPTER'
  sounds[0x1c] = 'sfx_CHAIN_IDK'
  sounds[0x1d] = 'sfx_CHAIN2_IDK'
  sounds[0x1e] = 'sfx_SICKLE'
  sounds[0x1f] = 'sfx_MORNING_STAR'
  sounds[0x20] = 'sfx_DEFEATED'
  sounds[0x21] = 'sfx_SWORD_SPECIAL'
  sounds[0x22] = 'sfx_NOSOUND'
  sounds[0x23] = 'sfx_BEEP'
  sounds[0x24] = 'sfx_BOOP'
  sounds[0x25] = 'sfx_FIRE_ATTACKED'

# dictionary of hero-projectile frames
hero_projectile_frame = {}
for i in range(0,48):
  hero_projectile_frame[i] = 'frame_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  hero_projectile_frame[0] = 'frame_SWORD'
  hero_projectile_frame[1] = 'frame_KAMEHAMEHA'
  hero_projectile_frame[2] = 'frame_FIRE'
  hero_projectile_frame[3] = 'frame_ICE'
  hero_projectile_frame[4] = 'frame_FIRE1'
  hero_projectile_frame[5] = 'frame_FIRE2'
  hero_projectile_frame[6] = 'frame_ICE1'
  hero_projectile_frame[7] = 'frame_ICE2'
  hero_projectile_frame[8] = 'frame_ICE3'
  hero_projectile_frame[9] = 'frame_ICE4'
  hero_projectile_frame[10] = 'frame_CURE1'
  hero_projectile_frame[11] = 'frame_CURE2'
  hero_projectile_frame[12] = 'frame_CURE3'
  hero_projectile_frame[13] = 'frame_CURE4'
  hero_projectile_frame[14] = 'frame_PURE'
  hero_projectile_frame[15] = 'frame_PURE1'
  hero_projectile_frame[16] = 'frame_PURE2'
  hero_projectile_frame[17] = 'frame_PURE3'
  hero_projectile_frame[18] = 'frame_PURE4'
  hero_projectile_frame[19] = 'frame_BLANK'
  hero_projectile_frame[20] = 'frame_SLEEP1'
  hero_projectile_frame[21] = 'frame_SLEEP2'
  hero_projectile_frame[22] = 'frame_SLEEP3'
  hero_projectile_frame[23] = 'frame_SLEEP4'
  hero_projectile_frame[24] = 'frame_MUTE1'
  hero_projectile_frame[25] = 'frame_MUTE2'
  hero_projectile_frame[26] = 'frame_MUTE3'
  hero_projectile_frame[27] = 'frame_MUTE4'
  hero_projectile_frame[28] = 'frame_NUKE1'
  hero_projectile_frame[29] = 'frame_NUKE2'
  hero_projectile_frame[30] = 'frame_THUNDER1'
  hero_projectile_frame[31] = 'frame_THUNDER2'
  hero_projectile_frame[32] = 'frame_THUNDER3'
  hero_projectile_frame[33] = 'frame_AXE'
  hero_projectile_frame[34] = 'frame_CHAIN'
  hero_projectile_frame[35] = 'frame_CHAIN1'
  hero_projectile_frame[36] = 'frame_CHAIN2'
  hero_projectile_frame[37] = 'frame_CHAIN3'
  hero_projectile_frame[38] = 'frame_CHAIN4'
  hero_projectile_frame[39] = 'frame_SICKLE'
  hero_projectile_frame[40] = 'frame_SICKLE1'
  hero_projectile_frame[41] = 'frame_SPEAR1'
  hero_projectile_frame[42] = 'frame_SPEAR2'
  hero_projectile_frame[43] = 'frame_MORNINGSTAR'
  hero_projectile_frame[44] = 'frame_MATTOCK'
  hero_projectile_frame[45] = 'frame_MATTOCK1'
  hero_projectile_frame[46] = 'frame_MATTOCK2'
  hero_projectile_frame[47] = 'frame_MATTOCK3'

# dictionary of hero-projectile frames
hero_projs_animation = {}
for i in range(0,48):
  hero_projs_animation[i] = 'anim_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  hero_projs_animation[0] = 'anim_EXPLOSION'
  hero_projs_animation[1] = 'anim_SWORD'
  hero_projs_animation[2] = 'anim_AXE'
  hero_projs_animation[3] = 'anim_CHAIN'
  hero_projs_animation[4] = 'anim_SICKLE'
  hero_projs_animation[5] = 'anim_SPEAR'
  hero_projs_animation[6] = 'anim_MORNINGSTAR'
  hero_projs_animation[7] = 'anim_NOTHING'
  hero_projs_animation[8] = 'anim_CURE'
  hero_projs_animation[9] = 'anim_PURE'
  hero_projs_animation[10] = 'anim_MUTE'
  hero_projs_animation[11] = 'anim_SLEEP'
  hero_projs_animation[12] = 'anim_FIRE'
  hero_projs_animation[13] = 'anim_ICE'
  hero_projs_animation[14] = 'anim_THUNDER'
  hero_projs_animation[15] = 'anim_NUKE'


# diccionario de magias
magic = {}
for i in range(0,8):
  magic[i] = 'magic_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  magic[0] = 'magic_CURE' 
  magic[1] = 'magic_HEAL' 
  magic[2] = 'magic_MUTE' 
  magic[3] = 'magic_SLEEP' 
  magic[4] = 'magic_FIRE' 
  magic[5] = 'magic_ICE' 
  magic[6] = 'magic_LIT' 
  magic[7] = 'magic_NUKE' 


#self.equipamiento = {}
# 0x09 empieza los items de items
# 0x42 empieza los items de armas

item = {}
for i in range(0,57):
  item[i] = 'item_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  item[0] = 'item_CURE'
  item[1] = 'item_X-CURE'
  item[2] = 'item_ETHER'
  item[3] = 'item_X-ETHER'
  item[4] = 'item_ELIXIR'
  item[5] = 'item_PURE'
  item[6] = 'item_EYEDROP'
  item[7] = 'item_SOFT'
  item[8] = 'item_MOOGLE'
  item[9] = 'item_UNICORN'
  item[10] = 'item_SILENCE'
  item[11] = 'item_PILLOW'
#  item[12] = 'item_UNUSED_1'
  item[12] = 'item_FLARE_WAVE'
#  item[13] = 'item_UNUSED_2'
  item[13] = 'item_FLARE_BAZOOKA'
  item[14] = 'item_FLAME'
  item[15] = 'item_BLAZE'
  item[16] = 'item_BLIZZARD'
  item[17] = 'item_FROST'
  item[18] = 'item_LITBOLT'
  item[19] = 'item_THUNDER'
  item[20] = 'item_CANDY'
#  item[21] = 'item_UNUSED_3'
  item[21] = 'item_DUMMY_SPARE_2'
  item[22] = 'item_KEY'
  item[23] = 'item_KEY_BONE'
  item[24] = 'item_KEY_BRONZE'
#  item[25] = 'item_UNUSED_4'
  item[25] = 'item_FIRE_RING'
#  item[26] = 'item_UNUSED_5'
  item[26] = 'item_RUSTED_KEY'
#  item[27] = 'item_UNUSED_6'
  item[27] = 'item_BLUE_ORB'
#  item[28] = 'item_UNUSED_7'
  item[28] = 'item_RED_ORB'
#  item[29] = 'item_UNUSED_8'
  item[29] = 'item_MANA_PENDANT'
  item[30] = 'item_MIRROR'
#  item[31] = 'item_UNUSED_9'
  item[31] = 'item_MYTHRIL'
#  item[32] = 'item_UNUSED_10'
  item[32] = 'item_STAR_SAPPHIRE'
  item[33] = 'item_AMANDA_TEAR'
#  item[34] = 'item_UNUSED_11'
  item[34] = 'item_BALANCER'
#  item[35] = 'item_UNUSED_12'
  item[35] = 'item_MOON_CRYSTAL'
  item[36] = 'item_OIL'
#  item[37] = 'item_UNUSED_13'
  item[37] = 'item_SCENARIO_SPARE_2'
#  item[38] = 'item_UNUSED_14'
  item[38] = 'item_SCENARIO_SPARE_3'
#  item[39] = 'item_UNUSED_15'
  item[39] = 'item_SCENARIO_SPARE_4'
#  item[40] = 'item_UNUSED_16'
  item[40] = 'item_SCENARIO_SPARE_5'
  item[41] = 'item_CRYSTAL'
#  item[42] = 'item_UNUSED_17'
  item[42] = 'item_MOON_CRYSTAL'
  item[43] = 'item_NECTAR'
  item[44] = 'item_STAMINA'
  item[45] = 'item_WISDOM'
  item[46] = 'item_WILL'
#  item[47] = 'item_UNUSED_18'
  item[47] = 'item_TORCH'
#  item[48] = 'item_UNUSED_19'
  item[48] = 'item_DWARF_LAMP'
  item[49] = 'item_GOLD'
  item[50] = 'item_FANG'
#  item[51] = 'item_UNUSED_20'
  item[51] = 'item_EARTH_DRUM'
#  item[52] = 'item_UNUSED_21'
  item[52] = 'item_MOOGLE_FLUTE'
  item[53] = 'item_MATTOCK'
  item[54] = 'item_RUBY'
  item[55] = 'item_OPAL'
#  item[56] = 'item_UNUSED_22'
  item[56] = 'item_RESERVE'

equip = {}
for i in range(0,8):
  equip[i] = 'equip_{:02x}'.format(i)
# si esta seteado mostrar los nombres originales
if(nombresOriginales):
  equip[0] = 'equip_BROAD_SWORD'
  equip[1] = 'equip_BATTLE_AXE'
  equip[2] = 'equip_SICKLE'
  equip[3] = 'equip_CHAIN'
  equip[4] = 'equip_SILVER_SWORD'
  equip[5] = 'equip_WIND_SPEAR'
  equip[6] = 'equip_WERE_AXE'
  equip[7] = 'equip_MORNING_STAR'
  equip[8] = 'equip_BLOOD_SWORD'
  equip[9] = 'equip_DRAGON_SWORD'
  equip[10] = 'equip_FLAME_CHAIN'
  equip[11] = 'equip_ICE_SWORD'
  equip[12] = 'equip_ZEUS_AXE'
  equip[13] = 'equip_RUSTY_SWORD'
  equip[14] = 'equip_THUNDER_SPEAR'
  equip[15] = 'equip_EXCALIBUR'
  equip[16] = 'equip_BRONZE_ARMOR'
  equip[17] = 'equip_IRON_ARMOR'
  equip[18] = 'equip_SILVER_ARMOR'
  equip[19] = 'equip_GOLD_ARMOR'
  equip[20] = 'equip_FLAME_ARMOR'
  equip[21] = 'equip_ICE_ARMOR'
  equip[22] = 'equip_DRAGON_ARMOR'
  equip[23] = 'equip_SAMURAI_ARMOR'
  equip[24] = 'equip_OPAL_ARMOR'
  equip[25] = 'equip_ARMOR_3'
  equip[26] = 'equip_ARMOR_4'
  equip[27] = 'equip_BRONZE_SHIELD'
  equip[28] = 'equip_IRON_SHIELD'
  equip[29] = 'equip_SILVER_SHIELD'
  equip[30] = 'equip_GOLD_SHIELD'
  equip[31] = 'equip_FLAME_SHIELD'
  equip[32] = 'equip_DRAGON_SHIELD'
  equip[33] = 'equip_AEGIS_SHIELD'
  equip[34] = 'equip_OPAL_SHIELD'
  equip[35] = 'equip_ICE_SHIELD'
  equip[36] = 'equip_SHIELD_3'
  equip[37] = 'equip_SHIELD_4'
  equip[38] = 'equip_BRONZE_HELMET'
  equip[39] = 'equip_IRON_HELMET'
  equip[40] = 'equip_SILVER_HELMET'
  equip[41] = 'equip_GOLD_HELMET'
  equip[42] = 'equip_OPAL_HELMET'
  equip[43] = 'equip_SAMURAI_HELMET'
  equip[44] = 'equip_HELMET_3'
  equip[45] = 'equip_HELMET_4'
  equip[46] = 'equip_AP'
  equip[47] = 'equip_DP'
 



def getLabel(val):
  # el primer bit indica si hay que negar la variable
  neg = val >= 0x80
  if(neg):
    val -= 0x80
  strNeg = '' if not neg else '~'
#  strVar = 'var[{:02x}] '.format(cond)
  strVar = flags[val]
  label = strNeg + strVar
  return label

def getVal(label):
  retVal = -1
#  print('ejecutando getVal(\'' + label + '\')')

  neg = False
  # si esta negada
  if(label.startswith('~')):
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

def getLabelSong(val):
  label = songs[val]
  return label
def getValSong(label):
  # por cada song
  for val in songs.keys():
    # me fijo el label
    lbl = songs[val]
    # si lo encontré
    if(lbl == label):
      retVal = val
      break
  return retVal

def getLabelSFX(val):
  label = sounds[val]
  return label
def getValSFX(label):
  # por cada sfx
  for val in sounds.keys():
    # me fijo el label
    lbl = sounds[val]
    # si lo encontré
    if(lbl == label):
      retVal = val
      break
  return retVal


