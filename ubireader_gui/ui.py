import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from .commands import ubi_commands
from .constants import (
    ACCENT,
    AMBER,
    BORDER,
    CARD,
    DARK,
    FONT_BADGE,
    FONT_BODY,
    FONT_HEAD,
    FONT_MONO,
    FONT_SMALL,
    FONT_TITLE,
    GREEN,
    MUTED,
    PANEL,
    RED,
    TEXT,
    WHITE,
)
from .tooltip import Tooltip


class UBIReaderUIMixin:
    def _setup_styles(self):

        style = ttk.Style(self)

        style.theme_use("clam")

        style.configure(
            "TFrame", 
            background=DARK
        )

        style.configure(
            "Card.TFrame", 
            background=CARD
        )

        style.configure(
            "Panel.TFrame", 
            background=PANEL
        )

        style.configure(
            "TLabel", 
            background=DARK, 
            foreground=TEXT, 
            font=FONT_BODY
        )

        style.configure(
            "Card.TLabel", 
            background=CARD, 
            foreground=TEXT, 
            font=FONT_BODY
        )

        style.configure(
            "Muted.TLabel", 
            background=CARD, 
            foreground=MUTED, 
            font=FONT_SMALL
        )

        style.configure(
            "TEntry",
            fieldbackground=DARK,
            background=DARK,
            foreground=TEXT,
            insertcolor=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            font=FONT_BODY,
            padding=6,
        )

        style.map(
            "TEntry", 
            bordercolor=[("focus", ACCENT)], 
            lightcolor=[("focus", ACCENT)]
        )

        style.configure(
            "TCheckbutton", 
            background=CARD, 
            foreground=TEXT, 
            font=FONT_BODY, 
            activebackground=CARD
        )

        style.configure(
            "TScrollbar", 
            background=PANEL, 
            troughcolor=PANEL, 
            arrowcolor=MUTED, 
            borderwidth=0
        )

    def _build_ui(self):

        header = tk.Frame(
            self, 
            bg=PANEL, 
            height=58
        )

        header.pack(
            fill="x",
            side="top"
        )
        
        header.pack_propagate(False)

        tk.Label(
            header, 
            text="⬡  UBI Reader", 
            font=FONT_TITLE, 
            bg=PANEL, 
            fg=WHITE
        ).pack(
            side="left", 
            padx=20, 
            pady=10
        )

        tk.Label(
            header, 
            text="Desktop UI for UBI/UBIFS images", 
            font=FONT_SMALL, 
            bg=PANEL, 
            fg=MUTED
        ).pack(
            side="left", 
            pady=16
        )

        status_color = GREEN if self._ubi_ok else RED

        badge = tk.Frame(
            header, 
            bg=status_color
        )

        badge.pack(
            side="right", 
            padx=20, 
            pady=16
        )

        status_text = "ubireader OK" if self._ubi_ok else "ubireader not found"

        tk.Label(
            badge, 
            text=f"  {status_text}  ", 
            font=FONT_BADGE, 
            bg=status_color, 
            fg=DARK
        ).pack()

        body = tk.Frame(self, bg=DARK)

        body.pack(
            fill="both",
            expand=True
        )

        left = tk.Frame(
            body, 
            bg=PANEL, 
            width=272
        )

        left.pack(
            side="left", 
            fill="y"
        )

        left.pack_propagate(False)
        self._build_left(left)

        tk.Frame(
            body, 
            bg=BORDER, 
            width=1
        ).pack(
            side="left", 
            fill="y"
        )

        right = tk.Frame(body, bg=DARK)

        right.pack(
            side="left", 
            fill="both", 
            expand=True
        )

        self._build_right(right)

    def _build_left(self, parent):
        sec = tk.Frame(parent, bg=PANEL)

        sec.pack(
            fill="x", 
            padx=14, 
            pady=(18, 0)
        )

        tk.Label(
            sec, 
            text="IMAGE", 
            font=("Segoe UI", 8, "bold"), 
            bg=PANEL, 
            fg=MUTED
        ).pack(
            anchor="w"
        )

        row = tk.Frame(sec, bg=PANEL)

        row.pack(
            fill="x", 
            pady=(5, 0)
        )

        ttk.Entry(
            row, 
            textvariable=self.selected_file, 
            font=FONT_SMALL
        ).pack(
            side="left", 
            fill="x", 
            expand=True
        )

        tk.Button(
            row,
            text=" … ",
            font=FONT_SMALL,
            bg=BORDER,
            fg=TEXT,
            bd=0,
            cursor="hand2",
            activebackground=ACCENT,
            activeforeground=WHITE,
            command=self._browse_file,
        ).pack(
            side="left", 
            padx=(3, 0)
        )

        self.file_info_label = tk.Label(sec, text="No file selected", font=FONT_SMALL, bg=PANEL, fg=MUTED)
        
        self.file_info_label.pack(
            anchor="w", 
            pady=(3, 0)
        )

        drop = tk.Frame(sec, bg=CARD, highlightbackground=BORDER, highlightthickness=1)

        drop.pack(
            fill="x", 
            pady=(6, 0)
        )

        drop_lbl = tk.Label(
            drop,
            text="Drop a .ubi/.ubifs file here\nor click ‘…’ to browse",
            font=FONT_SMALL,
            bg=CARD,
            fg=MUTED,
            justify="center",
        )

        drop_lbl.pack(pady=8)
        
        for widget in (drop, drop_lbl):
            widget.bind("<Button-1>", lambda _e: self._browse_file())
            widget.bind("<Enter>", lambda _e: drop.config(highlightbackground=ACCENT))
            widget.bind("<Leave>", lambda _e: drop.config(highlightbackground=BORDER))

        tk.Frame(
            parent, 
            bg=BORDER, 
            height=1
        ).pack(
            fill="x", 
            padx=14, 
            pady=12
        )
        
        tk.Label(
            parent, 
            text="OPERATION", 
            font=("Segoe UI", 8, "bold"), 
            bg=PANEL, fg=MUTED
        ).pack(
            anchor="w", 
            padx=14
        )

        for key, meta in ubi_commands().items():
            self._build_cmd_btn(parent, key, meta)

        tk.Frame(
            parent, 
            bg=BORDER, 
            height=1
        ).pack(
            fill="x", 
            padx=14, 
            pady=12 # lol pady
        )

        tk.Label(
            parent, 
            text="HISTORY", 
            font=("Segoe UI", 8, "bold"), 
            bg=PANEL, 
            fg=MUTED
        ).pack(
            anchor="w", 
            padx=14
        )

        hw = tk.Frame(parent, bg=PANEL)

        hw.pack(
            fill="both", 
            expand=True, 
            padx=6, 
            pady=(4, 8)
        )

        self.history_list = tk.Listbox(
            hw,
            bg=PANEL,
            fg=MUTED,
            font=FONT_SMALL,
            bd=0,
            selectbackground=CARD,
            selectforeground=TEXT,
            activestyle="none",
            highlightthickness=0,
        )

        self.history_list.pack(
            fill="both", 
            expand=True
        )

        self.history_list.bind(
            "<Double-Button-1>", 
            self._restore_history
        )

    def _build_cmd_btn(self, parent, key, meta):
        frame = tk.Frame(parent, bg=PANEL, cursor="hand2")

        frame.pack(
            fill="x", 
            padx=6, 
            pady=1
        )

        ind = tk.Frame(frame, width=3, bg=meta["color"] if key == "extract_files" else PANEL)
        ind.pack(side="left", fill="y")
        self._cmd_indicators[key] = ind

        inner = tk.Frame(frame, bg=PANEL, padx=8, pady=6)
        inner.pack(side="left", fill="x", expand=True)

        icon_lbl = tk.Label(inner, text=meta["icon"], font=("Segoe UI", 13), bg=PANEL, fg=meta["color"])
        icon_lbl.pack(side="left")

        tf = tk.Frame(inner, bg=PANEL)
        tf.pack(side="left", padx=(7, 0))
        nl = tk.Label(tf, text=meta["label"], font=("Segoe UI", 9, "bold"), bg=PANEL, fg=TEXT)
        nl.pack(anchor="w")
        desc = meta["desc"]
        dl = tk.Label(tf, text=(desc[:38] + "…") if len(desc) > 38 else desc, font=("Segoe UI", 8), bg=PANEL, fg=MUTED)
        dl.pack(anchor="w")

        self._cmd_frames[key] = frame
        active_bg = CARD

        def activate(target_key=key):
            for frame_key in self._cmd_frames:
                self._set_btn_bg(self._cmd_frames[frame_key], PANEL)
                self._cmd_indicators[frame_key].config(bg=PANEL)
            self._set_btn_bg(self._cmd_frames[target_key], active_bg)
            self._cmd_indicators[target_key].config(bg=ubi_commands()[target_key]["color"])
            self._select_cmd(target_key)

        for widget in (frame, inner, icon_lbl, tf, nl, dl):
            widget.bind("<Button-1>", lambda _e, fn=activate: fn())
            widget.bind("<Enter>", lambda _e, f=frame, k=key: f.config(bg=active_bg) if self.selected_cmd.get() != k else None)
            widget.bind("<Leave>", lambda _e, f=frame, k=key: f.config(bg=active_bg if self.selected_cmd.get() == k else PANEL))

        if key == "extract_files":
            self._set_btn_bg(frame, active_bg)

    @staticmethod
    def _set_btn_bg(frame, color):
        try:
            frame.config(bg=color)
            for c1 in frame.winfo_children():
                c1.config(bg=color)
                for c2 in c1.winfo_children():
                    c2.config(bg=color)
                    for c3 in c2.winfo_children():
                        try:
                            c3.config(bg=color)
                        except Exception:
                            pass
        except Exception:
            pass

    def _build_right(self, parent):
        top = tk.Frame(parent, bg=DARK)
        top.pack(fill="x", padx=22, pady=(18, 0))
        self.op_title = tk.Label(top, text="", font=FONT_HEAD, bg=DARK, fg=WHITE)
        self.op_title.pack(anchor="w")
        self.op_desc = tk.Label(top, text="", font=FONT_SMALL, bg=DARK, fg=MUTED)
        self.op_desc.pack(anchor="w", pady=(1, 0))

        self.args_card = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        self.args_card.pack(fill="x", padx=22, pady=10)
        self.args_inner = tk.Frame(self.args_card, bg=CARD)
        self.args_inner.pack(fill="x", padx=14, pady=10)

        cbar = tk.Frame(parent, bg=PANEL)
        cbar.pack(fill="x", padx=22, pady=(0, 0))

        tk.Label(cbar, text="CONSOLE", font=("Segoe UI", 8, "bold"), bg=PANEL, fg=MUTED).pack(side="left", padx=10, pady=5)

        button_opts = dict(bd=0, cursor="hand2", padx=9, pady=3)

        acf = tk.Frame(cbar, bg=PANEL)
        acf.pack(side="right", padx=(2, 10), pady=4)

        tk.Checkbutton(
            acf,
            text="Auto clear",
            variable=self.auto_clear_var,
            font=("Segoe UI", 9),
            bg=PANEL,
            fg=MUTED,
            activebackground=PANEL,
            selectcolor=CARD,
            cursor="hand2",
        ).pack()

        self.run_btn = tk.Button(
            cbar,
            text="Run",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT,
            fg=WHITE,
            activebackground="#3A7AE8",
            activeforeground=WHITE,
            command=self._run,
            **button_opts,
        )

        self.run_btn.pack(
            side="right", 
            padx=(2, 4), 
            pady=4
        )

        Tooltip(
            self.run_btn, 
            get_text=self._get_cmd_str
        )

        self.stop_btn = tk.Button(
            cbar,
            text="Stop",
            font=("Segoe UI", 9, "bold"),
            bg="#3A1E1E",
            fg=RED,
            activebackground="#4A2A2A",
            activeforeground=RED,
            state="disabled",
            command=self._stop,
            **button_opts,
        )

        self.stop_btn.pack(
            side="right", 
            padx=2, 
            pady=4
        )

        tk.Button(
            cbar,
            text="Save log",
            font=("Segoe UI", 9),
            bg=PANEL,
            fg=MUTED,
            activebackground=BORDER,
            activeforeground=TEXT,
            command=self._save_log,
            **button_opts,
        ).pack(
            side="right", 
            padx=2, 
            pady=4
        )

        tk.Button(
            cbar,
            text="Clear",
            font=("Segoe UI", 9),
            bg=PANEL,
            fg=MUTED,
            activebackground=BORDER,
            activeforeground=TEXT,
            command=self._clear_log,
            **button_opts,
        ).pack(
            side="right", 
            padx=2, 
            pady=4
        )

        self.progress_bar = tk.Canvas(parent, bg=PANEL, height=2, highlightthickness=0)
        self.progress_bar.pack(fill="x", padx=22)
        self._anim_x = 0
        self._anim_id = None

        lf = tk.Frame(parent, bg=DARK)
        lf.pack(fill="both", expand=True, padx=22, pady=(0, 12))

        self.log_text = tk.Text(
            lf,
            bg="#0A0C14",
            fg=TEXT,
            font=FONT_MONO,
            bd=0,
            padx=12,
            pady=10,
            wrap="word",
            state="disabled",
            insertbackground=TEXT,
            selectbackground=ACCENT,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(lf, command=self.log_text.yview)
        sb.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=sb.set)

        self.log_text.tag_config("info", foreground=MUTED)
        self.log_text.tag_config("ok", foreground=GREEN)
        self.log_text.tag_config("warn", foreground=AMBER)
        self.log_text.tag_config("error", foreground=RED)
        self.log_text.tag_config("cmd", foreground=ACCENT)
        self.log_text.tag_config("sep", foreground=BORDER)
        self.log_text.tag_config("out", foreground=TEXT)

        self._select_cmd("extract_files")



    def _select_cmd(self, key):
        old = self.selected_cmd.get()

        if hasattr(self, "log_text"):
            self._log_buffers[old] = self._dump_log_tagged()

        self.selected_cmd.set(key)

        meta = ubi_commands()[key]

        self.op_title.config(text=f"{meta['icon']}  {meta['label']}")
        self.op_desc.config(text=meta["desc"])

        for widget in self.args_inner.winfo_children():
            widget.destroy()
        self.arg_widgets.clear()
        self.arg_vars.clear()

        if not meta["args"]:
            tk.Label(self.args_inner, text="No additional options", font=FONT_SMALL, bg=CARD, fg=MUTED).pack(anchor="w")
        else:
            for arg in meta["args"]:
                self._build_arg_row(arg)

        self._restore_log_buffer(key)
        self._update_cmd_preview()

    def _build_arg_row(self, arg):
        row = tk.Frame(self.args_inner, bg=CARD)
        row.pack(fill="x", pady=3)
        req = " *" if arg.get("required") else ""

        tk.Label(
            row, 
            text=arg["label"] + req, 
            font=FONT_SMALL, 
            bg=CARD, 
            fg=TEXT, 
            width=28, 
            anchor="w"
        ).pack(
            side="left"
        )

        atype = arg["type"]

        if atype == "bool":
            var = tk.BooleanVar()
            ttk.Checkbutton(row, variable=var).pack(side="left")

        elif atype in ("dir", "file_save"):
            var = tk.StringVar()
            entry = ttk.Entry(row, textvariable=var, font=FONT_SMALL, width=28)
            entry.pack(side="left", fill="x", expand=True)
            tk.Button(
                row,
                text=" … ",
                font=FONT_SMALL,
                bg=BORDER,
                fg=TEXT,
                bd=0,
                cursor="hand2",
                activebackground=ACCENT,
                activeforeground=WHITE,
                command=lambda v=var, t=atype: self._pick_path(v, t),
            ).pack(
                side="left", 
                padx=(3, 0)
            )

            self.arg_widgets[arg["name"]] = entry

        else:
            var = tk.StringVar()
            entry = ttk.Entry(row, textvariable=var, font=FONT_SMALL, width=18)

            entry.pack(side="left")
            self.arg_widgets[arg["name"]] = entry

        self.arg_vars[arg["name"]] = var
        var.trace_add("write", lambda *_: self._update_cmd_preview())

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select a UBI/UBIFS image",
            filetypes=[
                ("UBI images", "*.ubi *.ubifs *.img *.bin *.raw *.flash"), 
                ("All files", "*.*")
                ],
        )
        
        if path:
            self._set_file(path)

    def _set_file(self, path):
        self.selected_file.set(path)
        p = Path(path)

        if p.exists():
            mb = p.stat().st_size / (1024 * 1024)
            self.file_info_label.config(fg=GREEN, text=f"{p.name}  ({mb:.1f} MB)")

        else:
            self.file_info_label.config(fg=RED, text="File not found")

        self._update_cmd_preview()

    def _pick_path(self, var, atype):
        if atype == "dir":
            path = filedialog.askdirectory(title="Select output directory")
        else:
            path = filedialog.asksaveasfilename(
                title="Save log",
                defaultextension=".log",
                filetypes=[("Log", "*.log"), ("All files", "*.*")],
            )
        if path:
            var.set(path)

    def _build_cmd(self) -> list:

        key = self.selected_cmd.get()
        meta = ubi_commands()[key]
        fp = self.selected_file.get().strip()

        if not fp:
            return []

        parts = [meta["cmd"]]

        for arg in meta["args"]:
            var = self.arg_vars.get(arg["name"])
            
            if var is None: continue

            val = var.get()

            if arg["type"] == "bool":
                if val:
                    parts.append(arg["flag"])

            elif str(val).strip():
                parts.extend([arg["flag"], str(val).strip()])

        parts.append(fp)

        return parts

    def _get_cmd_str(self) -> str:
        parts = self._build_cmd()
        return "$ " + " ".join(parts) if parts else "(file not selected)"

    def _update_cmd_preview(self):
        pass
