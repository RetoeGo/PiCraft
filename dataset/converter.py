import nbtlib
import trimesh
import open3d as o3d
import pyrender
import numpy as np
from PIL import Image
import pythreejs as p3js
from IPython.display import display
import matplotlib.pyplot as plt
import os
import time


def schematic_to_mesh(schematic):
    blocks = schematic['Blocks']
    data = schematic['Data']
    for j in blocks:
        data_val = int(j) 
    width = schematic['Width']
    height = schematic['Height']
    length = schematic['Length']
  
    block_colors = {
        "1.0": (131, 131, 131),  # stone
        "1.1": (131, 131, 131),  # granite
        "1.2": (131, 131, 131),  # polished granite
        "1.3": (131, 131, 131),  # diorite
        "1.4": (131, 131, 131),  # polished diorite
        "1.5": (131, 131, 131),  # andesite
        "1.6": (131, 131, 131),  # polished andesite

        "2.0": (131, 131, 131),  # Grass_block_top ?
        "3.0": (124, 90, 50),  # dirt
        "3.1": (124, 90, 50),  # coarse_dirt
        "3.2": (124, 90, 50),  # podzol_top

        "4.0": (131, 131, 131),  # cobblestone
        "5.0": (171, 131, 90),  # oak_planks
        "5.1": (171, 131, 90),  # spruce_planks
        "5.2": (171, 131, 90),  # birch_planks
        "5.3": (171, 131, 90),  # jungle_planks
        "5.4": (171, 131, 90),  # acacia_planks
        "5.5": (171, 131, 90),  # dark_oak_planks
        "6.0": (66, 136, 60), # oak_sapling Sapling -
        "6.1": (66, 136, 60),  # spruce_sapling
        "6.2": (66, 136, 60),  # birch_sapling
        "6.3": (66, 136, 60),  # jungle_sapling
        "6.4": (66, 136, 60),  # acacia_sapling
        "6.5": (66, 136, 60),  # dark_oak_sapling
        "7.0": (131, 131, 131), #bedrock
        "8.0": (111, 162, 225), #Water Flow
        "9.0": (111, 162, 225), #Water Still
        "10.0": (162, 60, 60), #Lava Flow
        "11.0": (162, 60, 60), #Lava Still
        "12.0": (255, 223, 127), #Sand
        "12.1": (255, 223, 127),  # red_sand
        "13.0": (131, 131, 131), #Gravel
        "14.0": (131, 131, 131), #Gold Ore
        "15.0": (131, 131, 131), #Iron Ore
        "16.0": (131, 131, 131), #Coal Ore
        "17.0": (171, 131, 90), #Wood - oak_log
        "17.1": (171, 131, 90),  # spruce_log
        "17.2": (171, 131, 90),  # birch_log
        "17.3": (171, 131, 90),  # jungle_log
        "18.0": (66, 136, 60), #oak_leaves
        "18.1": (66, 136, 60),  # spruce_leaves
        "18.2": (66, 136, 60),  # birch_leaves
        "18.3": (66, 136, 60),  # jungle_leaves
        "19.0": (238, 238, 60), #Sponge
        "19.1": (238, 238, 60),  # wet_sponge
        "20.0": (249, 249, 249), #Glass
        "21.0": (131, 131, 131), #Lapis Lazuli Ore
        "22.0": (60, 85, 187), #Lapis Lazuli Block
        "23.0": (131, 131, 131), #Dispenser
        "24.0": (255, 223, 127) , #Sandstone_side
        "24.1": (255, 223, 127),  # chiseled_sandstone
        "24.2": (255, 223, 127),  # cut_sandstone
        "25.0": (124, 90, 50), #Note Block
        "26.0": (162, 60, 60), #red_Bed
        #"27.0": (0.36518075980392156, 0.29657676479157913, 0.2522421207156652), #27: powered_rail
        #"28.0": (0.29618566176470584, 0.2608780551640972, 0.23964360115024866), #28: detector_rail
        #"29.0": (0.5613839637788614, 0.6208333333333333, 0.34022199244281054), #Sticky Piston
        #"30.0": (0.3769914215686274, 0.3761992435285797, 0.37293737778889124), #cobweb
        "31.0": (66, 136, 60),  # dead_shrub dead bush
        "31.1": (66, 136, 60),  # tall_grass_top
        "31.2": (66, 136, 60),  # fern
        "32.0": (66, 136, 60), #32: dead_bush
        #"33.0": (0.43098958333333337, 0.3976358139968661, 0.3940768572240094), #piston_side
        #"34.0": (0.6007199754901961, 0.46911396864163285, 0.317236832644746), #piston_top #check
        "35.0": (249, 249, 249), #white_Wool
        "35.1": (225, 136, 60), #orange_Wool
        "35.2": (187, 85, 225), #magenta_wool
        "35.3": (111, 162, 225), #light_blue_wool
        "35.4": (238, 238, 60), #yellow_wool
        "35.5": (111, 136, 60), #lime_wool
        "35.6": (187, 85, 225), #magenta_wool
        "35.7": (131, 131, 131), #gray_wool
        "35.8": (131, 131, 131), #light_grey_wool
        "35.9": (85, 136, 162), #cyan_wool
        "35.10": (136, 72, 187), #purple_wool
        "35.11": (60, 85, 187), #blue_wool
        "35.12": (124, 90, 50), #brown_wool
        "35.13": (111, 136, 60), #green_wool
        "35.14": (162, 60, 60), #red_wool
        "35.15": (0, 0, 0), #black_wool
        #36: Moved Block
        "37.0": (66, 136, 60), #dandelion
        "38.0": (66, 136, 60), #Poppy
        "38.1": (66, 136, 60), #blue_orchid
        "38.2": (66, 136, 60), #allium
        "38.3": (66, 136, 60), #azure_bluet
        "38.4": (66, 136, 60), #red_tulip
        "38.5": (66, 136, 60), #orange_tulip
        "38.6": (66, 136, 60), #white_tulip
        "38.7": (66, 136, 60), #pink_tulip
        "38.8": (66, 136, 60), #Oxeye_Daisy
        "39.0": (66, 136, 60), #39: Brown Mushroom
        "40.0": (66, 136, 60), #40: Red Mushroom
        "41.0": (238, 238, 60), # gold_block Block of Gold
        "42.0": (131, 131, 131), #Block of Iron
        "43.0": (131, 131, 131), #Double Stone Slab smooth_stone_slab_side
        "43.1": (131, 131, 131), #Double sandstone Slab
        "43.2": (131, 131, 131), #Double wooden Slab
        "43.3": (131, 131, 131), #Double cobble stone slab
        "43.4": (131, 131, 131), #Double brick Slab
        "43.5": (131, 131, 131), #Double stone brick Slab
        "43.6": (162, 60, 60), #Double nether brick Slab
        "43.7": (249, 249, 249), #Double quartz Slab
        "44.0": (131, 131, 131), #Stone Slab smooth_stone_slab_side
        "44.1": (255, 223, 127), # sandstone Slab
        "44.2": (171, 131, 90), # wooden Slab
        "44.3": (131, 131, 131), #cobble stone slab
        "44.4": (131, 131, 131), #brick Slab
        "44.5": (131, 131, 131), #stone brick Slab
        "44.6": (162, 60, 60), #nether brick Slab
        "44.7": (249, 249, 249), #quartz Slab
        "45.0": (131, 131, 131), #Brick Block
        "46.0": (162, 60, 60), #TNT
        "47.0": (171, 131, 90), #47: #bookshelf
        "48.0": (131, 131, 131), #Moss Stone
        "49.0": (136, 72, 187), #Obsidian
        #"50.0": (0.04253982843137255, 0.0408831454220595, 0.04080317642816165), #Torch
        #"51.0": (0.7926020603553922, 0.4036715809824868, 0.21846337120059087), #Fire
        #"52.0": (0.11564471569303271, 0.17017463235294117, 0.14986624794982084), #52: #spawner
        "53.0": (139, 99, 92), #Wooden Stairs
        "54.0": (171, 131, 90), #Chest
        #"55.0": (0.07352941176470588, 0.07352941176470588, 0.07352941176470588), #55: #redstone_dust_line0 Redstone Wire
        "56.0": (131, 131, 131), #Diamond Ore
        "57.0": (111, 162, 225), #Block of Diamond
        "58.0": (171, 131, 90), #Crafting Table
        "59.0": (66, 136, 60), #59: # wheat_stage7 Wheat Crops
        "60.0": (124, 90, 50), #farmland
        "61.0": (131, 131, 131), #Furnace
        "62.0": (131, 131, 131), #Burning Furnace
        "63.0": (171, 131, 90), #oak_sign  Sign Post
        "64.0": (249, 249, 249), #64: #oak_door_top Wooden Door
        #"65.0": (0.27496936274509803, 0.21683904657015138, 0.1886623430967056), #Ladder
        #"66.0": (0.27904411764705883, 0.2474515301459631, 0.22881361172685988), #66: #Rail
        "67.0": (139, 99, 92), #Cobblestone Stairs
        "68.0": (171, 131, 90), #68: #oak_hanging_sign Wall Sign
        #"69.0": (0.03409926470588235, 0.033062776233878335, 0.03302321560517589), #69: #lever
        #70: #Stone Pressure Plate
        "71.0": (249, 249, 249),#71: #iron_door_top
        #72: #Wooden Pressure Plate
        "73.0": (131, 131, 131), #Redstone Ore
        "74.0": (131, 131, 131), #Glowing Redstone Ore
        #"75.0": (0.031066176470588232, 0.029658444859666264, 0.02960471464550894), #75: #redstone_torch_off Redstone Torch (off)
        #"76.0": (0.06824448529411764, 0.0637842395935043, 0.06359135716844182), #76: #redstone_torch Redstone Torch (on)
        #77: #Stone Button
        "78.0": (249, 249, 249), #Snow
        "79.0": (249, 249, 249), #ice
        "80.0": (249, 249, 249), #snow
        "81.0": (66, 136, 60), #cactus_side Cactus
        "82.0": (131, 131, 131), #Clay
        #"83.0": (0.41659007352941174, 0.39528529110526817, 0.3075095875177966), #83: #sugar_cane
        "84.0": (171, 131, 90), #Jukebox
        "85.0": (171, 131, 90), #Fence bamboo_fence
        "86.0": (225, 136, 60), #Pumpkin
        "87.0": (162, 60, 60), #Netherrack
        "88.0": (255, 223, 127), #88: #soul_sand Soul Sand
        "89.0": (238, 238, 60), #Glowstone
#        "90.0": (0.33203729910651475, 0.0392276067861637, 0.7506792853860295), #nether_portal Nether Portal
        "91.0": (225, 136, 60), #91: #jack_o_lantern Jack o'Lantern
        #"92.0": (0.34852941176470587, 0.3267147076663237, 0.2764103049307958), #92: # cake_side Cake
        #"93.0": (0.5886384288607447, 0.6337316176470589, 0.5901553504688137), #93: #repeater Redstone Repeater (off)
        #"94.0": (0.6222608759438978, 0.6701286764705883, 0.6305233510715748), #94: #repeater_on Redstone Repeater (on)
        "95.0": (249, 249, 249), #white Stained Glass
        "95.1": (249, 249, 249), #orange Stained Glass
        "95.2": (249, 249, 249), #magenta Stained Glass
        "95.3": (249, 249, 249), #light blue Stained Glass
        "95.4": (249, 249, 249), #yellow Stained Glass
        "95.5": (249, 249, 249), #lime Stained Glass
        "95.6": (249, 249, 249), #pink Stained Glass
        "95.7": (249, 249, 249), #grey Stained Glass does not exist
        "95.8": (249, 249, 249), #light gray Stained Glass
        "95.9": (249, 249, 249), #cyan Stained Glass
        "95.10": (249, 249, 249), #purple Stained Glass
        "95.11": (249, 249, 249), #blue Stained Glass
        "95.12": (249, 249, 249), #brown Stained Glass
        "95.13": (249, 249, 249), #green Stained Glass
        "95.14": (249, 249, 249), #red Stained Glass
        "95.15": (249, 249, 249), #black Stained Glass
        "96.0": (171, 131, 90), #96: oak_trapdoor #Trapdoor
        "97.0": (131, 131, 131), #stone Monster Egg
        "97.1": (131, 131, 131), #97.1: #cobblestone Monster Egg
        "97.2": (131, 131, 131), #stone_bricks stone Monster Egg
        "97.3": (131, 131, 131), #mossy_stone_bricks stone Monster Egg
        "97.4": (131, 131, 131), #cracked_stone_bricks
        "97.5": (131, 131, 131), #chiseled_stone_bricks
        "98.0": (131, 131, 131), #Stone Bricks
        "98.1": (131, 131, 131), #mossy_stone_bricks
        "98.2": (131, 131, 131), #cracked_stone_bricks
        "98.3": (131, 131, 131), #chiseled_stone_bricks
        "99.0": (124, 90, 50), #Brown Mushroom Block
        "100.0": (162, 60, 60), #Red Mushroom Block
        "101.0": (139, 99, 92), #Iron Bars
        "102.0": (249, 249, 249), #glass_pane_top Glass Pane
        "103.0": (66, 136, 60), #Melon
        "104.0": (66, 136, 60), #pumpkin_stem Pumpkin Stem
        "105.0": (66, 136, 60), #melon_stem Melon Stem
        "106.0": (66, 136, 60), #twisting_vines Vines
        "107.0": (139, 99, 92), #bamboo fence Fence Gate #all gates bamboo and fences
        "108.0": (139, 99, 92), #Brick Stairs
        "109.0": (139, 99, 92), #Stone Brick Stairs
        "110.0": (66, 136, 60), #Mycelium
        "111.0": (66, 136, 60), #lily_pad Lily Pad
        "112.0": (162, 60, 60), #nether_bricks Nether Brick
        "113.0": (139, 99, 92), #Nether Brick Fence
        "114.0": (139, 99, 92), #Nether Brick Stairs
        "115.0": (66, 136, 60), #nether_wart_stage2 Nether Wart
        "116.0": (131, 131, 131), #enchanting_table_side Enchantment Table
        "117.0": (131, 131, 131), #brewing_stand Brewing Stand
        "118.0": (131, 131, 131), #cauldron_side
        "119.0": (255, 223, 127), #end_portal End Portal
        "120.0": (255, 223, 127), #end_portal_frame_side End Portal Frame
        "121.0": (136, 72, 187), #End Stone
        "122.0": (136, 72, 187), #dragon_egg Dragon Egg
        #"123.0": (0.373391544117647, 0.2055622108012238, 0.12097474200502814), #redstone_lamp Redstone Lamp (inactive)
        #"124.0": (0.5602022058823529, 0.3724902184034301, 0.2197043026194853), #redstone_lamp_on Redstone Lamp (active)
        "125.0": (171, 131, 90), #oak_plank => Double Wooden Slab
        "125.1": (171, 131, 90),  # spruce_planks
        "125.2": (171, 131, 90),  # birch_planks
        "125.3": (171, 131, 90),  # jungle_planks
        "125.4": (171, 131, 90),  # acacia_planks
        "125.5": (171, 131, 90),  # dark_oak_planks
        "126.0": (171, 131, 90), #oak_plank =>Wooden Slab
        "126.1": (171, 131, 90),  # spruce_planks
        "126.2": (171, 131, 90),  # birch_planks
        "126.3": (171, 131, 90),  # jungle_planks
        "126.4": (171, 131, 90),  # acacia_planks
        "126.5": (171, 131, 90),  # dark_oak_planks
        "127.0": (66, 136, 60), #cocoa_stage2 Cocoa
        "128.0": (139, 99, 92), #Sandstone Stairs
        "129.0": (131, 131, 131), #Emerald Ore
        "130.0": (171, 131, 90), #Ender Chest
        #"131.0": (0.10050551470588236, 0.09785473337761623, 0.09776193585775303), #tripwire_hook Tripwire Hook
        #"132.0": (0.08305759803921568, 0.08305759803921568, 0.08305759803921568), #tripwire Tripwire
        "133.0": (111, 136, 60), #133: #emerald_block Block of Emerald
        "134.0": (139, 99, 92), #Spruce Stairs
        "135.0": (139, 99, 92), #Birch Stairs
        "136.0": (139, 99, 92), #Jungle Stairs
        "137.0": (136, 72, 187), #command_block_side Command Block
        "138.0": ( 255, 223, 127), #138: #beacon Beacon
        "139.0": (131, 131, 131), #139: #Cobblestone (Wall)
        "139.1": (131, 131, 131), #mossy cobblestone wall
        "140.0": (66, 136, 60), #flower_pot Flower Pot
        "141.0": (66, 136, 60), #carrots_stage3 Carrots
        "142.0": (66, 136, 60), #potatoes_stage3 Potatoes
        #143: #Wooden Button
        #144: #Mob Head
        "145.0": (131, 131, 131), #anvil
        "146.0": (171, 131, 90), #trapped Trapped Chest
        #147: #Weighted Pressure Plate (light)
        #148: #Weighted Pressure Plate (heavy)
        #"149.0": (0.6190655898167876, 0.6576899509803922, 0.603396275339563), #comparator Redstone Comparator (inactive)
        #"150.0": (0.6413503067430191, 0.6942708333333333, 0.6314269859962213), #comparator_on Redstone Comparator (active)
        #"151.0": (0.5119638480392157, 0.4422616290080757, 0.33894077182228594), #daylight_detector_top Daylight Sensor
        "152.0": (162, 60, 60), #redstone_block Block of Redstone
        "153.0": (162, 60, 60), #nether_quartz_ore Nether Quartz Ore
        "154.0": (131, 131, 131), #hopper_outside Hopper
        "155.0": (249, 249, 249), #155: #quartz_block_side Block of Quartz
        "155.1": (249, 249, 249), #chiseled_quartz_block Chisseled quartz block
        "155.2": (249, 249, 249), #quartz_pillar pillar quartz block
        "156.0": (139, 99, 92), #Quartz Stairs
        #"157.0": (0.27653186274509806, 0.2253635195586252, 0.2027561439710688), #activator_rail Activator Rail
        "158.0": (131, 131, 131), #dropper_front Dropper
        "159.0": (249, 249, 249), #white Stained Clay
        "159.1": (225, 136, 60), #orange Stained Clay
        "159.2": (187, 85, 225), #magenta Stained Clay
        "159.3": (111, 162, 225), #light blue Stained Clay
        "159.4": (238, 238, 60), #yellow Stained Clay
        "159.5": (111, 136, 60), #lime Stained Clay
        "159.6": (255, 182, 193), #pink Stained Clay
        "159.7": (131, 131, 131), #gray Stained Clay
        "159.8": (131, 131, 131), #light gray Stained Clay
        "159.9": (85, 136, 162), #cyan Stained Clay
        "159.10": (136, 72, 187), #purple Stained Clay
        "159.11": (60, 85, 187), #blue Stained Clay
        "159.12": (124, 90, 50), #brown Stained Clay
        "159.13": (111, 136, 60), #green Stained Clay
        "159.14": (162, 60, 60), #red Stained Clay
        "159.15": (0, 0, 0), #black Stained Clay

        "160.0": (249, 249, 249), #white Stained Glass Pane
        "160.1": (249, 249, 249), #orange stained Glass Pane
        "160.2": (249, 249, 249), #magenta stained Glass Pane
        "160.3": (249, 249, 249), #light_blue stained Glass Pane
        "160.4": (249, 249, 249), #yellow stained Glass Pane
        "160.5": (249, 249, 249), #lime stained Glass Pane
        "160.6": (249, 249, 249), #pink stained Glass Pane
        "160.7": (249, 249, 249), #gray stained Glass Pane
        "160.8": (249, 249, 249), #light_gray stained Glass Pane
        "160.9": (249, 249, 249), #cyan stained Glass Pane
        "160.10": (249, 249, 249), #purple stained Glass Pane
        "160.11": (249, 249, 249), #blue stained Glass Pane
        "160.12": (249, 249, 249), #brown stained Glass Pane
        "160.13": (249, 249, 249), #green stained Glass Pane
        "160.14": (249, 249, 249), #red stained Glass Pane
        "160.15": (249, 249, 249), #black stained Glass Pane

        "161.0": (66, 136, 60), #Acacia Leaves
        "161.1": (66, 136, 60), #dark oak Leaves
        "162.0": (171, 131, 90), #Acacia log
        "162.1": (171, 131, 90), #dark oak log
        "163.0": (139, 99, 92), #Acacia Wood Stairs
        "164.0": (139, 99, 92), #Dark Oak Wood Stairs
        "165.0": (111, 136, 60), #slime_block Slime Block
        #166: #Barrier
        "167.0": (171, 131, 90), #iron_trapdoor Iron Trapdoor
        "168.0": (60, 85, 187), #prismarine
        "168.1": (60, 85, 187), #prismarine_bricks Prismarine brick
        "168.2": (60, 85, 187), #dark_prismarine dark Prismarine
        #"169.0": (0.6523253171856979, 0.7838970588235294, 0.7129934342306127), #sea_lantern Sea Lantern
        "170.0": (238, 238, 60), #170: #hay_block_side Hay Bale
        #"171.0": #white Carpet #gonna delete
        #"171.1": #orange Carpet
        #"171.2": #magenta Carpet
        #"171.3": #lightblue Carpet
        #"171.4": #yellow Carpet
        #"171.5": #lime Carpet
        #"171.6": #pink Carpet
        #"171.7": #gray Carpet
        #"171.8": #light gray Carpet
        #"171.9": #cyan Carpet
        #"171.10": #purple Carpet
        #"171.11": #blue Carpet
        #"171.12": #brown Carpet
        #"171.13": #green Carpet
        #"171.14": #red Carpet
        #"171.15": #black Carpet
        "172.0": (131, 131, 131), #Hardened Clay
        "173.0": (0, 0, 0), #coal_block Block of Coal
        "174.0": (249, 249, 249), #packed_ice Packed Ice
        "175.0": (66, 136, 60), #sunflower_front sun flower Double Plant
        "175.1": (66, 136, 60), #lilac_top lilac sun flower Double Plant
        "175.2": (66, 136, 60), #tall_grass_top double tallgrass /sun flower Double Plant
        "175.3": (66, 136, 60), #large_fern_top large fern Double Plant
        "175.4": (66, 136, 60), #rose_bush_top Rose bush sun flower Double Plant
        "175.5": (66, 136, 60), #peony_top Peony //sun flower Double Plant
        #176: #Standing Banner
        #177: #Wall Banner
        #"178.0": (0.33642970007779466, 0.48904718137254904, 0.3817520421792056), #daylight_detector_inverted_top Daylight Sensor (inverted)
        "179.0": (255, 223, 127), #red_sandstone Red Sandstone
        "179.1": (255, 223, 127), #chiseled_red_sandstone Chisseled Red Sandstone
        "179.2": (255, 223, 127), #chiseled_red_sandstone smooth Red Sandstone
        "180.0": (139, 99, 92), #Red Sandstone Stairs
        "181.0": (162, 60, 60), #Double Red Sandstone Slab
        "182.0": (162, 60, 60), #Red Sandstone Slab

        "183.0": (139, 99, 92), #Spruce Fence Gate
        "184.0": (139, 99, 92), #Birch Fence Gate
        "185.0": (139, 99, 92), #Jungle Fence Gate
        "186.0": (139, 99, 92), #Dark Oak Fence Gate
        "187.0": (139, 99, 92), #Acacia Fence Gate
        "188.0": (139, 99, 92), #Spruce Fence
        "189.0": (139, 99, 92), #Birch Fence
        "190.0": (139, 99, 92), #Jungle Fence
        "191.0": (139, 99, 92), #Dark Oak Fence
        "192.0": (139, 99, 92), #Acacia Fence

        "193.0": (249, 249, 249), #spruce_door_top Spruce Door
        "194.0": (249, 249, 249), #birch_door_top Birch Door
        "195.0": (249, 249, 249), #jungle_door_top Jungle Door
        "196.0": (249, 249, 249), #196: #acacia_door_top Acacia Door
        "197.0": (249, 249, 249), #dark_oak_door_top Dark Oak Door
        "198.0": (66, 136, 60), #end_rod End Rod
        "199.0": (66, 136, 60), #chorus_plant horus Plant
        "200.0": (66, 136, 60), #chorus_flower Chorus Flower
        "201.0": (136, 72, 187), #purpur_block Purpur Block
        "202.0": (136, 72, 187), #purpur_pillar Purpur Pillar
        "203.0": (139, 99, 92), #Purpur Stairs
        "204.0": (136, 72, 187), #Purpur Double Slab
        "205.0": (136, 72, 187), #Purpur Slab
        "206.0": (136, 72, 187), #end_stone_bricks End Stone Bricks
        "207.0": (66, 136, 60), #beetroots_stage3 Beetroot
        "208.0": (124, 90, 50), #dirt_path_top Grass Path
        #"209.0": (0.01120904660692402, 0.01120904660692402, 0.01120904660692402), #end_portal End Gateway
        #"210.0": (0.4947991097424083, 0.43763436375742276, 0.6816329656862744), #repeating_command_block_side Repeating Command Block
        #"211.0": (0.49842375007696865, 0.649624693627451, 0.6333233419009147), #chain_command_block_side Chain Command Block
        "212.0": (249, 249, 249), #frosted_ice_3 Frosted Ice
        "213.0": (162, 60, 60), #magma Magma Block
        "214.0": (162, 60, 60), #nether_wart_block Nether Wart Block
        "215.0": (162, 60, 60), #red_nether_bricks Red Nether Brick
        "216.0": (249, 249, 249), #bone_block_side Bone Block
        #217: #Structure Void
        "218.0": (131, 131, 131), #observer_side Observer
        "219.0": (249, 249, 249), #white_shulker_box White Shulker Box
        "220.0": (225, 136, 60), #Orange Shulker Box
        "221.0": (187, 85, 225), #Magenta Shulker Box
        "222.0": (111, 162, 225), #Light Blue Shulker Box
        "223.0": (238, 238, 60), #Yellow Shulker Box
        "224.0": (111, 136, 60), #Lime Shulker Box
        "225.0": (255, 182, 193), #Pink Shulker Box
        "226.0": (131, 131, 131), #Gray Shulker Box
        "227.0": (131, 131, 131), #Light Gray Shulker Box
        "228.0": (85, 136, 162), #Cyan Shulker Box
        "229.0": (136, 72, 187), #Purple Shulker Box
        "230.0": (60, 85, 187), #Blue Shulker Box
        "231.0": (171, 131, 90), #Brown Shulker Box
        "232.0": (111, 136, 60), #Green Shulker Box
        "233.0": (162, 60, 60), #Red Shulker Box
        "234.0": (0, 0, 0), #Black Shulker Box

        "235.0": (249, 249, 249), #white_glazed_terracotta White Glazed Terracotta
        "236.0": (225, 136, 60), #Orange Glazed Terracotta
        "237.0": (187, 85, 225), #Magenta Glazed Terracotta
        "238.0": (111, 162, 225), #Light Blue Glazed Terracotta
        "239.0": (238, 238, 60), #Yellow Glazed Terracotta
        "240.0": (111, 136, 60), #Lime Glazed Terracotta
        "241.0": (255, 182, 193), #Pink Glazed Terracotta
        "242.0": (131, 131, 131), #Gray Glazed Terracotta
        "243.0": (131, 131, 131), #Light Gray Glazed Terracotta
        "244.0": (85, 136, 162), #Cyan Glazed Terracotta
        "245.0": (136, 72, 187), #Purple Glazed Terracotta
        "246.0": (60, 85, 187), #Blue Glazed Terracotta
        "247.0": (124, 90, 50), #Brown Glazed Terracotta
        "248.0": (111, 136, 60), #Green Glazed Terracotta
        "249.0": (162, 60, 60), #Red Glazed Terracotta
        "250.0": (0, 0, 0), #Black Glazed Terracotta

        "251.0": (249, 249, 249), #white_concrete white Concrete
        "251.1": (225, 136, 60), #orange Concrete
        "251.2": (187, 85, 225), #magenta Concrete
        "251.3": (111, 162, 225), #light blue Concrete
        "251.4": (238, 238, 60), #yellow Concrete
        "251.5": (111, 136, 60), #lime Concrete
        "251.6": (255, 182, 193), #pink Concrete
        "251.7": (131, 131, 131), #gray Concrete
        "251.8": (131, 131, 131), #light gray Concrete
        "251.9": (85, 136, 162), #cyan Concrete
        "251.10": (136, 72, 187), #purple Concrete
        "251.11": (60, 85, 187), #blue Concrete
        "251.12": (124, 90, 50), #brown Concrete
        "251.13": (111, 136, 60), #green Concrete
        "251.14": (162, 60, 60), #red Concrete
        "251.15": (0, 0, 0), #black Concrete

        "252.0": (249, 249, 249), #white_concrete_powder Concrete Powder
        "252.1": (225, 136, 60), #orange Concrete
        "252.2": (187, 85, 225), #magenta Concrete
        "252.3": (111, 162, 225), #light blue Concrete
        "252.4": (238, 238, 60), #yellow Concrete
        "252.5": (111, 136, 60), #lime Concrete
        "252.6": (255, 182, 193), #pink Concrete
        "252.7": (131, 131, 131), #gray Concrete
        "252.8": (131, 131, 131), #light gray Concrete
        "252.9": (85, 136, 162), #cyan Concrete
        "252.10": (136, 72, 187), #purple Concrete
        "252.11": (60, 85, 187), #blue Concrete
        "252.12": (124, 90, 50), #brown Concrete
        "252.13": (111, 136, 60), #green Concrete
        "252.14": (162, 60, 60), #red Concrete
        "252.15": (0, 0, 0), #black Concrete
        "255.0": (136, 72, 187) #structure_block Structure Block
    }



    vertices = []
    faces = []
    vertex_index = 0
    materials = {}

    # Iterate through each block in the schematic
    for y in range(height):
        for z in range(length):
            for x in range(width):
                #print(blocks[y * length * width + z * width + x])
                block_id = int(blocks[y * length * width + z * width + x])
                block_val = int(data[y * length * width + z * width + x] & 0x0F)
                if block_id != 0 and block_id < 256:  # Assuming 0 is air
                    if f"{block_id}.{block_val}" not in block_colors:
                        block_val = 0
                    if f"{block_id}.{block_val}" not in block_colors:
                        continue

                    # Check if there is a block above and below, uncomment to produce interior images
