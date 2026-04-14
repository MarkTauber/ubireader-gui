import json
import queue
import tkinter as tk

from .commands import check_ubireader, ubi_commands
from .constants import DARK, SETTINGS_FILE
from .logs import UBIReaderLogMixin
from .process import UBIReaderProcessMixin
from .ui import UBIReaderUIMixin


class UBIReaderGUI(UBIReaderUIMixin, UBIReaderProcessMixin, UBIReaderLogMixin, tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UBI Reader GUI")

        self.geometry("1150x780")

        self.minsize(920, 620)
        self.configure(bg=DARK)
        self.resizable(True, True)

        self.selected_file = tk.StringVar()

        self.selected_cmd = tk.StringVar(value="extract_files")

        self.arg_widgets = {}
        self.arg_vars = {}
        self.history = []

        self.process = None

        self._output_queue = queue.Queue()
        self._poll_id = None
        self._ubi_ok = check_ubireader()

        self._log_buffers = {k: [] for k in ubi_commands()}

        self._settings = self._load_settings()
        self.auto_clear_var = tk.BooleanVar(value=self._settings.get("auto_clear", False))
        self.auto_clear_var.trace_add("write", lambda *_: self._save_settings())

        self._cmd_frames = {}
        self._cmd_indicators = {}

        self._setup_styles()

        self._build_ui()

        self._log_info("Welcome to UBI Reader GUI")


        if not self._ubi_ok:  # check if ubireader installed
            self._log_warn(
                "ubireader was not found. Install it with:\n"
                "   pip install ubireader\n"
                "Then restart the application."
            )
        else:
            self._log_ok("ubireader detected and ready.")
        self._log_sep()

    def _load_settings(self) -> dict:
        try:
            if SETTINGS_FILE.exists():
                return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        except Exception:  # fallback
            pass
        return {}

    def _save_settings(self):
        try:
            self._settings["auto_clear"] = self.auto_clear_var.get()

            SETTINGS_FILE.write_text(

                json.dumps(
                    self._settings, 
                    ensure_ascii=False, 
                    indent=2
                ),
                
            encoding="utf-8")

        except Exception:
            pass
