from django.shortcuts import render
from dotenv import load_dotenv
import os
import replicate
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

model = replicate.models.get("stability-ai/stable-diffusion")
version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

NEGATIVE_PROMPTS = """text, letters, words, numbers, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face"""
inputs = {
    # Input prompt
    'prompt': "a vision of paradise. unreal engine",

    # pixel dimensions of output image
    'image_dimensions': "512x512",

    # Specify things to not see in the output
    'negative_prompt': NEGATIVE_PROMPTS,

    # Number of images to output.
    # Range: 1 to 4
    'num_outputs': 1,

    # Number of denoising steps
    # Range: 1 to 500
    'num_inference_steps': 100,

    # Scale for classifier-free guidance
    # Range: 1 to 20
    'guidance_scale': 10,

    # Choose a scheduler.
    'scheduler': "K_EULER",
}


# Create your views here.
def home_view(request):
    template_name = "home.html"
    if request.method == "POST":
        prompt_prefix = "Create a cover art for a song. Please do not put any text over the image. The description of the artwork is: "

        inputs["prompt"] = request.POST["prompt"]
        image_url = version.predict(**inputs)[0]
        context = {"image_url": image_url, "prompt": request.POST["prompt"]}
        return render(
            request,
            template_name,
            context=context,
        )
    else:
        return render(request, template_name, {"image_url": False})
