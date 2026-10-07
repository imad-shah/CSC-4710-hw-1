from dataclasses import dataclass
import sqlite3


@dataclass(slots=True)
class Player:
    name: str
    team_id: int
    position: str | None = None
    player_id: int | None = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Player":
        return cls(**dict(row))
