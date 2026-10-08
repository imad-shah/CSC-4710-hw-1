import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk

from controller import IWorldCupController
from models import Match

from .entity_tab import EntityTab
from .widgets import run_action


class TeamsTab(EntityTab):
    tab_name = "Teams"
    title = "Team"
    fields = ("Team ID", "Name", "Coach")
    delete_warning = "\n\nThis also deletes the team's players and matches."

    def save(self, *values: str) -> None:
        self.controller.save_team(*values)

    def delete(self, record_id: str) -> None:
        self.controller.delete_team(record_id)

    def rows(self) -> list[tuple]:
        return [(t.team_id, t.name, t.coach) for t in self.controller.list_teams()]


class PlayersTab(EntityTab):
    tab_name = "Players"
    title = "Player"
    fields = ("Player ID", "Name", "Position", "Team ID")

    def save(self, *values: str) -> None:
        self.controller.save_player(*values)

    def delete(self, record_id: str) -> None:
        self.controller.delete_player(record_id)

    def rows(self) -> list[tuple]:
        return [
            (p.player_id, p.name, p.position, p.team_id)
            for p in self.controller.list_players()
        ]


def _match_rows(matches: list[Match]) -> list[tuple]:
    return [
        (
            m.match_id,
            m.home_team_id,
            m.away_team_id,
            m.match_date,
            m.venue,
            m.home_score,
            m.away_score,
        )
        for m in matches
    ]


class MatchesTab(EntityTab):
    tab_name = "Matches"
    title = "Match"
    fields = (
        "Match ID",
        "Home Team ID",
        "Away Team ID",
        "Date (YYYY-MM-DD)",
        "Venue",
        "Home Score",
        "Away Score",
    )

    def __init__(
        self,
        parent: ttk.Notebook,
        controller: IWorldCupController,
        on_change: Callable[[], None],
    ) -> None:
        super().__init__(parent, controller, on_change)
        self._searches = {
            "Team ID": controller.matches_for_team,
            "Player ID": controller.matches_for_player,
        }
        self._search_by = tk.StringVar(value="Team ID")
        self._search_id = tk.StringVar()
        self._build_search().grid(row=2, column=0, sticky="ew")

    def save(self, *values: str) -> None:
        self.controller.save_match(*values)

    def delete(self, record_id: str) -> None:
        self.controller.delete_match(record_id)

    def rows(self) -> list[tuple]:
        return _match_rows(self.controller.list_matches())

    def _build_search(self) -> ttk.LabelFrame:
        search = ttk.LabelFrame(self.sidebar, text="Search Matches", padding=10)
        ttk.Combobox(
            search,
            textvariable=self._search_by,
            values=list(self._searches),
            state="readonly",
            width=10,
        ).grid(row=0, column=0)
        ttk.Entry(search, textvariable=self._search_id, width=16).grid(
            row=0, column=1, padx=(8, 0)
        )
        ttk.Button(search, text="Search", command=self._search).grid(
            row=1, column=0, sticky="ew", pady=(8, 0)
        )
        ttk.Button(search, text="Show All", command=self.refresh).grid(
            row=1, column=1, sticky="ew", padx=(8, 0), pady=(8, 0)
        )
        return search

    def _search(self) -> None:
        find = self._searches[self._search_by.get()]
        run_action(lambda: self._show_results(find(self._search_id.get())))

    def _show_results(self, matches: list[Match]) -> None:
        self.table.show(_match_rows(matches))
        if not matches:
            messagebox.showinfo("Search", "No matches found.")
