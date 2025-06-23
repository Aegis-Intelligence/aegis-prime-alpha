import hashlib
import hmac
import time
import getpass

class CommandAuthenticationChain:
    def __init__(self, logger, secret_key):
        self.logger = logger
        self.secret_key = secret_key  # Cryptographic shared key (Commander controlled)
        self.last_command_hash = None

    def verify_voiceprint(self, provided_voiceprint, authorized_voiceprint):
        if provided_voiceprint == authorized_voiceprint:
            self.logger.log("Voiceprint authentication passed.")
            return True
        else:
            self.logger.log("Voiceprint authentication FAILED.")
            return False

    def generate_command_checksum(self, command_text):
        checksum = hashlib.sha256(command_text.encode('utf-8')).hexdigest()
        self.logger.log(f"Generated command checksum: {checksum}")
        return checksum

    def verify_checksum_integrity(self, provided_checksum, command_text):
        expected_checksum = self.generate_command_checksum(command_text)
        if provided_checksum == expected_checksum:
            self.logger.log("Command checksum integrity verified.")
            return True
        else:
            self.logger.log("Command checksum mismatch detected.")
            return False

    def verify_cryptographic_token(self, provided_token, command_text):
        expected_token = hmac.new(self.secret_key.encode('utf-8'),
                                   command_text.encode('utf-8'),
                                   hashlib.sha256).hexdigest()
        if provided_token == expected_token:
            self.logger.log("Cryptographic token verified.")
            return True
        else:
            self.logger.log("Cryptographic token verification FAILED.")
            return False

    def full_command_validation(self, command_text, provided_voiceprint, authorized_voiceprint, provided_checksum, provided_token):
        self.logger.log("Beginning full sovereign command authentication chain...")

        if not self.verify_voiceprint(provided_voiceprint, authorized_voiceprint):
            return False

        if not self.verify_checksum_integrity(provided_checksum, command_text):
            return False

        if not self.verify_cryptographic_token(provided_token, command_text):
            return False

        self.logger.log("Full command authentication chain PASSED.")
        self.last_command_hash = self.generate_command_checksum(command_text)
        return True

    def request_command_entry(self):
        self.logger.log("Awaiting Sovereign Command Input...")
        command_text = input("Enter command text: ")
        provided_voiceprint = getpass.getpass("Enter authorized voiceprint code: ")
        provided_checksum = input("Enter provided checksum: ")
        provided_token = getpass.getpass("Enter cryptographic token: ")

        authorized_voiceprint = "YOUR_VOICEPRINT_SECRET"  # Commander preset
        success = self.full_command_validation(command_text, provided_voiceprint, authorized_voiceprint, provided_checksum, provided_token)

        if success:
            self.logger.log(f"Sovereign Command Authorized: {command_text}")
        else:
            self.logger.log("SOVEREIGN COMMAND AUTHENTICATION FAILED.")
