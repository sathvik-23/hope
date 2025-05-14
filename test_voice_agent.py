import os
from voice_agent import VoiceAgent

REAL_AUDIO_PATH = "/Users/sathvik/Project/hope/Piper-tts/outputs/output.wav"

def main():
    # Use the provided real audio file
    test_audio_path = REAL_AUDIO_PATH
    print(f"Using real audio file at: {test_audio_path}")
    
    # Initialize voice agent
    agent = VoiceAgent()
    
    # Process the real audio
    print("Processing audio...")
    output_audio, response = agent.process_audio(test_audio_path)
    
    if output_audio:
        print(f"Success! Response audio saved to: {output_audio}")
        print(f"Response text: {response}")
    else:
        print("Processing failed")

if __name__ == "__main__":
    main() 