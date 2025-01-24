import trimesh
import numpy as np
import nbtlib
import os
from collections import Counter
import gzip
import colorsys
import random

# Color to Block Mapping (Complete list from the provided colors)
block_colors = {
    (0.635, 0.235, 0.235): 'minecraft:red_wool',
    (0.486, 0.353, 0.196): 'minecraft:dirt',
    (0.671, 0.514, 0.353): 'minecraft:oak_planks',
    (0.545, 0.388, 0.361): 'minecraft:dark_oak_stairs',
    (0.882, 0.533, 0.235): 'minecraft:orange_wool',
    (0.435, 0.533, 0.235): 'minecraft:green_wool',
    (0.259, 0.533, 0.235): 'minecraft:oak_leaves',
    (0.933, 0.933, 0.235): 'minecraft:yellow_wool',
    (0.514, 0.514, 0.514): 'minecraft:stone',
    (0.976, 0.976, 0.976): 'minecraft:glass',
    (0.435, 0.635, 0.882): 'minecraft:light_blue_wool',
    (0.235, 0.333, 0.733): 'minecraft:blue_wool',
    (0, 0, 0): 'minecraft:black_concrete',
    (0.733, 0.333, 0.882): 'minecraft:magenta_wool',
    (0.533, 0.282, 0.733): 'minecraft:purple_wool',
    (1.0, 0.875, 0.498): 'minecraft:sandstone',
    (1.0, 0.714, 0.757): 'minecraft:pink_concrete'
}

# Convert an RGB color (as a tuple) to HSV color space
def rgb_to_hsv(rgb):
    """
    Convert RGB values (0 to 1) to HSV color space.
    """
    # Normalize the RGB values to [0, 1] if they are in the range [0, 255]
    rgb = np.array(rgb)
    if rgb.max() > 1:
        rgb = rgb / 255.0
    
    # Convert to HSV using colorsys
    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    return hsv

# Convert HSV back to RGB
def hsv_to_rgb(hsv):
    """
    Convert HSV color space to RGB.
    """
    return colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])

# Increase the brightness of a color in HSV space
def brighten_color(hsv, factor=1.1):
    """
    Brighten the color by adjusting the value (brightness) component in HSV space.
    The factor should be greater than 1 to make the color brighter.
    """
    h, s, v = hsv
    v = min(v * 1.2, 1.0)  # Ensure the brightness doesn't exceed 1
    s = min(s * 1.1, 1.0)  # Ensure the brightness doesn't exceed 1
    return (h, s, v)

# Compute Euclidean distance between two colors in HSV space
def euclidean_distance_hsv(color1, color2):
    """
    Compute the Euclidean distance between two colors in HSV space.
    """
    return np.linalg.norm(np.array(color1) - np.array(color2))

# Map color to Minecraft block with fallback using HSV
def get_block_from_color(color):
    """
    Map the color to the closest Minecraft block type using HSV color space.
    """
    hsv_color = rgb_to_hsv(color)
    
    # Brighten the color slightly
    brightened_hsv = brighten_color(hsv_color, factor=1.1)
    
    # Convert back to RGB after brightening
    brightened_rgb = hsv_to_rgb(brightened_hsv)
    
    # Find the closest color based on Euclidean distance in HSV space
    closest_color = min(block_colors.keys(), key=lambda x: euclidean_distance_hsv(rgb_to_hsv(x), brightened_hsv))
    return block_colors.get(closest_color, "minecraft:stone")  # Default block if no match

# Load the .obj file using trimesh
def load_obj_file(obj_file):
    """
    Load an OBJ file and return the meshes.
    """
    scene = trimesh.load_mesh(obj_file)
    if isinstance(scene, trimesh.Scene):
        meshes = scene.dump()  # Decompose the scene into individual meshes
    else:
        meshes = [scene]
    print(f"Loaded {len(meshes)} mesh(es)")  # Debug print to verify mesh loading
    return meshes

# Function to count the most frequent color in a list of vertex colors
def get_most_frequent_color(colors):
    """
    Find the most frequent color in the list of vertex colors.
    """
    color_counter = Counter([tuple(color) for color in colors])  # Count colors
    most_common_color = color_counter.most_common(1)[0][0]  # Get the most frequent color
    return most_common_color

