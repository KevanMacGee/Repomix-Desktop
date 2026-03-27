# Repomix GUI

Note: This project has no official connection to Repormix. This is a GUI wrapper that provides a user-friendly interface for [Repomix](https://github.com/yamadashy/repomix) instead of using it in the terminal. This is only a GUI wrapper and you must have Node installed to use it.

This was a 45 minute AI assisted, quick and dirty project to make AI assisted coding easier. When using AI to code something, I will often feed a Repomix file of my codebase for analysis, feedback or to have the AI model make some changes. This makes it a little easier to accomplish.

![App Screenshot](screenshots/app_preview.png)

## 📥 Download (For Most Users)

**Just want to use the app?**

This app is a standalone exe and does not need to be installed.

- Go to [Releases](https://github.com/yourusername/repomix-gui/releases)
- Download `repomix-gui.exe` from the latest release
- Double-click to run (requires Node.js for Repomix)

## 🚧 Issues

These may or may not be fixed, depending on how often they come up. The fix might even be to not use this GUI and just use Repomix in the terminal as originally intended. If you encounter frequent errors, please submit an issue on it.

- Error reporting is a little broken and definitely incomplete.
- If this program runs for a long time, the GUI may freeze. I haven't been able to get the program to do this so I haven't bothered with a fix.
- env and log files are hardcoded to be ignored. This really shouldn't be much of an issue but the fact that it is not configurable should be noted.
- This isn't really an issue and if you are downloading the .exe, you can ignore it. If you are running the Python file directly, make sure to install CustomTkinker first. Instructions are below.

## 🛠️ For Developers

### Skip the .exe and run the Python file directly

It is intended to be used by running the .exe, but you can 100% run the .py file directly if you prefer. However if you do, you need to have CustomTkinter installed first. Do that with the following command:

```bash
pip install customtkinter
```

Next, simply save the `repomix_gui.py` file to the folder on your PC that you want to get the Repomix report of. Open a terminal in that same folder and run the following command in the terminal: 

```bash
python repomix_gui.py
```

### Build and Customize Your Own Executable

If you want to make changes to the program, edit the `repomix_gui.py` file and then make the executable by running:

```bash
pip install customtkinter pyinstaller
pyinstaller --onefile --windowed repomix_gui.py
```

## Requirements

- Node.js and npm (needed to run Repomix)
- Python 3.6+ (only if running from source, not needed to run the .exe)

## License

This project is licensed under CC BY-NC-SA 4.0