#                    has_block_above = (y < height - 1 and int(blocks[(y + 1) * length * width + z * width + x]) != 0)
#                    has_block_below = (y > 0 and int(blocks[(y - 1) * length * width + z * width + x]) != 0)

#                    if has_block_above and has_block_below:
#                        continue  # Skip this block

                    # Create vertices for the block
                    v0 = (x, y, z)
                    v1 = (x + 1, y, z)
                    v2 = (x + 1, y + 1, z)
                    v3 = (x, y + 1, z)
                    v4 = (x, y, z + 1)
                    v5 = (x + 1, y, z + 1)
                    v6 = (x + 1, y + 1, z + 1)
                    v7 = (x, y + 1, z + 1)

                    vertices.extend([v0, v1, v2, v3, v4, v5, v6, v7])


# Create faces for the block (two triangles per face)
                    faces.extend([
                        (vertex_index, vertex_index + 1, vertex_index + 2, block_id, block_val),
                        (vertex_index, vertex_index + 2, vertex_index + 3, block_id, block_val),
                        (vertex_index + 4, vertex_index + 5, vertex_index + 6, block_id, block_val),
                        (vertex_index + 4, vertex_index + 6, vertex_index + 7, block_id, block_val),
                        (vertex_index, vertex_index + 1, vertex_index + 5, block_id, block_val),
                        (vertex_index, vertex_index + 5, vertex_index + 4, block_id, block_val),
                        (vertex_index + 2, vertex_index + 3, vertex_index + 7, block_id, block_val),
                        (vertex_index + 2, vertex_index + 7, vertex_index + 6, block_id, block_val),
                        (vertex_index + 1, vertex_index + 2, vertex_index + 6, block_id, block_val),
                        (vertex_index + 1, vertex_index + 6, vertex_index + 5, block_id, block_val),
                        (vertex_index, vertex_index + 3, vertex_index + 7, block_id, block_val),
                        (vertex_index, vertex_index + 7, vertex_index + 4, block_id, block_val)
                    ])

                    # Assign a material (color) to the block
                    material_name = f"material_{block_id}.{block_val}"


                    if material_name not in materials:
                        color = block_colors.get(f"{block_id}.{block_val}", (255.0, 255.0, 255.0))  # Default to white if not found
                        materials[material_name] = tuple(c / 255.0 for c in color)
                    vertex_index += 8
    return vertices, faces, materials


