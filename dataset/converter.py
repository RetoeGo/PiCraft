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
    file_path = 'schem/name.txt'
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
