# system_operator_interface.py — Aegis Prime System Operator Interface (Commander-Controlled OS Access)

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import datetime
import json
import shutil

class SystemOperatorInterface:
    def __init__(self, logger):
        self.logger = logger
        self.operation_log_file = "system_operator_log.json"

    def log_operation(self, operation_type, target_path, details=None):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "operation": operation_type,
            "target_path": target_path,
            "details": details or {}
        }
        try:
            with open(self.operation_log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            self.logger.log(f"[SYSTEM OPERATOR LOG ERROR] {e}")

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            self.logger.log(f"[SYSTEM OPERATOR] File deleted: {file_path}")
            self.log_operation("delete_file", file_path)
        except Exception as e:
            self.logger.log(f"[SYSTEM OPERATOR ERROR] {e}")
            messagebox.showerror("Delete Error", f"Failed to delete file:\n{e}")

    def copy_file(self, src_path, dest_path):
        try:
            shutil.copy2(src_path, dest_path)
            self.logger.log(f"[SYSTEM OPERATOR] File copied from {src_path} to {dest_path}")
            self.log_operation("copy_file", src_path, {"destination": dest_path})
        except Exception as e:
            self.logger.log(f"[SYSTEM OPERATOR ERROR] {e}")
            messagebox.showerror("Copy Error", f"Failed to copy file:\n{e}")

    def rename_file(self, src_path, dest_path):
        try:
            os.rename(src_path, dest_path)
            self.logger.log(f"[SYSTEM OPERATOR] File renamed from {src_path} to {dest_path}")
            self.log_operation("rename_file", src_path, {"new_name": dest_path})
        except Exception as e:
            self.logger.log(f"[SYSTEM OPERATOR ERROR] {e}")
            messagebox.showerror("Rename Error", f"Failed to rename file:\n{e}")

    def create_folder(self, folder_path):
        try:
            os.makedirs(folder_path, exist_ok=True)
            self.logger.log(f"[SYSTEM OPERATOR] Folder created: {folder_path}")
            self.log_operation("create_folder", folder_path)
        except Exception as e:
            self.logger.log(f"[SYSTEM OPERATOR ERROR] {e}")
            messagebox.showerror("Create Folder Error", f"Failed to create folder:\n{e}")

    def launch_operator_gui(self):
        win = tk.Toplevel()
        win.title("Aegis System Operator Interface (Commander-Controlled)")
        win.geometry("600x550")

        tk.Label(win, text="Sovereign OS Operations", font=("Arial", 14)).pack(pady=10)

        log_box = scrolledtext.ScrolledText(win, width=70, height=20, state=tk.DISABLED)
        log_box.pack(pady=10)

        def log_gui_entry(msg):
            log_box.config(state=tk.NORMAL)
            log_box.insert(tk.END, msg + "\n")
            log_box.config(state=tk.DISABLED)
            log_box.see(tk.END)

        def run_delete():
            file_path = filedialog.askopenfilename(title="Select file to delete")
            if file_path:
                if messagebox.askyesno("Confirm Delete", f"Delete file: {file_path}?"):
                    self.delete_file(file_path)
                    log_gui_entry(f"Deleted: {file_path}")

        def run_copy():
            src_path = filedialog.askopenfilename(title="Select source file to copy")
            if src_path:
                dest_dir = filedialog.askdirectory(title="Select destination folder")
                if dest_dir:
                    dest_path = os.path.join(dest_dir, os.path.basename(src_path))
                    self.copy_file(src_path, dest_path)
                    log_gui_entry(f"Copied: {src_path} → {dest_path}")

        def run_rename():
            src_path = filedialog.askopenfilename(title="Select file to rename")
            if src_path:
                new_name = simpledialog.askstring("New File Name", "Enter new file name:")
                if new_name:
                    dest_path = os.path.join(os.path.dirname(src_path), new_name)
                    self.rename_file(src_path, dest_path)
                    log_gui_entry(f"Renamed: {src_path} → {dest_path}")

        def run_create_folder():
            folder_path = filedialog.askdirectory(title="Select parent directory for new folder")
            if folder_path:
                new_folder = simpledialog.askstring("New Folder Name", "Enter new folder name:")
                if new_folder:
                    full_path = os.path.join(folder_path, new_folder)
                    self.create_folder(full_path)
                    log_gui_entry(f"Created Folder: {full_path}")

        tk.Button(win, text="Delete File", command=run_delete).pack(pady=2)
        tk.Button(win, text="Copy File", command=run_copy).pack(pady=2)
        tk.Button(win, text="Rename File", command=run_rename).pack(pady=2)
        tk.Button(win, text="Create Folder", command=run_create_folder).pack(pady=2)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)
