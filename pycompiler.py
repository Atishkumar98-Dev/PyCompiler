#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import py_compile
import sys
import dis
from pathlib import Path
import tempfile
import re

class PyCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Test Compiler")
        self.root.geometry("800x600")

        # Menu
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        # Text area for code
        self.code_area = scrolledtext.ScrolledText(root, wrap=tk.NONE, font=("Consolas", 12), undo=True)
        self.code_area.pack(fill=tk.BOTH, expand=True)

        # Bind Return key for auto-indentation
        self.code_area.bind('<Return>', self.auto_indent)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="Run", command=self.run_code).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Compile", command=self.compile_code).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Show Bytecode", command=self.show_bytecode).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=5, pady=5)

        # Output area
        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, bg="#f0f0f0", font=("Consolas", 11))
        self.output_area.pack(fill=tk.BOTH, expand=False)

        self.current_file = None

    # Auto indentation
    def auto_indent(self, event=None):
        line_index = self.code_area.index("insert").split(".")[0]
        line_text = self.code_area.get(f"{line_index}.0", f"{line_index}.end")

        # Find leading whitespace of current line
        match = re.match(r"^(\s*)", line_text)
        indent = match.group(1) if match else ""

        # If the previous line ends with ':', increase indentation
        if line_text.rstrip().endswith(":"):
            indent += "    "

        # Insert newline + indentation
        self.code_area.insert("insert", "\n" + indent)
        return "break"  # prevent default newline

    # File operations
    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path:
            with open(path, "r") as f:
                code = f.read()
            self.code_area.delete("1.0", tk.END)
            self.code_area.insert(tk.END, code)
            self.current_file = path

    def save_file(self):
        if self.current_file:
            path = self.current_file
        else:
            path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if path:
            with open(path, "w") as f:
                f.write(self.code_area.get("1.0", tk.END))
            self.current_file = path
            messagebox.showinfo("Saved", f"File saved to {path}")

    # Run code
    def run_code(self):
        code = self.code_area.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "No code to run!")
            return

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        self.output_area.insert(tk.END, f"\n--- Running {tmp_path} ---\n")
        self.output_area.see(tk.END)
        self.root.update()

        try:
            result = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True, timeout=10)
            self.output_area.insert(tk.END, result.stdout)
            if result.stderr:
                self.output_area.insert(tk.END, "\n--- STDERR ---\n")
                self.output_area.insert(tk.END, result.stderr)
        except subprocess.TimeoutExpired:
            self.output_area.insert(tk.END, "\nERROR: Execution timed out!")
        except Exception as e:
            self.output_area.insert(tk.END, f"\nERROR: {e}")
        finally:
            self.output_area.see(tk.END)

    # Compile to .pyc
    def compile_code(self):
        code = self.code_area.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "No code to compile!")
            return
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        try:
            pyc_path = py_compile.compile(tmp_path, doraise=True)
            self.output_area.insert(tk.END, f"\nCompiled successfully: {pyc_path}\n")
        except py_compile.PyCompileError as e:
            self.output_area.insert(tk.END, f"\nCompilation Error:\n{e.msg}\n")
        self.output_area.see(tk.END)

    # Show bytecode
    def show_bytecode(self):
        code = self.code_area.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "No code to show bytecode!")
            return
        try:
            codeobj = compile(code, "<string>", "exec")
            self.output_area.insert(tk.END, "\n--- Bytecode ---\n")
            dis.dis(codeobj, file=self.output_area)
            self.output_area.insert(tk.END, "\n--- End Bytecode ---\n")
        except Exception as e:
            self.output_area.insert(tk.END, f"\nERROR generating bytecode: {e}\n")
        self.output_area.see(tk.END)

    def clear_output(self):
        self.output_area.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = PyCompilerGUI(root)
    root.mainloop()
