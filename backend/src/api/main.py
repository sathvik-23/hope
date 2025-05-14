from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List
import uvicorn

from src.agents.voice_agent import VoiceAgent
from src.config.config import Config

app = FastAPI(title="Voice Agent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize voice agent
agent = VoiceAgent()

@app.on_event("startup")
async def startup_event():
    await agent.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    await agent.cleanup()

@app.post("/process-audio")
async def process_audio(audio: UploadFile = File(...)):
    """Process uploaded audio file."""
    try:
        # Save uploaded file temporarily
        temp_path = os.path.join(Config.AUDIO_INPUT_PATH, audio.filename)
        with open(temp_path, "wb") as f:
            content = await audio.read()
            f.write(content)

        # Process the audio
        output_audio, response = await agent.process(temp_path)

        # Clean up temporary file
        os.remove(temp_path)

        if output_audio:
            return {
                "audioPath": output_audio,
                "text": response
            }
        else:
            return {"error": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/list-models")
async def list_models() -> List[str]:
    """List available models."""
    return [
        f"Whisper: {Config.WHISPER_MODEL}",
        f"Gemini: {Config.GEMINI_MODEL}"
    ]

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 