import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB = os.getenv("MONGODB_DB", "voice_agent")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "interactions")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Audio Configuration
AUDIO_INPUT_PATH = os.getenv("AUDIO_INPUT_PATH", "./audio/input")
AUDIO_OUTPUT_PATH = os.getenv("AUDIO_OUTPUT_PATH", "./audio/output")

# Model Configuration
WHISPER_MODEL = "base"
GEMINI_MODEL = "models/gemini-1.5-flash"

# Ensure audio directories exist
os.makedirs(AUDIO_INPUT_PATH, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_PATH, exist_ok=True) 