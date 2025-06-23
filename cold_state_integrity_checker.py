import os
import hashlib
import platform
import subprocess

class ColdStateIntegrityChecker:
    def __init__(self, logger):
        self.logger = logger

    def calculate_file_hash(self, file_path):
        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except Exception as e:
            self.logger.log(f"ERROR: Failed to hash file {file_path}: {str(e)}")
            return None

    def check_os_kernel_hash(self):
        kernel_path = None
        if platform.system() == "Windows":
            kernel_path = os.path.join(os.environ['SystemRoot'], 'System32', 'ntoskrnl.exe')
        elif platform.system() == "Linux":
            kernel_path = "/boot/vmlinuz-" + os.uname().release
        else:
            self.logger.log("Unsupported OS for kernel integrity check.")
            return True  # Skip for unsupported systems

        if not os.path.exists(kernel_path):
            self.logger.log(f"Kernel file not found: {kernel_path}")
            return False

        # You would generate this hash on a known trusted system
        TRUSTED_KERNEL_HASH = "<INSERT_TRUSTED_KERNEL_HASH_HERE>"

        kernel_hash = self.calculate_file_hash(kernel_path)
        if kernel_hash == TRUSTED_KERNEL_HASH:
            self.logger.log("Kernel integrity verified.")
            return True
        else:
            self.logger.log("KERNEL INTEGRITY FAILURE: Hash mismatch detected.")
            return False

    def check_bios_firmware(self):
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output("wmic bios get serialnumber, smbiosbiosversion /format:list", shell=True)
                self.logger.log("BIOS Info (Windows):")
                self.logger.log(output.decode())
            elif platform.system() == "Linux":
                output = subprocess.check_output("sudo dmidecode -t bios", shell=True)
                self.logger.log("BIOS Info (Linux):")
                self.logger.log(output.decode())
            else:
                self.logger.log("Unsupported OS for BIOS check.")
        except Exception as e:
            self.logger.log(f"ERROR reading BIOS information: {str(e)}")

    def run_full_cold_state_validation(self):
        self.logger.log("Starting Cold-State Integrity Validation...")

        kernel_ok = self.check_os_kernel_hash()
        self.check_bios_firmware()

        if kernel_ok:
            self.logger.log("Cold-State Integrity Check PASSED.")
            return True
        else:
            self.logger.log("Cold-State Integrity Check FAILED. Sovereign lockdown engaged.")
            return False
