import os
import whisper
import google.generativeai as genai
import pymongo
from datetime import datetime
from gtts import gTTS
from typing import Tuple, Optional

from src.core.base_agent import BaseAgent
from src.config.config import (
    MONGODB_URI,
    MONGODB_DB,
    MONGODB_COLLECTION,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    WHISPER_MODEL,
    AUDIO_OUTPUT_PATH
)

class VoiceAgent(BaseAgent):
    async def initialize(self) -> None:
        """Initialize the voice agent with necessary models and connections."""
        # Initialize Whisper model
        self.whisper_model = whisper.load_model(WHISPER_MODEL)
        
        # Initialize Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Initialize MongoDB
        self.mongo_client = pymongo.MongoClient(MONGODB_URI)
        self.db = self.mongo_client[MONGODB_DB]
        self.collection = self.db[MONGODB_COLLECTION]

    async def process(self, input_audio_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Process audio through the complete pipeline."""
        try:
            # 1. Transcribe audio
            transcription = await self.transcribe_audio(input_audio_path)
            if not transcription:
                return None, "Transcription failed"

            # 2. Generate response
            response = await self.generate_response(transcription)
            if not response:
                return None, "Response generation failed"

            # 3. Convert response to speech
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_audio_path = os.path.join(
                AUDIO_OUTPUT_PATH,
                f"response_{timestamp}.mp3"
            )
            audio_output = await self.text_to_speech(response, output_audio_path)
            if not audio_output:
                return None, "Text-to-speech conversion failed"

            # 4. Save interaction to MongoDB
            await self.save_interaction(transcription, response)

            return audio_output, response
        except Exception as e:
            print(f"Error in processing: {str(e)}")
            return None, str(e)

    async def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Transcribe audio using Whisper."""
        try:
            result = self.whisper_model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            print(f"Error in transcription: {str(e)}")
            return None

    async def generate_response(self, text: str) -> Optional[str]:
        """Generate response using Gemini."""
        try:
            response = self.gemini_model.generate_content(text)
            return response.text
        except Exception as e:
            print(f"Error in response generation: {str(e)}")
            return None

    async def text_to_speech(self, text: str, output_path: str) -> Optional[str]:
        """Convert text to speech using gTTS."""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
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
            print(f"Error saving to MongoDB: {str(e)}")
            return False

    async def cleanup(self) -> None:
        """Clean up resources."""
        if hasattr(self, 'mongo_client'):
            self.mongo_client.close() 