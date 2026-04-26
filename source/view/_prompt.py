import customtkinter as ctk
import getpass
import sys, os

from .event import _event

home = os.path.expanduser("~")

class _Prompt():

    def __init__(self,
        root: object = None,
    ):
        self.user = getpass.getuser()
        self.path = home

        self.root = root

        self.root.update()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        self.font = ("consolas", 15)

        self._box = ctk.CTkTextbox(
            self.root,
            width=width, height=height,
            font=self.font
        )
        self._box.pack(fill="both", expand=True)

        header = "\n".join([
            "VietNam Shell had been successly started up. Version: 0.0.1 beta (2026-2027).     ",
            "© 2026-2027 Coder-4389. All rights reserved. [Use help command to give more help] ",
        ])

        self._box.insert("end", header+'\n')
        self._render()

        self._key_bind()

        self._box.bind("<Key>", self._check_key)
        self._box.bind("<Return>", self._render)

    def _key_bind(self):
        self.event = _event(self)

        self._box.bind("<Control-Left>",  self.event._mwl)
        self._box.bind("<Control-Right>", self.event._mwr)
        self._box.bind("<Control-BackSpace>", self.event._bacw)
        self._box.bind("<Home>", self.event._mls)
        self._box.bind("<End>",  self.event._mle)

    def _check_key(self, event=None):
        inspos = self._box.index("insert")
        lockpos = self._box.index("lockpos")
        
        if self._box.compare(inspos, "<",lockpos): return "break"
        elif event.keycode == 22 and self._box.compare(inspos, "<=", lockpos): 
            return "break"

    def _render(self, event=None):
        if self.path.startswith(home): path = self.path.replace(home, "~", 1)
        else: path = self.path

        self._box.insert("end", f"\n{self.user}: {path}$ ")
        self._box.mark_set("lockpos", "insert")
        self._box.mark_gravity("lockpos", "left")

        self._box.see("end")

        return "break"

if __name__ == "__main__":
    print("[info] This file only import")
    input("Press Enter to exit...")