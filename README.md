# PiCraft
If you have any questions regarding PiCraft feel free to join the discord server of PiCraft
https://discord.gg/GDMZSDUxMx

PiCraft is a tool that generates Minecraft structures by converting text into an image, image into an object, and the object into a Minecraft nbt file.
The nbt files are placed in a datapack, therefore the dapack can be easily imported into Minecraft. 
The figure below shows the pipeline of the tool.
<p align="center">
  <img src="images/Pipeline.png" alt="Pipeline" width="50%" />
</p>

## Structure
- images: the images used for the Readme
- README.md: the text your reading now.
- Thesis.pdf: an eleborate explanation of StableDiffusion and what was created in the project.

### dataset
  - converter.py: the code used to generate images
  - push.py: A file to upload the generated images to huggingface
  - palette.txt: the color mappings as used to generate the first 2 datasets
  - schem: the location of your provided schematic files.
  - obj: the location for the generated obj files
  - image: the location of all the generated images
### bot
  - bot.py: the code that handles users request to transform text into a minecraft structure
  - response.py: the code that calls api's from chatGPT, Replicate and other websites that provide GPU's to generate the object belonging to each house.
  - converter.py: the conversion from object into Minecraft House structure
  - palette.txt: the color mappings as used to generate the first 2 datasets back into structures
  - Pack: the place for your generated intermediate image, obj and nbt files.
  - Japanese: ... This is the Datapack where the nbt structures are automatically replaced. This datapack was originally made available here: https://www.planetminecraft.com/data-pack/japanese-cherry-village-1-20-4/
### Replicate
#### cog-stable-diffusion
- cog.yaml
- predict.py
- pytorch_lora_weights.safetensors
- LICENSE
- README.md

## SLURM Fine-tune
stable.slurm

## Huggingface
Each of the datasets is published on huggingface below the links to the models on huggingface.
- 8k dataset: https://huggingface.co/datasets/Retoe/image8k
- 10k dataset: https://huggingface.co/datasets/Retoe/image10k
- 15k dataset: https://huggingface.co/datasets/Retoe/image15k
- 8k model: https://huggingface.co/Retoe/stable8k
- 10k model: https://huggingface.co/Retoe/sd10k
- 15k model: https://huggingface.co/Retoe/sd15k


## Replicate
Below the model as published on Replicate
- https://replicate.com/retoego/picraft
