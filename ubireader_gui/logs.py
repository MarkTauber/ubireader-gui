from pathlib import Path
from tkinter import filedialog


class UBIReaderLogMixin:
    def _dump_log_tagged(self) -> list:
        result = []
        current_text = []
        current_tag = "out"

        for key, value, _ in self.log_text.dump("1.0", "end", text=True, tag=True):
            if key == "tagon":
                if current_text:
                    result.append(("".join(current_text), current_tag))
                    current_text = []
                current_tag = value
            elif key == "tagoff":
                if current_text:
                    result.append(("".join(current_text), current_tag))
                    current_text = []
                current_tag = "out"
            elif key == "text":
                current_text.append(value)

        if current_text:
            result.append(("".join(current_text), current_tag))

        return result


    def _restore_log_buffer(self, key):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")

        for text, tag in self._log_buffers.get(key, []):
            self.log_text.insert("end", text, tag)
        
        self.log_text.see("end")
        self.log_text.config(state="disabled")


    def _write_log(self, text, tag):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")


    def _write_log_batch(self, items: list):
        max_lines = 5000
        self.log_text.config(state="normal")

        for text, tag in items:
            self.log_text.insert("end", text + "\n", tag)

        line_count = int(self.log_text.index("end-1c").split(".")[0])

        if line_count > max_lines:
            self.log_text.delete("1.0", f"{line_count - max_lines}.0")

        self.log_text.see("end")
        self.log_text.config(state="disabled")


    def _log_info(self, text):
        self._write_log(f"  [i] {text}", "info")


    def _log_ok(self, text):
        self._write_log(f"  [V] {text}", "ok")


    def _log_warn(self, text):
        self._write_log(f"  [!] {text}", "warn")


    def _log_error(self, text):
        self._write_log(f"  [X] {text}", "error")


    def _log_cmd(self, text):
        self._write_log(text, "cmd")


    def _log_sep(self):
        self._write_log("  " + "─" * 60, "sep")


    def _clear_log(self):
        key = self.selected_cmd.get()
        self._log_buffers[key] = []
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")


    def _save_log(self):

        path = filedialog.asksaveasfilename(
            title="Save log",
            defaultextension=".log",
            filetypes=[("Log", "*.log"), ("Text", "*.txt"), ("All", "*.*")],
        )

        if path:
            content = self.log_text.get("1.0", "end")
            Path(path).write_text(content, encoding="utf-8")
            self._log_ok(f"Log saved: {path}")
