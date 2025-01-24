import replicate
import os
import requests
import trimesh

def convert_glb_to_obj(glb_path, obj_path):
    """Convert a .glb file to .obj format and save it."""
    print("Converting GLB to OBJ...")
    mesh = trimesh.load(glb_path, force='glb')
    if mesh:
        # Export the mesh as .obj and save it
        mesh.export(obj_path, file_type='obj')
        print(f"OBJ file saved at: {obj_path}")
    else:
        raise ValueError("Failed to load the GLB file for conversion.")

def save_image_from_url(image_url, save_path):
    """Download and save the image from the URL."""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved at: {save_path}")
    else:
        raise ValueError(f"Failed to download the image from {image_url}")

def handle_request(prompt, generation_number):
    # Step 0: Generate the guidance image using the stable-diffusion-3.5-large model
    stable_diffusion_output = replicate.run(
        "stability-ai/stable-diffusion-3.5-large",  # Correct model version format
        input={
            "cfg": 4.5,
            "steps": 40, 
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "output_format": "webp",
            "output_quality": 90, 
            "prompt_strength": 0.85
        }   
    )   
    print("Generated guidance image URL:", stable_diffusion_output)
    guidance_image_url = stable_diffusion_output[0].url  # Extract the URL from FileOutput object
    guidance_image_path = os.path.join('/Users/robinkruijf/Desktop/Thesis/bot/generated', f'guidance_image_{generation_number}.webp')
    save_image_from_url(guidance_image_url, guidance_image_path)

    print("Using generated image as guidance image.")

    # Step 1: Generate the image using the new model (retoego/sd8kv19)
    output = replicate.run(
        "retoego/sd8kv19:93e06d3d45d352c36e2af90be1233978ad34a0525c0336f6f955195a27842c38",
        input={
            "width": 768,
            "height": 768,
            "prompt": prompt,
            "scheduler": "DPMSolverMultistep",
          "num_outputs": 1,
            "lora_strength": 1,
            "guidance_scale": 7.5,
            "image_strength": 0.75,
            "num_inference_steps": 50,
            "image": guidance_image_url  # Use the generated image as guidance (using 'image' for retoego model)
        }
    )
    image_url = output[0].url  # Extract the URL from FileOutput object
    print("Generated image URL:", image_url)

    # Save the generated image from the new model
    generated_image_path = os.path.join('/Users/robinkruijf/Desktop/Thesis/bot/generated', f'generated_image_{generation_number}.webp')
    save_image_from_url(image_url, generated_image_path)

    # Step 2: Send the image URL to another model to remove background and get the OBJ
    glb_output = replicate.run(
        "camenduru/tripo-sr:e0d3fe8abce3ba86497ea3530d9eae59af7b2231b6c82bedfc32b0732d35ec3a",
        input={
            "image_path": image_url,  # Use 'image_path' for camenduru model
            "do_remove_background": True
        }
    )

    # Step 3: Download and save the resulting GLB model
    glb_url = glb_output
    glb_response = requests.get(glb_url)
    glb_path = os.path.join('/Users/robinkruijf/Desktop/Thesis/bot/generated', f'generated_model_{generation_number}.glb')
    obj_path = os.path.join('/Users/robinkruijf/Desktop/Thesis/bot/generated', f'generated_model_{generation_number}.obj')
    print(f"GLB Response: {glb_response}")
    print(f"GLB URL: {glb_url}")

    # Save GLB file
    with open(glb_path, 'wb') as file:
        file.write(glb_response.content)

    # Step 4: Convert the downloaded GLB file to OBJ
    convert_glb_to_obj(glb_path, obj_path)
    print(f"OBJ model saved at: {obj_path}")

    return obj_path

# Call the function to test
#generation_number = 3  # Start with generation 1 and increment for each call
#prompt = "A high quality minecraft 3d Big Ben building"
#obj_model = handle_request(prompt, generation_number)
#print(f"Final OBJ model path: {obj_model}")
glb_path = ''
obj_path = ''
convert_glb_to_obj(glb_path, obj_path)