def convert_schematic_to_obj(schematic_path, obj_path):
    # Load the .schematic file
    schematic = nbtlib.load(schematic_path)

    # Extract the necessary data from the schematic
    vertices, faces, materials = schematic_to_mesh(schematic)
    #print(materials)
    mtl_path = obj_path.replace('.obj', '.mtl')
    with open(mtl_path, 'w') as mtl_file:
        for material_name, color in materials.items():
            mtl_file.write(f"newmtl {material_name}\n")
            mtl_file.write(f"Kd {color[0]} {color[1]} {color[2]}\n")

    with open(obj_path, 'w') as obj_file:
        obj_file.write(f"mtllib {mtl_path}\n")
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            material_name = f"material_{face[3]}.{face[4]}"
            obj_file.write(f"usemtl {material_name}\n")
            obj_file.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")


def convert_obj_to_glb(obj_path, glb_path):
    # Load the .obj file using trimesh
    mesh = trimesh.load(obj_path)
    
    # Export the mesh to .glb
    mesh.export(glb_path)

def create_image(glb_path, img_count):
    # Load the GLB file
   
    mesh = trimesh.load(glb_path, force='mesh')
    mesh.rezero()
    mesh.fix_normals()
    mesh.fill_holes()
    #print("test")
    # Render the mesh
    angle = np.radians(-135)
    rotation_matrix = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])

    # Apply the rotation to the mesh
    mesh.apply_transform(rotation_matrix)
    scene = mesh.scene()
    for i in range (1, 6):
        print(i)
        image = scene.save_image(resolution=[512, 512], cull=False, double_sided=True)
        img_path = f"img2/image_{img_count}.png"
        img_count = img_count + 1
        # Save the image
        with open(img_path, 'wb') as f:
            f.write(image)

        # Define a rotation matrix (e.g., 90 degrees around the Z-axis)
        angle = np.radians(45)
        rotation_matrix = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])

        # Apply the rotation to the mesh
        mesh.apply_transform(rotation_matrix)
        scene = mesh.scene()

