from diffusers import DiffusionPipeline
import torch
import AddTextToImage
import json

# Load comic panel script
with open("adaptive_comic_script_v1.1.json", "r", encoding="utf-8") as f:
    comic_script = json.load(f)

# Load SDXL pipeline
pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16"
)
pipe.load_lora_weights("lora/80sFantasyMovieMJ7SDXL.safetensors")
pipe.to("cuda")

def generate_sdxl_prompt(panel):
    camera_view = panel.get("camera_view", "")
    setting = panel.get("setting", "")
    lighting = panel.get("lighting", "")
    mood = panel.get("mood", "")
    action = panel.get("action", "")

    objects = ", ".join(panel.get("objects", []))
    characters = ", ".join(panel.get("characters", []))

    prompt_parts = [
        camera_view, setting, lighting,
        f"{mood} mood" if mood else "",
        action, objects, characters,
        "comic book style, highly detailed, cinematic lighting"
    ]

    prompt = ", ".join([p for p in prompt_parts if p])

    negative_prompt = (
        "deformed, blurry, extra limbs, poorly drawn hands, extra fingers, "
        "mutated, out of frame, ugly, tiling, low resolution, bad anatomy, watermark"
    )

    return prompt.strip(), negative_prompt

def generate_images_from_script(comic_script):
    for i, panel in enumerate(comic_script):
        prompt, negative_prompt = generate_sdxl_prompt(panel)

        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,
            guidance_scale=7.5
        ).images[0]

        image.save(f"images/imagesWithoutText/panel_{i}.png")

        image_with_text = AddTextToImage.add_text_to_panel(panel["text"], image)
        image_with_text.save(f"images/imagesWithText/panel_{i}.png")

        if i == 5:
            return

if __name__ == "__main__":
    generate_images_from_script(comic_script)
