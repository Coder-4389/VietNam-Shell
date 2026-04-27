import customtkinter as ctk
import tkinter as tk
import sys, os

from ._terminal import _Terminal

class _Tabbar(ctk.CTkSegmentedButton):
    def __init__(self,
        _box: object=None,
        root: object=None
    ): 
        root.update()
        width = root.winfo_width()
        height = root.winfo_height()

        super().__init__(
            root,
            width=width, height=height,
            values=["Tab: 1"],
            corner_radius=6,
            command=self._switch
        ); self.pack(side="top", fill="x", padx=0, pady=0)

        self.tablist = list(self.cget("values"))
        self.tabnum = len(self.tablist)

        self.currtab = None
        self.tab = dict()
        for _name in self.tablist: self.tab[_name] = _Terminal(_box)

    def _switch(self, name) -> None:
        if self.currtab: self.tab[self.currtab].pack_forget()
        
        if name in self.tablist: 
            self.currtab = name
            self.tab[name].pack(
                fill="both", 
                expand=True
            )
        else: tk.messagebox.showerror(
            "Error Not Found", 
            "The tab doesn't found. \nPlease Check your tab name"
        )

    def _default(self, name_val: str="") -> object:
        if name_val == "": return None 
        map: dict = {
            "tab_name": f"Tab: {self.tabnum+1}",
            "box_font": f"{self.tab[name].font}"
        }
        
        return map.get(name_val)

    def new_tab(self,_name: str="") -> None:
        if _name != "": pass
        else: _name = self._default("tab_name")
        self.tablist.append(_name)
        self.configure(values=self.tablist) 
        self.tabnum += 1

    def del_tab(self, _name) -> None: 
        try: self.tablist.remove(_name)
        except: tk.messagebox.showerror(
            "Error Not Found", 
            "The tab doesn't found. \nPlease Check your tab name"
        )

if __name__ == "__main__":
    print()