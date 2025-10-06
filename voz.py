import wave
from piper import PiperVoice

voice = PiperVoice.load("pt_BR-faber-medium.onnx")
with wave.open("test.wav", "wb") as wav_file:
    voice.synthesize_wav("sejam todos bem vindos", wav_file)