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
import source as src

__version__ = "0.0.1 beta"

def _load(path: str):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            full_name = os.path.basename(path)
            name = full_name.split(".")[0]
            Reg.set(name, data)
    except FileNotFoundError:
        showerror("Error",
            "[Error]: Couldn't be found .json file \nPlease check your path"
        ); sys.exit(0)

    except json.decoder.JSONDecodeError:
        showerror("Error",
            "[Error]: The .json file is not json format \nPlease check your file"
        ); sys.exit(0)

def setup():
    _load("data/cfg.json")
    _load("data/keywords.json")
    _load("data/msg.json")

class Core():
    def __init__(self): 
        self.lexer = src.Lexer()
        self.parser = src.Parser()

        # Global self with app's registry
        Reg.set("Core", self)

    def analyze(self, code: str) -> None:
        tokens = self.lexer(code) 
        ast = self.parser(tokens)

        print(tokens) # debug code
        print(ast) # debug code

class UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        Reg.set("UI", self)

    def __call__(self, **kwargs: any): 
        self.width: int = kwargs.get("width", 800)
        self.height: int = kwargs.get("height", 600)
        self.name: str = kwargs.get("title", "VietNam Shell")

        self.geometry(f"{self.width}x{self.height}")
        self.title(self.name)

        self._frame_setup()
        self._bar = src.Bar(root=self._bar_frame, _box=self._box_frame)
        self._bar._switch_tab("Tab: 1")
        
        self.mainloop()

    def _frame_setup(self) -> None: # frame setup
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

if __name__ == "__main__":
    setup()

    try: PROCESS = Core()
    except: PROCESS = None

    # if PROCESS: 
    INTERFACE = UI()
    INTERFACE()
