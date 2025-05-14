# Voice Agent Project

This project implements a voice agent that can:

1. Convert speech to text using Whisper
2. Generate responses using Google's Gemini LLM
3. Convert text responses to speech using gTTS
4. Store all interactions in MongoDB

## Prerequisites

- Python 3.8 or higher
- MongoDB installed and running
- Google Gemini API key
- FFmpeg (required for Whisper)

## Project Structure

```
hope/
├── venv/                      # Main project virtual environment
├── requirements.txt           # Main project dependencies
├── .env                      # Environment variables (not committed)
├── Piper-tts/
│   ├── venv/                  # Piper-tts virtual environment
│   └── requirements.txt       # Piper-tts dependencies
├── whisper/
│   ├── venv/                  # Whisper virtual environment
│   └── requirements.txt       # Whisper dependencies
├── audio/
│   ├── input/                 # Input audio files
│   └── output/                # Generated audio responses
├── voice_agent.py             # Main implementation
├── test_voice_agent.py        # Test script
└── README.md                  # This file
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd hope
```

### 2. Set up the main project virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up the Piper-tts virtual environment (if needed)

```bash
cd Piper-tts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

### 4. Set up the Whisper virtual environment (if needed)

```bash
cd whisper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

### 5. Set up your environment variables

Copy the example and edit it:

```bash
cp .env.example .env
```

Edit `.env` and add your:

- MongoDB connection string
- Gemini API key (as `GEMINI_API_KEY`)
- Audio input/output paths if needed

### 6. Ensure MongoDB is running

Start MongoDB if it is not already running:

```bash
brew services start mongodb-community  # macOS (Homebrew)
# or use your OS-specific method
```

### 7. Run the voice agent

```bash
source venv/bin/activate
python test_voice_agent.py
```

## Notes

- The main project uses the main `venv` and `requirements.txt`.
- Piper-tts and Whisper subfolders have their own `venv` and `requirements.txt` if you want to run or develop them independently.
- The `.env` file is required for API keys and configuration.
- All virtual environments and `.env` are excluded from git by `.gitignore`.

## Contributing

Feel free to submit issues and enhancement requests!
