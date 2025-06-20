# voiceprint_manager.py — VoiceprintManager Module

import os
import hashlib
import wave
import pyaudio
from constants import VOICE_SAMPLE_FILE

class VoiceprintManager:
    def __init__(self, logger):
        self.logger = logger

    def record_voice_sample(self, filename=VOICE_SAMPLE_FILE, duration=3):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        self.logger.log("Recording voice sample...")
        for _ in range(0, int(44100 / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))
        self.logger.log(f"Voice sample saved to {filename}")

    def hash_voice_sample(self, filename=VOICE_SAMPLE_FILE):
        if not os.path.exists(filename):
            return None
        with wave.open(filename, 'rb') as wf:
            audio_data = wf.readframes(wf.getnframes())
            return hashlib.sha256(audio_data).hexdigest()

    def verify_voiceprint(self, directives):
        stored_hash = directives.get("voice_lock_hash", "")
        current_hash = self.hash_voice_sample()
        if not current_hash:
            self.logger.log("Voice sample not found.")
            return False
        if not stored_hash:
            self.logger.log("Voiceprint not yet enrolled. Storing current hash...")
            directives["voice_lock_hash"] = current_hash
            return True
        if stored_hash == current_hash:
            self.logger.log("Voiceprint verified. Access granted.")
            return True
        else:
            self.logger.log("Voice mismatch! ACCESS DENIED.")
            return False