def get_name(number):
    file_path = 'TrainingData/08RFHbg.txt'
    with open(file_path, 'r') as file:
        for line in file:
            num, text = line.strip().split(' - ', 1)
            if int(num) == number:
                return text
    return None

# Run the code with
file_name = 'images/metadata.csv'
img_count = 1
start = 1
with open(file_name, 'a') as file:
    file.write("file_name,text\n")
    for i in range (start, 20000):
        schematic_path = f"./schem/{i}.schematic"
        obj_path = f"./obj/{i}.obj"
        glb_path = 'file.glb'
        if os.path.isfile(schematic_path):
            #print(i)
            convert_schematic_to_obj(schematic_path, obj_path)
            convert_obj_to_glb(obj_path, glb_path)
            create_image(obj_path, img_count)
            name = get_name(i)
            for i in range (1, 6):
                file.write(f"image_{img_count},{name}\n")
                img_count = img_count + 1











import nbtlib
import trimesh
import open3d as o3d
import pyrender
import numpy as np
from PIL import Image
import pythreejs as p3js
from IPython.display import display
import matplotlib.pyplot as plt
import os
import time


def schematic_to_mesh(schematic):
    blocks = schematic['Blocks']
    data = schematic['Data']
    #for i in data:
    #    print(i)
    #    data_val = i & 0x0F
        #print(bytes(i).dec())
        #print(bytes(i).hex())
        #print(f"{data_val} : {i} : {bytes(i).hex()}")
    #    print(i)
    #print("################")
    for j in blocks:
        data_val = int(j) 
        #print(f"{int(j)}")
    width = schematic['Width']
    height = schematic['Height']
    length = schematic['Length']

