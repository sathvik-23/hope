# Voice Agent with Agno Framework

A voice-based conversational agent built using the Agno agentic framework. This project implements a voice agent that can transcribe speech, generate responses using Google's Gemini model, and convert responses back to speech.

## Features

- Speech-to-text transcription using OpenAI's Whisper
- Natural language processing using Google's Gemini model
- Text-to-speech conversion using gTTS
- Interaction history storage in MongoDB
- Asynchronous processing using Agno framework

## Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── agents/
│   │   │   └── voice_agent.py
│   │   ├── core/
│   │   │   └── base_agent.py
│   │   ├── config/
│   │   │   └── config.py
│   │   └── main.py
│   ├── tests/
│   ├── audio/
│   │   ├── input/
│   │   └── output/
│   └── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory with the following variables:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   MONGODB_URI=your_mongodb_uri
   MONGODB_DB=voice_agent
   MONGODB_COLLECTION=interactions
   ```

## Usage

1. Place your input audio file in the `backend/audio/input` directory
2. Run the main script:
   ```bash
   cd backend
   python src/main.py
   ```
3. The processed audio response will be saved in the `backend/audio/output` directory

## Development

- The project uses the Agno framework for agent-based development
- All agents inherit from the base `BaseAgent` class
- Configuration is managed through environment variables and the config module
- Asynchronous processing is used throughout the application

## Testing

Run tests using pytest:

```bash
cd backend
pytest tests/
```

## License

MIT License
