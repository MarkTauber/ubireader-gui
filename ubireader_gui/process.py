import queue
import shutil
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

from .constants import ACCENT, POLL_MS


class UBIReaderProcessMixin:
    def _run(self):

        # NO UBIREADER
        if not self._ubi_ok:
            messagebox.showerror("ubireader not found", "Install ubireader:\n\npip install ubireader\n\nThen restart the application.")
            return

        fp = self.selected_file.get().strip()

        # SELECT FILE
        if not fp:
            messagebox.showwarning("No file selected", "Please select a UBI/UBIFS image.")
            return

        # NO FILE
        if not Path(fp).exists():
            messagebox.showerror("File not found", f"File does not exist:\n{fp}")
            return

        cmd = self._build_cmd()

        # COMMANDLINE FAILED
        if not cmd:
            messagebox.showwarning("Error", "Failed to build command.")
            return

        # NO COMAND (why)
        if not shutil.which(cmd[0]):
            messagebox.showerror("Command not found", f"Executable not found:\n{cmd[0]}\n\npip install ubireader")
            return

        # CLEAR (optional)
        if self.auto_clear_var.get():
            self._clear_log()

        entry = {
                    "time": datetime.now().strftime("%H:%M:%S"), 
                    "cmd": cmd[0], 
                    "file": Path(fp).name
                }

        self.history.append(entry)
        self.history_list.insert(0, f"{entry['time']}  {Path(fp).name}")

        self.run_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        self._log_sep()

        self._log_cmd(f"$ {' '.join(cmd)}")

        threading.Thread(
                            target=self._reader_thread, 
                            args=(cmd,), 
                            daemon=True
                        ).start()

        self._start_progress()
        self._poll_queue()

    def _reader_thread(self, cmd: list):
        try:
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                creationflags=flags,
            )

            # TODO
            # 1. Fix RU

            for raw in self.process.stdout:

                line = raw.rstrip("\n")
                lo = line.lower()

                if any(w in lo for w in ["error", "ошибка", "fail", "exception", "traceback"]):
                    tag = "error"

                elif any(w in lo for w in ["warn", "предупрежд"]):
                    tag = "warn"
                    
                else:
                    tag = "out"

                self._output_queue.put((tag, line))

            rc = self.process.wait()
            self._output_queue.put(("__done__", rc))

        except FileNotFoundError:
            self._output_queue.put(("error", f"Command not found: {cmd[0]}"))
            self._output_queue.put(("__done__", -1))

        except Exception as ex:
            self._output_queue.put(("error", f"Error: {ex}"))
            self._output_queue.put(("__done__", -1))

        finally:
            self.process = None

    def _poll_queue(self):
        batch = []
        done_rc = None

        try:
            for _ in range(200):
                tag, value = self._output_queue.get_nowait()

                if tag == "__done__":
                    done_rc = value
                    break

                if tag == "error":
                    batch.append((f"  X {value}", "error"))

                elif tag == "warn":
                    batch.append((f"  ! {value}", "warn"))

                else:
                    batch.append((f"  {value}", "out"))

        except queue.Empty:
            pass

        if batch:
            self._write_log_batch(batch)

        if done_rc is not None:

            if done_rc == 0:
                self._log_ok(f"Finished successfully (code {done_rc})")

            else:
                self._log_error(f"Process exited with code {done_rc}")

            self._done()
            return

        self._poll_id = self.after(POLL_MS, self._poll_queue)

    def _done(self):
        self._stop_progress()

        if self._poll_id is not None:
            self.after_cancel(self._poll_id)
            self._poll_id = None

        self.run_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def _stop(self):
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass

            self._log_warn("Process stopped by user.")

    def _start_progress(self):
        self._stop_progress()
        self._anim_x = 0
        self._animate_progress()

    def _stop_progress(self):
        if self._anim_id is not None:
            self.after_cancel(self._anim_id)
            self._anim_id = None
        try:
            self.progress_bar.delete("all")
        except Exception:
            pass

    # I like this one 
    def _animate_progress(self):
        try:
            width = self.progress_bar.winfo_width()

            if width < 2:
                width = 800

            self.progress_bar.delete("all")

            seg = int(width * 0.25)
            x1 = self._anim_x % width
            x2 = x1 + seg

            if x2 <= width:
                self.progress_bar.create_rectangle(
                    x1, 
                    0, 
                    x2, 
                    2, 
                    fill=ACCENT, 
                    outline=""
                )

            else:

                self.progress_bar.create_rectangle(
                    x1, 
                    0, 
                    width, 
                    2, 
                    fill=ACCENT, 
                    outline=""
                )

                self.progress_bar.create_rectangle(
                    0, 
                    0, 
                    x2 - width, 
                    2, 
                    fill=ACCENT, 
                    outline=""
                )

            self._anim_x = (self._anim_x + 6) % width

            self._anim_id = self.after(30, self._animate_progress)

        except Exception:
            pass

    def _restore_history(self, _event):
        sel = self.history_list.curselection()
        if sel:
            idx = len(self.history) - 1 - sel[0]
        
            if 0 <= idx < len(self.history):

                h = self.history[idx]

                self._log_info(f"History: {h['time']}  {h['cmd']}  ({h['file']})")