# Example block ID to color mapping (you can expand this as needed)

    block_colors = {
        "1.0": (0.49234068627450983, 0.49234068627450983, 0.49234068627450983),  # stone
        "1.1": (0.585998774509804, 0.40109866088331264, 0.3360965091363598),  # granite
        "1.2": (0.6043198529411764, 0.41552925400061347, 0.34893731949926104),  # polished granite
        "1.3": (0.7418396915953683, 0.7429074754901961, 0.7387877986193712),  # diorite
        "1.4": (0.7535733007587225, 0.7585939733561025, 0.7654871323529412),  # polished diorite
        "1.5": (0.5362357947265886, 0.539813112745098, 0.531882953812461),  # andesite
        "1.6": (0.5162288866699407, 0.5327971813725491, 0.524867851361843),  # polished andesite

        "2.0": (0.5781709558823529, 0.5781709558823529, 0.5781709558823529),  # Grass_block_top ?
        "3.0": (0.5264705882352941, 0.37242120362984554, 0.2631465812427913),  # dirt
        "3.1": (0.46841299019607846, 0.3308671345813311, 0.23341002080404774),  # coarse_dirt
        "3.2": (0.35983455882352944, 0.24668416660525472, 0.09734494958369377),  # podzol_top

        "4.0": (0.5005208129636074, 0.5011335784313725, 0.4998055130351006),  # cobblestone
        "5.0": (0.6360906862745098, 0.5084735137190094, 0.3058945299359021),  # oak_planks
        "5.1": (0.4506587009803921, 0.331132643866863, 0.18973504500222269),  # spruce_planks
        "5.2": (0.754779411764706, 0.6850560973959593, 0.4770094885380623),  # birch_planks
        "5.3": (0.6291819852941176, 0.4457357636762366, 0.3136753632260579),  # jungle_planks
        "5.4": (0.6593443627450981, 0.3483041499603943, 0.19734879754406362),  # acacia_planks
        "5.5": (0.2614123774509804, 0.16720706029266882, 0.0794248329406058),  # dark_oak_planks
        "6.0": (0.20306372549019605, 0.17605023316487037, 0.14444649443723565), # oak_sapling Sapling -
        "6.1": (0.08164828431372548, 0.07603365735336708, 0.06959240483302695),  # spruce_sapling
        "6.2": (0.24220281862745097, 0.21860741979396386, 0.19278646842372826),  # birch_sapling
        "6.3": (0.10684742647058824, 0.09168507549104199, 0.0780323384954855),  # jungle_sapling
        "6.4": (0.22374387254901962, 0.1774209223644007, 0.14388431019619857),  # acacia_sapling
        "6.5": (0.17247242647058822, 0.149778364070098, 0.11993808627541087),  # dark_oak_sapling
        "7.0": (0.3337928921568627, 0.3337928921568627, 0.3337928921568627), #bedrock
        "8.0": (0.6617837344898896, 0.6617837344898896, 0.6617837344898896), #Water Flow
        "9.0": (0.6944565716911765, 0.6944565716911765, 0.6944565716911765), #Water Still
        "10.0": (0.8136393229166667, 0.3524802056832637, 0.07760452725528898), #Lava Flow
        "11.0": (0.8328592218137255, 0.34609656433700065, 0.07126445156626855), #Lava Still
        "12.0": (0.8594362745098039, 0.8128684438102445, 0.6400088175971981), #Sand
        "12.1": (0.7477481617647059, 0.39334100834713015, 0.13197846690951198),  # red_sand
        "13.0": (0.5173866421568627, 0.49803027385885335, 0.49611418891622205), #Gravel
        "14.0": (0.5691789215686274, 0.4808782478819267, 0.4637221345531165), #Gold Ore
        "15.0": (0.5346660539215686, 0.49604056464137297, 0.4908722519865406), #Iron Ore
        "16.0": (0.41501225490196075, 0.41238149334564406, 0.4121514167477653), #Coal Ore
        "17.0": (0.42781862745098037, 0.3316345423912315, 0.19972733594050368), #Wood - oak_log
        "17.1": (0.23071384803921569, 0.14587857603302648, 0.06518160997835867),  # spruce_log
        "17.2": (0.8473725077271081, 0.8498008578431373, 0.8149913067727858),  # birch_log
        "17.3": (0.33417585784313725, 0.2657216323833387, 0.09893202556183321),  # jungle_log
        "18.0": (0.3789505522308878, 0.3829810049019608, 0.37959883276162104), #oak_leaves
        "17.1": (0.3090686274509804, 0.3090686274509804, 0.3090686274509804),  # spruce_leaves
        "17.2": (0.2875785694036905, 0.28877144607843136, 0.2866392794575704),  # birch_leaves
        "17.3": (0.4275172675157965, 0.42967218137254903, 0.4082412282085015),  # jungle_leaves
        "19.0": (0.7703584558823529, 0.7468088521766519, 0.2949972530659782), #Sponge
        "19.1": (0.6734138345967495, 0.7112285539215687, 0.2781505052331135),  # wet_sponge
        "20.0": (0.5930759803921568, 0.5862271977793068, 0.5623228830633049), #Glass
        "21.0": (0.5540441176470589, 0.5396120505772612, 0.45221474688220875), #Lapis Lazuli Ore
        "22.0": (0.12140388462370241, 0.2700392401392628, 0.5494485294117647), #Lapis Lazuli Block
        "23.0": (0.38650428921568625, 0.3836209009061268, 0.3836209009061268), #Dispenser
        "24.0": (0.8487591911764706, 0.7983455913786213, 0.6092395554556841) , #Sandstone_side
        "24.1": (0.8479319852941177, 0.7976740466763025, 0.6070481209056463),  # chiseled_sandstone
        "24.2": (0.8541513480392156, 0.8104793477795066, 0.6253832388309183),  # cut_sandstone
        "25.0": (0.3480698529411764, 0.25575221828644706, 0.17411490575665006), #Note Block
        "26.0": (0.5003255208333334, 0.42302404002792443, 0.3763377404680439), #red_Bed
        "27.0": (0.36518075980392156, 0.29657676479157913, 0.2522421207156652), #27: powered_rail
        "28.0": (0.29618566176470584, 0.2608780551640972, 0.23964360115024866), #28: detector_rail
        "29.0": (0.5613839637788614, 0.6208333333333333, 0.34022199244281054), #Sticky Piston
        "30.0": (0.3769914215686274, 0.3761992435285797, 0.37293737778889124), #cobweb
        "31.0": (0.12841605392156863, 0.10880225361254359, 0.1047786871335544),  # dead_shrub dead bush
        "31.1": (0.20823467494561623, 0.2088235294117647, 0.2078638624567474),  # tall_grass_top
        "31.2": (0.7021438576413411, 0.7025428921568627, 0.6987008607153798),  # fern
        "32.0": (0.12841605392156863, 0.10880225361254359, 0.1047786871335544), #32: dead_bush
        "33.0": (0.43098958333333337, 0.3976358139968661, 0.3940768572240094), #piston_side
        "34.0": (0.6007199754901961, 0.46911396864163285, 0.317236832644746), #piston_top #check
        "35.0": (0.9166607166189085, 0.9285232843137254, 0.9236168914252443), #white_Wool
        "35.1": (0.943734681372549, 0.4529666568526533, 0.07636039502159628), #orange_Wool
        "35.2": (0.7433057598039216, 0.2689359488481744, 0.7072048219848628), #magenta_wool
        "35.3": (0.22787256530503588, 0.6940681826052743, 0.8522212009803921), #light_blue_wool
        "35.4": (0.9756127450980392, 0.7683634227227547, 0.157147181597823), #yellow_wool
        "35.5": (0.4463146352434717, 0.7262561274509803, 0.10225214564034862), #lime_wool
        "35.6": (0.9329963235294118, 0.5541952426650807, 0.6791160402883544), #magenta_wool
        "35.7": (0.24667419363195645, 0.2678445331737317, 0.2806066176470588), #gray_wool
        "35.8": (0.5573422759424668, 0.5575061274509804, 0.5282814649488778), #light_grey_wool
        "35.9": (0.08429594292910181, 0.544693841180401, 0.5700061274509803), #cyan_wool
        "35.10": (0.4708561090642379, 0.16520806582053782, 0.6765012254901961), #purple_wool
        "35.11": (0.20876721749897872, 0.2289466313395487, 0.6176164215686274), #blue_wool
        "35.12": (0.4479779411764706, 0.2765634343818713, 0.1593245076638192), #brown_wool
        "35.13": (0.3367939073949682, 0.42954963235294114, 0.11129599389732911), #green_wool
        "35.14": (0.63125, 0.14911735490669156, 0.13684819240196086), #red_wool
        "35.15": (0.07824703042024102, 0.08109471974488361, 0.10052083333333334), #black_wool
        #36: Moved Block
        "37.0": (0.09401041666666667, 0.08615668841115973, 0.08469722174351511), #dandelion
        "38.0": (0.09606311274509803, 0.08765016768317664, 0.08386686460736255), #Poppy
        "38.1": (0.13962928921568626, 0.1293364145966218, 0.11996183648378927), #blue_orchid
        "38.2": (0.2034313725490196, 0.19987787575703084, 0.17608904928392927), #allium
        "38.3": (0.21043198529411763, 0.1974926416633394, 0.18543996351125466), #azure_bluet
        "38.4": (0.1287377450980392, 0.11507091106376231, 0.10803676301632785), #red_tulip
        "38.5": (0.16266850490196078, 0.14681942177211385, 0.13489176127233216), #orange_tulip
        "38.6": (0.1274203431372549, 0.11761697159561454, 0.1121896302466299), #white_tulip
        "38.7": (0.1391390931372549, 0.1296975689088322, 0.12102202371834149), #pink_tulip
        "38.8": (0.253875612745098, 0.2327902292146809, 0.20975850258914838), #Oxeye_Daisy
        "39.0": (0.07994791666666667, 0.07596847135623755, 0.07575334536483865), #39: Brown Mushroom
        "40.0": (0.10795036764705883, 0.10013978055468312, 0.09852290064405818), #40: Red Mushroom
        "41.0": (0.96640625, 0.8107703941437613, 0.24090577368642768), # gold_block Block of Gold
        "42.0": (0.8632046568627451, 0.8628344097672769, 0.8628344097672769), #Block of Iron
        "43.0": (0.49234068627450983, 0.49234068627450983, 0.49234068627450983), #Double Stone Slab smooth_stone_slab_side
        "43.1": (0.8487591911764706, 0.7983455913786213, 0.6092395554556841), #Double sandstone Slab
        "43.2": (0.6360906862745098, 0.5084735137190094, 0.3058945299359021), #Double wooden Slab
        "43.3": (0.5005208129636074, 0.5011335784313725, 0.4998055130351006), #Double cobble stone slab
        "43.4": (0.5919730392156862, 0.3811820809672116, 0.3254219437085496), #Double brick Slab
        "43.5": (0.47666889640928367, 0.48196997549019605, 0.4815850625789901), #Double stone brick Slab
        "43.6": (0.17369791666666667, 0.08685960158803104, 0.1045545045778596), #Double nether brick Slab
        "43.7": (0.9204350490196078, 0.8972383806932316, 0.8707050487455245), #Double quartz Slab
        "44.0": (0.6570465686274509, 0.6570465686274509, 0.6570465686274509), #Stone Slab smooth_stone_slab_side
        "44.1": (0.8487591911764706, 0.7983455913786213, 0.6092395554556841), # sandstone Slab
        "44.2": (0.6360906862745098, 0.5084735137190094, 0.3058945299359021), # wooden Slab
        "44.3": (0.5005208129636074, 0.5011335784313725, 0.4998055130351006), #cobble stone slab
        "44.4": (0.5919730392156862, 0.3811820809672116, 0.3254219437085496), #brick Slab
        "44.5": (0.47666889640928367, 0.48196997549019605, 0.4815850625789901), #stone brick Slab
        "44.6": (0.17369791666666667, 0.08685960158803104, 0.1045545045778596), #nether brick Slab
        "44.7": (0.9204350490196078, 0.8972383806932316, 0.8707050487455245), #quartz Slab
        "45.0": (0.5919730392156862, 0.3811820809672116, 0.3254219437085496), #Brick Block
        "46.0": (0.3805023632939458, 0.5680300245098039, 0.2550044102065611), #TNT
        "47.0": (0.5267156862745098, 0.5125026781095224, 0.18154263083910038), #47: #bookshelf
        "48.0": (0.4083152424285431, 0.478079044117647, 0.4438062941150495), #Moss Stone
        "49.0": (0.04355121839822123, 0.027731421799533234, 0.09627757352941176), #Obsidian
        "50.0": (0.04253982843137255, 0.0408831454220595, 0.04080317642816165), #Torch
        "51.0": (0.7926020603553922, 0.4036715809824868, 0.21846337120059087), #Fire
        "52.0": (0.11564471569303271, 0.17017463235294117, 0.14986624794982084), #52: #spawner
        "53.0": (0.43921569, 0.50196078, 0.56470588), #Wooden Stairs
        "54.0": (0.16613625919117647, 0.13705952811431066, 0.1287177443036846), #Chest
        "55.0": (0.07352941176470588, 0.07352941176470588, 0.07352941176470588), #55: #redstone_dust_line0 Redstone Wire
        "56.0": (0.5563878676470588, 0.5367199781684299, 0.49795350458657733), #Diamond Ore
        "57.0": (0.3750866459865196, 0.9338541666666668, 0.8588211383841583), #Block of Diamond
        "58.0": (0.4697303921568627, 0.2908948610652902, 0.1688597290555315), #Crafting Table
        "59.0": (0.3575520833333334, 0.2971361560267882, 0.2463483463860805), #59: # wheat_stage7 Wheat Crops
        "60.0": (0.5614736519607844, 0.3982292832497231, 0.2786553826014935), #farmland
        "61.0": (0.43282781862745096, 0.42962537015323127, 0.42962537015323127), #Furnace
        "62.0": (0.43282781862745096, 0.42962537015323127, 0.42962537015323127), #Burning Furnace
        "63.0": (0.29165134803921566, 0.23621127355492608, 0.21100045749381244), #oak_sign  Sign Post
        "64.0": (0.4498774509803921, 0.3601511285974549, 0.253572929056733), #64: #oak_door_top Wooden Door
        "65.0": (0.27496936274509803, 0.21683904657015138, 0.1886623430967056), #Ladder
        "66.0": (0.27904411764705883, 0.2474515301459631, 0.22881361172685988), #66: #Rail
        "67.0": (0.43921569, 0.50196078, 0.56470588), #Cobblestone Stairs
        "68.0": (0.3152726715686274, 0.2575753184816613, 0.2334601860237048), #68: #oak_hanging_sign Wall Sign
        "69.0": (0.03409926470588235, 0.033062776233878335, 0.03302321560517589), #69: #lever
        #70: #Stone Pressure Plate
        "71.0": (0.6185508578431372, 0.6166084110622266, 0.6166084110622266),#71: #iron_door_top
        #72: #Wooden Pressure Plate
        "73.0": (0.55078125, 0.4657510196461397, 0.4657510196461397), #Redstone Ore
        "74.0": (0.55078125, 0.4657510196461397, 0.4657510196461397), #Glowing Redstone Ore
        "75.0": (0.031066176470588232, 0.029658444859666264, 0.02960471464550894), #75: #redstone_torch_off Redstone Torch (off)
        "76.0": (0.06824448529411764, 0.0637842395935043, 0.06359135716844182), #76: #redstone_torch Redstone Torch (on)
        #77: #Stone Button
        "78.0": (0.9845256434054392, 0.9969515931372548, 0.9766093823214027), #Snow
        "79.0": (0.573156404828897, 0.7281755428664256, 0.9959712009803922), #ice
        "80.0": (0.9845256434054392, 0.9969515931372548, 0.9766093823214027), #snow
        "81.0": (0.3723279429481734, 0.4543658088235294, 0.18632617497251655), #cactus_side Cactus
        "82.0": (0.6318919002381896, 0.6548226016370489, 0.7037071078431373), #Clay
        "83.0": (0.41659007352941174, 0.39528529110526817, 0.3075095875177966), #83: #sugar_cane
        "84.0": (0.3677696078431372, 0.2726286312411867, 0.20807602169237793), #Jukebox
        "85.0": (0.5418198529411764, 0.44791377360481555, 0.3361640270193555), #Fence bamboo_fence
        "86.0": (0.7768688725490196, 0.45260291956127624, 0.09433577746164337), #Pumpkin
        "87.0": (0.38267463235294114, 0.14766504272320138, 0.14766504272320138), #Netherrack
        "88.0": (0.31916360294117646, 0.24185063896610126, 0.19828918879419877), #88: #soul_sand Soul Sand
        "89.0": (0.6735906862745098, 0.48784542635554395, 0.2990709627907535), #Glowstone
        "90.0": (0.33203729910651475, 0.0392276067861637, 0.7506792853860295), #nether_portal Nether Portal
        "91.0": (0.8417892156862744, 0.5895639056798375, 0.19073076423430887), #91: #jack_o_lantern Jack o'Lantern
        "92.0": (0.34852941176470587, 0.3267147076663237, 0.2764103049307958), #92: # cake_side Cake
        "93.0": (0.5886384288607447, 0.6337316176470589, 0.5901553504688137), #93: #repeater Redstone Repeater (off)
        "94.0": (0.6222608759438978, 0.6701286764705883, 0.6305233510715748), #94: #repeater_on Redstone Repeater (on)
        "95.0": (1.0, 1.0, 1.0), #white Stained Glass
        "95.1": (0.8470588235294118, 0.4907274577651129, 0.20262975778546716), #orange Stained Glass
        "95.2": (0.6858538571137803, 0.29896193771626306, 0.8470588235294118), #magenta Stained Glass
        "95.3": (0.40193771626297575, 0.6114064726236516, 0.8470588235294118), #light blue Stained Glass
        "95.4": (0.8980392156862744, 0.8898356740620124, 0.20073817762399085), #yellow Stained Glass
        "95.5": (0.5119261822376009, 0.8, 0.10039215686274511), #lime Stained Glass
        "95.6": (0.9490196078431373, 0.4987004998077662, 0.6576366555849559), #pink Stained Glass
        "95.7": (0.6, 0.6, 0.6), #grey Stained Glass does not exist
        "95.8": (0.6, 0.6, 0.6), #light gray Stained Glass
        "95.9": (0.2988235294117647, 0.5043321799307958, 0.6), #cyan Stained Glass
        "95.10": (0.4920572630436261, 0.24910419069588624, 0.6980392156862745), #purple Stained Glass
        "95.11": (0.20256824298346787, 0.3074915077911206, 0.6980392156862745), #blue Stained Glass
        "95.12": (0.4, 0.29453287197231837, 0.20078431372549022), #brown Stained Glass
        "95.13": (0.4037391953321121, 0.4980392156862745, 0.2011687812379854), #green Stained Glass
        "95.14": (0.6, 0.19999999999999996, 0.19999999999999996), #red Stained Glass
        "95.15": (0.09803921568627452, 0.09803921568627452, 0.09803921568627452), #black Stained Glass
        "96.0": (0.4209405637254902, 0.3293117416240005, 0.22223185643742793), #96: oak_trapdoor #Trapdoor
        "97.0": (0.49234068627450983, 0.49234068627450983, 0.49234068627450983), #stone Monster Egg
        "97.1": (0.5005208129636074, 0.5011335784313725, 0.4998055130351006), #97.1: #cobblestone Monster Egg
        "97.2": (0.47666889640928367, 0.48196997549019605, 0.4815850625789901), #stone_bricks stone Monster Egg
        "97.3": (0.4083152424285431, 0.478079044117647, 0.4438062941150495), #mossy_stone_bricks stone Monster Egg
        "97.4": (0.4610083648435247, 0.4651194852941176, 0.46365036430956746), #cracked_stone_bricks
        "97.5": (0.4659202294677828, 0.4687769524977839, 0.47110906862745094), #chiseled_stone_bricks
        "98.0": (0.47666889640928367, 0.48196997549019605, 0.4815850625789901), #Stone Bricks
        "98.1": (0.4083152424285431, 0.478079044117647, 0.4438062941150495), #mossy_stone_bricks
        "98.2": (0.4610083648435247, 0.4651194852941176, 0.46365036430956746), #cracked_stone_bricks
        "98.3": (0.4659202294677828, 0.4687769524977839, 0.47110906862745094), #chiseled_stone_bricks
        "99.0": (0.5856311274509803, 0.4371859078718191, 0.320428501995927), #Brown Mushroom Block
        "100.0": (0.7850643382352941, 0.17352471409921968, 0.17352471409921968), #Red Mushroom Block
        "101.0": (0.24736519607843135, 0.24523823398733555, 0.24408366636329773), #Iron Bars
        "102.0": (0.10664828431372549, 0.10486005177553832, 0.10371905064683655), #glass_pane_top Glass Pane
        "103.0": (0.4238303003285923, 0.5673713235294118, 0.12243504648527612), #Melon
        "104.0": (0.08307291666666666, 0.08302318331151226, 0.08297874700010212), #pumpkin_stem Pumpkin Stem
        "105.0": (0.08244485294117647, 0.08244485294117647, 0.08244485294117647), #melon_stem Melon Stem
        "106.0": (0.157827818627451, 0.15017540722383768, 0.12057581143670704), #twisting_vines Vines
        "107.0": (0.6067555147058823, 0.5046056151831682, 0.3432053826671983), #bamboo fence Fence Gate #all gates bamboo and fences
        "108.0": (0.43921569, 0.50196078, 0.56470588), #Brick Stairs
        "109.0": (0.43921569, 0.50196078, 0.56470588), #Stone Brick Stairs
        "110.0": (0.43599877450980395, 0.38601386598603904, 0.4300952260306644), #Mycelium
        "111.0": (0.3067708333333333, 0.3067708333333333, 0.3067708333333333), #lily_pad Lily Pad
        "112.0": (0.17369791666666667, 0.08685960158803104, 0.1045545045778596), #nether_bricks Nether Brick
        "113.0": (0.5418198529411764, 0.44791377360481555, 0.3361640270193555), #Nether Brick Fence
        "114.0": (0.43921569, 0.50196078, 0.56470588), #Nether Brick Stairs
        "115.0": (0.12384806737492793, 0.2724724264705882, 0.1258014941534831), #nether_wart_stage2 Nether Wart
        "116.0": (0.10246184141165658, 0.21217830882352942, 0.20307224539770946), #enchanting_table_side Enchantment Table
        "117.0": (0.25150122549019605, 0.22620865319980127, 0.21882301785220826), #brewing_stand Brewing Stand
        "118.0": (0.293168363106807, 0.2953890931372549, 0.2869410012731732), #cauldron_side
        "119.0": (0.01120904660692402, 0.01120904660692402, 0.01120904660692402), #end_portal End Portal
        "120.0": (0.4712411331972878, 0.534329044117647, 0.36476469856095006), #end_portal_frame_side End Portal Frame
        "121.0": (0.8716322423405785, 0.8806985294117646, 0.6211164153735943), #End Stone
        "122.0": (0.043245095411019806, 0.05991330060582068, 0.06161151960784314), #dragon_egg Dragon Egg
        "123.0": (0.373391544117647, 0.2055622108012238, 0.12097474200502814), #redstone_lamp Redstone Lamp (inactive)
        "124.0": (0.5602022058823529, 0.3724902184034301, 0.2197043026194853), #redstone_lamp_on Redstone Lamp (active)
        "125.0": (0.6360906862745098, 0.5084735137190094, 0.3058945299359021), #oak_plank => Double Wooden Slab
        "125.1": (0.4506587009803921, 0.331132643866863, 0.18973504500222269),  # spruce_planks
        "125.2": (0.754779411764706, 0.6850560973959593, 0.4770094885380623),  # birch_planks
        "125.3": (0.6291819852941176, 0.4457357636762366, 0.3136753632260579),  # jungle_planks
        "125.4": (0.6593443627450981, 0.3483041499603943, 0.19734879754406362),  # acacia_planks
        "125.5": (0.2614123774509804, 0.16720706029266882, 0.0794248329406058),  # dark_oak_planks
        "126.0": (0.6360906862745098, 0.5084735137190094, 0.3058945299359021), #oak_plank =>Wooden Slab
        "126.1": (0.4506587009803921, 0.331132643866863, 0.18973504500222269),  # spruce_planks
        "126.2": (0.754779411764706, 0.6850560973959593, 0.4770094885380623),  # birch_planks
        "126.3": (0.6291819852941176, 0.4457357636762366, 0.3136753632260579),  # jungle_planks
        "126.4": (0.6593443627450981, 0.3483041499603943, 0.19734879754406362),  # acacia_planks
        "126.5": (0.2614123774509804, 0.16720706029266882, 0.0794248329406058),  # dark_oak_planks
        "127.0": (0.34770220588235295, 0.2313993847891825, 0.19449059509488537), #cocoa_stage2 Cocoa
        "128.0": (0.43921569, 0.50196078, 0.56470588), #Sandstone Stairs
        "129.0": (0.5347426470588236, 0.5009812073542261, 0.4442017390021266), #Emerald Ore
        "130.0": (0.06679112813938183, 0.07135703890931372, 0.054576711955321655), #Ender Chest
        "131.0": (0.10050551470588236, 0.09785473337761623, 0.09776193585775303), #tripwire_hook Tripwire Hook
        "132.0": (0.08305759803921568, 0.08305759803921568, 0.08305759803921568), #tripwire Tripwire
        "133.0": (0.15863915677714102, 0.7978400735294118, 0.3233743930430756), #133: #emerald_block Block of Emerald
        "134.0": (0.43921569, 0.50196078, 0.56470588), #Spruce Stairs
        "135.0": (0.43921569, 0.50196078, 0.56470588), #Birch Stairs
        "136.0": (0.43921569, 0.50196078, 0.56470588), #Jungle Stairs
        "137.0": (0.5976250501509817, 0.7020565257352941, 0.40678249913515924), #command_block_side Command Block
        "138.0": (0.43810460707720594, 0.8682291666666667, 0.6976025490942299), #138: #beacon Beacon
        "139.0": (0.5005208129636074, 0.5011335784313725, 0.4998055130351006), #139: #Cobblestone (Wall)
        "139.1": (0.39655101098606, 0.4659466911764706, 0.36640483218218356), #mossy cobblestone wall
        "140.0": (0.09508272058823529, 0.08494266151328837, 0.08452137244201448), #flower_pot Flower Pot
        "141.0": (0.23334865196078433, 0.2116813997977446, 0.16293655413107339), #carrots_stage3 Carrots
        "142.0": (0.17582720588235293, 0.1569789388925656, 0.1391749905384948), #potatoes_stage3 Potatoes
        #143: #Wooden Button
        #144: #Mob Head
        "145.0": (0.268734681372549, 0.268734681372549, 0.268734681372549), #anvil
        "146.0": (0.1667767693014706, 0.1374548718210256, 0.12913846767484935), #trapped Trapped Chest
        #147: #Weighted Pressure Plate (light)
        #148: #Weighted Pressure Plate (heavy)
        "149.0": (0.6190655898167876, 0.6576899509803922, 0.603396275339563), #comparator Redstone Comparator (inactive)
        "150.0": (0.6413503067430191, 0.6942708333333333, 0.6314269859962213), #comparator_on Redstone Comparator (active)
        "151.0": (0.5119638480392157, 0.4422616290080757, 0.33894077182228594), #daylight_detector_top Daylight Sensor
        "152.0": (0.6884957107843137, 0.08698147113091838, 0.018435822647839745), #redstone_block Block of Redstone
        "153.0": (0.4620710784313725, 0.24209917147084029, 0.21877593278426563), #nether_quartz_ore Nether Quartz Ore
        "154.0": (0.25724287561800147, 0.2696384803921569, 0.26017088152513196), #hopper_outside Hopper
        "155.0": (0.9246323529411765, 0.900784944994607, 0.8754829309940889), #155: #quartz_block_side Block of Quartz
        "155.1": (0.9092677696078431, 0.8879539129727946, 0.8561296485745415), #chiseled_quartz_block Chisseled quartz block
        "155.2": (0.9235294117647058, 0.9022491890138408, 0.8792769607843136), #quartz_pillar pillar quartz block
        "156.0": (0.43921569, 0.50196078, 0.56470588), #Quartz Stairs
        "157.0": (0.27653186274509806, 0.2253635195586252, 0.2027561439710688), #activator_rail Activator Rail
        "158.0": (0.48017769607843136, 0.47733105440590756, 0.47733105440590756), #dropper_front Dropper
        "159.0": (0.8132850146559466, 0.8361085202501606, 0.8395067401960784), #white Stained Clay
        "159.1": (0.879779411764706, 0.3745625012588839, 0.003382730275014467), #orange Stained Clay
        "159.2": (0.6635569852941177, 0.1911995541265679, 0.6247003767559779), #magenta Stained Clay
        "159.3": (0.14100261543036333, 0.5469889296413851, 0.7800551470588235), #light blue Stained Clay
        "159.4": (0.9450520833333332, 0.6724641339963144, 0.08690483542049639), #yellow Stained Clay
        "159.5": (0.37638934290972825, 0.6619791666666667, 0.0974411429610907), #lime Stained Clay
        "159.6": (0.8372549019607842, 0.39773455521914647, 0.563201038698351), #pink Stained Clay
        "159.7": (0.21471848642949828, 0.2267522115274527, 0.2416360294117647), #gray Stained Clay
        "159.8": (0.49031862745098037, 0.4898661996517177, 0.4518622645136486), #light gray Stained Clay
        "159.9": (0.08483902675653598, 0.4759330320669933, 0.5340686274509804), #cyan Stained Clay
        "159.10": (0.38897591969077083, 0.12442872642508296, 0.613265931372549), #purple Stained Clay
        "159.11": (0.17569317540128795, 0.1847930706974975, 0.562438725490196), #blue Stained Clay
        "159.12": (0.3782322303921568, 0.2319452172524651, 0.12499393238740807), #brown Stained Clay
        "159.13": (0.2903241353947409, 0.35819546568627453, 0.14347023347578156), #green Stained Clay
        "159.14": (0.5583639705882353, 0.12943814287548666, 0.12943814287548666), #red Stained Clay
        "159.15": (0.03290985213019031, 0.04131901558471572, 0.06040134803921569), #black Stained Clay

        "160.0": (0.12064950980392157, 0.12064950980392157, 0.12064950980392157), #white Stained Glass Pane
        "160.1": (0.10225183823529412, 0.09302396364714788, 0.09247776546280277), #orange stained Glass Pane
        "160.2": (0.10225183823529412, 0.09885929148300215, 0.09401279612258506), #magenta stained Glass Pane
        "160.3": (0.10225183823529412, 0.09847880301413085, 0.09548673882753929), #light_blue stained Glass Pane
        "160.4": (0.10833333333333334, 0.09908404895352749, 0.0977804585375817), #yellow stained Glass Pane
        "160.5": (0.09636948529411765, 0.08769279282762252, 0.08583350158480212), #lime stained Glass Pane
        "160.6": (0.11439950980392156, 0.11241615613409435, 0.10765610732650903), #pink stained Glass Pane
        "160.7": (0.03610600490196078, 0.03610600490196078, 0.03610600490196078), #gray stained Glass Pane
        "160.8": (0.07221200980392156, 0.07221200980392156, 0.07221200980392156), #light_gray stained Glass Pane
        "160.9": (0.07221200980392156, 0.06958078990228588, 0.06771645821318723), #cyan stained Glass Pane
        "160.10": (0.0840533088235294, 0.08114293573908667, 0.07732183366223327), #purple stained Glass Pane
        "160.11": (0.0840533088235294, 0.0800979158015982, 0.07654027179863213), #blue stained Glass Pane
        "160.12": (0.04794730392156863, 0.04513017514959956, 0.04494472153138216), #brown stained Glass Pane
        "160.13": (0.060263480392156864, 0.056469644072486266, 0.05572156367142445), #green stained Glass Pane
        "160.14": (0.07221200980392156, 0.06616889997612095, 0.06616889997612095), #red stained Glass Pane
        "160.15": (0.011825980392156862, 0.011825980392156862, 0.011825980392156862), #black stained Glass Pane

        "161.0": (0.33883272058823527, 0.33767005929209915, 0.33767005929209915), #Acacia Leaves
        "161.1": (0.41320315034331745, 0.416360294117647, 0.41347823970894837), #dark oak Leaves
        "162.0": (0.40490196078431373, 0.37808142224290325, 0.34131349721261056), #Acacia log
        "162.1": (0.23684129901960785, 0.1807237021380683, 0.10247522197930183), #dark oak log
        "163.0": (0.43921569, 0.50196078, 0.56470588), #Acacia Wood Stairs
        "164.0": (0.43921569, 0.50196078, 0.56470588), #Dark Oak Wood Stairs
        "165.0": (0.441894375678472, 0.7529411764705882, 0.35883506343713956), #slime_block Slime Block
        #166: #Barrier
        "167.0": (0.6840686274509804, 0.6823500726883891, 0.6823500726883891), #iron_trapdoor Iron Trapdoor
        "168.0": (0.3823654966783359, 0.6467371323529412, 0.628579806547992), #prismarine
        "168.1": (0.3863377066512879, 0.6730392156862745, 0.6174907983107458), #prismarine_bricks Prismarine brick
        "168.2": (0.2091420498576269, 0.35935968137254903, 0.29681502413333977), #dark_prismarine dark Prismarine
        "169.0": (0.6523253171856979, 0.7838970588235294, 0.7129934342306127), #sea_lantern Sea Lantern
        "170.0": (0.6518229166666667, 0.5256287197866883, 0.15036460327946277), #170: #hay_block_side Hay Bale
        #"171.0": #white Carpet #gonna delete
        #"171.1": #orange Carpet
        #"171.2": #magenta Carpet
        #"171.3": #lightblue Carpet
        #"171.4": #yellow Carpet
        #"171.5": #lime Carpet
        #"171.6": #pink Carpet
        #"171.7": #gray Carpet
        #"171.8": #light gray Carpet
        #"171.9": #cyan Carpet
        #"171.10": #purple Carpet
        #"171.11": #blue Carpet
        #"171.12": #brown Carpet
        #"171.13": #green Carpet
        #"171.14": #red Carpet
        #"171.15": #black Carpet
        "172.0": (0.6318919002381896, 0.6548226016370489, 0.7037071078431373), #Hardened Clay
        "173.0": (0.06283700980392157, 0.06263679384131103, 0.06263679384131103), #coal_block Block of Coal
        "174.0": (0.5556260531556373, 0.7113623410041215, 0.9823223039215686), #packed_ice Packed Ice
        "175.0": (0.19597120098039217, 0.16951433061982393, 0.16493942548201113), #sunflower_front sun flower Double Plant
        "175.1": (0.20142641645312853, 0.20713848039215688, 0.1764484775987601), #lilac_top lilac sun flower Double Plant
        "175.2": (0.20823467494561623, 0.2088235294117647, 0.2078638624567474), #tall_grass_top double tallgrass /sun flower Double Plant
        "175.3": (0.201388499543245, 0.20176164215686274, 0.20023483071039383), #large_fern_top large fern Double Plant
        "175.4": (0.2190870098039216, 0.20298909396815962, 0.16052956269824106), #rose_bush_top Rose bush sun flower Double Plant
        "175.5": (0.2477648334320708, 0.2699142156862745, 0.22072350759773884), #peony_top Peony //sun flower Double Plant
        #176: #Standing Banner
        #177: #Wall Banner
        "178.0": (0.33642970007779466, 0.48904718137254904, 0.3817520421792056), #daylight_detector_inverted_top Daylight Sensor (inverted)
        "179.0": (0.7322763480392156, 0.38035069844557595, 0.11310573555881456), #red_sandstone Red Sandstone
        "179.1": (0.7184895833333332, 0.3710440163892857, 0.10591337715099063), #chiseled_red_sandstone Chisseled Red Sandstone
        "179.2": (0.7184895833333332, 0.3710440163892857, 0.10591337715099063), #chiseled_red_sandstone smooth Red Sandstone
        "180.0": (0.43921569, 0.50196078, 0.56470588), #Red Sandstone Stairs
        "181.0": (0.7322763480392156, 0.38035069844557595, 0.11310573555881456), #Double Red Sandstone Slab
        "182.0": (0.7322763480392156, 0.38035069844557595, 0.11310573555881456), #Red Sandstone Slab

        "183.0": (0.6067555147058823, 0.5046056151831682, 0.3432053826671983), #Spruce Fence Gate
        "184.0": (0.6067555147058823, 0.5046056151831682, 0.3432053826671983), #Birch Fence Gate
        "185.0": (0.6067555147058823, 0.5046056151831682, 0.3432053826671983), #Jungle Fence Gate
        "186.0": (0.6067555147058823, 0.5046056151831682, 0.3432053826671983), #Dark Oak Fence Gate
        "187.0": (0.6067555147058823, 0.5046056151831682, 0.3432053826671983), #Acacia Fence Gate
        "188.0": (0.5418198529411764, 0.44791377360481555, 0.3361640270193555), #Spruce Fence
        "189.0": (0.5418198529411764, 0.44791377360481555, 0.3361640270193555), #Birch Fence
        "190.0": (0.5418198529411764, 0.44791377360481555, 0.3361640270193555), #Jungle Fence
        "191.0": (0.5418198529411764, 0.44791377360481555, 0.3361640270193555), #Dark Oak Fence
        "192.0": (0.5418198529411764, 0.44791377360481555, 0.3361640270193555), #Acacia Fence

        "193.0": (0.4175551470588236, 0.30378265367271506, 0.19452006092533522), #spruce_door_top Spruce Door
        "194.0": (0.8635110294117646, 0.8151790441723609, 0.6769725407971092), #birch_door_top Birch Door
        "195.0": (0.5662683823529412, 0.4142961870403511, 0.326463090837208), #jungle_door_top Jungle Door
        "196.0": (0.47317708333333336, 0.3053923519270918, 0.259218119702308), #196: #acacia_door_top Acacia Door
        "197.0": (0.3004595588235294, 0.1973149498683868, 0.09966991032971091), #dark_oak_door_top Dark Oak Door
        "198.0": (0.18440563725490197, 0.1807335097879757, 0.1803519900511522), #end_rod End Rod
        "199.0": (0.3667055412736092, 0.21227424735978945, 0.3681525735294117), #chorus_plant horus Plant
        "200.0": (0.5863808897209829, 0.43060755112591914, 0.5953125), #chorus_flower Chorus Flower
        "201.0": (0.6652746816525308, 0.49254203588125667, 0.6663449754901961), #purpur_block Purpur Block
        "202.0": (0.6723884813653502, 0.5059268140371191, 0.6736060049019608), #purpur_pillar Purpur Pillar
        "203.0": (0.43921569, 0.50196078, 0.56470588), #Purpur Stairs
        "204.0": (0.6652746816525308, 0.49254203588125667, 0.6663449754901961), #Purpur Double Slab
        "205.0": (0.6652746816525308, 0.49254203588125667, 0.6663449754901961), #Purpur Slab
        "206.0": (0.8655381029852292, 0.8833946078431373, 0.6368479417847103), #end_stone_bricks End Stone Bricks
        "207.0": (0.2394454656862745, 0.21616221977080927, 0.15559186900959068), #beetroots_stage3 Beetroot
        "208.0": (0.5815410539215686, 0.47507175540615654, 0.25742634551427035), #dirt_path_top Grass Path
        "209.0": (0.01120904660692402, 0.01120904660692402, 0.01120904660692402), #end_portal End Gateway
        "210.0": (0.4947991097424083, 0.43763436375742276, 0.6816329656862744), #repeating_command_block_side Repeating Command Block
        "211.0": (0.49842375007696865, 0.649624693627451, 0.6333233419009147), #chain_command_block_side Chain Command Block
        "212.0": (0.5322647297707763, 0.7041030137417318, 0.9887101715686275), #frosted_ice_3 Frosted Ice
        "213.0": (0.5597375408496732, 0.21769903356859238, 0.1555912594402293), #magma Magma Block
        "214.0": (0.45022977941176473, 0.008165750976397924, 0.006165830618782481), #nether_wart_block Nether Wart Block
        "215.0": (0.2727328431372549, 0.02207598564854863, 0.032374112054564384), #red_nether_bricks Red Nether Brick
        "216.0": (0.8998008578431373, 0.8855960563228998, 0.8169331685454514), #bone_block_side Bone Block
        #217: #Structure Void
        "218.0": (0.27524509803921565, 0.2703456678320838, 0.2703456678320838), #observer_side Observer
        "219.0": (0.8464738434436274, 0.8655008327039743, 0.8667892156862744), #white_shulker_box White Shulker Box
        "220.0": (0.9180300245098039, 0.40847190701816205, 0.03410267784062927), #Orange Shulker Box
        "221.0": (0.6817861519607843, 0.21219131815850575, 0.6469981523243287), #Magenta Shulker Box
        "222.0": (0.19360789556037647, 0.653068553379234, 0.8318780637254902), #Light Blue Shulker Box
        "223.0": (0.9726868872549019, 0.7321100921977243, 0.11674328678986144), #Yellow Shulker Box
        "224.0": (0.3990249126896831, 0.6769914215686275, 0.09157221587700644), #Lime Shulker Box
        "225.0": (0.9037224264705883, 0.476683123631461, 0.6206518885959751), #Pink Shulker Box
        "226.0": (0.2172994142126826, 0.231066227008835, 0.24497549019607842), #Gray Shulker Box
        "227.0": (0.48791360294117647, 0.4875029634288972, 0.4530092443974373), #Light Gray Shulker Box
        "228.0": (0.08009297196015357, 0.4795208466943497, 0.5297334558823529), #Cyan Shulker Box
        "229.0": (0.3989120860968662, 0.12786406708056997, 0.613296568627451), #Purple Shulker Box
        "230.0": (0.1709031710685193, 0.18135071757884877, 0.5498008578431373), #Blue Shulker Box
        "231.0": (0.41695772058823527, 0.25684935707699463, 0.14150247153663853), #Brown Shulker Box
        "232.0": (0.3144567180488349, 0.39554227941176473, 0.12690314797794117), #Green Shulker Box
        "233.0": (0.24226557032694296, 0.5506280637254902, 0.11683133135204908), #Red Shulker Box
        "234.0": (0.09697255651935252, 0.0982703357144348, 0.11582414215686274), #Black Shulker Box

        "235.0": (0.5877204375833515, 0.9314491421568627, 0.7425563182005186), #white_glazed_terracotta White Glazed Terracotta
        "236.0": (0.438063776842313, 0.8356770833333332, 0.12846230899586403), #Orange Glazed Terracotta
        "237.0": (0.8167432598039216, 0.38148466198960446, 0.7337720895955674), #Magenta Glazed Terracotta
        "238.0": (0.34602653905273806, 0.668057692468696, 0.8198835784313725), #Light Blue Glazed Terracotta
        "239.0": (0.9190104166666667, 0.7452827363841033, 0.3486552080141953), #Yellow Glazed Terracotta
        "240.0": (0.6870425579549121, 0.8307751225490196, 0.20449947065318924), #Lime Glazed Terracotta
        "241.0": (0.9221813725490197, 0.6073852679858709, 0.7858468831463029), #Pink Glazed Terracotta
        "242.0": (0.3236548597782404, 0.3672487745098039, 0.3608178707281716), #Gray Glazed Terracotta
        "243.0": (0.555313584130803, 0.6586397058823529, 0.6150964826993698), #Light Gray Glazed Terracotta
        "244.0": (0.2370304094466371, 0.4350615177993107, 0.49149816176470584), #Cyan Glazed Terracotta
        "245.0": (0.3946293357423628, 0.23702726922187384, 0.5974877450980393), #Purple Glazed Terracotta
        "246.0": (0.19593199346029766, 0.2283193484180228, 0.5465533088235294), #Blue Glazed Terracotta
        "247.0": (0.5363268882288743, 0.5721660539215686, 0.22982178461822073), #Brown Glazed Terracotta
        "248.0": (0.36098742154127844, 0.5589001225490197, 0.23402230315188272), #Green Glazed Terracotta
        "249.0": (0.7137101715686275, 0.22774674840176948, 0.2038469079181535), #Red Glazed Terracotta
        "250.0": (0.2008892390256573, 0.27547487745098037, 0.17994906861430998), #Black Glazed Terracotta

        "251.0": (0.8132850146559466, 0.8361085202501606, 0.8395067401960784), #white_concrete white Concrete
        "251.1": (0.879779411764706, 0.3745625012588839, 0.003382730275014467), #orange Concrete
        "251.2": (0.6635569852941177, 0.1911995541265679, 0.6247003767559779), #magenta Concrete
        "251.3": (0.14100261543036333, 0.5469889296413851, 0.7800551470588235), #light blue Concrete
        "251.4": (0.9450520833333332, 0.6724641339963144, 0.08690483542049639), #yellow Concrete
        "251.5": (0.37638934290972825, 0.6619791666666667, 0.0974411429610907), #lime Concrete
        "251.6": (0.8372549019607842, 0.39773455521914647, 0.563201038698351), #pink Concrete
        "251.7": (0.21471848642949828, 0.2267522115274527, 0.2416360294117647), #gray Concrete
        "251.8": (0.49031862745098037, 0.4898661996517177, 0.4518622645136486), #light gray Concrete
        "251.9": (0.08483902675653598, 0.4759330320669933, 0.5340686274509804), #cyan Concrete
        "251.10": (0.38897591969077083, 0.12442872642508296, 0.613265931372549), #purple Concrete
        "251.11": (0.17569317540128795, 0.1847930706974975, 0.562438725490196), #blue Concrete
        "251.12": (0.3782322303921568, 0.2319452172524651, 0.12499393238740807), #brown Concrete
        "251.13": (0.2903241353947409, 0.35819546568627453, 0.14347023347578156), #green Concrete
        "251.14": (0.5583639705882353, 0.12943814287548666, 0.12943814287548666), #red Concrete
        "251.15": (0.03290985213019031, 0.04131901558471572, 0.06040134803921569), #black Concrete

        "252.0": (0.8860848979077307, 0.8934895833333333, 0.893049930136188), #white_concrete_powder Concrete Powder
        "252.1": (0.8912990196078431, 0.5100057739469006, 0.1263219750216263), #orange Concrete
        "252.2": (0.7557904411764705, 0.32897955554579367, 0.729663966008269), #magenta Concrete
        "252.3": (0.29208251953125003, 0.7157274109335504, 0.83671875), #light blue Concrete
        "252.4": (0.91328125, 0.7739773234507067, 0.21612084482230398), #yellow Concrete
        "252.5": (0.49860257190373297, 0.7422487745098039, 0.1654709928835965), #lime Concrete
        "252.6": (0.8974877450980392, 0.6018997163050269, 0.7133700915015093), #pink Concrete
        "252.7": (0.3025175699588199, 0.31844888168271285, 0.3329963235294117), #gray Concrete
        "252.8": (0.6076899509803921, 0.6076287530194678, 0.5820809581013012), #light gray Concrete
        "252.9": (0.14497513937885964, 0.5854113299953895, 0.6163449754901961), #cyan Concrete
        "252.10": (0.5111848171116894, 0.21923384264953685, 0.6964613970588235), #purple Concrete
        "252.11": (0.27620931740496446, 0.29233135318374326, 0.6542432598039215), #blue Concrete
        "252.12": (0.4922947303921568, 0.3301370189684089, 0.21189487338478588), #brown Concrete
        "252.13": (0.38421881351746584, 0.467141544117647, 0.17732486922848184), #green Concrete
        "252.14": (0.6596047794117647, 0.2088207519824231, 0.19969009276217387), #red Concrete
        "252.15": (0.09741226096558415, 0.10335929092706417, 0.1253982843137255), #black Concrete
        "255.0": (0.29710381636570066, 0.32816075892247515, 0.3533547794117647) #structure_block Structure Block
    }



    vertices = []
    faces = []
    vertex_index = 0
    materials = {}

    # Iterate through each block in the schematic
    for y in range(height):
        for z in range(length):
            for x in range(width):
                #print(blocks[y * length * width + z * width + x])
                block_id = int(blocks[y * length * width + z * width + x])
                block_val = int(data[y * length * width + z * width + x] & 0x0F)
                if block_id != 0 and block_id < 256:  # Assuming 0 is air
                    if f"{block_id}.{block_val}" not in block_colors:
                        block_val = 0
                    if f"{block_id}.{block_val}" not in block_colors:
                        continue

                    # Check if there is a block above and below
                    has_block_above = (y < height - 1 and int(blocks[(y + 1) * length * width + z * width + x]) != 0)
                    has_block_below = (y > 0 and int(blocks[(y - 1) * length * width + z * width + x]) != 0)

                    if has_block_above and has_block_below:
                        continue  # Skip this block

                    # Create vertices for the block
                    v0 = (x, y, z)
                    v1 = (x + 1, y, z)
                    v2 = (x + 1, y + 1, z)
                    v3 = (x, y + 1, z)
                    v4 = (x, y, z + 1)
                    v5 = (x + 1, y, z + 1)
                    v6 = (x + 1, y + 1, z + 1)
                    v7 = (x, y + 1, z + 1)

                    vertices.extend([v0, v1, v2, v3, v4, v5, v6, v7])


