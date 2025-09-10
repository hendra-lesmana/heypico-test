# Integrating with Open WebUI

This guide explains how to integrate the LLM with Google Maps application with [Open WebUI](https://github.com/open-webui/open-webui), an extensible, feature-rich, and user-friendly self-hosted AI platform.

## What is Open WebUI?

Open WebUI is a user-friendly interface for interacting with local LLMs like Ollama. It provides a chat interface, model management, and other features that enhance the experience of using local language models.

## Installation Options

### Option 1: Docker (Recommended)

1. Install Docker if you haven't already.
2. Run the following command to start Open WebUI:

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

3. Access Open WebUI at http://localhost:3000

### Option 2: Manual Installation

1. Clone the Open WebUI repository:

```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
```

2. Follow the installation instructions in the repository's README.md file.

## Configuring Open WebUI to Use Ollama

1. Open Open WebUI in your browser (http://localhost:3000).
2. Go to Settings > LLM Providers.
3. Select Ollama as the provider.
4. Set the Ollama API URL to `http://localhost:11434` (or the appropriate URL if running on a different host).
5. Save the settings.

## Creating a Custom Tool for Google Maps Integration

Open WebUI supports custom tools through its plugin system. Here's how to create a tool for our Google Maps integration:

### Method 1: Using Function Calling

1. In Open WebUI, go to Settings > Tools.
2. Click "Add Tool".
3. Configure a new tool with the following settings:
   - Name: `GoogleMaps`
   - Description: `Search for locations and get directions using Google Maps`
   - API Endpoint: `http://localhost:8000/api/llm`
   - Method: `POST`
   - Parameters:
     ```json
     {
       "prompt": "{{input}}"
     }
     ```

4. Save the tool.

### Method 2: Using iframes for Map Display

To display maps directly in Open WebUI:

1. Make sure your FastAPI server is running: `python -m app.main`
2. In Open WebUI, when you want to show a map, use the following markdown:

```markdown
<iframe src="http://localhost:8000/?query=YOUR_QUERY_HERE" width="100%" height="500px"></iframe>
```

Replace `YOUR_QUERY_HERE` with the encoded query string.

## Using the Integration

1. Start a chat in Open WebUI.
2. Ask a question about locations or directions, such as:
   - "Where can I find coffee shops in Seattle?"
   - "Show me directions from the Empire State Building to Central Park"
3. The LLM will process your query and either:
   - Use function calling to invoke your custom tool
   - Provide a response with an iframe link to display the map

## Troubleshooting

### Maps Not Displaying

If maps are not displaying in Open WebUI:

1. Ensure your FastAPI server is running.
2. Check that the URL in the iframe is correct.
3. Verify that CORS is properly configured in your FastAPI application.

### Function Calling Issues

If the custom tool is not being invoked:

1. Make sure your LLM model supports function calling (e.g., llama3 or GPT-4).
2. Check that the tool is properly configured in Open WebUI.
3. Verify that your FastAPI server is accessible from Open WebUI.

## Advanced: Creating a Custom Plugin

For a more integrated experience, you can create a custom plugin for Open WebUI:

1. Follow the plugin development guide in the Open WebUI documentation.
2. Create a plugin that directly interfaces with your Google Maps integration API.
3. Package and install the plugin in your Open WebUI installation.

This approach requires more development work but provides a more seamless integration.