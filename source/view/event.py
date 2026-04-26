import customtkinter as ctk
import sys, os


class _event():
    def __init__(self,
        prompt: object=None
    ):
        self.prompt = prompt

    def _mwr(self,event=None):
        self.prompt._box.mark_set("insert", "insert wordend")
        self.prompt._box.see("insert")

    def _mwl(self,event=None):
        self.prompt._box.mark_set("insert", "insert wordstart")
        self.prompt._box.see("insert")

    def _bacw(self,event=None):
        self.prompt._box.delete("insert -1c wordstart", "insert")
        self.prompt._box.see("insert")

    def _mls(self,event=None):
        self.prompt._box.mark_set("insert", "3.0")
        self.prompt._box.see("insert")

    def _mle(self,event=None):
        self.prompt._box.mark_set("insert", "end")
        self.prompt._box.see("insert")

if __name__ == "__main__":
    print("[info] This file only import")