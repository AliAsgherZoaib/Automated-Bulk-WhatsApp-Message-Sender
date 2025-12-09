import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
import os
import json
import sys
import subprocess
import tempfile
import traceback

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("WhatsApp Automation GUI")
        self.geometry("900x700")
        
        # Allow resizing
        self.resizable(True, True)
        self.minsize(800, 600)

        # Variables
        self.df = None
        self.phone_var = ctk.StringVar()
        self.country_var = ctk.StringVar(value="+92")
        self.file_path = ""  # Store full file path

        # outer scrollable window
        self.main_scroll = ctk.CTkScrollableFrame(self, width=880, height=650)
        self.main_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):

        # ========== Upload File ==========
        top = ctk.CTkFrame(self.main_scroll)
        top.pack(fill="x", pady=10)

        ctk.CTkLabel(top, text="Excel File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.file_label = ctk.CTkLabel(top, text="(no file selected)", wraplength=500)
        self.file_label.grid(row=0, column=1, sticky="w", padx=5)
        self.choose_file_btn = ctk.CTkButton(top, text="Choose Excel", command=self.upload_file)
        self.choose_file_btn.grid(row=0, column=2, padx=5)

        # ========== Phone column ==========
        ctk.CTkLabel(top, text="Phone Column:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.phone_combo = ctk.CTkComboBox(top, values=[], width=300)
        self.phone_combo.grid(row=1, column=1, columnspan=2, sticky="w", padx=5)

        # ========== Country Code ==========
        ctk.CTkLabel(top, text="Country Code (e.g. +92):").grid(row=2, column=0, sticky="w", padx=5)
        ctk.CTkEntry(top, textvariable=self.country_var, width=120).grid(row=2, column=1, sticky="w", padx=5)

        # ========== Headers Checkbox Area ==========
        hdr_frame = ctk.CTkFrame(self.main_scroll)
        hdr_frame.pack(fill="both", pady=10)

        ctk.CTkLabel(hdr_frame, text="Select Columns to Use as Variables:").pack(anchor="w", padx=5, pady=5)

        self.headers_scroll = ctk.CTkScrollableFrame(hdr_frame, width=850, height=220)
        self.headers_scroll.pack(padx=5, pady=5)

        self.header_vars = {}

        # ========== Message Textbox ==========
        ctk.CTkLabel(self.main_scroll, text="Custom Message (use {ColumnName} variables):")\
            .pack(anchor="w", padx=5, pady=(10, 5))

        self.msg_box = ctk.CTkTextbox(self.main_scroll, width=850, height=260)
        self.msg_box.pack(padx=5, pady=5)
        self.msg_box.insert("0.0", "Hello {Name},\nThis is an Automated WhatsApp Message.\nThankYou")

        # ========== Status Label ==========
        self.status_label = ctk.CTkLabel(self.main_scroll, text="Status: Ready", text_color="green")
        self.status_label.pack(pady=5)

        # ========== Start Button ==========
        self.start_button = ctk.CTkButton(self.main_scroll,
                      text="Start Sending Messages",
                      fg_color="#2fa572",
                      hover_color="#238b5d",
                      command=self.start_automation
                      )
        self.start_button.pack(pady=15)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path:
            return

        self.file_path = file_path
        filename = os.path.basename(file_path)
        self.file_label.configure(text=filename)
        
        try:
            self.df = pd.read_excel(file_path)
            self.populate_headers()
            self.status_label.configure(text="Status: File loaded successfully", text_color="green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file:\n{str(e)}")

    def populate_headers(self):
        if self.df is None:
            return

        cols = list(self.df.columns)

        self.phone_combo.configure(values=cols)
        if len(cols) > 0:
            self.phone_combo.set(cols[0])

        for widget in self.headers_scroll.winfo_children():
            widget.destroy()

        self.header_vars = {}

        for col in cols:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(self.headers_scroll, text=col, variable=var)
            chk.pack(anchor="w", padx=5)
            self.header_vars[col] = var

    def validate_inputs(self):
        if self.df is None:
            messagebox.showerror("Error", "Please select an Excel file first!")
            return False
        
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return False
        
        if not self.phone_combo.get():
            messagebox.showerror("Error", "Please select a phone column!")
            return False
        
        if not self.msg_box.get("0.0", "end").strip():
            messagebox.showerror("Error", "Message template cannot be empty!")
            return False
        
        country_code = self.country_var.get().strip()
        if not country_code.startswith('+'):
            messagebox.showerror("Error", "Country code must start with '+' (e.g., +92)")
            return False
        
        return True

    def start_automation(self):
        if not self.validate_inputs():
            return
        
        if not messagebox.askyesno("Confirm", 
                                   "The GUI will close and automation will run in background.\n"
                                   "A new Chrome window will open.\n"
                                   "You have 60 seconds to scan QR code.\n\n"
                                   "Continue?"):
            return
        
        config = {
            'file_path': self.file_path,
            'phone_column': self.phone_combo.get(),
            'country_code': self.country_var.get(),
            'selected_vars': [h for h, v in self.header_vars.items() if v.get()],
            'message_template': self.msg_box.get("0.0", "end").strip()
        }
        
        try:
            temp_dir = tempfile.gettempdir()
            config_file = os.path.join(temp_dir, "whatsapp_automation_config.json")
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            automation_script = os.path.join(script_dir, "whatsapp_automation.py")
            
            if not os.path.exists(automation_script):
                messagebox.showerror("Error", 
                    f"Automation script not found!\n\n"
                    f"Make sure 'whatsapp_automation.py' exists in:\n"
                    f"{script_dir}")
                return
            
            python_exe = sys.executable
            
            if os.name == 'nt':
                subprocess.Popen([python_exe, automation_script, config_file], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([python_exe, automation_script, config_file])
            
            self.after(500, self.destroy)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start automation:\n{str(e)}")

def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()