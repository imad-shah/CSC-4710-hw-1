from dataclasses import dataclass
import sqlite3


@dataclass(slots=True)
class Match:
    match_date: str
    venue: str
    match_id: int
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Match":
        return cls(**dict(row))
