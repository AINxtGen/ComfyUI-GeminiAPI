# ComfyUI Gemini API Node

A custom node for ComfyUI that integrates Google's Gemini AI models for image analysis and description. This node allows you to send images to Gemini API and get AI-generated descriptions or analysis based on your prompts.

## Features

- Support for multiple Gemini models:
  - gemini-2.0-flash-exp
  - gemini-1.5-flash
  - gemini-1.5-pro
- Configurable safety filters
- Streaming response support
- Custom API key configuration
- Image to text generation

## Installation

1. Navigate to your ComfyUI custom nodes directory:
```
cd ComfyUI/custom_nodes/
```

2. Clone this repository:
```
git clone https://github.com/AINxtGen/ComfyUI-GeminiAPI.git
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Create a `config.json` file in the node directory with your Gemini API key:
```
{
"GEMINI_API_KEY": "your-api-key-here"
}
```


## Usage

1. Start ComfyUI
2. Find the "Gemini API" node under the "Gemini" category
3. Connect an image input to the node
4. Configure the following parameters:
   - `prompt`: Your text prompt for image analysis
   - `model_name`: Select the Gemini model to use
   - `api_key`: (Optional) Override the default API key
   - `stream`: Enable/disable response streaming
   - `safety_filter`: Enable/disable content safety filters


## Configuration

You can configure the API key in two ways:
1. Add it to `config.json` file
2. Input it directly in the node parameters
