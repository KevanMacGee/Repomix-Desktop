import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
from datetime import datetime

class RepomixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Repomix Generator")
        self.root.geometry("850x635")
        self.root.minsize(750, 500)
        self.root.resizable(True, True)
        
        # Dark theme background colors
        window_bg = "#1e1e1e"  
        self.root.configure(bg=window_bg)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles for dark theme
        self.style.configure("Custom.TLabelframe", background=window_bg, borderwidth=0, relief="flat")
        self.style.configure("Custom.TLabelframe.Label", foreground="#e0e0e0", background=window_bg, font=("Segoe UI", 11, "bold"))
        self.style.configure("Custom.TFrame", background=window_bg)
        
        # Custom colors for dark theme
        self.accent_color = "#64B5F6"  # Lighter blue for dark theme
        self.success_color = "#81C784"  # Lighter green
        self.error_color = "#E57373"    # Lighter red
        self.button_color = "#2E7CD6"   # Dark blue button
        
        self.selected_folder = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20", style="Custom.TFrame")
        main_frame.pack(fill="both", expand=True)
        
        # Title with custom styling
        title_label = tk.Label(main_frame, text="🗂️ Repomix Generator", 
                              font=("Segoe UI", 24, "bold"),
                              fg=self.accent_color, bg="#1e1e1e")
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = tk.Label(main_frame, 
                             text="Select a repository folder to generate a comprehensive text summary",
                             font=("Segoe UI", 11, "bold"), fg="#cccccc",
                             bg="#1e1e1e")
        desc_label.pack(pady=(0, 30))
        
        # Folder selection section
        folder_section = ttk.LabelFrame(main_frame, text="Repository Selection", 
                                       padding="15", style="Custom.TLabelframe")
        folder_section.pack(fill="x", pady=(0, 20))
        
        self.folder_label = tk.Label(folder_section, text="No folder selected", 
                                   relief="solid", anchor="w", bg="#2d2d2d", 
                                   font=("Consolas", 10), fg="#cccccc",
                                   padx=10, pady=8)
        self.folder_label.pack(fill="x", pady=(0, 10))
        
        # Browse button
        browse_btn = tk.Button(folder_section, text="Browse Folder",
                              command=self.browse_folder,
                              bg=self.button_color, fg="white",
                              font=("Segoe UI", 14, "bold"),
                              pady=12, padx=15,
                              relief="flat",
                              cursor="hand2")
        browse_btn.pack(pady=5)
        
        # Add subtle dark line between sections
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
        self.style.configure("TSeparator", background="#2d2d2d")
        
        # Output preview section (no title)
        preview_section = ttk.LabelFrame(main_frame, text="", 
                                        padding="15", style="Custom.TLabelframe")
        preview_section.pack(fill="x", pady=(0, 20))
        
        self.output_label = tk.Label(preview_section, text="Select a folder to see output filename", 
                                   relief="solid", anchor="w", bg="#2d2d2d",
                                   font=("Consolas", 10), fg="#cccccc",
                                   padx=10, pady=8)
        self.output_label.pack(fill="x")
        
        # Generate button
        generate_btn = tk.Button(main_frame, text="🚀 Generate Repomix", 
                               command=self.run_repomix, 
                               bg=self.button_color, fg="white", 
                               font=("Segoe UI", 14, "bold"),
                               pady=12, relief="flat",
                               cursor="hand2")
        generate_btn.pack(pady=20, ipadx=20)
        
        # Status with icon
        self.status_label = tk.Label(main_frame, text="✅ Ready to generate repomix", 
                                   fg=self.success_color, font=("Segoe UI", 12),
                                   bg="#1e1e1e")
        self.status_label.pack(pady=(0, 15))
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Select Repository Folder")
        if folder_path:
            self.selected_folder = folder_path
            folder_name = os.path.basename(folder_path)
            self.folder_label.config(text=folder_path, 
                                   font=("Consolas", 10), fg="#ffffff")
            
            # Update output preview
            timestamp = datetime.now().strftime('%m%d%y_%H%M')
            output_filename = f"{folder_name}-summary_{timestamp}.txt"
            self.output_label.config(text=output_filename, 
                                   font=("Consolas", 10), fg="#ffffff")
            
            self.status_label.config(text="✅ Folder selected - ready to generate!", 
                                   fg=self.success_color)
    
    def run_repomix(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return
        
        try:
            folder_name = os.path.basename(self.selected_folder)
            timestamp = datetime.now().strftime('%m%d%y_%H%M')
            output_filename = f"{folder_name}-summary_{timestamp}.txt"
            
            self.status_label.config(text="⚡ Running Repomix...", fg="#FFB74D")
            self.root.update()
            
            # On Windows, npx is actually npx.cmd
            import platform
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
                self.status_label.config(text="🎉 Success! Repomix file generated!", 
                                       fg=self.success_color)
                
                messagebox.showinfo("Success! 🎉", 
                                  f"Repomix completed successfully!\n\n📄 File: {output_filename}\n📍 Location: {self.selected_folder}")
            else:
                self.status_label.config(text="❌ Error during generation", 
                                       fg=self.error_color)
                messagebox.showerror("Error ❌", f"Repomix failed.\n\nCheck output for details.")
                
        except FileNotFoundError:
            error_msg = "npx or repomix not found. Make sure Node.js is installed."
            messagebox.showerror("Error ❌", error_msg)
            self.status_label.config(text="❌ npx/repomix not found", fg=self.error_color)
        except Exception as e:
            messagebox.showerror("Error ❌", f"An error occurred: {str(e)}")
            self.status_label.config(text="❌ Unexpected error", fg=self.error_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = RepomixGUI(root)
    root.mainloop()