# Create faces for the block (two triangles per face)
                    faces.extend([
                        (vertex_index, vertex_index + 1, vertex_index + 2, block_id, block_val),
                        (vertex_index, vertex_index + 2, vertex_index + 3, block_id, block_val),
                        (vertex_index + 4, vertex_index + 5, vertex_index + 6, block_id, block_val),
                        (vertex_index + 4, vertex_index + 6, vertex_index + 7, block_id, block_val),
                        (vertex_index, vertex_index + 1, vertex_index + 5, block_id, block_val),
                        (vertex_index, vertex_index + 5, vertex_index + 4, block_id, block_val),
                        (vertex_index + 2, vertex_index + 3, vertex_index + 7, block_id, block_val),
                        (vertex_index + 2, vertex_index + 7, vertex_index + 6, block_id, block_val),
                        (vertex_index + 1, vertex_index + 2, vertex_index + 6, block_id, block_val),
                        (vertex_index + 1, vertex_index + 6, vertex_index + 5, block_id, block_val),
                        (vertex_index, vertex_index + 3, vertex_index + 7, block_id, block_val),
                        (vertex_index, vertex_index + 7, vertex_index + 4, block_id, block_val)
                    ])

                    # Assign a material (color) to the block
                    material_name = f"material_{block_id}.{block_val}"
                    if material_name not in materials:
                        color = block_colors.get(f"{block_id}.{block_val}", (1.0, 1.0, 1.0))  # Default to white if not found
                        materials[material_name] = color

                    vertex_index += 8
    #print(materials)
    return vertices, faces, materials


