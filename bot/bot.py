import discord
import asyncio
import responses  # Assuming this contains your custom functions
import os
from discord import app_commands
from discord.ext import commands
from converter import process_obj_to_nbt

# Ensure the token is correct and replace 'YOUR_TOKEN_HERE' with the actual token
TOKEN = ''  # Replace with your actual token securely
# Predefined file paths
OBJ_PATH = ''
NBT_PATH = ''


# Setting up intents and client
intents = discord.Intents.default()
intents.messages = True  # Ensure that the necessary intents are enabled
intents.message_content = True  # For handling message content
theClient = discord.Client(intents=intents)
theTree = app_commands.CommandTree(theClient)

@theClient.event
async def on_ready():
    await theTree.sync()  # Sync commands with Discord
    print(f'{theClient.user} is now running!')

# Command for generating NBT file
@theTree.command(name="generate_nbt", description="Generate an NBT file from a prompt")
async def generate_nbt_command(interaction: discord.Interaction, prompt: str):
    try:
        await interaction.response.send_message("Generating OBJ file... Please wait.")
        # Call your custom function from `responses` here
        responses.handle_request(prompt)

        if not os.path.exists(OBJ_PATH):
            await interaction.channel.send("Failed to generate the OBJ file.")
            return

        # Convert OBJ to NBT
        process_obj_to_nbt(OBJ_PATH, NBT_PATH, max_size=63)

        if os.path.exists(NBT_PATH):
            await interaction.channel.send(
                "Here's the NBT file you requested:",
                file=discord.File(NBT_PATH)
            )   
        else:
            await interaction.channel.send("Failed to generate the NBT file.")
    
    except Exception as e:
        await interaction.channel.send(f"An error occurred: {e}")
        print(e)

# Run the bot
theClient.run(TOKEN)
