import sys, os

class Reg(): 
    _data = dict()
    @classmethod
    def get(cls, _name: str) -> object: return cls._data.get(_name, None)
    @classmethod 
    def set(cls, _name: str, _val: object) -> None: cls._data[_name] = _val

if __name__ == "__main__":
    print("[info] This file only import")
    input("Press Enter to exit...")