# Function to process the faces of a mesh and determine the block type
def process_faces_and_assign_block_type(meshes, center):
    """
    Process each face in the mesh, map the color to a Minecraft block, and create the NBT data.
    """
    voxel_data = []
    block_palette = []
    block_to_state_index = {}
    new_max_coords = np.array([0, 0, 0])
    processed_blocks = 0

    # Process each mesh and each face in the mesh
    for mesh in meshes:
        for face_idx, face in enumerate(mesh.faces):
            vertices = mesh.vertices[face]
            vertex_colors = mesh.visual.vertex_colors[face, :3]  # Assuming vertex colors are stored

            # Get the most frequent color for this face
            most_frequent_color = get_most_frequent_color(vertex_colors)

            # Map the most frequent color to a Minecraft block type
            block_type = get_block_from_color(most_frequent_color)
            properties = {}

            # Handle Dark Oak Stairs with a facing property
            if block_type == "minecraft:dark_oak_stairs":
                facing = determine_stair_facing(vertices[0], center)  # Assuming the first vertex of the stair defines its orientation
                properties = {
                    "facing": facing,
                    "half": "bottom"
                }

            for vertex in vertices:
                shifted_vertex = tuple(np.round(vertex).astype(int))

                # Create block state if not already in the palette
                state_key = (block_type, tuple(properties.items()))
                if state_key not in block_to_state_index:
                    block_palette.append(nbtlib.Compound({
                        "Name": nbtlib.String(block_type),
                        "Properties": nbtlib.Compound({k: nbtlib.String(v) for k, v in properties.items()})
                    }))
                    block_to_state_index[state_key] = len(block_palette) - 1

                state = block_to_state_index[state_key]

                if shifted_vertex not in [pos for pos, _ in voxel_data]:
                    voxel_data.append((shifted_vertex, state))
                    new_max_coords = np.maximum(new_max_coords, shifted_vertex)
                    processed_blocks += 1

    

    return block_to_state_index, voxel_data, block_palette, new_max_coords, processed_blocks

# Determine the facing direction of stairs towards the center
def determine_stair_facing(position, center):
    """
    Determine the facing direction of a stair block based on its position relative to the center.
    This method ensures that all blocks are correctly facing north, south, east, or west.
    """
    dx, dy, dz = np.array(position) - np.array(center)  # Calculate relative position
    
    # Ensure facing direction is based on relative position (east/west or north/south)
    if abs(dx) > abs(dz):  # East/West direction
        return "east" if dx < 0 else "west"
    else:  # North/South direction
        return "south" if dz < 0 else "north"

# Main conversion function
def convert_faces_to_nbt(generation_number):
    """
    Main function to convert OBJ faces to NBT format.
    """
    print("Starting the conversion process...")  # Debug print

    obj_path = os.path.join('', f'updated_object_with_color_flipped.obj') 
    output_file = os.path.join('', f'pagoda20.nbt')

    meshes = load_obj_file(obj_path)

    # Scaling factor
    scaling_factor = 32
    print("Scaling factor:", scaling_factor)

    # Initialize min and max coordinates
    min_coords = np.array([np.inf, np.inf, np.inf])
    max_coords = np.array([-np.inf, -np.inf, -np.inf])

    # Scale and adjust vertices first
    for mesh in meshes:
        mesh.apply_scale(scaling_factor)
        mesh.vertices = np.round(mesh.vertices).astype(int)

    # Recalculate min and max coordinates after scaling
    for mesh in meshes:
        for face in mesh.faces:
            vertices = mesh.vertices[face]
            min_coords = np.minimum(min_coords, vertices.min(axis=0))
            max_coords = np.maximum(max_coords, vertices.max(axis=0))

    # Ensure that all coordinates are above zero by shifting each axis independently
    print("Min coordinates after scaling:", min_coords)

    # Shift all vertices by their respective minimum coordinate values
    for mesh in meshes:
        mesh.vertices -= min_coords  # Shift each axis by its respective minimum value

    # Recalculate min and max coordinates across all meshes after shifting
    final_min_coords = np.array([np.inf, np.inf, np.inf])
    final_max_coords = np.array([-np.inf, -np.inf, -np.inf])
    for mesh in meshes:
        final_min_coords = np.minimum(final_min_coords, mesh.vertices.min(axis=0))
        final_max_coords = np.maximum(final_max_coords, mesh.vertices.max(axis=0))

    # Calculate dimensions and center after shifting
    dimensions = np.ceil((final_max_coords - final_min_coords)).astype(int)
    center = (dimensions / 2).astype(int)

    # Output the dimensions and center
    print("Dimensions:", dimensions)
    print("Center:", center)
    print(final_min_coords)
    print(final_max_coords)

    # Process faces and assign block types
    block_to_state_index, voxel_data, block_palette, new_max_coords, processed_blocks = process_faces_and_assign_block_type(meshes, center)
    print(max_coords)
    print(new_max_coords)

    # Final structure size
    final_size = new_max_coords + 1
    print("Final structure size:", final_size)

    # Create NBT data
    nbt_voxel_data = []


