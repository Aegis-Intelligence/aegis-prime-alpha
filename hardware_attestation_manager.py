import platform
import subprocess
import hashlib
import json
import os

class HardwareAttestationManager:
    def __init__(self, logger, trust_file="trusted_hardware_fingerprint.json"):
        self.logger = logger
        self.trust_file = trust_file
        self.trusted_fingerprint = {}

        if not os.path.exists(self.trust_file):
            self.logger.log("No trusted hardware fingerprint found. Generating initial trusted hardware fingerprint.")
            self.generate_trusted_fingerprint()
        else:
            self.load_trusted_fingerprint()

    def get_hardware_snapshot(self):
        system_info = {}

        try:
            if platform.system() == "Windows":
                bios_info = subprocess.check_output("wmic bios get serialnumber, smbiosbiosversion", shell=True).decode()
                board_info = subprocess.check_output("wmic baseboard get product, serialnumber", shell=True).decode()
                cpu_info = subprocess.check_output("wmic cpu get processorid", shell=True).decode()
                system_info['bios'] = bios_info.strip()
                system_info['baseboard'] = board_info.strip()
                system_info['cpu'] = cpu_info.strip()
            elif platform.system() == "Linux":
                bios_info = subprocess.check_output("sudo dmidecode -t bios", shell=True).decode()
                board_info = subprocess.check_output("sudo dmidecode -t baseboard", shell=True).decode()
                cpu_info = subprocess.check_output("lscpu", shell=True).decode()
                system_info['bios'] = bios_info.strip()
                system_info['baseboard'] = board_info.strip()
                system_info['cpu'] = cpu_info.strip()
            else:
                self.logger.log("Unsupported OS for hardware attestation.")
        except Exception as e:
            self.logger.log(f"ERROR retrieving hardware information: {str(e)}")

        return system_info

    def calculate_fingerprint_hash(self, hardware_snapshot):
        hasher = hashlib.sha256()
        combined_data = json.dumps(hardware_snapshot, sort_keys=True).encode('utf-8')
        hasher.update(combined_data)
        return hasher.hexdigest()

    def generate_trusted_fingerprint(self):
        snapshot = self.get_hardware_snapshot()
        fingerprint = self.calculate_fingerprint_hash(snapshot)
        self.trusted_fingerprint = {'hash': fingerprint}
        with open(self.trust_file, 'w') as f:
            json.dump(self.trusted_fingerprint, f, indent=4)
        self.logger.log("Trusted hardware fingerprint generated and stored.")

    def load_trusted_fingerprint(self):
        with open(self.trust_file, 'r') as f:
            self.trusted_fingerprint = json._
