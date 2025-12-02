from pathlib import Path
import openai
from dotenv import load_dotenv
import os


load_dotenv()

client = openai.OpenAI()

tts_model = "gpt-4o-mini-tts"
tts_voice = "alloy"

text_to_speak = "Hello! This is a test of my new text to speech engine."

outputfilename = "speech_output.mp3"

speech_filepath = Path(__file__).parent / outputfilename

print(f"Generating speech using model {tts_model} and voice {tts_voice}...")

with client.audio.speech.with_streaming_response.create(
    model=tts_model,
    voice=tts_voice,
    input=text_to_speak
    #instructions="Speak with a happy and energetic tone."
) as response:
    response.stream_to_file(speech_filepath)
print(f"Speech saved to {speech_filepath}")