def convert_schematic_to_obj(schematic_path, obj_path):
    # Load the .schematic file
    schematic = nbtlib.load(schematic_path)
    
    # Extract the necessary data from the schematic
    # This part will depend on the structure of your .schematic file
    # and how you want to convert it to a 3D model.
    
    # For simplicity, let's assume you have a function that converts
    # the schematic data to vertices and faces for an .obj file.
    vertices, faces, materials = schematic_to_mesh(schematic)
    #print(materials)
    mtl_path = obj_path.replace('.obj', '.mtl')
    with open(mtl_path, 'w') as mtl_file:
        for material_name, color in materials.items():
            mtl_file.write(f"newmtl {material_name}\n")
            mtl_file.write(f"Kd {color[0]} {color[1]} {color[2]}\n")

    with open(obj_path, 'w') as obj_file:
        obj_file.write(f"mtllib {mtl_path}\n")
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            material_name = f"material_{face[3]}.{face[4]}"
            obj_file.write(f"usemtl {material_name}\n")
            obj_file.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")


def convert_obj_to_glb(obj_path, glb_path):
    # Load the .obj file using trimesh
    mesh = trimesh.load(obj_path)
    
    # Export the mesh to .glb
    mesh.export(glb_path)

def create_image(glb_path, img_count):
    # Load the GLB file
   
    mesh = trimesh.load(glb_path, force='mesh')
    mesh.rezero()
    mesh.fix_normals()
    mesh.fill_holes()
    #print("test")
    # Render the mesh
    angle = np.radians(-135)
    rotation_matrix = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])

    # Apply the rotation to the mesh
    mesh.apply_transform(rotation_matrix)
    scene = mesh.scene()
    for i in range (1, 6):
        print(i)
        #time.sleep(0.4)
        image = scene.save_image(resolution=[512, 512], cull=False, double_sided=True)
        img_path = f"images/image_{img_count}.png"
        img_count = img_count + 1
        # Save the image
        with open(img_path, 'wb') as f:
            f.write(image)

        # Define a rotation matrix (e.g., 90 degrees around the Z-axis)
        angle = np.radians(45)
        rotation_matrix = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])

        # Apply the rotation to the mesh
        mesh.apply_transform(rotation_matrix)
        scene = mesh.scene()

