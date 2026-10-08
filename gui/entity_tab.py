from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from tkinter import messagebox, ttk

from controller import IWorldCupController

from .widgets import Form, Table, run_action


class EntityTab(ttk.Frame, ABC):
    tab_name: str
    title: str
    fields: Sequence[str]
    delete_warning: str = ""

    def __init__(
        self,
        parent: ttk.Notebook,
        controller: IWorldCupController,
        on_change: Callable[[], None],
    ) -> None:
        super().__init__(parent, padding=10)
        self.controller = controller
        self._on_change = on_change

        self.sidebar = ttk.Frame(self)
        self.sidebar.grid(row=0, column=0, sticky="n", padx=(0, 10))
        self.form = Form(self.sidebar, self.title, self.fields)
        self.form.grid(row=0, column=0, sticky="ew")
        self._build_buttons().grid(row=1, column=0, sticky="ew", pady=10)

        self.table = Table(self, self.fields, on_select=self.form.fill)
        self.table.grid(row=0, column=1, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    @abstractmethod
    def save(self, *values: str) -> None:
        pass

    @abstractmethod
    def delete(self, record_id: str) -> None:
        pass

    @abstractmethod
    def rows(self) -> list[tuple]:
        pass

    def refresh(self) -> None:
        self.table.show(self.rows())

    def _build_buttons(self) -> ttk.Frame:
        buttons = ttk.Frame(self.sidebar)
        actions = [
            ("Save", self._save),
            ("Delete", self._delete),
            ("Clear", self.form.clear),
        ]
        for column, (text, command) in enumerate(actions):
            ttk.Button(buttons, text=text, command=command).grid(
                row=0, column=column, padx=2
            )
        return buttons

    def _save(self) -> None:
        if run_action(lambda: self.save(*self.form.values())):
            self._finish(f"{self.title} saved.")

    def _delete(self) -> None:
        record_id = self.form.values()[0]
        prompt = f"Delete {self.title.lower()} {record_id}?{self.delete_warning}"
        if not messagebox.askyesno("Confirm Delete", prompt):
            return
        if run_action(lambda: self.delete(record_id)):
            self._finish(f"{self.title} deleted.")

    def _finish(self, message: str) -> None:
        self.form.clear()
        self._on_change()
        messagebox.showinfo("Success", message)
