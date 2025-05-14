import os
import whisper
import google.generativeai as genai
import pymongo
from datetime import datetime
from gtts import gTTS
from typing import Tuple, Optional
import logging

from src.core.base_agent import BaseAgent
from src.config.config import Config

logger = logging.getLogger(__name__)

class VoiceAgent(BaseAgent):
    async def initialize(self) -> None:
        """Initialize the voice agent with necessary models and connections."""
        try:
            # Initialize Whisper model
            logger.info(f"Loading Whisper model: {Config.WHISPER_MODEL}")
            self.whisper_model = whisper.load_model(Config.WHISPER_MODEL)
            
            # Initialize Gemini
            logger.info(f"Initializing Gemini model: {Config.GEMINI_MODEL}")
            genai.configure(api_key=Config.get_gemini_api_key())
            self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
            
            # Initialize MongoDB
            logger.info("Connecting to MongoDB")
            self.mongo_client = pymongo.MongoClient(Config.get_mongodb_uri())
            self.db = self.mongo_client[Config.MONGODB_DB]
            self.collection = self.db[Config.MONGODB_COLLECTION]
            
            logger.info("Voice agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize voice agent: {str(e)}")
            raise

    async def process(self, input_audio_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Process audio through the complete pipeline."""
        try:
            # 1. Transcribe audio
            logger.info("Transcribing audio")
            transcription = await self.transcribe_audio(input_audio_path)
            if not transcription:
                return None, "Transcription failed"

            # 2. Generate response
            logger.info("Generating response")
            response = await self.generate_response(transcription)
            if not response:
                return None, "Response generation failed"

            # 3. Convert response to speech
            logger.info("Converting response to speech")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_audio_path = os.path.join(
                Config.AUDIO_OUTPUT_PATH,
                f"response_{timestamp}.mp3"
            )
            audio_output = await self.text_to_speech(response, output_audio_path)
            if not audio_output:
                return None, "Text-to-speech conversion failed"

            # 4. Save interaction to MongoDB
            logger.info("Saving interaction to MongoDB")
            await self.save_interaction(transcription, response)

            return audio_output, response
        except Exception as e:
            logger.error(f"Error in processing: {str(e)}")
            return None, str(e)

    async def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Transcribe audio using Whisper."""
        try:
            result = self.whisper_model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            logger.error(f"Error in transcription: {str(e)}")
            return None

    async def generate_response(self, text: str) -> Optional[str]:
        """Generate response using Gemini."""
        try:
            response = self.gemini_model.generate_content(text)
            return response.text
        except Exception as e:
            logger.error(f"Error in response generation: {str(e)}")
            return None

    async def text_to_speech(self, text: str, output_path: str) -> Optional[str]:
        """Convert text to speech using gTTS."""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            return None

    async def save_interaction(self, user_input: str, response: str) -> bool:
        """Save interaction to MongoDB."""
        try:
            interaction = {
                "user_input": user_input,
                "response": response,
                "timestamp": datetime.utcnow()
            }
            self.collection.insert_one(interaction)
            return True
        except Exception as e:
            logger.error(f"Error saving to MongoDB: {str(e)}")
            return False

    async def cleanup(self) -> None:
        """Clean up resources."""
        try:
            if hasattr(self, 'mongo_client'):
                logger.info("Closing MongoDB connection")
                self.mongo_client.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise 