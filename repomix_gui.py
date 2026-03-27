import os
import subprocess
import platform
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")  # Forces dark mode
ctk.set_default_color_theme("blue")  # Themes the accent colors

class RepomixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Repomix Generator")
        self.root.geometry("850x635")
        self.root.minsize(750, 500)
        
        self.selected_folder = ""
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="🗂️ Repomix Generator", 
                                   font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
                                   text_color="#64B5F6")
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ctk.CTkLabel(main_frame, 
                                  text="Select a repository folder to generate a comprehensive text summary",
                                  font=ctk.CTkFont(family="Segoe UI", size=14), 
                                  text_color="gray75")
        desc_label.pack(pady=(0, 30))
        
        # Folder selection section
        folder_section = ctk.CTkFrame(main_frame)
        folder_section.pack(fill="x", pady=(0, 20), padx=10)
        
        self.folder_label = ctk.CTkLabel(folder_section, text="No folder selected", 
                                         font=ctk.CTkFont(family="Consolas", size=12), 
                                         text_color="gray75",
                                         anchor="w", justify="left")
        self.folder_label.pack(fill="x", padx=15, pady=(15, 10))
        
        # Browse button
        browse_btn = ctk.CTkButton(folder_section, text="Browse Folder",
                                   command=self.browse_folder,
                                   font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                                   height=40)
        browse_btn.pack(pady=(0, 15))
        
        # Output preview section (no title)
        preview_section = ctk.CTkFrame(main_frame)
        preview_section.pack(fill="x", pady=(0, 20), padx=10)
        
        self.output_label = ctk.CTkLabel(preview_section, text="Select a folder to see output filename", 
                                         font=ctk.CTkFont(family="Consolas", size=12), 
                                         text_color="gray75",
                                         anchor="w")
        self.output_label.pack(fill="x", padx=15, pady=15)
        
        # Generate button
        generate_btn = ctk.CTkButton(main_frame, text="🚀 Generate Repomix", 
                                     command=self.run_repomix, 
                                     font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                                     height=50,
                                     fg_color="#2E7CD6", hover_color="#1E528F")
        generate_btn.pack(pady=20)
        
        # Status with icon
        self.status_label = ctk.CTkLabel(main_frame, text="✅ Ready to generate repomix", 
                                         font=ctk.CTkFont(family="Segoe UI", size=14),
                                         text_color="#81C784")
        self.status_label.pack(pady=(0, 15))
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Select Repository Folder")
        if folder_path:
            self.selected_folder = folder_path
            folder_name = os.path.basename(folder_path)
            self.folder_label.configure(text=folder_path, text_color="white")
            
            # Update output preview [cite: 56]
            timestamp = datetime.now().strftime('%m%d%y_%H%M')
            output_filename = f"{folder_name}-summary_{timestamp}.txt"
            self.output_label.configure(text=output_filename, text_color="white")
            
            self.status_label.configure(text="✅ Folder selected - ready to generate!", 
                                        text_color="#81C784")
    
    def run_repomix(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return
        
        try:
            folder_name = os.path.basename(self.selected_folder)
            timestamp = datetime.now().strftime('%m%d%y_%H%M')
            output_filename = f"{folder_name}-summary_{timestamp}.txt"
            
            self.status_label.configure(text="⚡ Running Repomix...", text_color="#FFB74D")
            self.root.update()
            
            # On Windows, npx is actually npx.cmd [cite: 59]
            npx_command = "npx.cmd" if platform.system() == "Windows" else "npx"
            
            cmd = [
                npx_command, "repomix", 
                "--output", output_filename,
                "--ignore", ".env,*.log"
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.selected_folder,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
            )
            
            if result.returncode == 0:
                self.status_label.configure(text="🎉 Success! Repomix file generated!", 
                                            text_color="#81C784")
                
                messagebox.showinfo("Success! 🎉", 
                                    f"Repomix completed successfully!\n\n📄 File: {output_filename}\n📍 Location: {self.selected_folder}")
            else:
                self.status_label.configure(text="❌ Error during generation", 
                                            text_color="#E57373")
                messagebox.showerror("Error ❌", f"Repomix failed.\n\nCheck output for details.")
                
        except FileNotFoundError:
            error_msg = "npx or repomix not found. Make sure Node.js is installed."
            messagebox.showerror("Error ❌", error_msg)
            self.status_label.configure(text="❌ npx/repomix not found", text_color="#E57373")
        except Exception as e:
            messagebox.showerror("Error ❌", f"An error occurred: {str(e)}")
            self.status_label.configure(text="❌ Unexpected error", text_color="#E57373")

if __name__ == "__main__":
    # Note the change from tk.Tk() to ctk.CTk()
    root = ctk.CTk()
    app = RepomixGUI(root)
    root.mainloop()