#jigsaw
    jig_block_type = 'minecraft:jigsaw'
    jig_prop1 = {"orientation": "south_up"}
    jig_state_key1 = (jig_block_type, tuple(jig_prop1.items()))
    jig_state1 = block_to_state_index.get(jig_state_key1, None) 

    jig_prop2 = {"orientation": "up_south"}
    jig_state_key2 = (jig_block_type, tuple(jig_prop2.items()))
    jig_state2 = block_to_state_index.get(jig_state_key2, None) 

    # If the block state is not found, add it to the block palette
    if jig_state1 is None:
        block_palette.append(nbtlib.Compound({
            "Name": nbtlib.String(jig_block_type),
            "Properties": nbtlib.Compound({k: nbtlib.String(v) for k, v in jig_prop1.items()})
        }))
        jig_state1 = len(block_palette) - 1
        block_to_state_index[jig_state_key1] = jig_state1

    # If the block state is not found, add it to the block palette
    if jig_state2 is None:
        block_palette.append(nbtlib.Compound({
            "Name": nbtlib.String(jig_block_type),
            "Properties": nbtlib.Compound({k: nbtlib.String(v) for k, v in jig_prop2.items()})
        }))
        jig_state2 = len(block_palette) - 1
        block_to_state_index[jig_state_key2] = jig_state2

    # Add floor block at the current (x, y, z) position
    nbt_voxel_data.append(nbtlib.Compound({
        "pos": nbtlib.List([nbtlib.Int(v) for v in (0, 0, 0)]),
        "state": nbtlib.Int(jig_state1),
        "nbt": nbtlib.Compound({
            "name": nbtlib.String("japanese:houses"),
            "selection_priority": nbtlib.Int(0),
            "target": nbtlib.String("japanese:houses"),
            "id": nbtlib.String("minecraft:jigsaw"),
            "joint": nbtlib.String("rollable"),
            "placement_priority": nbtlib.Int(0),
            "pool": nbtlib.String("japanese:pool"),
            "final_state": nbtlib.String("minecraft:stone_bricks")
        })
    }))

    # Add floor block at the current (x, y, z) position
    nbt_voxel_data.append(nbtlib.Compound({
        "pos": nbtlib.List([nbtlib.Int(v) for v in (0, 1, 0)]),
        "state": nbtlib.Int(jig_state2),
        "nbt": nbtlib.Compound({
            "name": nbtlib.String("minecraft:empty"),
            "selection_priority": nbtlib.Int(0),
            "target": nbtlib.String("japanese:villager"),
            "id": nbtlib.String("minecraft:jigsaw"),
            "joint": nbtlib.String("rollable"),
            "placement_priority": nbtlib.Int(0),
            "pool": nbtlib.String("japanese:mobs"),
            "final_state": nbtlib.String("minecraft:spruce_planks")
        })
    }))


    for position, state in voxel_data:
        if position not in {(0, 0, 0), (0, 1, 0)}:
            nbt_voxel_data.append(nbtlib.Compound({
                "pos": nbtlib.List([nbtlib.Int(v) for v in position]),
                "state": nbtlib.Int(state),
            }))

    schematic = nbtlib.Compound()
    data_tag = nbtlib.Compound()

    interior = False
    # Ensure that min_coords is of integer type
    min_coords = np.floor(final_min_coords).astype(int)
    max_coords = np.floor(final_max_coords).astype(int)
    if interior:
        # Initialize floor block type and properties
        floor_block_type = 'minecraft:dark_oak_planks'
        properties = {}

        # Create a state key for the floor block
        state_key = (floor_block_type, tuple(properties.items()))
        state = block_to_state_index.get(state_key, None)

        # If the block state is not found, add it to the block palette
        if state is None:
            block_palette.append(nbtlib.Compound({
                "Name": nbtlib.String(floor_block_type),
                "Properties": nbtlib.Compound({k: nbtlib.String(v) for k, v in properties.items()})
            }))
            state = len(block_palette) - 1
            block_to_state_index[state_key] = state


        # Loop through all positions in the structure
        for y in range(min_coords[1], max_coords[1] + 1):
            if y % 5 == 0:
                for x in range(min_coords[0], max_coords[0] + 1):
            #for y in range(min_coords[1], max_coords[1] + 1):
                    for z in range(min_coords[2], max_coords[2] + 1):
                        position = (x, y, z)

                    # Add floor blocks only if the y-coordinate is divisible by 5
#                    if y % 5 == 0:
                        # Check if there is a block directly above or below
                        block_above_direct = (x, y + 1, z) in [pos for pos, _ in voxel_data]
                        block_below_direct = (x, y - 1, z) in [pos for pos, _ in voxel_data]
                        block2above_direct = (x, y + 2, z) in [pos for pos, _ in voxel_data]
    #                    # Check if there are blocks above (but not directly above) and below (but not directly below)
                        block_above = False
                        block_below = False
                        block_before_x = False
                        block_after_x = False
                        block_before_z = False
                        block_after_z = False

                        # Look for blocks above, excluding directly above (y + 1)
