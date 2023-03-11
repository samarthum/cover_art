from django.shortcuts import render
from dotenv import load_dotenv
import os
import replicate
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

model = replicate.models.get("stability-ai/stable-diffusion")
version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

inputs = {
    # Input prompt
    'prompt': "a vision of paradise. unreal engine",

    # pixel dimensions of output image
    'image_dimensions': "512x512",

    # Specify things to not see in the output
    'negative_prompt': "text, words, letters",

    # Number of images to output.
    # Range: 1 to 4
    'num_outputs': 1,

    # Number of denoising steps
    # Range: 1 to 500
    'num_inference_steps': 50,

    # Scale for classifier-free guidance
    # Range: 1 to 20
    'guidance_scale': 7.5,

    # Choose a scheduler.
    'scheduler': "DPMSolverMultistep",
}


# Create your views here.
def home_view(request):
    template_name = "home.html"
    if request.method == "POST":
        prompt_prefix = "Create a cover art for a song. Please do not put any text over the image. The description of the artwork is: "

        inputs["prompt"] = prompt_prefix + request.POST["prompt"]
        image_url = version.predict(**inputs)[0]
        context = {"image_url": image_url, "prompt": request.POST["prompt"]}
        return render(
            request,
            template_name,
            context=context,
        )
    else:
        return render(request, template_name, {"image_url": False})
