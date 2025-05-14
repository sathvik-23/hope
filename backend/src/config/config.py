import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class Config:
    # MongoDB Configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "voice_agent")
    MONGODB_COLLECTION: str = os.getenv("MONGODB_COLLECTION", "interactions")

    # API Keys
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    # Audio Configuration
    AUDIO_INPUT_PATH: str = os.getenv("AUDIO_INPUT_PATH", "./audio/input")
    AUDIO_OUTPUT_PATH: str = os.getenv("AUDIO_OUTPUT_PATH", "./audio/output")

    # Model Configuration
    WHISPER_MODEL: str = "base"
    GEMINI_MODEL: str = "models/gemini-1.5-flash"

    @classmethod
    def validate(cls) -> None:
        """Validate the configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Please set it in your .env file.")

        # Create necessary directories
        try:
            os.makedirs(cls.AUDIO_INPUT_PATH, exist_ok=True)
            os.makedirs(cls.AUDIO_OUTPUT_PATH, exist_ok=True)
            logger.info(f"Created audio directories: {cls.AUDIO_INPUT_PATH}, {cls.AUDIO_OUTPUT_PATH}")
        except Exception as e:
            logger.error(f"Failed to create audio directories: {str(e)}")
            raise

    @classmethod
    def get_mongodb_uri(cls) -> str:
        """Get MongoDB URI with validation."""
        if not cls.MONGODB_URI:
            raise ValueError("MONGODB_URI is required")
        return cls.MONGODB_URI

    @classmethod
    def get_gemini_api_key(cls) -> str:
        """Get Gemini API key with validation."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        return cls.GEMINI_API_KEY 