r"""
--- VietNam Shell version 0.0.1 beta ---
Edition 2026 - 2027. Author Coder-4389
© Copyright Coder-4389. All rights reserved.

- VietNam Shell is a CLI had been made by a VietNamese.
- You can write your code in it and it will do anything from your code.
- So VietNam Shell is not have package support, 
  if you want download the package you can download by your brower or your CLI.
- VietNam Shell use Customtkinter to make the UI. so if you are develop and 
  you want develop it UI it you should learning about Customtkinter.
- Thank you for using VietNam Shell.
"""

import customtkinter as ctk
import tkinter as tk
import PIL

import view
import script

class View():
    def __init__(self,
        process: object=None,
        width = 800, height = 600, 
        title = "VietNam Shell 0.0.1"
    ):  
        self.root = ctk.CTk()
        self.root.geometry(f"{width}x{height}+64+32")
        self.root.title(title)

        self.icon = PIL.ImageTk.PhotoImage(
            PIL.Image.open("assets/icon.png")
        )
        self.root.iconphoto(True, self.icon)

        self.prompt = view._Prompt(root=self.root)

        self.root.mainloop()

    def show(self, text: str):
        pass

class Process():
    def __init__(self,
        view: object=None, 
        script: object=None,
        
        code: str=None
    ):
        pass

def Main():
    pass

if __name__ == "__main__":
    View()
