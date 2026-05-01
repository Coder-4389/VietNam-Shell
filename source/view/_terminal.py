# UI modules
import customtkinter as ctk
import tkinter as tk
import PIL

from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import askokcancel

# process modules
import json

# system modules
import sys, os
import getpass

# Registry
from source.registry import Reg

home = os.path.expanduser("~")
user = getpass.getuser()

def _make_prompt(path: str) -> str:
    global home, user

    if path.startswith(home): path=path.replace(home, "~", 1)
    return f"\n{user}: {path}$ "

class _Terminal(ctk.CTkTextbox):
    def __init__(self, root: object=None):
        self.root = root; self.root.update()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        super().__init__(
            self.root,
            width=width, height=height,
            corner_radius=0,
            border_width=0,
            font=tuple(Reg.get("cfg")["font"])
        ); self.pack(fill="both", expand=True)

        header = "\n".join([
            "VietNam Shell had been successly started up. Version: 0.0.1 beta (2026-2027).     ",
            "© 2026-2027 Coder-4389. All rights reserved. [Use help command to give more help] ",
        ]); self.insert("end", header)

        self.mark_set("lockpos", "end-1c")
        self.mark_gravity("lockpos", "left")

        self.path = home
        self._prompt()

        self.bind("<Key>", self._check_key)
        self.bind("<Return>", self._prompt)

    def _check_key(self, event=None):
        inspos = self.index("insert")
        lockpos = self.index("lockpos")
        
        if self.compare(inspos, "<",lockpos): return "break"
        elif event.keycode == 22 and self.compare(inspos, "<=", lockpos): 
            return "break"

    def _prompt(self, event=None): 
        if self.index("end-1c") != self.index("lockpos"): 
            code = self.get("lockpos", "end-1c")
            Reg.get("Process").run(code)

        self.insert("end", _make_prompt(self.path))
        self.mark_set("lockpos", "end-1c")
        self.mark_gravity("lockpos", "left")
        self.see("end")

        return "break"

    def write(self, *args, **kwargs: str):
        for i, val in enumerate(args):
            # if i!=0: 
            self.insert("end", "\n") 
            self.insert("end", val)

        self.mark_set("lockpos", "end-1c")
        self.mark_gravity("lockpos", "left")

class Bar(ctk.CTkSegmentedButton):
    def __init__(self, 
        root: object=None,
        _box: object=None
    ):
        self.root = root; self.root.update()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        self._box = _box

        super().__init__(
            self.root,
            width=width, height=height,
            corner_radius=8,
            border_width=0,
            values=["Tab: 1"],
            font=tuple(Reg.get("cfg")["font"])
        ); self.pack(fill="both", expand=True)

        self.tablist = set(self.cget("values"))
        self.tabnum = len(self.tablist)

        self.curr = None
        self._tab = dict()
        for _name in self.tablist:
            self._tab[_name] = _Terminal(self._box)

        Reg.set("Bar", self)
    
    def curr_tab(self) -> object:
        if self.curr is None: 
            first_tab = self.cget("values")[0]
            self.curr = first_tab
        return self._tab[self.curr]

    def _switch_tab(self, _name: str) -> None:
        if _name not in self.tablist: 
            showerror("Error", "Tab not found")
            return
        
        self.curr_tab().pack_forget()
        self.curr = _name
        self.curr_tab().pack(fill="both", expand=True)

        Reg.set("curr_tab", self.curr_tab())

    def _new_tab(self, name: str) -> None:
        if name is None or name.strip() == "": 
            name = f"Tab: {self.tabnum+1}"
            self.curr_tab().write(f"Don't have name, use default name: {name}")
        elif name in self.tablist: 
            showerror("Error", "Tab already exists")
            return
        
        self.tabnum += 1
        self.tablist.add(name)
        _box = _Terminal(Reg.get("UI")._box_frame)
        self._tab[name] = _Terminal(_box)

        values = list(self.cget("values")).append(name)
        self.configure(values=values)

if __name__ == "__main__":
    print("[info] This file only import")
    input("Press Enter to exit...")