#                        for y_above in range(y + 2, max_coords[1] + 1):  # Start at y + 2
#                            if (x, y_above, z) in [pos for pos, _ in voxel_data]:
#                                block_above = True
#                                break

                        # Look for blocks below, excluding directly below (y - 1)
#                        for y_below in range(y - 2, min_coords[1] - 1, -1):  # Start at y - 2
#                            if (x, y_below, z) in [pos for pos, _ in voxel_data]:
#                                block_below = True
#                                break

                        # Look for blocks before the current x (but not directly before)
                        for x_before in range(x - 1, min_coords[0] - 1, -1):  # Start at x - 1
                            if (x_before, y, z) in [pos for pos, _ in voxel_data]:
                                block_before_x = True
                                break

                        # Look for blocks after the current x (but not directly after)
                        for x_after in range(x + 1, max_coords[0] + 1):  # Start at x + 1
                            if (x_after, y, z) in [pos for pos, _ in voxel_data]:
                                block_after_x = True
                                break

                        # Look for blocks before the current z (but not directly before)
                        for z_before in range(z - 1, min_coords[2] - 1, -1):  # Start at z - 1
                            if (x, y, z_before) in [pos for pos, _ in voxel_data]:
                                block_before_z = True
                                break

                    # Look for blocks after the current z (but not directly after)
                        for z_after in range(z + 1, max_coords[2] + 1):  # Start at z + 1
                            if (x, y, z_after) in [pos for pos, _ in voxel_data]:
                                block_after_z = True
                                break



                        # Add floor if blocks above, below, before, and after exist
                        if block_before_x and block_after_x and block_before_z and block_after_z and (not block_above_direct or not block_below_direct):
                            if position not in [tuple(data['pos']) for data in nbt_voxel_data]:
                                # Add floor block at the current (x, y, z) position
                                nbt_voxel_data.append(nbtlib.Compound({
                                    "pos": nbtlib.List([nbtlib.Int(v) for v in position]),
                                    "state": nbtlib.Int(state),
                                }))


                            # Randomly decide whether to place furniture above the block, 10% chance
                            if random.random() < 0.15:  # 10% chance
                                print("test")
                                # Randomly pick a furniture type
                                furniture_types = ['minecraft:crafting_table', 'minecraft:chest', 'minecraft:flower_pot', 'minecraft:furnace', 'minecraft:lantern', 'minecraft:brewing_stand', 'minecraft:torch', 'minecraft:bookshelf' ]

                                # Assign weights for each furniture type (higher value means higher chance of being selected)
                                weights = [0.1, 0.2, 0.05, 0.1, 0.4, 0.01, 0.15, 0.04]  # crafting_table has 50%, chest has 30%, bed has 20%

                                # Use random.choices() with weights
                                furniture_type = random.choices(furniture_types, weights=weights, k=1)[0]


                                furniture_type = random.choice(furniture_types)

                                # Define the position for the furniture to be placed above the current block
                                furniture_position = (position[0], position[1] + 1, position[2])  # Place 1 block above

                                # Add furniture block to nbt_voxel_data
                                properties = {}
                                state_key2 = (furniture_type, tuple(properties.items()))
                                if state_key2 not in block_to_state_index:
                                    print("test2")
                                    block_palette.append(nbtlib.Compound({
                                        "Name": nbtlib.String(furniture_type),
                                        "Properties": nbtlib.Compound({k: nbtlib.String(v) for k, v in properties.items()})
                                    }))
                                    block_to_state_index[state_key2] = len(block_palette) - 1
                                state2 = block_to_state_index[state_key2]

                            # Ensure unique positions for the furniture by checking position
                            # Extract the position from each nbt_voxel_data item
                                if furniture_position not in [tuple(data['pos']) for data in nbt_voxel_data]:  # Extract positions from nbt_voxel_data
                                    print("test3")
                                    nbt_voxel_data.append(nbtlib.Compound({
                                        "pos": nbtlib.List([nbtlib.Int(v) for v in furniture_position]),
                                        "state": nbtlib.Int(state2),
                                    }))
                                  
    data_tag['size'] = nbtlib.List([nbtlib.Int(v) for v in final_size])
    data_tag['entities'] = nbtlib.List([])
    data_tag['blocks'] = nbtlib.List(nbt_voxel_data)
    data_tag['palette'] = nbtlib.List(block_palette)
    data_tag['DataVersion'] = nbtlib.Int(3686)

    schematic[''] = data_tag

    # Save the NBT file
    with gzip.open(output_file, 'wb') as f:
        schematic.write(f)

    print(f"Conversion complete! NBT file saved as {output_file}")
    return output_file


if __name__ == "__main__":
    generation_number = 1  # You can change this to whatever you need
    convert_faces_to_nbt(generation_number)

