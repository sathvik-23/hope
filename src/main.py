import asyncio
import os
from src.agents.voice_agent import VoiceAgent
from src.config.config import AUDIO_INPUT_PATH

async def main():
    # Initialize the voice agent
    agent = VoiceAgent()
    await agent.initialize()

    try:
        # Example usage
        input_audio = os.path.join(AUDIO_INPUT_PATH, "input.wav")  # Replace with actual audio path
        output_audio, response = await agent.process(input_audio)
        
        if output_audio:
            print(f"Response audio saved to: {output_audio}")
            print(f"Response text: {response}")
        else:
            print("Processing failed")
    finally:
        # Clean up resources
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 