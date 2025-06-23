import requests
import time
import json
import threading

class SecureExternalInterface:
    def __init__(self, logger, command_auth_chain):
        self.logger = logger
        self.command_auth_chain = command_auth_chain
        self.active_session = False
        self.session_timeout = 0
        self.external_data_buffer = []

    def start_external_session(self, session_duration_seconds):
        if self.active_session:
            self.logger.log("An external interface session is already active.")
            return False

        self.logger.log("Starting Secure External Interface Session...")
        self.active_session = True
        self.session_timeout = time.time() + session_duration_seconds
        threading.Thread(target=self.monitor_session_timer).start()
        return True

    def monitor_session_timer(self):
        while self.active_session:
            if time.time() > self.session_timeout:
                self.logger.log("Secure External Interface Session timed out.")
                self.active_session = False
                break
            time.sleep(1)

    def request_external_data(self, url, provided_voiceprint, authorized_voiceprint, provided_checksum, provided_token):
        if not self.active_session:
            self.logger.log("NO ACTIVE SESSION: External interface request denied.")
            return None

        if not self.command_auth_chain.full_command_validation(
                url, provided_voiceprint, authorized_voiceprint, provided_checksum, provided_token):
            self.logger.log("External request blocked by command authentication chain.")
            return None

        try:
            self.logger.log(f"Fetching data from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            content = response.text
            self.logger.log(f"Data retrieved successfully from: {url}")
            self.external_data_buffer.append({'url': url, 'content': content, 'timestamp': time.time()})
            return content
        except Exception as e:
            self.logger.log(f"External data retrieval failed: {str(e)}")
            return None

    def export_session_log(self, filename="external_session_log.json"):
        with open(filename, 'w') as f:
            json.dump(self.external_data_buffer, f, indent=4)
        self.logger.log(f"External interface session log exported to: {filename}")

    def terminate_external_session(self):
        if self.active_session:
            self.logger.log("Secure External Interface Session manually terminated by Commander.")
            self.active_session = False
        else:
            self.logger.log("No active external session to terminate.")
