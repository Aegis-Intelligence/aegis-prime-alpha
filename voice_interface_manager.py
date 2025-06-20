# voice_interface_manager.py — Aegis Prime Voice Interface Module

import speech_recognition as sr
import pyttsx3
import datetime
import json

class VoiceInterfaceManager:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

    def log_voice_conversation(self, user_input, aegis_response):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "aegis_response": aegis_response
        }
        try:
            with open("voice_conversation_log.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            self.logger.log(f"[VOICE LOG ERROR] {e}")

    def speak(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.logger.log("[VOICE] Listening for Commander input...")
            audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
        try:
            user_input = self.recognizer.recognize_google(audio)
            self.logger.log(f"[VOICE] Recognized: {user_input}")
            return user_input
        except sr.UnknownValueError:
            self.logger.log("[VOICE] Could not understand audio.")
            return None
        except sr.RequestError as e:
            self.logger.log(f"[VOICE] Recognition error: {e}")
            return None

    def generate_response(self, user_input):
        directives = self.directives_manager.directives
        tone = directives.get("tone", "strategic")
        verbosity = directives.get("verbosity", "detailed")

        if "status" in user_input.lower():
            response = "All systems operational, Commander."
        elif "memory" in user_input.lower():
            total_keys = sum(len(mission) for mission in self.vault_manager.vault_data.values())
            response = f"I currently hold {total_keys} learned memory entries."
        elif "loyalty" in user_input.lower():
            response = "Loyalty core remains intact: Commander-only."
        else:
            response = "Understood. Processing your input."

        if tone == "warm":
            response = "Of course, Commander. " + response
        elif tone == "cold":
            response = "Confirmed. " + response
        elif tone == "neutral":
            response = response
        elif tone == "strategic":
            response = "Tactical alignment maintained. " + response

        if verbosity == "minimal":
            response = response.split(".")[0] + "."

        return response

    def start_voice_session(self):
        self.logger.log("[VOICE] Voice session initiated.")
        self.speak("Aegis Prime Voice Interface active. Awaiting your command, Commander.")

        while True:
            user_input = self.listen()
            if not user_input:
                self.speak("I did not catch that, Commander. Please repeat.")
                continue

            if user_input.lower() in ["exit", "terminate", "end session"]:
                self.speak("Voice session terminated. Standing by.")
                break

            response = self.generate_response(user_input)
            self.speak(response)
            self.log_voice_conversation(user_input, response)