def get_name(number):
    file_path = 'TrainingData/08RFHbg.txt'
    with open(file_path, 'r') as file:
        for line in file:
            num, text = line.strip().split(' - ', 1)
            if int(num) == number:
                return text
    return None

file_name = 'images/metadata.csv'
img_count = 15007
start = 1912
with open(file_name, 'a') as file:
    file.write("file_name,text\n")
    for i in range (start, 20000):
        schematic_path = f"TrainingData/schem/{i}.schematic"
        obj_path = f"obji/{i}.obj"
        glb_path = 'file.glb'
        #print(i)
        #img_path = 'images/image_{image_count}.png'
        #print(schematic_path)
        #print(os.path.isfile(schematic_path))
        if os.path.isfile(schematic_path):
            #print(i)
            convert_schematic_to_obj(schematic_path, obj_path)
            convert_obj_to_glb(obj_path, glb_path)
            create_image(obj_path, img_count)
            name = get_name(i)
            for i in range (1, 6):
                file.write(f"image_{img_count},{name}\n")
                img_count = img_count + 1


# Example usage
#schematic_path = 'TrainingData/Schematics/1.schematic' #69
#obj_path = 'file.obj'
#glb_path = 'file.glb'
#img_path = 'file.png'

#convert_schematic_to_obj(schematic_path, obj_path)
#convert_obj_to_glb(obj_path, glb_path)
#create_image(obj_path, img_path)
