<!--
Short, actionable instructions for AI coding agents working on Repomix-gui.
Keep this file concise (20-50 lines) and tie recommendations directly to files and patterns found in the repo.
-->

# Copilot instructions for Repomix-gui

Purpose: help an AI agent make safe, focused edits to the GUI wrapper around Repomix.

- Project entry: `repomix_gui.py` — a single-file Tkinter GUI that wraps the `npx repomix` command.
- Author notes and developer workflows are in `README.md` (run with `python repomix_gui.py` and build with PyInstaller).

Quick rules
- Preserve the single-file nature of the GUI unless adding a clear benefit (e.g., splitting UI into modules). Note: many users run the `.exe` produced by PyInstaller.
- Keep UI text and messages in-place; any i18n or refactor must preserve the current message shapes used by tests or user flows (messagebox, status_label text).

Platform-specific behavior
- Windows: the code uses `npx.cmd` if platform.system() == "Windows". Keep this detection when invoking external commands.
- Repomix is invoked via `subprocess.run` with `capture_output=True` and `cwd=self.selected_folder`. Avoid changing to shell=True or removing `cwd` without confirming effects on output file generation.

Patterns and conventions
- GUI uses Tkinter + ttk with a dark theme configured in `RepomixGUI.setup_ui()`. When changing colors/styles, match the existing style names (`Custom.TLabelframe`, `Custom.TFrame`).
- Filenames include a timestamp: look for `timestamp = datetime.now().strftime('%m%d%y_%H%M')` when altering naming behavior.
- The `--ignore` list is hardcoded to ".env,*.log" in `run_repomix()`; if you need to make it configurable, add a new UI control and maintain backward compatibility.

Build and run notes
- Run from source: `python repomix_gui.py` (see `README.md`).
- Build exe with PyInstaller (project expects `pyinstaller --onefile --windowed repomix_gui.py`). If editing imports or adding modules, update the pyinstaller spec or include hidden imports.

Testing and debugging
- No automated tests are present. For quick checks, run `python repomix_gui.py` and exercise Browse + Generate flows.
- For debugging Repomix invocation failures, inspect `subprocess.CompletedProcess.stdout` and `.stderr` — consider exposing a log window instead of messageboxes for long-run diagnostic edits.

Integration points
- External: Node.js (npx, repomix) — verify environment checks before invoking. Missing npx raises FileNotFoundError which is handled; preserve that behavior or improve the error message.
- File system: program writes the summary into the selected repo folder; do not change write location without adding explicit UI affordance.

Examples to reference
- `repomix_gui.py`:
  - Windows npx detection: `npx_command = "npx.cmd" if platform.system() == "Windows" else "npx"`
  - subprocess usage: `subprocess.run(cmd, cwd=self.selected_folder, capture_output=True, text=True, encoding='utf-8', errors='replace')`

If you plan broader changes
- Add a short PR description explaining user-visible changes (UI text, file locations, external command behavior).
- When adding dependencies, update README with build/run instructions and the PyInstaller spec if needed.

If anything here is unclear or you need more repo-specific examples, ask and I will expand the file with additional snippets or rules.
