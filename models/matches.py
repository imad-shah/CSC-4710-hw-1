from dataclasses import dataclass
import sqlite3


@dataclass(slots=True)
class Match:
    match_date: str | None
    venue: str | None
    match_id: int
    home_team_id: int
    away_team_id: int
    home_score: int | None
    away_score: int | None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Match":
        return cls(**dict(row))
