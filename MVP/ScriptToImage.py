from diffusers import DiffusionPipeline
import torch
import AddTextToImage

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe.to("cuda")

def generate_images_from_script(comic_script):
    # Iterate through each panel in the script
    # Segment and print each JSON panel separately
    for i, panel in enumerate(comic_script):
        image = pipe(prompt=panel["panel art"]).images[0]
        image.save(f"images/imagesWithoutText/panel_{i}.png")
        AddTextToImage.add_text_to_panel(panel["text"], image)
        if i == 5:
            return