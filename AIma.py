# Install required libraries
!pip install python-dotenv requests

# Import libraries
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv("sk-1234567890abcdef1234567890abcdef")
if not API_KEY:
    raise ValueError("Please set your STABILITY_API_KEY in the .env file.")

# Stability AI API endpoint
API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"

def generate_image(prompt, width=512, height=512, samples=1):
    """
    Generate an image using Stability AI's API.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "text_prompts": [{"text": prompt}],
        "width": width,
        "height": height,
        "samples": samples,
        "cfg_scale": 7,
        "steps": 30,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        # Save the generated images
        image_paths = []
        for i, image in enumerate(response.json()["artifacts"]):
            image_path = f"generated_image_{i + 1}.png"
            with open(image_path, "wb") as f:
                f.write(image["base64"])
            image_paths.append(image_path)
            print(f"Image saved to {image_path}")

        return image_paths

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Get user input for the image prompt
prompt = input("Enter a text prompt to generate an image: ")

# Generate the image
image_paths = generate_image(prompt)

if image_paths:
    print("Image generation successful!")
else:
    print("Image generation failed.")