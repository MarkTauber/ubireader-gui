import tkinter as tk

from .constants import BORDER, CARD, FONT_MONO, TEXT


class Tooltip:
    _DELAY = 600
    _PAD = 8

    def __init__(self, widget: tk.Widget, *, get_text):
        self._widget = widget
        self._get_text = get_text
        self._tw = None
        self._after_id = None

        widget.bind(
            "<Enter>", 
            self._on_enter, 
            add="+"
        )

        widget.bind(
            "<Leave>", 
            self._on_leave,
            add="+"
        )

        widget.bind(
            "<ButtonPress>", 
            self._on_leave, 
            add="+"
        )

    def _on_enter(self, _event):
        self._schedule()

    def _on_leave(self, _event=None):
        if self._after_id:
            self._widget.after_cancel(self._after_id)
            self._after_id = None
        self._hide()

    def _schedule(self):
        self._on_leave()
        self._after_id = self._widget.after(self._DELAY, self._show)

    def _show(self):
        self._after_id = None
        text = self._get_text()
        if not text:
            return

        self._hide()

        tw = tk.Toplevel(self._widget)
        tw.wm_overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        tw.configure(bg=CARD)

        tk.Label(
            tw,
            text=text,
            font=FONT_MONO,
            bg=CARD,
            fg=TEXT,
            justify="left",
            padx=self._PAD,
            pady=self._PAD,
            wraplength=700,
            relief="flat",
            bd=0,
        ).pack()

        tw.update_idletasks()

        width = tw.winfo_width()
        wx = self._widget.winfo_rootx()
        wy = self._widget.winfo_rooty() + self._widget.winfo_height() + 4
        sw = self._widget.winfo_screenwidth()

        if wx + width > sw:
            wx = sw - width - 8

        tw.wm_geometry(f"+{wx}+{wy}")
        
        tw.configure(highlightbackground=BORDER, highlightthickness=1)

        self._tw = tw

    def _hide(self):
        if self._tw:
            try:
                self._tw.destroy()
            except Exception:
                pass
            self._tw = None
