from django.shortcuts import render
from dotenv import load_dotenv
import os
import openai
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Create your views here.
def home_view(request):
    template_name = "home.html"
    if request.method == "POST":
        prompt_prefix = "I want to generate a cover art for my song. Please do not put any text over the image. The description of the artwork I want is: "
        prompt = prompt_prefix + request.POST["prompt"]
        response = openai.Image.create(prompt=prompt, n=1, size="256x256")
        image_url = response["data"][0]["url"]
        return render(
            request,
            template_name,
            {"image_url": image_url, "prompt": request.POST["prompt"]},
        )
    else:
        return render(request, template_name, {"image_url": False})
