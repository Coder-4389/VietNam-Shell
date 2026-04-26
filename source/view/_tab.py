import customtkinter as ctk
import tkinter as tk
import sys, os

class _Tabbar(ctk.CTkSegmentedButton):
    def __init__(self,
        root: object=None
    ): 
        root.update()
        width = root.winfo_width()
        height = root.winfo_height()

        super().__init__(
            root,
            width=width, height=height,
            values=["Terminal: 1"],
            corner_radius=12,
        ); self.pack(side="top", fill="x", padx=0, pady=0)

        self.tablist = list(self.cget("values"))
        self.tabnum = len(self.tablist)

    def new_tab(self,_name):
        self.tablist.append(_name)
        self.configure(
            values=self.tablist
        ) 
        self.tabnum += 1

    def del_tab(self, _name): 
        try: self.tablist.remove(_name)
        except: tk.messagebox.showerror("Error", 
            "The tab doesn't found. \nPlease Check your tab name"
        )

if __name__ == "__main__":
    print()