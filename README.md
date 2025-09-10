# LLM with Google Maps Integration

This project integrates a Local Language Model (LLM) with Google Maps API to provide location information and directions based on natural language queries. Users can ask questions about places to visit, eat, or get directions, and the application will display the relevant information on an embedded Google Map.

## Features

- Natural language processing for location and direction queries
- Google Maps integration for displaying locations and directions
- FastAPI backend with rate limiting and security best practices
- Responsive web interface

## Prerequisites

- Python 3.8 or higher
- Ollama (for running the local LLM)
- Google Cloud account with Maps API enabled

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Google Cloud account and set up Google Maps API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the following APIs:
   - Maps JavaScript API
   - Places API
   - Directions API
4. Create an API key with appropriate restrictions (HTTP referrers, IP addresses)
5. Copy the API key for later use

### 3. Set up environment variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit the `.env` file and add your Google Maps API key:

```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Ollama (in a separate terminal)

Make sure you have Ollama installed and running with a compatible model:

```bash
ollama run llama3
```

You can adjust the model in the `.env` file if you're using a different one.

### 6. Start the application

```bash
python -m app.main
```

The application will be available at http://localhost:8000

## Usage

1. Open the application in your web browser
2. Type natural language queries in the chat box, such as:
   - "Where can I find good pizza in New York?"
   - "Show me directions from Central Park to Times Square"
   - "What are some tourist attractions in Paris?"
3. The LLM will process your query and display relevant locations or directions on the map

## Integration with Open WebUI

This application can be integrated with [Open WebUI](https://github.com/open-webui/open-webui) for an enhanced user experience:

1. Install Open WebUI following their documentation
2. Configure Open WebUI to use your local Ollama instance
3. Add this application as a custom tool in Open WebUI

## Security Best Practices

- API key is stored in environment variables, not hardcoded
- Rate limiting is implemented to prevent abuse
- CORS is configured to restrict access to trusted origins
- API key restrictions are recommended (HTTP referrers, IP addresses)

## License

MIT