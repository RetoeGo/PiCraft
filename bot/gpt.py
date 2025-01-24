# chat-gpt was used to help write the file.

import requests
import multiprocessing
from pydantic import BaseModel
from openai import OpenAI
import json
from responses import handle_request  # Ensure the correct import
from converter import convert_faces_to_nbt  # Ensure the correct import
import gzip

# Initialize OpenAI client
client = OpenAI(api_key='')

# Define Pydantic Model for structured response
class BuildingPromptsResponse(BaseModel):
    building_prompts: list[str]
    characters: list[str]

# Function to read the latest generation number from a file
def read_generation_number(filename='generation_number.txt'):
    try:
        with open(filename, 'r') as file:
            generation_number = int(file.read().strip())
    except FileNotFoundError:
        generation_number = 0  # Start from 0 if file doesn't exist
    return generation_number

# Function to update the generation number in the file
def update_generation_number(generation_number, filename='generation_number.txt'):
    with open(filename, 'w') as file:
        file.write(str(generation_number))

# Function to generate related prompts using OpenAI
def generate_related_prompts(original_prompt: str):
    """ 
    Use OpenAI to generate detailed, high-quality building prompts, focusing on 3D mesh details in a Minecraft theme.
    This version also includes character names and their descriptions.
    """
    # Make the API request using the function call
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # Example model version
        messages=[
            {"role": "system", "content": "Generate high-quality detailed prompts for 3D Minecraft-like meshes, do not include the surroundings, only include the structure itself, provide names of the characters, nothing else 1 word no spaces for name"},
            {"role": "user", "content": f"Generate a list of 4 related 3D Minecraft object prompts based on the following theme: {original_prompt}. Add the name of the character in all prompts"}
        ],  
        response_format=BuildingPromptsResponse,  # Parse the response into structured format using Pydantic
    )   

    # Return the structured response
    return response.choices[0].message.parsed

# Function to try and download the character image
def download_character_image(character, save_path):
    # Define the URL to download the image
    url = f"https://mineskin.eu/download/{character}"

    # Try to download the URL
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded and saved image for character: {character}")
            return True
    except requests.RequestException as e:
        print(f"Failed to download image for {character} from {url}: {e}")

    return False

# Function to download and save the first character image that works
def download_and_save_image(characters, image_save_path):
    # Loop over each character to try and download the image
    for character in characters:
        if download_character_image(character, image_save_path):
            break

# Function to handle processing of structures and character images
def process_structure_and_image(prompt, character, generation_number, i):
    # Proceed with structure generation regardless of image download
    handle_request(prompt, generation_number)

    # Convert faces to NBT and write the resulting file
    nbt_file_location = convert_faces_to_nbt(generation_number)

    # Define the structure filename (house1.nbt, house2.nbt, etc.)
    structure_filename = f'./reskin/japanese-cherry-village-beta-1-20-4/data/japanese/structures/house_{i}.nbt'

    # Overwrite the NBT file with the converted structure
    with gzip.open(structure_filename, 'wb') as nbt_file:
        with gzip.open(nbt_file_location, 'rb') as converted_file:
            nbt_file.write(converted_file.read())

# Main function to process and update the generation number
def process_and_generate_structures(original_prompt: str):
    # Read the latest generation number
    generation_number = read_generation_number()

    # Generate related prompts using OpenAI
    building_prompts = generate_related_prompts(original_prompt)

    # Define the path to save the downloaded character image
    image_save_path = './reskin/japanese-cherry-village-beta-1-20-4/assets/minecraft/textures/entity/villager/villager.png'

    # Download and save the first valid character image
    download_and_save_image(building_prompts.characters, image_save_path)

    # Create a pool of processes to handle each structure
    processes = []

    int_value2 = int(generation_number)
    # Create a child process for each structure and image download
    for i, (prompt, character) in enumerate(zip(building_prompts.building_prompts, building_prompts.characters)):
        int_value1 = int(i)
        int_value3 = int_value1 + int_value2
        process = multiprocessing.Process(target=process_structure_and_image, args=(prompt, character, int_value3, int_value1+1))
        processes.append(process)
        process.start()  # Start the process

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Update the generation number for the next time (4 structures generated)
    update_generation_number(int_value2 + 4)

#if __name__ == "__main__":
    # Example usage
#    original_prompt = "Bikini Bottom"
#    process_and_generate_structures(original_prompt)
