from dataclasses import dataclass
import sqlite3


@dataclass(slots=True)
class Team:
    name: str
    coach: str
    team_id: int

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Team":
        return cls(**dict(row))
