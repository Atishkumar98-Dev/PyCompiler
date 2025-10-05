# Python Test Compiler — README

A tiny, cross-platform Tkinter app for quickly **writing, running, compiling, and inspecting Python code**. Ideal for quick experiments, teaching demos, or peeking at CPython bytecode without leaving a GUI.

---

## ✨ Features

* **Editor with auto-indent** (adds 4 spaces after lines ending with `:`).
* **Run** code in a sandboxed temp file (10-second timeout) and view stdout/stderr.
* **Compile** to `.pyc` with clear compile errors.
* **Show Bytecode** using `dis` for the current buffer.
* **Open / Save** `.py` files.
* **Clear Output** button to reset the console panel.

---

## 📦 Requirements

* **Python 3.8+** (works on 3.x).
* **Tkinter** (bundled with most Python builds).

  * macOS (Homebrew Python): `brew install python-tk@3.12` (or matching version).
  * Ubuntu/Debian: `sudo apt-get install python3-tk`.
  * Fedora: `sudo dnf install python3-tkinter`.
* No third-party packages required (uses stdlib: `tkinter`, `subprocess`, `py_compile`, `dis`, etc.).

---

## 🚀 Getting Started

1. **Save** the script as `py_compiler_gui.py`.
2. (Optional) Make it executable on macOS/Linux:

   ```bash
   chmod +x py_compiler_gui.py
   ```
3. **Run**:

   ```bash
   # Using the current Python
   python3 py_compiler_gui.py

   # Or with the shebang on Unix
   ./py_compiler_gui.py
   ```

> On Windows, double-clicking may work if `.py` is associated with Python; otherwise run from `cmd`/PowerShell.

---

## 🖱️ Usage

* **Editor**: Type or paste Python code. Auto-indent triggers when you press **Enter** after a line ending with `:`.
* **File → Open / Save**: Load or save `.py` files. The current file path is remembered for subsequent saves.
* **Run**:

  * Executes the current buffer by writing it to a **temporary `.py`** and invoking `sys.executable`.
  * Output and errors appear in the **Output** panel.
  * Execution is **terminated after 10 seconds** (to prevent runaway scripts).
* **Compile**:

  * Compiles the buffer to **`.pyc`** via `py_compile.compile()` and reports the `.pyc` path or compile errors.
* **Show Bytecode**:

  * Compiles the buffer to a code object and disassembles it via `dis.dis(...)` into the Output panel.
* **Clear Output**: Wipes the Output panel.

---

## ⌨️ Shortcuts & Tips

* **Enter**: Auto-indent continues current line’s leading whitespace; adds four spaces if the line ends with `:`.
* **Undo/Redo**: The editor widget supports undo/redo (Ctrl/Cmd+Z / Ctrl/Cmd+Y).
* **Scrolling**: Both editor and output are scrollable.

---

## 🔒 Safety & Limits

* **Never run untrusted code.** The app does **not** sandbox OS access or imports.
* The **10-second timeout** applies only to the *Run* action (not to compilation or bytecode view).
* Temporary files are created during run/compile steps; the OS typically cleans them up.

---

## 🧰 Troubleshooting

* **`ModuleNotFoundError: No module named 'tkinter'`**

  * Install the Tk bindings for your OS (see *Requirements*).
* **`_tkinter.TclError: no display name and no $DISPLAY environment variable` (Linux/WSL)**

  * You’re in a headless environment. Run under a desktop session or use X11 forwarding.
* **Nothing happens on Run**

  * Check the Output panel for exceptions.
  * Scripts waiting for **input()** will hang until timeout (no interactive stdin).
* **Permissions on macOS**

  * If Gatekeeper blocks execution, run from Terminal or allow in **System Settings → Privacy & Security**.

---

## 📦 Packaging (optional)

Create a single-file executable using **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name PythonTestCompiler py_compiler_gui.py
```

The binary will appear in the `dist/` folder. On macOS, you may need to sign/notarize for distribution.

---

## 🗺️ Roadmap Ideas

* Line numbers and basic syntax highlighting.
* Find/Replace, Go-to-line.
* Configurable run timeout.
* Basic REPL input support.
* Bytecode diff (before/after small edits).

---

## 🤝 Contributing

Issues and PRs welcome! Keep dependencies stdlib-only where possible, and test on Windows, macOS, and Linux with Python 3.8–3.12.

---

## 📝 License

MIT (or your preferred license). Add a `LICENSE` file at the repo root.

---

## 📁 File Structure (suggested)

```
.
├── py_compiler_gui.py     # The GUI application (this file)
├── README.md              # You are here
└── LICENSE                # MIT or similar
```

---

## 💡 Notes for Maintainers

* The app uses `sys.executable` to ensure it runs the buffer with the **same Python** that launched the GUI.
* `dis.dis()` is directed at the output text widget via its file-like interface.
* Auto-indent uses a simple regex for leading whitespace and a `:` suffix check—easy to extend for other cases.
