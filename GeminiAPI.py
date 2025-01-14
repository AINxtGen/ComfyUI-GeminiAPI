import os
import json
import google.generativeai as genai
from PIL import Image
import torch
from google.generativeai.types import HarmCategory, HarmBlockThreshold

p = os.path.dirname(os.path.realpath(__file__))

def get_gemini_api_key():
    try:
        config_path = os.path.join(p, 'config.json')
        with open(config_path, 'r') as f:  
            config = json.load(f)
        api_key = config["GEMINI_API_KEY"]
    except:
        print("Error: API key is required")
        return ""
    return api_key

class GeminiAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key is not None:
            genai.configure(api_key=self.api_key, transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"default": "Describe this image", "multiline": True}),
                "model_name": (["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],),
                "api_key": ("STRING", {"default": ""}),
                "stream": ("BOOLEAN", {"default": False}),
                "safety_filter": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"
    CATEGORY = "Gemini"

    def tensor_to_image(self, tensor):
        tensor = tensor.cpu()
        image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
        image = Image.fromarray(image_np, mode='RGB')
        return image

    def generate_content(self, image, prompt, model_name, api_key, stream, safety_filter):
        # Handle API key
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=self.api_key, transport='rest')
        elif not self.api_key:
            self.api_key = get_gemini_api_key()
            if not self.api_key:
                raise ValueError("API key is required")
            genai.configure(api_key=self.api_key, transport='rest')

        # Convert tensor to PIL image
        pil_image = self.tensor_to_image(image)

        # Initialize model
        model = genai.GenerativeModel(model_name)

        # Set safety settings based on safety_filter
        if not safety_filter:
            # Disable all safety filters
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            }
        else:
            # Use default safety settings (BLOCK_MEDIUM_AND_ABOVE)
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            }

        # Generate content with safety settings
        if stream:
            response = model.generate_content(
                [prompt, pil_image], 
                stream=True,
                safety_settings=safety_settings
            )
            text_output = "\n".join([chunk.text for chunk in response])
        else:
            response = model.generate_content(
                [prompt, pil_image],
                safety_settings=safety_settings
            )
            text_output = response.text

        return (text_output,)

NODE_CLASS_MAPPINGS = {
    "GeminiAPI": GeminiAPI
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiAPI": "Gemini API"
} 