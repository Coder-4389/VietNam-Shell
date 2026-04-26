import customtkinter as ctk
import getpass
import sys, os

from .event import _event

home = os.path.expanduser("~")

class _Terminal(ctk.CTkTextbox):
    def __init__(self,
        root: object = None,
    ):
        self.user = getpass.getuser()
        self.path = home

        root.update()
        width = root.winfo_width()
        height = root.winfo_height()

        self.font = ("consolas", 15)

        super().__init__(
            root,
            width=width, height=height,
            font=self.font
        ); self.pack(fill="both", expand=True)

        header = "\n".join([
            "VietNam Shell had been successly started up. Version: 0.0.1 beta (2026-2027).     ",
            "© 2026-2027 Coder-4389. All rights reserved. [Use help command to give more help] ",
        ])

        self.insert("end", header+'\n')

        self.mark_set("lockpos", "end-1c")
        self.mark_gravity("lockpos", "left")
        self._prompt()

        self._key_bind()

        self.bind("<Key>", self._check_key)
        self.bind("<Return>", self._prompt)

    def _key_bind(self):
        self.event = _event(self)

        self.bind("<Control-Left>",  self.event._mwl)
        self.bind("<Control-Right>", self.event._mwr)
        self.bind("<Control-BackSpace>", self.event._bacw)
        self.bind("<Home>", self.event._mls)
        self.bind("<End>",  self.event._mle)

    def _check_key(self, event=None):
        inspos = self.index("insert")
        lockpos = self.index("lockpos")
        # print(inspos, lockpos) # debug code
        
        if self.compare(inspos, "<",lockpos): return "break"
        elif event.keycode == 22 and self.compare(inspos, "<=", lockpos): 
            return "break"

    def _prompt(self, event=None):
        if self.index("end-1c") != self.index("lockpos"):
            self.code = self.get("lockpos", "end-1c")
            # print(self.code) # debug code

        if self.path.startswith(home): path = self.path.replace(home, "~", 1)
        else: path = self.path

        self.insert("end", f"\n{self.user}: {path}$ ")
        self.mark_set("lockpos", "end-1c")
        self.mark_gravity("lockpos", "left")

        self.see("end")

        return "break"

    def write(self, *arg: object):
        for i, val in enumerate(arg):
            if i!=0: self.insert("end", "\n") 
            self.insert("end", val)

        self.mark_set("lockpos", "end-1c")
        self.mark_gravity("lockpos", "left")

if __name__ == "__main__":
    print("[info] This file only import")
    input("Press Enter to exit...")