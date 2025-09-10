# Setting Up Ollama for Local LLM

This guide will help you install and configure Ollama to run a local Large Language Model (LLM) for the LLM with Google Maps Integration project.

## What is Ollama?

Ollama is an open-source tool that allows you to run large language models locally on your machine. It simplifies the process of downloading, setting up, and running various open-source LLMs.

## Installation Instructions

### macOS

1. Download the Ollama installer from the [official website](https://ollama.ai/download).
2. Open the downloaded file and follow the installation instructions.
3. Once installed, Ollama will run as a service in the background.

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows

1. Download the Ollama installer for Windows from the [official website](https://ollama.ai/download).
2. Run the installer and follow the instructions.

## Running a Model

After installing Ollama, you need to download and run a language model. For this project, we recommend using `llama3` or another model that has good performance with structured outputs.

1. Open a terminal or command prompt.
2. Run the following command to download and start the model:

```bash
ollama run llama3
```

The first time you run this command, Ollama will download the model, which may take some time depending on your internet connection. Subsequent runs will be much faster.

## Verifying the Installation

To verify that Ollama is running correctly:

1. Open a new terminal or command prompt.
2. Run the following command:

```bash
curl -X POST http://localhost:11434/api/generate -d '{"model":"llama3","prompt":"Hello, world!"}'
```

You should receive a response from the model.

## Configuring the Application to Use Ollama

The application is pre-configured to connect to Ollama running on the default host and port. If you need to change these settings:

1. Open the `.env` file in your project directory.
2. Modify the following settings as needed:

```
OLLAMA_HOST=http://localhost
OLLAMA_PORT=11434
OLLAMA_MODEL=llama3
```

## Using a Different Model

If you want to use a different model:

1. List available models:

```bash
ollama list
```

2. Pull a new model (for example, mistral):

```bash
ollama pull mistral
```

3. Update the `.env` file to use the new model:

```
OLLAMA_MODEL=mistral
```

## Troubleshooting

### Model Not Responding

If the model is not responding:

1. Check if Ollama is running:

```bash
ps aux | grep ollama
```

2. If not running, start Ollama:

```bash
ollama serve
```

### Slow Responses

If the model is responding slowly:

1. Consider using a smaller model like `llama3:7b` instead of a larger variant.
2. Ensure your computer meets the minimum requirements for running the model.

### Out of Memory Errors

If you encounter out of memory errors:

1. Try a smaller model.
2. Close other memory-intensive applications.
3. If available, increase the swap space on your system.

## Integration with Open WebUI

For an enhanced user experience, you can use Open WebUI with Ollama:

1. Clone the Open WebUI repository:

```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
```

2. Follow the installation instructions in the Open WebUI repository.
3. Configure Open WebUI to connect to your local Ollama instance.

## Resources

- [Ollama Official Documentation](https://github.com/ollama/ollama/blob/main/README.md)
- [Open WebUI GitHub Repository](https://github.com/open-webui/open-webui)