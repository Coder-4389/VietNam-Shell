r"""
--- VietNam Shell version 0.0.1 beta ---
Edition 2026 - 2027. Author Coder-4389
© Copyright Coder-4389. All rights reserved.
"""

# UI modules
import customtkinter as ctk
import tkinter as tk
import PIL

from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import askokcancel

# data process modules
import json

# system modules
import sys, os

# Registry
from source.registry import Reg

# App modules
import source

__version__ = "0.0.1 beta"

def cfg_load():
    try:
        with open("data/cfg.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        Reg.set("cfg", config)

    except FileNotFoundError:
        showerror("Error",
            "[Error]: Couldn't be found data/cfg.json \nPlease check your path"
        ); sys.exit(0)

    except json.decoder.JSONDecodeError:
        showerror("Error",
            "[Error]: data/cfg.json is not json format \nPlease check your file"
        ); sys.exit(0)

class UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width: int = 800; self.height: int = 600
        self.geometry(f"{self.width}x{self.height}")
        self.title("VietNam Shell - 0.0.1 beta")

        self._frame_setup()
        self._bar = source._Bar(root=self._bar_frame, _box=self._box_frame)
        self._bar._switch_tab("Tab: 1")

        Reg.set("UI", self)

        self.mainloop()

    def _frame_setup(self) -> None:
        self._bar_frame = ctk.CTkFrame(
            self,
            width=self.width, height=36,
            corner_radius=0,
            border_width=0,
        ); self._bar_frame.pack(fill="x", expand=True)

        self._box_frame = ctk.CTkFrame(
            self,
            width=self.width, height=self.height-36,
            corner_radius=0,
            border_width=0,
        ); self._box_frame.pack(fill="both", expand=True)

class Process():
    def __init__(self):
        Reg.set("Process", self)

if __name__ == "__main__":
    cfg_load()
    UI()
