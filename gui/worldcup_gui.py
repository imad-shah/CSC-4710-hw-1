import tkinter as tk
from tkinter import ttk

from controller import IWorldCupController

from .tabs import MatchesTab, PlayersTab, TeamsTab


class WorldCupApp(tk.Tk):
    def __init__(self, controller: IWorldCupController) -> None:
        super().__init__()
        self.title("FIFA World Cup 2026")
        self.minsize(1150, 450)

        notebook = ttk.Notebook(self, padding=10)
        notebook.pack(fill="both", expand=True)
        self._tabs = [
            tab(notebook, controller, self.refresh)
            for tab in (TeamsTab, PlayersTab, MatchesTab)
        ]
        for tab in self._tabs:
            notebook.add(tab, text=tab.tab_name)
        self.refresh()

    def refresh(self) -> None:
        for tab in self._tabs:
            tab.refresh()
