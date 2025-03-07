import tkinter as tk
from .core.app import GestaoVistaApp


def main():
    """Ponto de entrada principal da aplicação"""
    root = tk.Tk()
    app = GestaoVistaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
