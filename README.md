## Repomix Desktop

![GitHub last commit](https://img.shields.io/github/last-commit/kevanmacgee/repomix-desktop) ![GitHub repo size](https://img.shields.io/github/repo-size/kevanmacgee/repomix-desktop) ![GitHub license](https://img.shields.io/github/license/kevanmacgee/repomix-desktop) ![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue) ![Status](https://img.shields.io/badge/status-active-brightgreen)

**Note:** This is an **unofficial** community desktop app for [Repomix](https://github.com/yamadashy/repomix). It is maintained independently and is not the official Repomix CLI app.

Repomix Desktop is an open-source GUI wrapper for the Repomix CLI. It provides a desktop interface rather than using Repomix directly in the terminal. Node.js must be installed to use this app.

![App Screenshot](screenshots/app_preview.png)

### ⚠️ Important Prerequisite: Node.js

Because this app is simply a wrapper around the Repomix command-line tool, **you must have Node.js installed on your computer.** If you already use Repomix in the terminal, you can skip this. If not, follow the steps below:

- Go to [Nodejs.org](https://nodejs.org/)
- Download and install the LTS (Long Term Support) version.
- Now you are good to go to download and use the .exe. (To use the .py file there are a few more prereqs. See below.)

### 📥 Download (Best for most users)

**Just want to use the app?**

This app is a standalone .exe and does not need to be installed itself.

- Go to [Releases](https://github.com/kevanmacgee/repomix-desktop/releases)
- Download `repomix_desktop.exe` from the latest release
- Double-click to run (Note: The app will open without Node.js, but will fail to generate a report until Node is installed).

### 🚧 Issues

These may or may not be fixed in the future, depending on how often they come up. The fix might even be to not use this GUI and just use Repomix in the terminal as originally intended. If you encounter frequent errors, please submit an issue on it.

- More error handling has been added but there are some edge cases that haven't been addressed yet. I'd move it to "not really broken anymore and only just a little bit incomplete" ~~Error reporting is a little broken and definitely incomplete as most of the errors you may encounter are actually handled and reported to you by the underlying tech this is built on.~~
- This should be fixed, please create an issue if you experience it .~~If this program runs for a long time, the GUI may freeze. I haven't been able to get the program to do this so I haven't bothered with a fix~~.
- env and log files are hardcoded to be ignored. This really shouldn't be much of an issue but the fact that it is not configurable should be noted.

### 🧑‍💻 For Developers

#### Skip the .exe and run the Python file directly

It is intended to be used by running the .exe, but you can 100% run the .py file directly if you prefer. However if you do, you need to have [CustomTkinter](https://customtkinter.tomschimansky.com/) installed. Do that with the following command:

```bash
pip install customtkinter
```

Next, simply save the `repomix_desktop.py` file to your computer. Open a terminal in that same folder and run the following command in the terminal:

```bash
python repomix_desktop.py
```

#### Build and Customize Your Own Executable

If you want to make changes to the program, edit the `repomix_desktop.py` file and then make the executable by running:

```bash
pip install customtkinter pyinstaller
pyinstaller repomix_desktop.spec
```

### 🛠️ Requirements

- Node.js and npm (needed to run Repomix).
- Python 3.6+ (Only if running from source, not needed to run the .exe).
- [CustomTkinter](https://customtkinter.tomschimansky.com/) if you are only running the .py file.

### ⚖️ Credits and Legal

This project is licensed under the [MIT License](LICENSE).

Obviously this couldn't exist without Repomix. In their own words: "Repomix is a powerful tool that packs your entire repository into a single, AI-friendly file. Perfect for when you need to feed your codebase to Large Language Models (LLMs) or other AI tools".

Website: https://repomix.com/ GitHub: https://github.com/yamadashy/repomix

The look and feel of the app is all to do with CustomTkinter. In their own words: "CustomTkinter is a python desktop UI-library based on Tkinter, which provides modern looking and fully customizable widgets."

Website: https://customtkinter.tomschimansky.com/ GitHub: https://github.com/tomschimansky/customtkinter
