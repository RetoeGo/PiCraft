# chat gpt was used to write code
import os
from typing import List
import torch
from cog import BasePredictor, Input, Path
from diffusers import StableDiffusionXLPipeline
from diffusers import (
    PNDMScheduler,
    LMSDiscreteScheduler,
    DDIMScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
)
from huggingface_hub import login
import numpy as np
from PIL import Image

MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
MODEL_CACHE = "diffusers-cache"
LORA_WEIGHTS_PATH = "./pytorch_lora_weights.safetensors"  # Local path to the LoRA weights


def make_scheduler(name, config):
    """Create a scheduler from a configuration."""
    return {
        "PNDM": PNDMScheduler.from_config(config),
        "KLMS": LMSDiscreteScheduler.from_config(config),
        "DDIM": DDIMScheduler.from_config(config),
        "K_EULER": EulerDiscreteScheduler.from_config(config),
        "K_EULER_ANCESTRAL": EulerAncestralDiscreteScheduler.from_config(config),
        "DPMSolverMultistep": DPMSolverMultistepScheduler.from_config(config),
    }[name]


class Predictor(BasePredictor):
    def setup(self):
        # Log in to Hugging Face Hub
        login('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')
        print("Loading pipeline...")

        # Load SDXL pipeline
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            MODEL_ID,
            cache_dir=MODEL_CACHE,
            torch_dtype=torch.float32,  # Use float32 for CPU
        ).to("cuda")  # Use CPU for inference

        # Load LoRA weights directly
        print("Loading LoRA weights...")
        self.pipe.load_lora_weights(LORA_WEIGHTS_PATH)  # Use local path to LoRA weights
        print("LoRA weights loaded successfully.")

        # Debugging: Inspect loaded LoRA weights
        print("Inspecting LoRA layers and weights:")
        for name, param in self.pipe.unet.named_parameters():
            if "lora" in name:
                print(f"LoRA applied to U-Net layer: {name}, Parameter shape: {param.shape}")

        if hasattr(self.pipe, "text_encoder"):
            for name, param in self.pipe.text_encoder.named_parameters():
                if "lora" in name:
                    print(f"LoRA applied to Text Encoder layer: {name}, Parameter shape: {param.shape}")

        print("LoRA inspection complete.")

    @torch.inference_mode()
    def predict(
        self,
        prompt: str = Input(
            description="Input prompt",
            default="a photo of an astronaut riding a horse on mars",
        ),
        negative_prompt: str = Input(
            description="Specify things to not see in the output",
            default=None,
        ),
        width: int = Input(
            description="Width of output image. Maximum size is 1024x768 or 768x1024",
            choices=[128, 256, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024],
            default=768,
        ),
        height: int = Input(
            description="Height of output image. Maximum size is 1024x768 or 768x1024",
            choices=[128, 256, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024],
            default=768,
        ),
        num_outputs: int = Input(
            description="Number of images to output.",
            ge=1,
            le=4,
            default=1,
        ),
        num_inference_steps: int = Input(
            description="Number of denoising steps", ge=1, le=500, default=50
        ),
        guidance_scale: float = Input(
            description="Scale for classifier-free guidance", ge=1, le=20, default=7.5
        ),
        scheduler: str = Input(
            default="DPMSolverMultistep",
            choices=[
                "DDIM",
             "K_EULER",
                "DPMSolverMultistep",
                "K_EULER_ANCESTRAL",
                "PNDM",
                "KLMS",
            ],
            description="Choose a scheduler.",
        ),
        seed: int = Input(
            description="Random seed. Leave blank to randomize the seed", default=None
        ),
        image: Path = None,  # Input for img2img or inpainting
        mask: Path = None,  # Input for inpainting
        image_strength: float = Input(
            description="Controls the influence of the input image. 0.0 means no influence, 1.0 means full influence.",
            ge=0.0, le=1.0, default=0.75
        ),
        lora_strength: float = Input(
            description="Controls the influence of LoRA weights. 0.0 means no influence, 1.0 means full influence.",
            ge=0.0, le=1.0, default=1.0
        )
    ) -> List[Path]:
        """Run a single prediction on the model"""
        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")
        print(f"Using seed: {seed}")

        if width * height > 786432:
            raise ValueError(
                "Maximum size is 1024x768 or 768x1024 pixels, due to memory limits."
            )

        self.pipe.scheduler = make_scheduler(scheduler, self.pipe.scheduler.config)

        generator = torch.Generator("cuda").manual_seed(seed)  # Use CPU for generator

        # Prepare image and mask
        init_image = None
        init_mask = None
        if image:
            init_image = Image.open(image).convert("RGB")
            init_image = init_image.resize((width, height))
            init_image = np.array(init_image).astype(np.float32) / 255.0
            init_image = torch.from_numpy(init_image).permute(2, 0, 1).unsqueeze(0).to("cuda")

        if mask:
            init_mask = Image.open(mask).convert("L")
            init_mask = init_mask.resize((width, height))
            init_mask = np.array(init_mask).astype(np.float32) / 255.0
            init_mask = torch.from_numpy(init_mask).unsqueeze(0).unsqueeze(0).to("cuda")

        # Perform img2img or inpainting
      # Perform img2img or inpainting
        if init_image is not None and init_mask is not None:
            output = self.pipe(
                prompt=[prompt] * num_outputs if prompt else None,
                negative_prompt=[negative_prompt] * num_outputs if negative_prompt else None,
                init_image=init_image,
                mask_image=init_mask,
                strength=image_strength,  # Control image influence
                guidance_scale=guidance_scale,
                generator=generator,
                num_inference_steps=num_inference_steps,
            )
        else:
            output = self.pipe(
                prompt=[prompt] * num_outputs if prompt else None,
                negative_prompt=[negative_prompt] * num_outputs if negative_prompt else None,
                width=width,
                height=height,
                guidance_scale=guidance_scale,
                generator=generator,
                num_inference_steps=num_inference_steps,
            )

        # Apply LoRA influence
        # If LoRA strength is less than 1, we can scale the LoRA weights
        if lora_strength < 1.0:
            for name, param in self.pipe.unet.named_parameters():
                if "lora" in name:
                    param.data *= lora_strength

        # Save outputs
        output_paths = []
        for i, sample in enumerate(output.images):
            output_path = f"/tmp/out-{i}.png"
            sample.save(output_path)
            output_paths.append(Path(output_path))

        if len(output_paths) == 0:
            raise Exception("NSFW content detected. Try a different prompt.")

        return output_paths
