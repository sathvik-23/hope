import asyncio
import os
import sys
import logging
import argparse
from typing import Optional, Tuple

from src.agents.voice_agent import VoiceAgent
from src.config.config import Config

# Configure logging
logger = logging.getLogger(__name__)

async def process_audio(agent: VoiceAgent, input_audio: str) -> Tuple[Optional[str], Optional[str]]:
    """Process audio file using the voice agent."""
    try:
        if not os.path.exists(input_audio):
            logger.error(f"Audio file not found: {input_audio}")
            return None, f"Audio file not found: {input_audio}"

        logger.info(f"Processing audio file: {input_audio}")
        output_audio, response = await agent.process(input_audio)
        
        if output_audio:
            logger.info(f"Response audio saved to: {output_audio}")
            logger.info(f"Response text: {response}")
            return output_audio, response
        else:
            logger.error("Processing failed")
            return None, "Processing failed"
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        return None, str(e)

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Voice Agent CLI")
    parser.add_argument("input_audio", nargs="?", help="Path to input audio file")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    args = parser.parse_args()

    try:
        # Validate configuration
        Config.validate()

        # Initialize the voice agent
        agent = VoiceAgent()
        await agent.initialize()

        if args.list_models:
            # TODO: Implement model listing
            print("Available models:")
            print("- Whisper: base")
            print("- Gemini: models/gemini-1.5-flash")
            return

        if not args.input_audio:
            parser.print_help()
            return

        # Process the audio file
        output_audio, response = await process_audio(agent, args.input_audio)
        
        if output_audio:
            print(f"\nResponse audio saved to: {output_audio}")
            print(f"Response text: {response}")
        else:
            print(f"\nProcessing failed: {response}")
            sys.exit(1)

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up resources
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 