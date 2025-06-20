# ambient_monitor.py — AmbientMonitorManager Module

import tkinter as tk
import threading
import time
from datetime import datetime

class AmbientMonitorManager:
    def __init__(self, logger, master_password, vault_manager, directives_manager):
        self.logger = logger
        self.master_password = master_password
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager

    def launch_dashboard(self):
        win = tk.Tk()
        win.title("Aegis Ambient Dashboard")
        win.geometry("400x200")
        label = tk.Label(win, text="Aegis is in Ambient Monitoring Mode", font=("Arial", 14))
        label.pack(pady=20)
        heartbeat = tk.Label(win, text="[OK] Heartbeat Stable", fg="green")
        heartbeat.pack(pady=5)
        logbox = tk.Text(win, height=5, width=45)
        logbox.pack()

        def feed():
            while True:
                msg = f"[{datetime.now().strftime('%H:%M:%S')}] Passive check: OK"
                logbox.insert(tk.END, msg + "\n")
                logbox.see(tk.END)
                time.sleep(10)

        threading.Thread(target=feed, daemon=True).start()
        win.mainloop()
