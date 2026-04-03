import os
import subprocess
import platform
import threading
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class RepomixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Repomix Desktop")
        self.root.geometry("935x695")
        self.root.minsize(750, 500)
        
        # Apply the custom dark slate background to the main window
        self.root.configure(fg_color="#101922")
        
        self.selected_folder = ""
        self.setup_ui()
    
    def setup_ui(self):
        # --- CENTER CONTAINER ---
        center_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Title & Subtitle
        title_label = ctk.CTkLabel(center_frame, text="Repomix Desktop", 
                                   font=ctk.CTkFont(family="Segoe UI", size=38, weight="bold"),
                                   text_color="#FFFFFF")
        title_label.pack(pady=(0, 2))
        
        subtitle_label = ctk.CTkLabel(center_frame, text="An unofficial desktop app for Repomix",
                                      font=ctk.CTkFont(family="Segoe UI", size=14),
                                      text_color="gray60")
        subtitle_label.pack(pady=(0, 40))
        
        desc_label = ctk.CTkLabel(center_frame, 
                                  text="Select any project folder to pack its contents into a single text file for AI analysis.",
                                  font=ctk.CTkFont(family="Segoe UI", size=18), 
                                  text_color="gray70")
        desc_label.pack(pady=(0, 25))

        # The main interaction "Card" 
        card_frame = ctk.CTkFrame(center_frame, fg_color="#182430", 
                                  border_width=1, border_color="#2C3A4A", corner_radius=10)
        card_frame.pack(fill="x", ipadx=10, ipady=10)

        # Folder path display
        self.folder_label = ctk.CTkLabel(card_frame, text="No folder selected", 
                                         font=ctk.CTkFont(family="Segoe UI", size=12), 
                                         text_color="gray50",
                                         fg_color="#0A1016", # Darker inset background 
                                         corner_radius=6,
                                         anchor="w")
        self.folder_label.pack(fill="x", padx=20, pady=(20, 15), ipady=8, ipadx=10)

        # Button row inside the card 
        btn_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 15))
        btn_frame.columnconfigure((0, 1), weight=1)

        # Left Button: Browse
        self.browse_btn = ctk.CTkButton(btn_frame, text="📂 Browse",
                                   command=self.browse_folder,
                                   font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                                   fg_color="#2A3B4C", hover_color="#364A5F", 
                                   height=40)
        self.browse_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        # Right Button: Generate 
        self.generate_btn = ctk.CTkButton(btn_frame, text="🪄 Generate Report", 
                                     command=self.run_repomix, 
                                     font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                                     height=40,
                                     fg_color="#1F6EAA", hover_color="#185A8C")
        self.generate_btn.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        # --- STATUS BAR (Anchored to the absolute bottom) ---
        status_container = ctk.CTkFrame(self.root, fg_color="transparent")
        status_container.pack(side="bottom", fill="x", pady=0)

        # Visible separator line: 
        separator = ctk.CTkFrame(status_container, height=1.5, fg_color="#1A2836")
        separator.pack(fill="x", padx=0, pady=0)

        # Text area holding the left/right labels
        text_frame = ctk.CTkFrame(status_container, fg_color="transparent")
        text_frame.pack(fill="x", padx=15, pady=(8, 6))

        # Output Preview (Left Justified, with default placeholder text)
        self.output_label = ctk.CTkLabel(text_frame, text="Output: [No selection made]", 
                                         font=ctk.CTkFont(family="Consolas", size=11), 
                                         text_color="gray50")
        self.output_label.pack(side="left")

        # Status Label (Right Justified)
        self.status_label = ctk.CTkLabel(text_frame, text="✅ Ready to generate repomix", 
                                         font=ctk.CTkFont(family="Segoe UI", size=12),
                                         text_color="#81C784")
        self.status_label.pack(side="right")
    
    def format_command_error(self, result):
        """Build a readable error message from a failed subprocess result."""
        stderr_text = (result.stderr or "").strip()
        stdout_text = (result.stdout or "").strip()
        max_length = 1200

        def trim_text(text):
            if len(text) > max_length:
                return text[:max_length] + "\n\n...output truncated..."
            return text

        message = f"Repomix failed with exit code {result.returncode}."

        if stderr_text:
            message += f"\n\nError details:\n{trim_text(stderr_text)}"

        if stdout_text:
            message += f"\n\nAdditional output:\n{trim_text(stdout_text)}"

        if not stderr_text and not stdout_text:
            message += "\n\nNo error output was returned."

        return message

    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Select Repository Folder")
        if folder_path:
            self.selected_folder = folder_path
            folder_name = os.path.basename(folder_path)
            self.folder_label.configure(text=folder_path, text_color="#E0E0E0")
            
            # Update output preview
            timestamp = datetime.now().strftime('%m%d%y_%H%M')
            output_filename = f"{folder_name}-summary_{timestamp}.txt"
            self.output_label.configure(text=f"Output: {output_filename}", text_color="gray60")
            
            self.status_label.configure(text="✅ Folder selected - ready to generate!", 
                                        text_color="#81C784")
    
    def _set_buttons_enabled(self, enabled):
        """Enable or disable the Browse and Generate buttons."""
        state = "normal" if enabled else "disabled"
        self.browse_btn.configure(state=state)
        self.generate_btn.configure(state=state)

    def _open_folder(self, folder_path):
        """Open a folder in the system file manager."""
        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", folder_path])
            else:
                subprocess.Popen(["xdg-open", folder_path])
        except Exception:
            pass

    def _show_success_dialog(self, output_path):
        """Custom success dialog with an Open Folder button."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Success!")
        dialog.geometry("480x200")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#182430")
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 480) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        dialog.geometry(f"+{x}+{y}")

        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=30, pady=30)

        title_label = ctk.CTkLabel(
            content_frame, text="Repomix completed successfully!",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#81C784")
        title_label.pack(expand=True)

        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))
        btn_frame.columnconfigure((0, 1), weight=1)

        folder_path = os.path.dirname(output_path)

        open_btn = ctk.CTkButton(
            btn_frame, text="📂 Open Folder",
            command=lambda: (self._open_folder(folder_path), dialog.destroy()),
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#2A3B4C", hover_color="#364A5F", height=40)
        open_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        ok_btn = ctk.CTkButton(
            btn_frame, text="OK",
            command=dialog.destroy,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#1F6EAA", hover_color="#185A8C", height=40)
        ok_btn.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        dialog.bind("<Return>", lambda e: dialog.destroy())
        dialog.bind("<Escape>", lambda e: dialog.destroy())

    def run_repomix(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return
        
        # UI prep on main thread, then hand off to worker
        self._set_buttons_enabled(False)
        self.status_label.configure(text="⚡ Running Repomix...", text_color="#FFB74D")
        
        thread = threading.Thread(target=self._generate_report_thread, daemon=True)
        thread.start()

    def _generate_report_thread(self):
        """Worker thread — runs subprocess off the main UI thread."""
        try:
            folder_name = os.path.basename(self.selected_folder)
            timestamp = datetime.now().strftime('%m%d%y_%H%M')
            output_filename = f"{folder_name}-summary_{timestamp}.txt"
            
            # On Windows, npx is actually npx.cmd
            npx_command = "npx.cmd" if platform.system() == "Windows" else "npx"
            
            cmd = [
                npx_command, "repomix", 
                "--output", output_filename,
                "--ignore", ".env,.env.*,*.log"
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.selected_folder,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
            )
            
            output_path = os.path.join(self.selected_folder, output_filename)

            if result.returncode == 0:
                if os.path.isfile(output_path) and os.path.getsize(output_path) > 0:
                    self.root.after(0, lambda: self.status_label.configure(
                        text="🎉 Success! Repomix file generated!", text_color="#81C784"))
                    self.root.after(0, lambda p=output_path: self._show_success_dialog(p))
                elif os.path.isfile(output_path):
                    self.root.after(0, lambda: self.status_label.configure(
                        text="⚠️ File created but appears empty", text_color="#FFB74D"))
                    self.root.after(0, lambda p=output_path: messagebox.showwarning(
                        "Warning",
                        f"Repomix exited successfully but the output file is empty.\n\n📄 {p}"))
                else:
                    self.root.after(0, lambda: self.status_label.configure(
                        text="❌ Output file not found", text_color="#E57373"))
                    self.root.after(0, lambda p=output_path: messagebox.showerror(
                        "Error",
                        f"Repomix exited successfully but the output file was not created.\n\nExpected: {p}"))
            else:
                error_msg = self.format_command_error(result)
                self.root.after(0, lambda: self.status_label.configure(
                    text="❌ Error during generation", text_color="#E57373"))
                self.root.after(0, lambda: messagebox.showerror("Error ❌", error_msg))
                
        except FileNotFoundError:
            self.root.after(0, lambda: self.status_label.configure(
                text="❌ npx/repomix not found", text_color="#E57373"))
            self.root.after(0, lambda: messagebox.showerror(
                "Error ❌", "npx or repomix not found. Make sure Node.js is installed."))
        except Exception as e:
            error_str = str(e)
            self.root.after(0, lambda: self.status_label.configure(
                text="❌ Unexpected error", text_color="#E57373"))
            self.root.after(0, lambda: messagebox.showerror(
                "Error ❌", f"An error occurred: {error_str}"))
        finally:
            self.root.after(0, lambda: self._set_buttons_enabled(True))

if __name__ == "__main__":
    root = ctk.CTk()
    app = RepomixGUI(root)
    root.mainloop()