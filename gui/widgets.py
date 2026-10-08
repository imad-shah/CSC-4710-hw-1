import tkinter as tk
from collections.abc import Callable, Iterable, Sequence
from tkinter import messagebox, ttk

from controller import AppError


def run_action(action: Callable[[], object]) -> bool:
    try:
        action()
    except AppError as e:
        messagebox.showerror("Error", str(e))
        return False
    return True


class Form(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc, title: str, fields: Sequence[str]) -> None:
        super().__init__(parent, text=title, padding=10)
        self._vars: list[tk.StringVar] = []
        for row, field in enumerate(fields):
            var = tk.StringVar()
            ttk.Label(self, text=field).grid(row=row, column=0, sticky="w", pady=2)
            ttk.Entry(self, textvariable=var, width=28).grid(
                row=row, column=1, padx=(8, 0), pady=2
            )
            self._vars.append(var)

    def values(self) -> list[str]:
        return [var.get() for var in self._vars]

    def fill(self, values: Sequence[object]) -> None:
        for var, value in zip(self._vars, values):
            var.set(value)

    def clear(self) -> None:
        for var in self._vars:
            var.set("")


class Table(ttk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        columns: Sequence[str],
        on_select: Callable[[Sequence[object]], None],
    ) -> None:
        super().__init__(parent)
        self._on_select = on_select
        self._tree = ttk.Treeview(
            self, columns=columns, show="headings", selectmode="browse"
        )
        for column in columns:
            self._tree.heading(column, text=column)
            self._tree.column(column, width=110, anchor="w")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._tree.bind("<<TreeviewSelect>>", self._handle_select)

    def show(self, rows: Iterable[Sequence[object]]) -> None:
        self._tree.delete(*self._tree.get_children())
        for row in rows:
            values = ["" if value is None else value for value in row]
            self._tree.insert("", "end", values=values)

    def _handle_select(self, _event: tk.Event) -> None:
        selection = self._tree.selection()
        if selection:
            self._on_select(self._tree.item(selection[0], "values"))
