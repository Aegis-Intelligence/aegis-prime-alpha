# encryption.py — VaultEncryption Module

import base64
import hashlib
import json
from cryptography.fernet import Fernet

class VaultEncryption:
    def __init__(self, master_password):
        self.key = self._generate_key(master_password)
        self.cipher = Fernet(self.key)

    def _generate_key(self, master_password):
        digest = hashlib.sha256(master_password.encode()).digest()
        return base64.urlsafe_b64encode(digest)

    def encrypt(self, data_dict):
        data_str = json.dumps(data_dict)
        return self.cipher.encrypt(data_str.encode())

    def decrypt(self, token):
        decrypted = self.cipher.decrypt(token)
        return json.loads(decrypted.decode())
