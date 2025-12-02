import soundfile as sf

from kokoro_onnx import Kokoro

kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
samples, sample_rate = kokoro.create(
    "Hey, what are you up to today.         hey", voice="bf_emma", speed=0.7, lang="en-us"
)
sf.write("audio.wav", samples, sample_rate)
print("Created audio.wav")