import os
import whisper
import google.generativeai as genai
import pymongo
from datetime import datetime
import soundfile as sf
import numpy as np
from dotenv import load_dotenv
from gtts import gTTS

# Load environment variables
load_dotenv()

class VoiceAgent:
    def __init__(self):
        # Initialize Whisper model
        self.whisper_model = whisper.load_model("base")
        
        # Initialize Gemini
        api_key = os.getenv("GEMINI_API_KEY", "your-api-key-here")
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Initialize MongoDB with default values
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        mongo_db = os.getenv("MONGODB_DB", "voice_agent")
        mongo_collection = os.getenv("MONGODB_COLLECTION", "interactions")
        
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.db = self.mongo_client[mongo_db]
        self.collection = self.db[mongo_collection]
        
        # Create audio directories if they don't exist
        input_path = os.getenv("AUDIO_INPUT_PATH", "./audio/input")
        output_path = os.getenv("AUDIO_OUTPUT_PATH", "./audio/output")
        
        os.makedirs(input_path, exist_ok=True)
        os.makedirs(output_path, exist_ok=True)

    def transcribe_audio(self, audio_path):
        """Transcribe audio using Whisper."""
        try:
            result = self.whisper_model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            print(f"Error in transcription: {str(e)}")
            return None

    def generate_response(self, text):
        """Generate response using Gemini."""
        try:
            response = self.gemini_model.generate_content(text)
            return response.text
        except Exception as e:
            print(f"Error in response generation: {str(e)}")
            return None

    def text_to_speech(self, text, output_path):
        """Convert text to speech using gTTS."""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save the audio file
            tts.save(output_path)
            
            return output_path
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            return None

    def save_interaction(self, user_input, response):
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

    def process_audio(self, input_audio_path):
        """Process audio through the complete pipeline."""
        # Generate output paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.getenv("AUDIO_OUTPUT_PATH", "./audio/output")
        output_audio_path = os.path.join(
            output_path,
            f"response_{timestamp}.mp3"
        )

        # 1. Transcribe audio
        transcription = self.transcribe_audio(input_audio_path)
        if not transcription:
            return None, "Transcription failed"

        # 2. Generate response
        response = self.generate_response(transcription)
        if not response:
            return None, "Response generation failed"

        # 3. Convert response to speech
        audio_output = self.text_to_speech(response, output_audio_path)
        if not audio_output:
            return None, "Text-to-speech conversion failed"

        # 4. Save interaction to MongoDB
        if not self.save_interaction(transcription, response):
            print("Warning: Failed to save interaction to MongoDB")

        return audio_output, response

def main():
    # Example usage
    agent = VoiceAgent()
    
    # Example audio processing
    input_audio = "path/to/your/audio.wav"  # Replace with actual audio path
    output_audio, response = agent.process_audio(input_audio)
    
    if output_audio:
        print(f"Response audio saved to: {output_audio}")
        print(f"Response text: {response}")
    else:
        print("Processing failed")

if __name__ == "__main__":
    main() 